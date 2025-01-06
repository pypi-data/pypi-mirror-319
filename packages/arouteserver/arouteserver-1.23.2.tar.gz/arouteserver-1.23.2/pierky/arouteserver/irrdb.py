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

import hashlib
import json
import logging
import re
import subprocess

from .cached_objects import CachedObject
from .config.validators import ValidatorPrefixListEntry
from .errors import IRRDBToolsError
from .ipaddresses import IPNetwork


TIMEDOUT_IRR_HOSTS = set()


class AS_SET_Bundle(object):

    @staticmethod
    def get_source(object_names):
        """Returns (source_to_use, is_same_for_all)

        In case of multiple objects, the first specific source found
        will be used. Otherwise source_to_use will be None (use the
        default sources).
        """

        sources = []
        for name in object_names:
            source_macro = name.split("::")
            if len(source_macro) > 1:
                sources.append(source_macro[0])
            else:
                sources.append(None)

        same_for_all = len(set(sources)) == 1

        not_none = [_ for _ in sources if _ is not None]
        if not_none:
            used_source = not_none[0].upper()
        else:
            used_source = None

        return (used_source, same_for_all)

    def __init__(self, object_names):
        assert isinstance(object_names, list)

        self.source, _ = self.get_source(object_names)

        self.object_names = sorted([n.upper() for n in set(object_names)])

        # id, internal unique identifier.
        buf = "_".join(self.object_names)
        hasher = hashlib.sha512()
        hasher.update(buf.encode("utf-8"))
        self.id = hasher.hexdigest()

        # descr, textual description of the bundle.
        # Do not use it in templates unless within comments.
        self.descr = ", ".join(self.object_names[:3])
        if len(self.object_names) > 3:
            self.descr += " and {} more".format(len(self.object_names) - 3)

        # name, brief textual representation of the bundle.
        # Only [a-zA-Z0-9_] characters.
        # Can be used in templates.
        if len(self.object_names) == 1:
            self.name = self.object_names[0]
        elif len(self.object_names) <= 3:
            self.name = "_".join(self.object_names)
        else:
            self.name = "{name}_and_{more}_more_{short_hash}".format(
                name=self.object_names[0],
                more=len(self.object_names) - 1,
                short_hash=self.id[:7]
            )
        self.name = re.sub("[^a-zA-Z0-9_]", "_", self.name)

        # The name will be used to generate config statements
        # like AS_SET_<name>_asns and AS_SET_<name>_prefixes.
        #
        # In BIRD there is a limit of 64 characters for symbols:
        #
        #   #define SYM_MAX_LEN 64
        #
        # so every name that, once concatenated to the prefix
        # and suffix above, will be longer than 64 characters
        # is here truncated, and a "random" tag is attached
        # to it in order to make it unique.
        #
        # 16 is the length of "AS_SET_" + "_prefixes", the longest
        # combination of prefix and suffix.

        if len(self.name) + 16 > 64:
            TAG_LEN = 5
            hash_str = hashlib.md5(self.name.encode("utf-8")).hexdigest()
            tag = hash_str[:TAG_LEN]
            max_name_len = 64 - 16 - TAG_LEN - 1
            self.name = self.name[:max_name_len] + "_" + tag

