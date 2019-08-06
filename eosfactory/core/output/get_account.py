import json
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
      "proxy": "",
      "producers": [],
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
   TITLE_WIDTH = "%20s: "

   def __init__(self, account_json):
      self.account_json = account_json
      self.info = ""

      if "account_object_name" in account_json:
         self.addln("Account object name: {}".format(
                                          account_json["account_object_name"]))   
      self.addln("Account object name: {}".format(
                                                account_json["account_name"]))
      self.addln("created: {}".format(account_json["created"]))
      self.addln()

      self.permissions()
      self.memory()
      self.net_bandwidth()
      self.cpu_bandwidth()
   

   def permissions(self):
      permissions = self.account_json["permissions"].copy()
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
            self.addln("### permissions:")
            indent = GetAccount.INDENT
         else:
            indent = GetAccount.INDENT \
               + " " * len(GetAccount.ARROW) * (depth -1) + GetAccount.ARROW
         indent_det = GetAccount.INDENT + " " * len(GetAccount.ARROW) * depth \
                     + "              "
         
         self.add(indent)
         self.addln("%s thrd=%s" % (
                        node["perm_name"], node["required_auth"]["threshold"]))

         if "keys" in node["required_auth"]:
            for key in node["required_auth"]["keys"]:
               self.addln(indent_det + "wght=%s key=%s" % (
                                                   key["weight"], key["key"]))

         if "accounts" in node["required_auth"]:
            for acc in node["required_auth"]["accounts"]:
               self.addln(indent_det + "wght=%s perm=%s@%s " % (
                                    acc["weight"], acc["permission"]["actor"], 
                                    acc["permission"]["permission"]))

      for perm in permissions:
         for perm in permissions:
            process_a_node(
               permission_root, 0, add_permission_to_tree,
               [permissions, perm])

      process_a_node(permission_root, 0, print_required_auth)

   def format_bytes(self, value):
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


   def memory(self):
      self.addln("### memory:")
      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s, used: %s") % (
                              "quota",
                           self.format_bytes(self.account_json["ram_quota"]), 
                           self.format_bytes(self.account_json["ram_usage"])))

   def net_bandwidth(self):
      self.addln("### net bandwidth:")

   #    if ( json.total_jsonources.is_object() ) {
   #       auto net_total = to_asset(json.total_jsonources.get_object()["net_weight"].as_string());

   #       if( net_total.get_symbol() != unstaking.get_symbol() ) {
   #          // Core symbol of nodeos jsonponding to the request is different than core symbol built into cleos
   #          unstaking = asset( 0, net_total.get_symbol() ); // Correct core symbol for unstaking asset.
   #          staked = asset( 0, net_total.get_symbol() ); // Correct core symbol for staked asset.
   #       }

   #       if( json.self_delegated_bandwidth.is_object() ) {
   #          asset net_own =  asset::from_string( json.self_delegated_bandwidth.get_object()["net_weight"].as_string() );
   #          staked = net_own;

   #          auto net_others = net_total - net_own;

   #          std::cout << indent << "staked:" << std::setw(20) << net_own
   #                    << std::string(11, ' ') << "(total stake delegated from account to self)" << std::endl
   #                    << indent << "delegated:" << std::setw(17) << net_others
   #                    << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
   #       }
   #       else {
   #          auto net_others = net_total;
   #          std::cout << indent << "delegated:" << std::setw(17) << net_others
   #                    << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
   #       }
   #    }

      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s") % (
                  "used",
                  self.format_bytes(self.account_json["net_limit"]["used"])))
      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s") % (
                  "available",
                  self.format_bytes(self.account_json["net_limit"]["available"])))
      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s") % (
                  "limit",
                  self.format_bytes(self.account_json["net_limit"]["max"])))


   def cpu_bandwidth(self):
      def format_time(micro):
         if micro == -1:
            return string("unlimited")

         if micro > 1000000*60*60:
            return "%0.1f %s" % (micro / (1000000*60*60), "hr")
         elif micro > 1000000*60:
            return "%0.1f %s" % (micro / (1000000*60), "min")
         elif micro > 1000000:
            return "%0.1f %s" % (micro / 1000000, "sec")
         elif micro > 1000:
            return "%0.1f %s" % (micro / 1000, "ms")

      self.addln("### cpu bandwidth:")
      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s") % (
                  "used",
                  format_time(self.account_json["cpu_limit"]["used"])))      
      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s") % (
               "available",
               format_time(self.account_json["cpu_limit"]["available"])))      
      self.addln(GetAccount.INDENT + (GetAccount.TITLE_WIDTH + "%s") % (
                  "max",
                  format_time(self.account_json["cpu_limit"]["max"])))      


   def __str__(self):
      return self.info

   def add(self, msg=""):
      self.info = self.info + msg

   def addln(self, msg=""):
      self.info = self.info + msg + "\n"



         



   # if( json.core_liquid_balance.valid() ) {
   #    unstaking = asset( 0, json.core_liquid_balance->get_symbol() ); 
   #    staked = asset( 0, json.core_liquid_balance->get_symbol() ); 
   # }


      # std::cout << "cpu bandwidth:" << std::endl;

      # if ( json.total_jsonources.is_object() ) {
      #    auto cpu_total = to_asset(json.total_jsonources.get_object()["cpu_weight"].as_string());

      #    if( json.self_delegated_bandwidth.is_object() ) {
      #       asset cpu_own = asset::from_string( json.self_delegated_bandwidth.get_object()["cpu_weight"].as_string() );
      #       staked += cpu_own;

      #       auto cpu_others = cpu_total - cpu_own;

      #       std::cout << indent << "staked:" << std::setw(20) << cpu_own
      #                 << std::string(11, ' ') << "(total stake delegated from account to self)" << std::endl
      #                 << indent << "delegated:" << std::setw(17) << cpu_others
      #                 << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
      #    } else {
      #       auto cpu_others = cpu_total;
      #       std::cout << indent << "delegated:" << std::setw(17) << cpu_others
      #                 << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
      #    }
      # }

      # if( json.refund_request.is_object() ) {
      #    auto obj = json.refund_request.get_object();
      #    auto request_time = fc::time_point_sec::from_iso_string( obj["request_time"].as_string() );
      #    fc::time_point refund_time = request_time + fc::days(3);
      #    auto now = json.head_block_time;
      #    asset net = asset::from_string( obj["net_amount"].as_string() );
      #    asset cpu = asset::from_string( obj["cpu_amount"].as_string() );
      #    unstaking = net + cpu;

      #    if( unstaking > asset( 0, unstaking.get_symbol() ) ) {
      #       std::cout << std::fixed << setprecision(3);
      #       std::cout << "unstaking tokens:" << std::endl;
      #       std::cout << indent << std::left << std::setw(25) << "time of unstake request:" << std::right << std::setw(20) << string(request_time);
      #       if( now >= refund_time ) {
      #          std::cout << " (available to claim now with 'eosio::refund' action)\n";
      #       } else {
      #          std::cout << " (funds will be available in " << to_pretty_time( (refund_time - now).count(), 0 ) << ")\n";
      #       }
      #       std::cout << indent << std::left << std::setw(25) << "from net bandwidth:" << std::right << std::setw(18) << net << std::endl;
      #       std::cout << indent << std::left << std::setw(25) << "from cpu bandwidth:" << std::right << std::setw(18) << cpu << std::endl;
      #       std::cout << indent << std::left << std::setw(25) << "total:" << std::right << std::setw(18) << unstaking << std::endl;
      #       std::cout << std::endl;
      #    }
      # }

      # if( json.core_liquid_balance.valid() ) {
      #    std::cout << json.core_liquid_balance->get_symbol().name() << " balances: " << std::endl;
      #    std::cout << indent << std::left << std::setw(11)
      #              << "liquid:" << std::right << std::setw(18) << *json.core_liquid_balance << std::endl;
      #    std::cout << indent << std::left << std::setw(11)
      #              << "staked:" << std::right << std::setw(18) << staked << std::endl;
      #    std::cout << indent << std::left << std::setw(11)
      #              << "unstaking:" << std::right << std::setw(18) << unstaking << std::endl;
      #    std::cout << indent << std::left << std::setw(11) << "total:" << std::right << std::setw(18) << (*json.core_liquid_balance + staked + unstaking) << std::endl;
      #    std::cout << std::endl;
      # }

      # if ( json.voter_info.is_object() ) {
      #    auto& obj = json.voter_info.get_object();
      #    string proxy = obj["proxy"].as_string();
      #    if ( proxy.empty() ) {
      #       auto& prods = obj["producers"].get_array();
      #       std::cout << "producers:";
      #       if ( !prods.empty() ) {
      #          for ( size_t i = 0; i < prods.size(); ++i ) {
      #             if ( i%3 == 0 ) {
      #                std::cout << std::endl << indent;
      #             }
      #             std::cout << std::setw(16) << std::left << prods[i].as_string();
      #          }
      #          std::cout << std::endl;
      #       } else {
      #          std::cout << indent << "<not voted>" << std::endl;
      #       }
      #    } else {
      #       std::cout << "proxy:" << indent << proxy << std::endl;
      #    }
      # }
      # std::cout << std::endl;
   # }

print(GetAccount(example))
