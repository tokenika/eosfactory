#!/usr/bin/env python3
"""Pretty output for GetAccount object."""

import json
import re

example =\
{
    "account_name": "MASTER",
    "head_block_num": 42763415,
    "head_block_time": "2019-08-05T11:21:25.500",
    "privileged": False,
    "last_code_update": "1970-01-01T00:00:00.000",
    "created": "2019-02-20T16:11:09.500",
    "core_liquid_balance": "123.4027 EOS",
    "ram_quota": 5469,
    "net_weight": 10000,
    "cpu_weight": 10000,
    "net_limit": {
        "used": 337,
        "available": 134578,
        "max": 134915
    },
    "cpu_limit": {
        "used": 1233,
        "available": 46243,
        "max": 47476
    },
    "ram_usage": 5334,
    "permissions": [
        {
            "parent": "owner",
            "perm_name": "active",
            "required_auth": {
                "accounts": [
                    {
                        "permission":
                        {
                            "actor": "yyaefgfd",
                            "permission": "active"
                        },
                        "weight": "1"
                    },
                    {
                        "permission":
                        {
                            "actor": "ssnnnsns",
                            "permission": "active"
                        },
                        "weight": "1"
                    }
                ],
                "keys": [
                    {
                        "key": "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
                        "weight": 1
                    },
                    {
                        "key": "5KQwrPbwdL6PhXujxW37FSRRZ1JiwsST4cqQzDeyXtP79zkvFD3",
                        "weight": 1
                    }               
                ],
                "threshold": 1,
                "waits": []
            }
        },
        {
            "parent": "",
            "perm_name": "owner",
            "required_auth": {
                "accounts": [
                    {
                        "permission":
                        {
                            "actor": "yyrrefgfd",
                            "permission": "active"
                        },
                        "weight": "1"
                    },
                    {
                        "permission":
                        {
                            "actor": "tfppefgfd",
                            "permission": "active"
                        },
                        "weight": "1"
                    }
                ],
                "keys": [
                    {
                        "key": "ALICE@active",
                        "weight": 1
                    }
                ],
                "threshold": 1,
                "waits": []
            }
        },
        {
            "parent": "active",
            "perm_name": "xxx",
            "required_auth": {
               "accounts": [
                  {
                     "permission":
                        {
                           "actor": "tfrrefgfd",
                           "permission": "active"
                        },
                     "weight": "1"
                  },
                  {
                     "permission":
                        {
                           "actor": "tfrssrefgfd",
                           "permission": "active"
                        },
                     "weight": "1"
                  }
               ],
               "keys": [
                  {
                        "key": "ALICE@owner",
                        "weight": "1"
                  }
               ],
               "threshold": 1,
               "waits": []
            }
        },
        {
            "parent": "owner",
            "perm_name": "active1",
            "required_auth": {
               "accounts": [
                  {
                     "permission":
                        {
                           "actor": "ggarefgfd",
                           "permission": "active"
                        },
                     "weight": "1"
                  },
                  {
                     "permission":
                        {
                           "actor": "tfrsddfgfd",
                           "permission": "active"
                        },
                     "weight": "1"
                  }
               ],
               "keys": [
                  {
                        "key": "5J18aGyFVDN1MeL8UzQpuaPEV3Cxyr8LLw6x2UaQRtnB9Xy8rce",
                        "weight": "1"
                  }
               ],
               "threshold": "1",
               "waits": []
            }
        }
    ],
   #  "privileged": False,
   #  "ram_quota": -1,
   #  "ram_usage": 2724,
   #  "refund_request": None,
   #  "self_delegated_bandwidth": None,
   #  "total_resources": None,
   #  "voter_info": None

   # "total_resources": None,
   # "self_delegated_bandwidth": None,
   # "refund_request": None,
   # "voter_info": None

    "total_resources": {
        "owner": "MASTER",
        "net_weight": "1.0000 EOS",
        "cpu_weight": "1.0000 EOS",
        "ram_bytes": 4069
    },
    "self_delegated_bandwidth": {
        "from": "MASTER",
        "to": "MASTER",
        "net_weight": "1.0000 EOS",
        "cpu_weight": "1.0000 EOS"
    },
    "refund_request": None,
    "voter_info": {
        "owner": "MASTER",
        "proxy": "proxy",
        "producers": ["tokenika4eos", "junglelion"],
        "staked": 680000,
        "last_vote_weight": "0.00000000000000000",
        "proxied_vote_weight": "0.00000000000000000",
        "is_proxy": 0,
        "flags1": 0,
        "reserved2": 0,
        "reserved3": "0 "
    }
}