class IRRDBInfo(CachedObject, AS_SET_Bundle):

    BGPQ3_DEFAULT_HOST = ["rr.ntt.net", "rr1.ntt.net"]
    BGPQ3_DEFAULT_SOURCES = ("RIPE,APNIC,AFRINIC,ARIN,NTTCOM,ALTDB,"
                             "BBOI,BELL,JPIRR,LEVEL3,RADB,TC")
    BGPQ3_DEFAULT_TIMEOUT = 120
    EXPIRY_TIME_TAG = "irr_as_sets"

    def __init__(self, object_names, *args, **kwargs):
        assert isinstance(object_names, list)

        CachedObject.__init__(self, *args, **kwargs)
        self.bgpq3_path = kwargs.get("bgpq3_path")
        self.bgpq3_host = kwargs.get("bgpq3_host", self.BGPQ3_DEFAULT_HOST)
        self.bgpq3_sources = kwargs.get("bgpq3_sources",
                                        self.BGPQ3_DEFAULT_SOURCES)
        self.bgpq3_timeout = kwargs.get("bgpq3_timeout", self.BGPQ3_DEFAULT_TIMEOUT)

        self.bgpq = "bgpq4" if "bgpq4" in self.bgpq3_path else "bgpq3"

        AS_SET_Bundle.__init__(self, object_names)

    def _get_bgpq3_sources(self):
        if self.source:
            return "{},{}".format(self.source, self.bgpq3_sources)
        return self.bgpq3_sources

    def _get_bgpq3_names(self):
        res = []
        for name in self.object_names:
            source_macro = name.split("::")
            if len(source_macro) > 1:
                res.append(source_macro[1])
            else:
                res.append(source_macro[0])
        return res

    def _run_cmd(self, cmd):
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        try:
            out, err = proc.communicate(timeout=self.bgpq3_timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise

        if err is not None:
            err = err.decode("utf-8").strip()

        if proc.returncode != 0:
            err_msg = "{} exit code is {}".format(self.bgpq, proc.returncode)
            if err:
                err_msg += ", stderr: {}".format(err)
            raise ValueError(err_msg)

        if err:
            # If an error was returned, remove any line containing
            # "Invalid AS number:". This is printed to stderr when
            # private ASNs are found in the output, but it's just
            # confusing and not useful for the user.
            err_lines = err.split("\n")
            err = "\n".join([
                line
                for line in err_lines
                if "Invalid AS number:" not in line
            ])

            if err:
                logging.warning("{} succeeded but an error was "
                                "printed when executing '{}': {}".format(
                                    self.bgpq,
                                    " ".join(cmd), err
                                ))

        return out

    def _run_query(self, args):
        hosts_to_use = [
            host
            for host in self.bgpq3_host
            if host not in TIMEDOUT_IRR_HOSTS
        ]

        if not hosts_to_use:
            raise IRRDBToolsError(
                "All the IRRD hosts timed out so far; there are no more hosts "
                "to use to perform the IRR queries."
            )

        num_of_hosts = len(hosts_to_use)

        attempt_n = 0
        for host in hosts_to_use:
            attempt_n += 1

            cmd = [self.bgpq3_path]
            cmd += ["-h", host]
            cmd += ["-S", self._get_bgpq3_sources()]
            if "bgpq4" not in self.bgpq3_path:
                cmd += ["-3"]
            cmd += ["-j"]
            cmd += args

            try:
                out = self._run_cmd(cmd)

                return json.loads(out.decode("utf-8"))
            except subprocess.TimeoutExpired:
                err_msg = (
                    "{} timed out while running the following command: '{}' "
                    "The host {} will not be used for the next IRR queries. "
                    "The timeout is {} seconds; to modify it, please "
                    "edit the program's configuration file (usually "
                    "arouteserver.yml) and change the 'bgpq3_timeout' setting."
                ).format(
                    self.bgpq,
                    " ".join(cmd),
                    host,
                    self.bgpq3_timeout
                )
                TIMEDOUT_IRR_HOSTS.add(host)
            except Exception as e:
                err_msg = (
                    "Error while parsing {} output "
                    "for the following command: '{}': {}".format(
                        self.bgpq,
                        " ".join(cmd), str(e)
                    )
                )

            if attempt_n == num_of_hosts:
                raise IRRDBToolsError(
                    "{} - No more attempts will be performed, all the "
                    "hosts in the list failed.".format(err_msg)
                )
            else:
                logging.warning(
                    "{} - Another attempt will be performed using the next "
                    "host in the list.".format(err_msg)
                )


class ASSet(IRRDBInfo):

    def load_data(self):
        logging.debug("Getting ASNs for "
                      "{} from IRRdb".format(self.descr))

        IRRDBInfo.load_data(self)

        # list of int
        self.asns = self.raw_data

    def _get_object_filename(self):
        return "{}-as_set.json".format(self.name)

    def _get_data(self):
        object_names = self._get_bgpq3_names()

        # If the list of objects to expand is made up by
        # an 'ASxxx' element only, avoid to run bgpq3 and
        # return only that ASN.
        if len(object_names) == 1 and \
            re.match("^AS[0-9]+$", object_names[0]):
            return [int(object_names[0][2:])]

        query_args = []
        query_args += ["-f", "1"]
        query_args += ["-l", "asn_list"]
        query_args += object_names

        try:
            data = self._run_query(query_args)
        except Exception as e:
            raise IRRDBToolsError(
                "Can't get list of authorized ASNs for {}: {}".format(
                    self.descr, str(e)
                )
            )

        return data["asn_list"]

class RSet(IRRDBInfo):

    def __init__(self, object_names, ip_ver, allow_longer_prefixes, **kwargs):
        IRRDBInfo.__init__(self, object_names, **kwargs)

        assert ip_ver in (4, 6)
        self.ip_ver = ip_ver
        self.allow_longer_prefixes = allow_longer_prefixes

    def load_data(self):
        logging.debug("Getting prefixes for {} IPv{} "
                      "from IRRdb".format(self.descr, self.ip_ver))

        IRRDBInfo.load_data(self)

        # list of dict as returned by ValidatorPrefixListEntry
        self.prefixes = self.raw_data

    def _get_object_filename(self):
        return "{}-r_set-ipv{}{}.json".format(
            self.name, self.ip_ver,
            "_and_more_specific" if self.allow_longer_prefixes else ""
        )

    def _get_data(self):
        query_args = []
        query_args += ["-4"] if self.ip_ver == 4 else ["-6"]
        query_args += ["-A"]
        query_args += ["-l", "prefix_list"]
        if self.allow_longer_prefixes:
            query_args += ["-R"]
            query_args += ["32"] if self.ip_ver == 4 else ["128"]
        query_args += self._get_bgpq3_names()

        try:
            data = self._run_query(query_args)
        except Exception as e:
            raise IRRDBToolsError(
                "Can't get authorized prefix list for {} IPv{}: {}".format(
                    self.descr, self.ip_ver, str(e)
                )
            )

        return [self._parse_prefix(prefix) for prefix in data["prefix_list"]]

    def _parse_prefix(self, raw):
        prefix = IPNetwork(raw["prefix"])
        res = {
            "prefix": prefix.ip,
            "length": prefix.prefixlen,
            "exact": raw["exact"] if "exact" in raw else False
        }
        if res["exact"]:
            res["ge"] = None
            res["le"] = None
        else:
            if "greater-equal" in raw:
                res["ge"] = raw["greater-equal"]
            else:
                res["ge"] = None

            if "less-equal" in raw:
                res["le"] = raw["less-equal"]
            else:
                res["le"] = None

        return ValidatorPrefixListEntry().validate(res)
