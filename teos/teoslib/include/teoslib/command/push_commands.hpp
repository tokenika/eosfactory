#pragma once

#include <vector>
#include <boost/algorithm/string.hpp>

#include <teoslib/config.h>
#include <teoslib/eos_interface.hpp>
#include <teoslib/command.hpp>

using namespace std;

extern const char* pushSubcommands;

namespace teos
{
  namespace command
  {
    /**
    Push a transaction with a single message
    */
    class PushAction : public TeosCommand
    {
    public:
      PushAction(string contractName, string action, string data,
        string scope, string permission, bool forceUnique = false,
        bool skip = false, int expiration = 30, bool raw = false)
        : TeosCommand("")
      {
        vector<string> scopes;
        boost::split(scopes, scope, boost::is_any_of(","));
        vector<string> permissions;
        boost::split(permissions, permission, boost::is_any_of(","));

        copy(pushAction(contractName, action, data, scopes, permissions, 
          skip, expiration, forceUnique));
      }

      PushAction(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson)
      {
        vector<string> scopes;
        string scope = reqJson.get<string>("scope");
        boost::split(scopes, scope, boost::is_any_of(","));
        vector<string> permissions;
        string permission = reqJson.get<string>("permission");
        boost::split(permissions, permission, boost::is_any_of(","));

        copy(pushAction(reqJson.get<string>("contract"), reqJson.get<string>("action"), 
          reqJson.get<string>("data"), scopes, permissions,
          reqJson.get<bool>("skip"), reqJson.get<int>("expiration"), 
          reqJson.get<bool>("force-unique")));
      }
    };

    /**
    * @brief Command-line driver for the PushAction class.
    */
    class PushActionOptions : public CommandOptions
    {
    public:
      PushActionOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Push a transaction with a single message.
Usage: ./teos push message [contract] [action] [data] [scope] [permission] [Options]
Usage: ./teos create key [-j '{
  "contract":"<contract name>",
  "action":"<action on contract>",
  "data":"<json tree>",
  "scope":"<account list>",
  "permission":"<accountName@permitionLevel>",
  "skip":<true|false>,
  "expiration":<int>,
  "force-unique":<true|false>
  }'] [OPTIONS]
)EOF";
      }

      string contract;
      string action;
      string data;
      string scope;      
      string permission;
      bool skip;
      int expiration;
      bool forceUnique;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("contract,c", value<string>(&contract), "The account providing the contract to execute")
          ("action,a", value<string>(&action), "The action to execute on the contract")
          ("data,d", value<string>(&data), "The arguments to the contract")
          ("scope,S", value<string>(&scope), "A comma separated list of accounts in scope for this operation")
          ("permission,p", value<string>(&permission), "An account and permission level to authorize, as in 'account@permission'")
          ("skip,s", value<bool>(&skip)->default_value(false), "Specify that unlocked wallet keys should not be used to sign transaction, defaults to false")
          ("expiration,x", value<int>(&expiration)->default_value(30), "The time in seconds before a transaction expires")
          ("force-unique,f", value<bool>(&forceUnique)->default_value(false), 
            "force the transaction to be unique. this will consume extra bandwidth and remove any protections against accidentally issuing the same transaction multiple times");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("contract", 1);
        pos_desc.add("action", 1);
        pos_desc.add("data", 1);
        pos_desc.add("scope", 1);
        pos_desc.add("permission", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("contract")) {
          reqJson_.put("contract", contract);
          if (vm.count("action")) {
            reqJson_.put("action", action);
            if (vm.count("data")){
              reqJson_.put("data", data);
              if (vm.count("scope")){
                reqJson_.put("scope", scope);
                if (vm.count("permission")){
                  reqJson_.put("permission", scope);
                  ok = true;
                }
              }
            }
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return PushAction(reqJson_);
      }

    };
  }
}