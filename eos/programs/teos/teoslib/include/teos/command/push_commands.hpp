#pragma once

#include <vector>
#include <boost/algorithm/string.hpp>

#include <teoslib/config.h>
#include <teos/eos_interface.hpp>
#include <teos/command/command.hpp>

using namespace std;

extern const char* pushSubcommands;

namespace teos
{
  namespace command
  {
    /**
    Push a transaction with a single message
    */
    class PushMessage : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param contract  the account providing the contract to execute.
      * @param action the account providing the contract to execute.
      * @param data the arguments to the contract.
      * @param scope a comma separated list of accounts in scope for this operation.
      * @param skip specifies that unlocked wallet keys should not be used to sign transaction.
      * @expiration sets the time in seconds before a transaction expires.
      * @param forceUnique forces the transaction to be unique.
      * @param raw if true, the resulting json is not formated.
      * @param getResponse() returns {"password":"<password>"}.
      */
      PushMessage(string contractName, string action, string data,
        string scope, string permission, bool forceUnique = false,
        bool skip = false, int expiration = 30, bool raw = false)
        : TeosCommand("", raw)
      {
        vector<string> scopes;
        boost::split(scopes, scope, boost::is_any_of(","));
        vector<string> permissions;
        boost::split(permissions, permission, boost::is_any_of(","));

        copy(pushMessage(contractName, action, data, scopes, permissions, 
          skip, expiration, forceUnique));
      }

      /**
      * @brief A constructor.
      * @param reqJson json tree argument: {"contract":"<contract name>", 
      * "action":"<action on contract>", "data":"<json tree>", "scope":"<account list>",
      * "permission":"<accountName@permitionLevel>", "skip":<true|false>, "expiration":<int>,
      * "force-unique":<true|false>}.
      * @param raw if true, the resulting json is not formated.
      * @param getResponse() returns {?????????????????????????}.
      */
      PushMessage(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson, raw)
      {
        vector<string> scopes;
        string scope = reqJson.get<string>("scope");
        boost::split(scopes, scope, boost::is_any_of(","));
        vector<string> permissions;
        string permission = reqJson.get<string>("permission");
        boost::split(permissions, permission, boost::is_any_of(","));

        copy(pushMessage(reqJson.get<string>("contract"), reqJson.get<string>("action"), 
          reqJson.get<string>("data"), scopes, permissions,
          reqJson.get<bool>("skip"), reqJson.get<int>("expiration"), 
          reqJson.get<bool>("force-unique")));
      }
    };

    /**
    * @brief Command-line driver for the PushMessage class.
    */
    class PushMessageOptions : public CommandOptions
    {
    public:
      PushMessageOptions(int argc, const char **argv)
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

      options_description options() {
        options_description special("");
        special.add_options()
          ("contract,c", value<string>(&contract), "The account providing the contract to execute")
          ("action,a", value<string>(&action), "The action to execute on the contract")
          ("data,d", value<string>(&data), "The arguments to the contract")
          ("scope,S", value<string>(&scope), "A comma separated list of accounts in scope for this operation")
          ("permission,p", value<string>(&permission), "An account and permission level to authorize, as in 'account@permission'")
          ("skip,s", value<bool>(&skip)->default_value(false), "Specify that unlocked wallet keys should not be used to sign transaction, defaults to false")
          ("expiration,x", value<int>(&expiration)->default_value(30), "The time in seconds before a transaction expires")
          ("force-unique,f", value<bool>(&forceUnique)->default_value(false), 
            "force the transaction to be unique. this will consume extra bandwidth and remove any protections against accidentally issuing the same transaction multiple times");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("contract", 1);
        pos_desc.add("action", 1);
        pos_desc.add("data", 1);
        pos_desc.add("scope", 1);
        pos_desc.add("permission", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("contract")) {
          reqJson.put("contract", contract);
          if (vm.count("action")) {
            reqJson.put("action", action);
            if (vm.count("data")){
              reqJson.put("data", data);
              if (vm.count("scope")){
                reqJson.put("scope", scope);
                if (vm.count("permission")){
                  reqJson.put("permission", scope);
                  ok = true;
                }
              }
            }
          }
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return PushMessage(reqJson, is_raw);
      }

      void getExample() {
        cout << R"EOF(
)EOF" << endl;
      }
    };
  }
}