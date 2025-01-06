# Copyright (C) 2017-2025 Pier Carlo Chiodi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from aggregate6 import aggregate
import logging
import os
from packaging import version
import sys
import time
import yaml
import copy
import re

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .config.general import ConfigParserGeneral
from .config.bogons import ConfigParserBogons
from .config.asns import ConfigParserASNS
from .config.clients import ConfigParserClients
from .enrichers.arin_db_dump import ARINWhoisDBDumpEnricher
from .enrichers.registrobr_db_dump import RegistroBRWhoisDBDumpEnricher
from .enrichers.irrdb import IRRDBConfigEnricher_ASNs, \
                             IRRDBConfigEnricher_Prefixes
from .enrichers.pdb_as_set import PeeringDBConfigEnricher_ASSet
from .enrichers.pdb_max_prefix import PeeringDBConfigEnricher_MaxPrefix
from .enrichers.pdb_never_via_route_servers import NeverViaRouteServersEnricher
from .enrichers.rpki_roas import RPKIROAsEnricher
from .enrichers.rtt import RTTGetterConfigEnricher
from .errors import MissingDirError, MissingFileError, BuilderError, \
                    ARouteServerError, MissingArgumentError, \
                    TemplateRenderingError, CompatibilityIssuesError, \
                    ConfigError, MissingGeneralConfigFileError
from .ipaddresses import IPNetwork, IPAddress
from .irrdb import IRRDBInfo
from .cached_objects import CachedObject, normalize_expiry_time
from .reject_reasons import REJECT_REASONS