class GetAccount():
    ARROW = "|--> "
    INDENT = "    "
    FORMAT_LABEL = "%20s"


    def __init__(self, received_json):

        class Asset():
            def __init__(self, value, symbol=None):
                if not symbol:
                    symbol = re.sub(r"\d+\.*\d+\s*", "", value)
                    value = re.sub(r"\s*[a-zA-Z]+\s*", "", value)

                self.value = float(value)
                self.symbol = symbol = re.sub(r"\d+\.*\d+\s*", "", symbol)

            def add(self, asset, mult=1):
                if not isinstance(asset, Asset):
                    raise Exception("``asset`` must be of the Asset type!")
                return Asset(self.value + mult * asset.value, self.symbol)

            def __str__(self):
                return "%f %s" % (self.value, self.symbol)


        def add(msg=""):
            self.info = self.info + msg


        def addln(msg=""):
            self.info = self.info + msg + "\n"

        def format_bytes(value):
            if value == -1:
                return "unlimited"
            
            if value >= 1024 * 1024 * 1024 * 1024:
                return "%0.1f %s" % (value / (1024 * 1024 * 1024 * 1024), "TiB")
            elif value >= 1024 * 1024 * 1024:
                return "%0.1f %s" % (value / (1024 * 1024 * 1024), "GiB")
            elif value >= 1024 * 1024:
                return "%0.1f %s" % (value / (1024 * 1024), "MiB")
            elif value >= 1024:
                return "%0.1f %s" % (value / 1024, "KiB")
            else:
                return "%0.0f %s" % (value, "bytes")
                
        def format_time(micro):
            if micro == -1:
                return "unlimited"

            if micro > 1000000*60*60:
                return "%0.1f %s" % (micro / (1000000*60*60), "hr")
            elif micro > 1000000*60:
                return "%0.1f %s" % (micro / (1000000*60), "min")
            elif micro > 1000000:
                return "%0.1f %s" % (micro / 1000000, "sec")
            elif micro > 1000:
                return "%0.1f %s" % (micro / 1000, "ms")            


        unstaking = None
        staked = None

        if "core_liquid_balance" in received_json:
            symbol = re.sub(
                r"\d+\.*\d+\s*", "", received_json["core_liquid_balance"])
            unstaking = Asset(0, symbol)
            staked = Asset(0, symbol)

        self.info = ""

        if "account_object_name" in received_json:
            addln("Account object name: {}".format(
                                            received_json["account_object_name"]))   
        addln("name: {}".format(received_json["account_name"]))
        addln("created: {}".format(received_json["created"]))
        addln()

        ##########################################################################
        # permissions
        ##########################################################################
        permissions = received_json["permissions"].copy()
        permission_root = {}

        def process_a_node(node, depth, do, args=None):
            do(node, depth, args)
            if "permissions" in node:
                for node1 in node["permissions"]:
                    if node1:
                        process_a_node(node1, depth + 1, do, args)

        def add_permission_to_tree(node, depth, args):
            permissions = args[0]
            permission = args[1]

            if not permission:
                return

            if not depth and not permission["parent"] :
                permission.update({"permissions": []})
                node.update(permission)
                permissions[permissions.index(permission)] = None

            if "perm_name" in node and node["perm_name"] == permission["parent"]:
                permission.update({"permissions": []})
                node["permissions"].append(permission)
                permissions[permissions.index(permission)] = None                  

        def print_required_auth(node, depth, args):
            if depth == 0:
                addln("### permissions:")
                indent = GetAccount.INDENT
            else:
                indent = GetAccount.INDENT \
                + " " * len(GetAccount.ARROW) * (depth -1) + GetAccount.ARROW
            indent_det = GetAccount.INDENT + " " * len(GetAccount.ARROW) * depth \
                        + "              "
            
            add(indent)
            addln("%s thrd=%s" % (
                            node["perm_name"], node["required_auth"]["threshold"]))

            if "keys" in node["required_auth"]:
                for key in node["required_auth"]["keys"]:
                    addln(indent_det + "wght=%s key=%s" % (
                                                    key["weight"], key["key"]))

            if "accounts" in node["required_auth"]:
                for acc in node["required_auth"]["accounts"]:
                    addln(indent_det + "wght=%s perm=%s@%s " % (
                                        acc["weight"], acc["permission"]["actor"], 
                                        acc["permission"]["permission"]))

        for perm in permissions:
            for perm in permissions:
                process_a_node(
                permission_root, 0, add_permission_to_tree,
                [permissions, perm])

        process_a_node(permission_root, 0, print_required_auth)

        ##########################################################################
        # memory
        ##########################################################################
        addln("### memory:")
        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s, used: %s") % (
                                        "quota",
                                        format_bytes(received_json["ram_quota"]), 
                                        format_bytes(received_json["ram_usage"])))

        ##########################################################################
        addln("### net bandwidth:")

        if "total_resources" in received_json \
                                and not received_json["total_resources"] is None:

            net_total = Asset(received_json["total_resources"]["net_weight"])
            if not net_total.symbol == unstaking.symbol:
                unstaking = Asset(0, net_total.symbol)
                staked = Asset(0, net_total.symbol)

            if "self_delegated_bandwidth" in received_json \
                        and not received_json["self_delegated_bandwidth"] is None:
                net_own = Asset(
                            received_json["self_delegated_bandwidth"]["net_weight"])
                staked = net_own
                net_others = net_total.add(net_own, -1)
                addln(
                GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s %s") % (
                                "staked", net_own, 
                                "(total stake delegated from account to self)"))         
                addln(
                GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s %s") % (
                            "delegated", net_others, 
                            "(total staked delegated to account from others)"))
            else:
                net_others = net_total
                addln(
                GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s %s") % (
                            "delegated", net_others, 
                            "(total staked delegated to account from others)"))         

        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                                "used",
                                format_bytes(received_json["net_limit"]["used"])))
        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                            "available",
                            format_bytes(received_json["net_limit"]["available"])))
        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                                "limit",
                                format_bytes(received_json["net_limit"]["max"])))

        ##########################################################################
        # cpu bandwidth
        ##########################################################################
        addln("### cpu bandwidth:")

        if "total_resources" in received_json \
                                and not received_json["total_resources"] is None:

            cpu_total = Asset(
                            received_json["self_delegated_bandwidth"]["cpu_weight"])

            if "self_delegated_bandwidth" in received_json \
                    and not received_json["self_delegated_bandwidth"] is None:

                cpu_own = Asset(received_json["total_resources"]["cpu_weight"])
                staked = staked.add(cpu_own)
                cpu_others = cpu_total.add(cpu_own, -1)
                addln(
                GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s %s") % (
                                "staked", cpu_own, 
                                "(total stake delegated from account to self)"))
                addln(
                GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s %s") % (
                            "delegated", cpu_others, 
                            "(total staked delegated to account from others)"))
            else:
                net_others = net_total
                addln(
                GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s %s") % (
                            "delegated", net_others, 
                            "(total staked delegated to account from others)"))

        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                    "used", format_time(received_json["cpu_limit"]["used"])))      
        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                "available", format_time(received_json["cpu_limit"]["available"])))      
        addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                    "max", format_time(received_json["cpu_limit"]["max"])))

        ##########################################################################
        # balances
        ##########################################################################
        if "core_liquid_balance" in received_json:
            liquid = Asset(received_json["core_liquid_balance"])
            addln("### {} balances:".format(liquid.symbol))

            addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                        "liquid",
                        received_json["core_liquid_balance"]))
            addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                        "staked", str(staked)))         
            addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                        "unstaking", str(unstaking)))
            total = liquid.add(staked)
            total = total.add(unstaking)
            addln(GetAccount.INDENT + (GetAccount.FORMAT_LABEL + ": %s") % (
                            "total", str(total)))
   

        ##########################################################################
        # producers
        # ########################################################################      
        add("### producers: ")
        if "voter_info" in received_json and received_json["voter_info"]:
            if received_json["voter_info"]["proxy"]:
                prods = received_json["voter_info"]["producers"]
                if prods:
                    addln()
                    for prod in prods:
                        addln(GetAccount.INDENT + GetAccount.FORMAT_LABEL % prod)
                else:
                    addln("not voted")
        else:
            addln("not voted")


    def __str__(self):
        return self.info


if __name__ == '__main__':
   print(GetAccount(example))
