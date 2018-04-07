#pragma once

#include <teoslib/config.h>
#include <teoslib/eos_interface.hpp>
#include <teoslib/command.hpp>

using namespace std;

extern const char* setSubcommands;
extern const string setCommandPath;

namespace teos
{
  namespace command
  {
    /**
    Create or update the contract on an account.
    */
    class SetContract : public TeosCommand
    {
    public:
      SetContract(
          string accountName,
          string wastFile, string abiFile = "",
          string permission  = "",
          int expiration = 30,
          bool skipSignature = false,
          bool dontBroadcast = false,
          bool forceUnique = false)
        : TeosCommand("")
      {
        copy(setContract(
          accountName, wastFile, abiFile, permission, 
          expiration, skipSignature, dontBroadcast, forceUnique));
      }

      SetContract(ptree reqJson) : TeosCommand(
        "", reqJson)
      {
        copy(setContract(
          reqJson.get<string>("account"),
          reqJson.get<string>("wast"), reqJson.get<string>("abi"),
          reqJson.get<string>("permission"),
          reqJson.get<int>("expiration"),
          reqJson.get<bool>("skip"),
          reqJson.get<bool>("dontBroadcast"),
          reqJson.get<bool>("forceUnique")
          ));
      }
    };

    /**
    * @brief Command-line driver for the SetContract class.
    */
    class SetContractOptions : public CommandOptions
    {
    public:
      SetContractOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Create or update the contract on an account.
Usage: ./teos [http address] set contract [account] [wast] [abi] [Options]
Usage: ./teos [http address] create key [-j '{
  "account":"<account name>"
  "wast":"<wast file>"
  "abi":"<abi file>"
  "permission":"<accountName@permitionLevel,accountName@permitionLevel>"
  "expiration":<expiration time sec>,  
  "skipSignature":<true|false>,
  "dontBroadcast":<true|false>,
  "forceUnique":<true|false>
  }'] [OPTIONS]
)EOF";
      }

      string account;
      string wast;
      string abi;
      string permission;
      int expiration;      
      bool skipSignature;
      bool dontBroadcast;
      bool forceUnique;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("account,n", value<string>(&account)
            , "The name of account to publish a contract for")
          ("wast,o", value<string>(&wast), "The WAST file for the contract")
          ("abi,a", value<string>(&abi)->default_value("")
            , "The ABI file for the contract")
          ("permission,p", value<string>(&permission)
            ->default_value("")
            ,"An account and permission level to authorize, as in "
            "'account@permission'")
          ("expiration,x", value<int>(&expiration)->default_value(30)
            , "The time in seconds before a transaction expires")
          ("skip,s", value<bool>(&skipSignature)->default_value(false)
            , "Specify that unlocked wallet keys should not be used to sign "
            "transaction, defaults to false")
          ("dont-broadcast,d", value<bool>(&dontBroadcast)->default_value(false)
            , "Don't broadcast transaction to the network (just print to stdout)");
          ("force-unique,f", value<bool>(&forceUnique)->default_value(false)
            , "force the transaction to be unique. this will consume extra "
            "bandwidth and remove any protections against accidently issuing "
            "the same transaction multiple times");         
          return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("account", 1);
        pos_desc.add("wast", 1);
        pos_desc.add("abi", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("account")) {
          reqJson_.put("account", account);
          if (vm.count("wast")) {
            reqJson_.put("wast", wast);
            reqJson_.put("permission", permission);
            reqJson_.put("expiration", expiration);                
            reqJson_.put("skip", skipSignature);
            reqJson_.put("dontBroadcast", dontBroadcast);
            reqJson_.put("forceUnique", forceUnique);            
            ok = true;
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return SetContract(reqJson_);
      }

    };
  }
}