class ConfigBuilder(object):
    """The base configuration builder class.

    This class must be derived by BGP-daemon-specific classes.
    """

    LOCAL_FILES_IDS = None
    LOCAL_FILES_BASE_DIR = None

    DEFAULT_VERSION = None

    IGNORABLE_ISSUES = ["ext-comms-32bit-asn", "roles_not_available"]

    def validate_bgpspeaker_specific_configuration(self):
        """Check compatibility between config and target BGP speaker

        Returns:
            True if there are no compatibility issues;
            False if there are compatibility issues that can be acknowledged
            via command line argument.
        Raises exception in case of blocking errors.
        """
        return True

    def process_compatibility_issue(self, issue_id, text):
        """Handle a compatibility issue which can be acknowledged by the user.

        If the issue has been ignored via command-line, logs a warning
        message and returns True.
        Otherwise, logs an error message and returns False.

        """
        assert issue_id in self.IGNORABLE_ISSUES

        msg = "Compatibility issue ID '{}'. {}".format(issue_id, text)
        if issue_id in self.ignore_errors or "*" in self.ignore_errors:
            logging.warning(
                "{} - Ignored via --ignore-issues {}".format(msg, issue_id)
            )
            return True

        msg += (
            " - This issue can be acknowledged and ignored via the CLI option "
            "--ignore-issues {}".format(issue_id)
        )
        logging.error(msg)
        return False

    def enrich_j2_environment(self, env):
        pass

    @staticmethod
    def _get_cfg(obj_or_path, cls, descr, **kwargs):
        assert obj_or_path is not None
        if isinstance(obj_or_path, cls):
            return obj_or_path
        elif isinstance(obj_or_path, str):
            path = os.path.expanduser(obj_or_path)
            if not os.path.isfile(path):
                raise MissingFileError(path)
            obj = cls(**kwargs)
            try:
                obj.load(path)
            except ARouteServerError as e:
                raise BuilderError(
                    "One or more errors occurred while loading "
                    "{} configuration file{}".format(
                        descr, ": {}".format(str(e)) if str(e) else ""
                    )
                )
            return obj

    @staticmethod
    def _check_is_dir(arg, path):
        if path is None:
            raise MissingArgumentError(arg)
        dir_path = os.path.expanduser(path)
        if not os.path.isdir(dir_path):
            raise MissingDirError(path)
        return dir_path

    def __init__(self, template_dir=None, template_name=None,
                 cache_dir=None, cache_expiry=CachedObject.DEFAULT_EXPIRY,
                 bgpq3_path="bgpq4", bgpq3_host=IRRDBInfo.BGPQ3_DEFAULT_HOST,
                 bgpq3_sources=IRRDBInfo.BGPQ3_DEFAULT_SOURCES,
                 bgpq3_timeout=IRRDBInfo.BGPQ3_DEFAULT_TIMEOUT,
                 rtt_getter_path=None, threads=4,
                 ip_ver=None, perform_graceful_shutdown=False,
                 ignore_errors=[], live_tests=False,
                 local_files=[], local_files_dir=None, target_version=None,
                 cfg_general=None, cfg_bogons=None, cfg_clients=None,
                 **kwargs):
        """Initialize the configuration builder.

        Here, external data sources are also queried to enrich the
        configuration with additional data (PeeringDB records, ASNs and
        prefixes from IRRDBs, ...).

        Raises:

            ARouteServerError or derived exceptions
              (from pierky.arouteserver.errors).

              Exceptions raised here can have no arguments and their string
              representation can be empty: in these cases, it means that
              one or more errors have been logged using the ``logging`` module.

        Args:

            template_dir (str): the directory that contains the templates
                that must be used to render the output configuration.

                Example: /home/user/arouteserver/templates/bird

                Same of:

                - *--templates-dir* CLI argument.
                - *templates_dir* program's configuration file option.

            template_name (str): the name of the file that must be used to
                render the output configuration.

                Example: main.j2

                Same of:

                - *--template-file-name* CLI argument.
                - *template_name* program's configuration file option.

            cfg_general (str)
            cfg_clients (str)
            cfg_bogons (str): paths to the YAML
                files containing the general route server policy, the clients
                list and the list of bogon prefixes.

                Example: ``cfg_general="/home/user/arouteserver/general.yml"``

                Same of:

                - *--general*, *--clients*, *--bogons* CLI arguments.
                - *cfg_general*, *cfg_clients*, *cfg_bogons* program's
                  configuration file options.

            cache_dir (str): the directory that will be used to store results
                from external data sources queries (PeeringDB info, IRRDBs).

                Same of:

                - *--cache-dir* CLI argument.
                - *cache_dir* program's configuration file option.

            cache_expiry (int or dict): how long cached data must be considered
                valid, in seconds. Each "cacheable object" (PeeringDB info,
                IRR datasets, ...) can have its own expiry time. If an int is
                given here, all the expiry times will have the same duration,
                otherwise cacheable objects will pick their specific value
                or use the 'general' one if no more specific value is given.

                Same of:

                - *cache_expiry* program's configuration file option.

            ip_ver (int): if *None*, the output configuration will be targeted
                for both IPv4 and IPv6; otherwise, set this to *4* or to
                *6* to obtain AFI-specific output configuration.

                Same of:

                - *--ip-ver* CLI argument.

            perform_graceful_shutdown (bool): when True, the output config
                includes an outbound policy which is applied to BGP
                sessions toward the clients and which adds the
                GRACEFUL_SHUTDOWN BGP community (65535:0) to all the
                routes that the route server announces to them.

                Same of:

                - *--perform-graceful-shutdown* CLI argument.

            target_version (str): the BGP daemon target version for which the
                output configuration must be generated.

                This is used to detect and/or solve any compatibility issue
                with some features that are available only using a specific
                version of the target BGP daemon.

                The list of available versions is taken from the derived BGP
                daemon specific classes' ``AVAILABLE_VERSION`` attribute.

                The default value is taken from the derived BGP daemon
                specific classes' ``DEFAULT_VERSION`` attribute.

                Example: on OpenBGPD, to avoid errors when building configs
                that use large BGP communities (available only on
                OpenBGPD/OpenBSD > 6.1) use ``target_version="6.1"``

                Same of:

                - *--target-version* CLI argument.

            ignore_errors (list): a list of issue IDs (strings) that must be
                ignored when building the configuration.

                Depending on the target BGP daemon and its version, some
                features may be unavailable; ARouteServer produces errors
                when one or more of these features are enabled in the route
                server configuration YAML file. These errors are marked with
                an 'issue ID' that can be reported in this list to instruct
                ARouteServer to ignore it and to continue the building process.

                Use ``ignore_errors=["*"]`` to ignore any issue.

                Example: ``ignore_errors=["add_path"]`` to ignore the issue due
                to the lack of support for ADD_PATH in OpenBGPD.

                Same of:

                - *--ignore-issues* CLI argument.

            local_files (list): the list of local files IDs for which the
                relative inclusion point must be enabled on the output
                configuration. Details: https://arouteserver.readthedocs.io/en/latest/CONFIG.html#site-specific-custom-configuration-files

                The list of available IDs is taken from the derived BGP daemon
                specific classes' ``LOCAL_FILES_IDS`` attribute.

                Example: ``local_files=["header4", "footer4"]``

                Same of:

                - *--use-local-files* CLI argument.

            local_files_dir (str): the base directory of the local files that
                will be included in the output configuration.

                The default value is taken from the derived BGP daemon
                specific classes' ``LOCAL_FILES_BASE_DIR`` attribute.

                Example: /etc/bird

                Same of:

                - *--local-files-dir* CLI argument.

            bgpq3_path (str): path to the 'bgpq3' or 'bgpq4' external program; this will
                be used to expand AS macros and to obtain the list of
                authorized origin ASNs and prefixes from IRRDBs.

                Same of:

                - *bgpq3_path* program's configuration file option.

            bgpq3_host (str): the host(s) that will be queried by bgpq3/bgpq4; this
                will be used to set the *-h* argument of the program. Multiple hosts
                can be passed using a comma-delimited string, in which case they
                will be used sequentially in case of failures of the IRR queries or
                timeouts.

                Same of:

                - *bgpq3_host* program's configuration file option.

            bgpq3_sources (str): a comma separated list of sources that will
                be used by the bgpq3/bgpq4 program; this will be used to set the
                *-S* argument of the program.

                Same of:

                - *bgpq3_sources* program's configuration file option.

            bgpq3_timeout (int): timeout for the bgpq4/bgpq3 queries (in seconds).

                Same of:

                - *bgpq3_timeout* program's configuration file option.

            rtt_getter_path (str): path to the program that is executed to
                determine the RTT of a peer.
                Syntax and details can be found at the following URL:
                https://arouteserver.readthedocs.io/en/latest/RTT_GETTER.html

                Same of:

                - *rtt_getter_path* program's configuration file option.

            threads (int): number of concurrent threads used to gather
                additional data from external sources (bgpq3/bgpq4, PeeringDB, ...)

                Same of:

                - *threads* program's configuration file option.

            kwargs: additional arguments used by BGP daemon specific builder
                classes.

            live_tests (bool): only used on live tests.
        """

        # Parameters initialization

        self.template_dir = self._check_is_dir(
            "template_dir", template_dir
        )

        self.template_name = template_name
        if not self.template_name:
            raise MissingArgumentError("template_name")

        self.template_path = os.path.join(self.template_dir,
                                          self.template_name)
        if not os.path.isfile(self.template_path):
            raise MissingFileError(self.template_path)

        self.cache_dir = self._check_is_dir(
            "cache_dir", cache_dir
        )

        self.cache_expiry = normalize_expiry_time(cache_expiry)

        self.bgpq3_path = bgpq3_path
        self.bgpq3_host = bgpq3_host
        self.bgpq3_sources = bgpq3_sources
        self.bgpq3_timeout = bgpq3_timeout

        self.rtt_getter_path = rtt_getter_path

        self.threads = threads

        try:
            with open(os.path.join(self.cache_dir, "write_test"), "w") as f:
                f.write("OK")
        except Exception as e:
            raise BuilderError(
                "Can't write into cache dir {}: {}".format(
                    self.cache_dir, str(e)
                )
            )

        self.ip_ver = ip_ver
        if self.ip_ver is not None:
            self.ip_ver = int(self.ip_ver)
            if self.ip_ver not in (4, 6):
                raise BuilderError("Invalid IP version: {}".format(ip_ver))

        self.perform_graceful_shutdown = perform_graceful_shutdown

        self.ignore_errors = ignore_errors or []

        self.live_tests = live_tests

        self.local_files = local_files
        self.local_files_dir = local_files_dir

        self.target_version = target_version or self.DEFAULT_VERSION

        try:
            self.cfg_general = self._get_cfg(cfg_general,
                                             ConfigParserGeneral,
                                             "general")
        except MissingFileError as e:
            raise MissingGeneralConfigFileError(e.path)

        self.cfg_bogons = self._get_cfg(cfg_bogons,
                                        ConfigParserBogons,
                                        "bogons")

        if isinstance(cfg_clients, str):
            self.cfg_asns = self._get_cfg(cfg_clients,
                                            ConfigParserASNS,
                                            "asns")
        else:
            self.cfg_asns = ConfigParserASNS()
            self.cfg_asns._load_from_yaml("{}")
            self.cfg_asns.parse()

        self.cfg_clients = self._get_cfg(cfg_clients,
                                         ConfigParserClients,
                                         "clients",
                                         general_cfg=self.cfg_general)

        self.asn3216_map = self.cfg_clients.asn3216_map

        self.kwargs = kwargs

        # Initially None; is set to IRRDB() and finally populated by
        # the IRRDB enrichers.
        # { "<as_set_bundle_id>": <IRRDBRecord>, ... }
        self.irrdb_info = None

        # { "<len>": [{"prefix": "<ip>/<len>", "max_len": x, "asn": "AS<n>"}]
        self.rpki_roas = {}

        # [<asn (int)>]
        self.never_via_route_servers_asns = []

        # { "<origin_asn>": ["a/b", "c/d"] }
        self.arin_whois_records = {}
        self.registrobr_whois_records = {}

        # Validation

        if self.local_files:
            if not isinstance(self.local_files, list):
                raise BuilderError(
                    "local_files must be a list of .local files IDs"
                )
            for local_file_id in self.local_files:
                if local_file_id not in self.LOCAL_FILES_IDS:
                    raise BuilderError(
                        "The .local file ID '{}' is invalid.".format(
                            local_file_id
                        )
                    )

        if self.cfg_general["rs_as"] > 65535 and self._are_there_32bit_clients():
            ext_comms_32bit = []

            for comm_name in ConfigParserGeneral.COMMUNITIES_SCHEMA:
                comm = self.cfg_general["communities"][comm_name]

                ext_comm = comm.get("ext")
                if not ext_comm:
                    continue

                if all(
                    (part.isdigit() and int(part) > 65535) or part == "peer_as"
                    for part in ext_comm.split(":")[1:]
                ):
                    ext_comms_32bit.append((comm_name, ext_comm))

            if ext_comms_32bit:
                ext_comms_32bit_asn_issue = (
                    "One or more BGP extended communities are defined which "
                    "may end up containing or matching both value parts "
                    "against a 32bit number. This is not possible since "
                    "only one part at a time can represent a 32bit integer. "
                    "This happens because the ASN used for the route server "
                    "is a 32bit number and also one or more 32bit ASN "
                    "clients are configured. In order to avoid unexpected "
                    "behaviours and/or loosing the functionalities implemented "
                    "by those communities please consider changing them, for "
                    "example using a 'placeholder' ASN instead of the "
                    "actual route server ASN ({rs_as}) or 'rs_as' macro. "
                    "The list of affected communities follows: {comms_list}"
                ).format(
                    rs_as=self.cfg_general["rs_as"],
                    comms_list=", ".join(
                        "{comm_name} ({comm_value})".format(
                            comm_name=comm_name,
                            comm_value=comm_value
                        )
                        for comm_name, comm_value in ext_comms_32bit
                    )
                )
                if not self.process_compatibility_issue(
                    "ext-comms-32bit-asn",
                    ext_comms_32bit_asn_issue
                ):
                    raise CompatibilityIssuesError(
                        "One or more compatibility issues have been found."
                    )

        # Check overlapping BGP communities again, this time after we know
        # if there are 16bit private ASNs used to map 32bit ASN clients.
        self.cfg_general.check_overlapping_communities(
            mapped_16bit_asns=self.asn3216_map.values()
        )

        if not self.validate_bgpspeaker_specific_configuration():
            raise CompatibilityIssuesError(
                "One or more compatibility issues have been found."
            )

        # Processing

        logging.info("Started processing configuration "
                     "for {}".format(self.template_path))

        start_time = int(time.time())

        self.enrich_config()

        stop_time = int(time.time())

        logging.info("Configuration processing completed after "
                     "{} seconds.".format(stop_time - start_time))

    def _are_there_32bit_clients(self):
        for client in self.cfg_clients.cfg["clients"]:
            if client["asn"] > 65535:
                return True
        return False

    def _get_rfc8950_clients(self):
        res = []
        for client in self.cfg_clients.cfg["clients"]:
            if client["cfg"]["rfc8950"]:
                res.append(client["ip"])
        return res

    def enrich_config(self):
        # Unique ASNs from clients list.
        clients_asns = {}

        for client in self.cfg_clients.cfg["clients"]:
            # Unique ASNs
            asn = "AS{}".format(client["asn"])
            if asn in clients_asns:
                clients_asns[asn] += 1
            else:
                clients_asns[asn] = 1

            # Client's ID
            # Set 'id' as ASx_y where
            # x = ASN
            # y = progressive counter of clients per ASN
            client_id = "{}_{}".format(
                asn, clients_asns[asn]
            )
            client["id"] = client_id

        # BGP communities metadata
        for comm_name in ConfigParserGeneral.COMMUNITIES_SCHEMA:
            comm = ConfigParserGeneral.COMMUNITIES_SCHEMA[comm_name]
            self.cfg_general["communities"][comm_name]["type"] = comm["type"]
            self.cfg_general["communities"][comm_name]["peer_as"] = comm.get("peer_as", False)

        # Enrichers
        # Order matters: AS-SET from PeeringDB must be run first
        # in order to acquire missing AS-SETs that are processed
        # later by IRRDB enrichers. RPKI ROAs (when only used as
        # route objects) are processed only
        # for those origin ASNs that have been gathered from AS-SETs.
        filtering = self.cfg_general["filtering"]
        irrdb_cfg = filtering["irrdb"]
        used_enricher_classes = []

        if irrdb_cfg["peering_db"]:
            used_enricher_classes += [PeeringDBConfigEnricher_ASSet]

        used_enricher_classes += [IRRDBConfigEnricher_ASNs,
                                  IRRDBConfigEnricher_Prefixes,
                                  PeeringDBConfigEnricher_MaxPrefix]

        if self.cfg_general.rtt_based_functions_are_used:
            used_enricher_classes.append(RTTGetterConfigEnricher)

        if self.cfg_general.rpki_roas_needed and \
            self.cfg_general["rpki_roas"]["source"] == \
                "ripe-rpki-validator-cache":
            used_enricher_classes.append(RPKIROAsEnricher)

        if irrdb_cfg["use_arin_bulk_whois_data"]["enabled"]:
            used_enricher_classes.append(ARINWhoisDBDumpEnricher)

        if irrdb_cfg["use_registrobr_bulk_whois_data"]["enabled"]:
            used_enricher_classes.append(RegistroBRWhoisDBDumpEnricher)

        self.never_via_route_servers_asns = list(
            set(filtering["never_via_route_servers"]["asns"] or [])
        )
        if filtering["never_via_route_servers"]["peering_db"]:
            used_enricher_classes.append(NeverViaRouteServersEnricher)

        for enricher_class in used_enricher_classes:
            enricher = enricher_class(self, threads=self.threads)
            try:
                enricher.enrich()
            except ARouteServerError as e:
                if str(e):
                    logging.error(str(e))

                raise BuilderError()

    def _include_local_file(self, local_file_id):
        raise NotImplementedError()

    def render_template(self, output_file=None):
        """Render the output configuration.

        Raises:

            ARouteServerError or derived exceptions
              (from pierky.arouteserver.errors).

              Exceptions raised here can have no arguments and their string
              representation can be empty: in these cases, it means that
              one or more errors have been logged using the ``logging`` module.

        Args:

            output_file (file): the output file where the configuration must
                be written.
        """

        def sorted_rpki_roas():
            """Returns a list of ROAs, sorted by prefix length, prefix, ASN"""
            res = []
            prefix_lengths = sorted(map(int, self.rpki_roas.keys()))
            for pref_len in prefix_lengths:
                for roa in sorted(self.rpki_roas[str(pref_len)],
                                  key=lambda r: (r["prefix"], r["asn"])):
                    res.append(roa)
            return res

        def get_output_file_for_router_id(router_id):
            if (
                output_file is sys.stdout or \
                output_file.name == "<stdout>" or \
                output_file.fileno() == 1
            ):
                output_file.write("\n\n# Configuration for router_id {} follows\n\n".format(router_id))
                return output_file

            output_file_path = output_file.name
            output_file_name = os.path.basename(output_file_path)
            output_file_dir = os.path.dirname(output_file_path)

            if "." in output_file_name:
                output_file_ext = "." + output_file_name.split(".")[-1]
                output_file_name_no_ext = ".".join(output_file_name.split(".")[0:-1])
            else:
                output_file_ext = ""
                output_file_name_no_ext = output_file_name

            return open(
                os.path.join(
                    output_file_dir,
                    output_file_name_no_ext + "-" + router_id + output_file_ext
                ), "w"
            )

        router_ids = copy.deepcopy(self.cfg_general["router_id"])

        if not isinstance(router_ids, list):
            router_ids = [router_ids]

        multiple_router_ids = len(router_ids) > 1

        if multiple_router_ids and not output_file:
            raise RuntimeError(
                "When multiple router IDs are configured, render_template "
                "must be called with output_file set. If it's used as a library "
                "and the route server configuration is expected to be returned "
                "as a string, then multiple calls must be made, one for each "
                "route server."
            )

        self.data = {}
        self.data["ip_ver"] = self.ip_ver
        if self.ip_ver is None:
            self.data["list_ip_vers"] = [4, 6]
        else:
            self.data["list_ip_vers"] = [self.ip_ver]
        self.data["cfg"] = self.cfg_general
        self.data["bogons"] = self.cfg_bogons
        self.data["clients"] = self.cfg_clients
        self.data["asns"] = self.cfg_asns
        self.data["asn3216_map"] = self.asn3216_map
        self.data["irrdb_info"] = self.irrdb_info
        self.data["rpki_roas"] = sorted_rpki_roas()
        self.data["arin_whois_records"] = self.arin_whois_records
        self.data["registrobr_whois_records"] = self.registrobr_whois_records
        self.data["never_via_route_servers_asns"] = self.never_via_route_servers_asns
        self.data["live_tests"] = self.live_tests
        self.data["rtt_based_functions_are_used"] = \
            self.cfg_general.rtt_based_functions_are_used
        self.data["perform_graceful_shutdown"] = self.perform_graceful_shutdown
        self.data["reject_reasons"] = REJECT_REASONS
        self.data["any_reject_cause_map_community_set"] = self.cfg_general.any_reject_cause_map_community_set

        def ipaddr_ver(ip):
            return IPNetwork(ip).version

        def current_ipver(ip):
            if self.ip_ver is None:
                return True
            return IPNetwork(ip).version == self.ip_ver

        def is_ipver(data, ip_ver):
            prefix = data
            return IPNetwork(prefix).version == ip_ver

        def is_local_file_used(local_file_id):
            if local_file_id not in self.LOCAL_FILES_IDS:
                raise AssertionError(
                    "Local file ID '{}' is referenced in J2 "
                    "templates but is not in LOCAL_FILES_IDS.".format(
                        local_file_id
                    )
                )
            local_files = self.local_files or []
            return local_file_id in local_files

        def include_local_file(local_file_id):
            # The 'rpki_rtr_config' local_file_id is always allowed
            # to be included, because it's referenced directly in
            # the Jinja2 template for RPKI configuration.
            if local_file_id == "rpki_rtr_config":
                return self._include_local_file(local_file_id)

            if local_file_id not in self.LOCAL_FILES_IDS:
                raise AssertionError(
                    "Local file ID '{}' is referenced in J2 "
                    "templates but is not in LOCAL_FILES_IDS.".format(
                        local_file_id
                    )
                )
            local_files = self.local_files or []
            if local_file_id in local_files:
                return self._include_local_file(local_file_id)
            return ""

        def target_version_ge(v):
            if self.target_version:
                return version.parse(self.target_version) >= version.parse(v)
            return False

        def target_version_le(v):
            if self.target_version:
                return version.parse(self.target_version) <= version.parse(v)
            return False

        def target_version_lt(v):
            if self.target_version:
                return version.parse(self.target_version) < version.parse(v)
            return False

        def get_normalized_rtt(v):
            if not v:
                return 0
            if v < 1:
                return 1
            if v > 60000:
                return 60000
            return int(round(v))

        def community_is_set(comm):
            if not comm:
                return False
            if not comm["std"] and not comm["lrg"] and not comm["ext"]:
                return False
            return True

        def to_bgp_role(internal_role):
            return {
                "provider": "provider",
                "rs": "rs_server",
                "rs-client": "rs_client",
                "customer": "customer",
                "peer": "peer"
            }[internal_role]

        env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined
        )
        env.tests["current_ipver"] = current_ipver
        env.tests["is_ipver"] = is_ipver
        env.tests["used_local_file"] = is_local_file_used
        env.filters["community_is_set"] = community_is_set
        env.filters["ipaddr_ver"] = ipaddr_ver
        env.filters["include_local_file"] = include_local_file
        env.filters["target_version_ge"] = target_version_ge
        env.filters["target_version_le"] = target_version_le
        env.filters["target_version_lt"] = target_version_lt
        env.filters["get_normalized_rtt"] = get_normalized_rtt
        env.filters["to_bgp_role"] = to_bgp_role

        self.enrich_j2_environment(env)

        tpl = env.get_template(self.template_name)

        start_time = int(time.time())

        logging.info("Started template rendering "
                     "for {}".format(self.template_path))

        try:
            for router_id in router_ids:
                self.data["cfg"]["router_id"] = router_id

                if output_file and not multiple_router_ids:
                    for buf in tpl.generate(self.data):
                        output_file.write(buf)

                elif output_file and multiple_router_ids:
                    output_file_router_id = get_output_file_for_router_id(router_id)
                    output_file.write(
                        "Configuration for router_id {}: {}\n".format(
                            router_id, output_file_router_id.name
                        )
                    )
                    for buf in tpl.generate(self.data):
                        output_file_router_id.write(buf)

                else:
                    return tpl.render(self.data)
        except Exception as e:
            _, _, traceback = sys.exc_info()
            raise TemplateRenderingError(
                "Error while rendering template: {}".format(str(e)),
                traceback=traceback
            )
        finally:
            stop_time = int(time.time())

            logging.info("Template rendering completed after "
                        "{} seconds.".format(stop_time - start_time))

class BIRDConfigBuilder(ConfigBuilder):
    """BIRD configuration builder.

    The ``kwargs`` parameter of the ``__init__`` method can be used
    to pass the following additional arguments.

    Args:

        hooks (list): list of hook IDs for which to enable hooks in
            the output configuration. Details: https://arouteserver.readthedocs.io/en/latest/CONFIG.html#bird-hooks
    """

    LOCAL_FILES_IDS = ["logging",
                       "header", "header4", "header6",
                       "footer", "footer4", "footer6",
                       "client", "client4", "client6"]
    LOCAL_FILES_BASE_DIR = "/etc/bird"

    HOOKS = ["pre_receive_from_client", "post_receive_from_client",
             "pre_announce_to_client", "post_announce_to_client",
             "route_can_be_announced_to", "announce_rpki_invalid_to_client",
             "scrub_communities_in", "scrub_communities_out",
             "apply_blackhole_filtering_policy"]

    IGNORABLE_ISSUES = ConfigBuilder.IGNORABLE_ISSUES + ["max_prefix_count_rejected_routes", "ipv6_link_local_next_hop"]

    AVAILABLE_VERSION = ["1.6.3", "1.6.4", "1.6.6", "1.6.7", "1.6.8",
                         "2.0.7", "2.0.7+b962967e", "2.0.8", "2.0.9",
                         "2.0.10", "2.0.11", "2.13", "2.14", "2.15",
                         "2.16",
                         "3.0"]
    DEFAULT_VERSION = "2.16"

    def validate_bgpspeaker_specific_configuration(self):
        res = True

        if self.ip_ver is None and \
           version.parse(self.target_version) < version.parse("2.0"):
            raise BuilderError(
                "An explicit target IP version is needed "
                "to build BIRD 1.x configuration. Use the "
                "--ip-ver command line argument to supply one."
            )

        hooks = self.kwargs.get("hooks", [])
        if hooks:
            if not isinstance(hooks, list):
                raise BuilderError(
                    "hooks must be a list of hook names."
                )

        for client in self.cfg_clients.cfg["clients"]:
            if client["cfg"]["multihop"]:
                if self.cfg_general["path_hiding"]:
                    raise BuilderError(
                        "multihop is not supported on BIRD configurations "
                        "when path_hiding mitigation is enabled; "
                        "see https://github.com/pierky/arouteserver/pull/61 "
                        "for more details."
                    )

        if self.ip_ver is None or self.ip_ver == 6:
            link_local_clients = []

            for client in self.cfg_clients.cfg["clients"]:
                ip = client["ip"]
                if IPAddress(ip).obj.is_link_local:
                    link_local_clients.append(ip)

            if link_local_clients:
                if not self.process_compatibility_issue(
                    "ipv6_link_local_next_hop",
                    "Due to a limitation of BIRD, it is not possible to verify "
                    "the NEXT_HOP attribute of routes announced by the following "
                    "IPv6 clients, because the BGP sessions are configured "
                    "using link-local addresses, which are not handled correctly "
                    "by the BIRD function that returns the next-hop: {}".format(
                        ", ".join(link_local_clients)
                    )
                ):
                    res = False

        if version.parse(self.target_version) == version.parse("2.0.7"):
            max_prefix_count_rejected_routes_clients = []

            for client in self.cfg_clients.cfg["clients"]:
                max_prefix_count_rejected_routes = client["cfg"]["filtering"]["max_prefix"]["count_rejected_routes"]
                if max_prefix_count_rejected_routes:
                    max_prefix_count_rejected_routes_clients.append(client["ip"])

            if (
                self.cfg_general["filtering"]["max_prefix"]["count_rejected_routes"] or \
                max_prefix_count_rejected_routes_clients
            ):
                if not self.process_compatibility_issue(
                    "max_prefix_count_rejected_routes",
                    "In BIRD, the functionality represented by the "
                    "'count_rejected_routes: True' option is "
                    "implemented using the 'receive limit' statement. "
                    "According to some tests, BIRD 2.0.7 is affected by "
                    "an issue that prevents that statement from working "
                    "correctly when it's used along with some other "
                    "options that are needed by ARouteServer "
                    "configurations (see {link_bird} for more details). "
                    "Even though beginning with ARouteServer 1.0.1 the "
                    "default value of 'count_rejected_routes' is True, "
                    "it's not advisable to deploy any configuration for "
                    "BIRD 2.0.7 that uses that setting at the moment. "
                    "Now, there are 3 ways to unblock the build of the "
                    "configuration: 1) this error can be ignored using "
                    "the command line argument mentioned later on in "
                    "this message; 2) the value of "
                    "'count_rejected_routes' can be set to False; 3) "
                    "--target-version can be set to 2.0.7+b962967e. "
                    "If this error will be ignored, the configuration "
                    "will be generated as if that option was set to "
                    "False; this may be a good option if the goal is "
                    "to have the desired behaviour of counting rejected "
                    "routes towards the max-prefix limit implemented in "
                    "any future release of BIRD 2.0 for which the issue "
                    "will be solved. In this case, future releases of "
                    "ARouteServer will skip this check if the "
                    "--target-version will be set to the release for "
                    "which the issue is fixed. "
                    "The other option, that is to specifically configure "
                    "'count_rejected_routes: False', may be the best one "
                    "if the goal is to keep the currently available "
                    "behaviour (that is to not count rejected routes "
                    "towards the max-prefix limit) permanent in the "
                    "configurations generated by this tool. For more "
                    "details on how to configure it, see the general.yml "
                    "file distributed with the package or check this "
                    "URL: {link_ars}. The third option is to apply the "
                    "patch mentioned at {patch_url} and pass the value "
                    "2.0.7+b962967e via the --target-version command "
                    "line argument.".format(
                        link_bird=("https://www.mail-archive.com/bird-users"
                                   "@network.cz/msg05597.html"),
                        link_ars=("https://arouteserver.readthedocs.io/"
                                  "en/latest/GENERAL.html#max-prefix-max-prefix"),
                        patch_url=("https://www.mail-archive.com/bird-users"
                                   "@network.cz/msg05638.html")
                    )
                ):
                    res = False
                else:
                    self.cfg_general["filtering"]["max_prefix"]["count_rejected_routes"] = False
                    for client in self.cfg_clients.cfg["clients"]:
                        client["cfg"]["filtering"]["max_prefix"]["count_rejected_routes"] = False

        if version.parse(self.target_version) < version.parse("2.0.11"):
            if self.cfg_general["filtering"]["roles"]["enabled"]:
                if not self.process_compatibility_issue(
                    "roles_not_available",
                    "RFC9234 roles are not available in BIRD < 2.0.11, but "
                    "they are enabled in the general.yml file."
                ):
                    res = False

            for client in self.cfg_clients.cfg["clients"]:
                if client["cfg"]["filtering"]["roles"]["enabled"]:
                    if not self.process_compatibility_issue(
                        "roles_not_available",
                        "RFC9234 roles are not available in BIRD < 2.0.11, but "
                        "they are enabled in the configuration of client {}".format(
                            client["ip"]
                        )
                    ):
                        res = False

        if version.parse(self.target_version) < version.parse("2.0"):
            rfc8950_clients = self._get_rfc8950_clients()
            cnt = len(rfc8950_clients)
            if rfc8950_clients:
                raise BuilderError(
                    "RFC8950 is not supported on BIRD 1.x, but it is "
                    "enabled for the following clients: {}{}.".format(
                        ", ".join(rfc8950_clients[:3]),
                        "" if cnt <= 3 else " and {} more".format(cnt - 3)
                    )
                )

        return res

    def _include_local_file(self, local_file_id):
        return 'include "{}";\n\n'.format(
            os.path.join(
                self.local_files_dir or self.LOCAL_FILES_BASE_DIR,
                "{}.local".format(local_file_id)
            )
        )

    def enrich_j2_environment(self, env):

        def hook_is_set(hook_name):
            if hook_name not in self.HOOKS:
                raise AssertionError(
                    "Hook '{}' is referenced in J2 "
                    "templates but is not in HOOKS.".format(hook_name)
                )
            hooks = self.kwargs.get("hooks", []) or []
            return hook_name in hooks

        env.filters["hook_is_set"] = hook_is_set

class OpenBGPDConfigBuilder(ConfigBuilder):
    """OpenBGPD configuration builder.
    """

    LOCAL_FILES_IDS = ["logging", "header",
                       "pre-irrdb", "post-irrdb",
                       "pre-clients", "post-clients", "client",
                       "pre-filters", "post-filters",
                       "footer"]
    LOCAL_FILES_BASE_DIR = "/etc/bgpd"

    AVAILABLE_VERSION = ["7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7",
                         "7.8", "8.0", "8.3", "8.4", "8.7"]
    DEFAULT_VERSION = AVAILABLE_VERSION[-1]

    IGNORABLE_ISSUES = ConfigBuilder.IGNORABLE_ISSUES + \
                        ["transit_free_action",
                        "add_path", "max_prefix_action",
                        "max_prefix_count_rejected_routes",
                        "rfc8950",
                        "extended_communities",
                        "internal_communities",
                        "roles_discouraged"]

    def _include_local_file(self, local_file_id):
        return 'include "{}"\n\n'.format(
            os.path.join(
                self.local_files_dir or self.LOCAL_FILES_BASE_DIR,
                "{}.local".format(local_file_id)
            )
        )

    def validate_bgpspeaker_specific_configuration(self):
        res = True

        transit_free_action = self.cfg_general["filtering"]["transit_free"]["action"]
        if transit_free_action and transit_free_action != "reject":
            if not self.process_compatibility_issue(
                "transit_free_action",
                "Transit free ASNs policy is configured with "
                "'action' = '{}' but only 'reject' is supported "
                "for OpenBGPD.".format(transit_free_action)
            ):
                res = False

        reject_policy = self.cfg_general["filtering"]["reject_policy"]["policy"]
        if reject_policy == "tag_and_reject":
            raise BuilderError(
                "For OpenBGP, 'reject_policy' can't be set to "
                "'tag_and_reject'."
            )

        add_path_clients = []
        max_prefix_action_clients = []
        max_prefix_count_rejected_routes_clients = []
        for client in self.cfg_clients.cfg["clients"]:
            if client["cfg"]["add_path"]:
                add_path_clients.append(client["ip"])

            max_prefix_action = client["cfg"]["filtering"]["max_prefix"]["action"]
            if max_prefix_action:
                if max_prefix_action not in ("shutdown", "restart"):
                    max_prefix_action_clients.append(client["ip"])

            max_prefix_count_rejected_routes = client["cfg"]["filtering"]["max_prefix"]["count_rejected_routes"]
            if not max_prefix_count_rejected_routes:
                max_prefix_count_rejected_routes_clients.append(client["ip"])

        if add_path_clients and \
            version.parse(self.target_version) < version.parse("7.5"):

            clients = add_path_clients
            cnt = len(clients)
            if not self.process_compatibility_issue(
                "add_path",
                "ADD_PATH not supported by OpenBGPD < 7.5 but "
                "enabled for the following clients: {}{}.".format(
                    ", ".join(clients[:3]),
                    "" if cnt <= 3 else " and {} more".format(cnt - 3)
                )
            ):
                res = False

        if max_prefix_action_clients:
            clients = max_prefix_action_clients
            cnt = len(clients)
            if not self.process_compatibility_issue(
                "max_prefix_action",
                "Invalid max-prefix 'action' for the following "
                "clients: {}{}; only 'shutdown' and 'restart' "
                "are supported by OpenBGPD.".format(
                    ", ".join(clients[:3]),
                    "" if cnt <= 3 else " and {} more".format(cnt - 3)
                )
            ):
                res = False

        if max_prefix_count_rejected_routes_clients:
            clients = max_prefix_count_rejected_routes_clients
            cnt = len(clients)
            if not self.process_compatibility_issue(
                "max_prefix_count_rejected_routes",
                "Invalid max-prefix 'count_rejected_routes' option for "
                "the following clients: {}{}; in OpenBGPD, the "
                "only available behaviour is to have the "
                "rejected routes counted towards the limit.".format(
                    ", ".join(clients[:3]),
                    "" if cnt <= 3 else " and {} more".format(cnt - 3)
                )
            ):
                res = False

        rfc8950_clients = self._get_rfc8950_clients()
        if rfc8950_clients:
            cnt = len(rfc8950_clients)
            if not self.process_compatibility_issue(
                "rfc8950",
                "RFC8950 not supported by OpenBGPD but "
                "enabled for the following clients: {}{}.".format(
                    ", ".join(rfc8950_clients[:3]),
                    "" if cnt <= 3 else " and {} more".format(cnt - 3)
                )
            ):
                res = False

        if self.cfg_general["filtering"]["roles"]["enabled"]:
            if version.parse(self.target_version) < version.parse("7.5"):
                if not self.process_compatibility_issue(
                    "roles_not_available",
                    "RFC9234 roles are not available in OpenBGPD < 7.5, but "
                    "they are enabled in the general.yml file."
                ):
                    res = False
            elif version.parse(self.target_version) <= version.parse("7.7"):
                if not self.process_compatibility_issue(
                    "roles_discouraged",
                    "Implementation of RFC9234 roles in OpenBGPD <= 7.7 "
                    "is discouraged by the developers "
                    "(see https://github.com/openbgpd-portable/openbgpd-portable/issues/51) "
                    "but they are enabled in the general.yml file."
                ):
                    res = False

            for client in self.cfg_clients.cfg["clients"]:
                if client["cfg"]["filtering"]["roles"]["enabled"]:
                    if version.parse(self.target_version) < version.parse("7.5"):
                        if not self.process_compatibility_issue(
                            "roles_not_available",
                            "RFC9234 roles are not available in OpenBGPD < 7.5, but "
                            "they are enabled in the configuration of client {}".format(
                                client["ip"]
                            )
                        ):
                            res = False
                    elif version.parse(self.target_version) <= version.parse("7.7"):
                        if not self.process_compatibility_issue(
                            "roles_discouraged",
                            "Implementation of RFC9234 roles in OpenBGPD <= 7.7 "
                            "is discouraged by the developers "
                            "(see https://github.com/openbgpd-portable/openbgpd-portable/issues/51) "
                            "but they are enabled in the configuration of client {}".format(
                                client["ip"]
                            )
                        ):
                            res = False

        peer_as_ext_comms = []
        for comm_name in ConfigParserGeneral.COMMUNITIES_SCHEMA:
            comm = self.cfg_general["communities"][comm_name]

            # peer_as ext communities not scrubbed
            comm_def = ConfigParserGeneral.COMMUNITIES_SCHEMA[comm_name]
            peer_as = comm_def.get("peer_as", False)
            direction = comm_def.get("type", None)

            if peer_as and direction == "inbound" and comm["ext"]:
                peer_as_ext_comms.append((comm_name, comm["ext"]))

        if peer_as_ext_comms:
            comms = peer_as_ext_comms
            if not self.process_compatibility_issue(
                "extended_communities",
                "The peer-ASN-specific communit{y_ies} '{names}' "
                "ha{s_ve} been configured to be implemented using the "
                "extended communit{y_ies} '{comms}'; please be aware that "
                "peer-ASN-specific extended communities are not scrubbed "
                "from routes that leave OpenBGPD route servers and they are "
                "propagated to the route server clients.".format(
                    y_ies="y" if len(comms) == 1 else "ies",
                    names=", ".join([_[0] for _ in comms]),
                    s_ve="s" if len(comms) == 1 else "ve",
                    comms=", ".join([_[1] for _ in comms])
                )
            ):
                res = False

        try:
            self.cfg_general.check_overlapping_communities(
                mapped_16bit_asns=self.asn3216_map.values(),
                allow_private_asns=False
            )
        except ConfigError as e:
            raise BuilderError(
                "{}OpenBGPD doesn't allow to delete BGP "
                "communities using ranges of values, but only "
                "using the wildcard ('*'), so also "
                "outbound communities whose last part contain "
                "private ASNs collide with inbound communities "
                "that use the 'peer_as' macro.".format(
                    str(e) + " " if str(e) else ""
                )
            )

        internal_communities_collistion = []
        for comm_name in ConfigParserGeneral.COMMUNITIES_SCHEMA:
            comm = self.cfg_general["communities"][comm_name]
            if comm["ext"] and comm["ext"].startswith("ro:65535:"):
                internal_communities_collistion.append(comm_name)
        if internal_communities_collistion:
            if not self.process_compatibility_issue(
                "internal_communities",
                "The Extended BGP communities in the range ro:65535:* "
                "are reserved for internal purposes. "
                "A collision has been detected with the following "
                "communit{y_ies}: {comms}".format(
                    y_ies="y" if len(internal_communities_collistion) == 1 else "ies",
                    comms=", ".join(internal_communities_collistion)
                )
            ):
                res = False

        return res

    def enrich_j2_environment(self, env):

        def convert_ext_comm(s):
            parts = s.split(":")
            return "{} {}:{}".format(
                parts[0], parts[1], parts[2]
            )

        def at_least_one_client_uses_tag_reject_policy():
            for client in self.cfg_clients.cfg["clients"]:
                policy = client["cfg"]["filtering"]["reject_policy"]["policy"]
                if policy == "tag":
                    return True
            return False

        def community_is_set(comm):
            if not comm:
                return False

            if not comm["std"] and not comm["ext"] and not comm["lrg"]:
                return False

            return True

        def aggregated_roas_covered_space():
            prefixes = []
            for pref_len in self.rpki_roas:
                for roa in self.rpki_roas[pref_len]:
                    prefixes.append(roa["prefix"])
            return aggregate(prefixes)

        env.filters["convert_ext_comm"] = convert_ext_comm
        env.filters["community_is_set"] = community_is_set
        self.data["at_least_one_client_uses_tag_reject_policy"] = \
            at_least_one_client_uses_tag_reject_policy()
        self.data["rpki_roas_covered_space"] = aggregated_roas_covered_space()

class TemplateContextDumper(ConfigBuilder):

    def enrich_j2_environment(self, env):

        def to_yaml(obj):
            return yaml.safe_dump(obj, default_flow_style=False)

        def parse_irrdb_info(irrdb_info):
            lst = []
            for bundle_id in irrdb_info:
                bundle = irrdb_info[bundle_id]
                lst.append(bundle.to_dict())
            return lst

        def parse_generic_irr_whois_records(records):
            res = {}
            for origin_asn in records:
                res[origin_asn] = list(records[origin_asn].prefixes)
            return res

        env.filters["to_yaml"] = to_yaml
        env.filters["parse_irrdb_info"] = parse_irrdb_info
        env.filters["parse_generic_irr_whois_records"] = parse_generic_irr_whois_records

class IRRASSetBuilder(ConfigBuilder):

    @staticmethod
    def _get_source_from_template_file(path):
        with open(path, "r") as f:
            for line in f.readlines():
                if not line.strip():
                    continue

                if line.strip().startswith(("source:", "- source:")):
                    return line.strip().split(":")[1].strip()

        return None

    @staticmethod
    def _get_as_set_info(as_set):
        v = as_set.strip()

        # Removing "ipv4:" and "ipv6:".
        pattern = re.compile("^(?:ipv4|ipv6):", flags=re.IGNORECASE)
        v, number_of_subs_made = pattern.subn("", v)
        if number_of_subs_made > 0:
            v = v.strip()

        # Catching AS-FOO@SOURCE
        pattern = re.compile("^([^@]+)@(.+)$", flags=re.IGNORECASE)
        match = pattern.match(v)
        if match:
            return match.group(2), match.group(1)

        # Catching ASxxx:AS-FOO.
        pattern = re.compile("^AS\\d+:[^:].+$", flags=re.IGNORECASE)
        if pattern.match(v):
            return None, v

        # Catching "SOURCE:AS-FOO" (single colon)
        pattern = re.compile("^([^:]+):([^:].+)$", flags=re.IGNORECASE)
        match = pattern.match(v)
        if match:
            return match.group(1), match.group(2)

        # Catching "SOURCE::AS-FOO" (double colon)
        pattern = re.compile("^([^:]+)::([^:]?.+)$", flags=re.IGNORECASE)
        match = pattern.match(v)
        if match:
            return match.group(1), match.group(2)

        return None, v

    def _get_valid_as_sets(self, original_list):
        res = []
        for raw_as_set in original_list:
            source, as_set = self._get_as_set_info(raw_as_set)

            if source:
                if source == self._source:
                    res.append(as_set)
                else:
                    logging.warning(
                        f"AS-SET {raw_as_set} omitted because its source "
                        f"({source}) does not match the source used in "
                        f"the template ({self._source})"
                    )
            else:
                res.append(as_set)

        return res

    def __init__(self, *args, **kwargs):
        super(IRRASSetBuilder, self).__init__(*args, **kwargs)

        self._source = self._get_source_from_template_file(self.template_path)
        self._include_members = kwargs.get("include_members")
        self._exclude_members = kwargs.get("exclude_members")

    def enrich_j2_environment(self, env):

        if self.ip_ver is None:
            self.data["ip_ver_suffix"] = ""
            self.data["ip_ver_descr"] = "IPv4 and IPv6"
        else:
            self.data["ip_ver_suffix"] = "-V{}".format(self.ip_ver)
            self.data["ip_ver_descr"] = "IPv{}".format(self.ip_ver)

        members = set()

        for client in self.cfg_clients.cfg["clients"]:
            if self.ip_ver is not None:
                ip = client["ip"]
                if IPAddress(ip).version != self.ip_ver:
                    # The address family of this client is not the
                    # current one used to build the configuration.
                    continue

            client_irrdb = client["cfg"]["filtering"]["irrdb"]

            # Client's own ASN.
            members.add("AS{}".format(client["asn"]))

            # White lists.
            if client_irrdb.get("white_list_asn", None):
                for white_list_asn in client_irrdb.get("white_list_asn", []):
                    members.add("AS{}".format(white_list_asn))

            # The client has its own list of AS-SETs.
            # Use it and move to the next client.
            if client_irrdb["as_sets"]:
                members.update(self._get_valid_as_sets(client_irrdb["as_sets"]))
                continue

            # If we're here, it means that the client
            # has no AS-SETs configured.
            # Let's look into the 'asns' configuration.

            asn = "AS{}".format(client["asn"])
            if asn in self.cfg_asns.cfg["asns"] and \
                self.cfg_asns.cfg["asns"][asn]["as_sets"]:

                # The client ASN is configured in the 'asns'
                # section of the clients.yml file and there
                # are AS-SETs set on it. Let's use them.
                members.update(self._get_valid_as_sets(self.cfg_asns.cfg["asns"][asn]["as_sets"]))
                continue

            # Let's check if AS-SETs were found on PeeringDB.

            as_sets_from_pdb = client.get("as_sets_from_pdb", None)
            if as_sets_from_pdb:
                logging.info("No AS-SETs provided for the '{}' client. "
                             "Using AS{} + those obtained from PeeringDB: "
                             "{}.".format(
                                    client["id"], client["asn"],
                                    ", ".join(as_sets_from_pdb)
                                ))
                members.update(self._get_valid_as_sets(as_sets_from_pdb))
                continue

            # No other AS-SETs found for the client.
            logging.warning("No AS-SETs provided for the '{}' client. "
                            "Only AS{} will be expanded.".format(
                                client["id"], client["asn"]
                            ))

        if self._include_members:
            for member in self._include_members.split(","):
                members.add(member.strip())

        if self._exclude_members:
            for member in self._exclude_members.split(","):
                member = member.strip()
                if member in members:
                    members.remove(member)

        self.data["as_sets_rpsl_objects"] = sorted(members)
