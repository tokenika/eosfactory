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
          string contractDir,
          string wastFile = "", string abiFile = "",
          string permission  = "",
          unsigned expiration = 30,
          bool skipSignature = false,
          bool dontBroadcast = false,
          bool forceUnique = false,
          unsigned maxCpuUsage = 0,
          unsigned maxNetUsage = 0)
      {
        copy(setContract(
          accountName, contractDir, wastFile, abiFile, permission, 
          expiration, skipSignature, dontBroadcast, forceUnique,
          maxCpuUsage, maxNetUsage));
      }

      SetContract(ptree reqJson) : TeosCommand("", reqJson)
      {
        copy(setContract(
          reqJson.get<string>("account"),
          reqJson.get<string>("contract-dir"),
          reqJson.get<string>("wast-file"), reqJson.get<string>("abi-file"),
          reqJson.get<string>("permission"),
          reqJson.get<unsigned>("expiration"),
          reqJson.get<bool>("skip-sign"),
          reqJson.get<bool>("dont-broadcast"),
          reqJson.get<bool>("force-unique"),
          reqJson.get<unsigned>("max-cpu-usage"),
          reqJson.get<unsigned>("max-net-usage")
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
Usage: ./teos [http address] set contract <account> <contract dir> 
          [wast] [abi] [Options]
Usage: ./teos [http address] create key --jarg '{
  "account":"<account name>",
  "contract-dir":"<contract dir>",
  "wast-file":"<wast file>",
  "abi-file":"<abi file>",
  "permission":"<permission list>",
  "expiration":<expiration time sec>,  
  "skip-sign":<true|false>,
  "dont-broadcast":<true|false>,
  "force-unique":<true|false>,
  "max-cpu-usage":"<max cpu usage>",
  "max-net-usage":"<max net usage>"
  }' [OPTIONS]
)EOF";
      }

      string account;
      string contractDir;
      string wastFile;
      string abiFile;
      string permission;
      unsigned expiration;      
      bool skipSignature;
      bool dontBroadcast;
      bool forceUnique;
      unsigned maxCpuUsage;
      unsigned maxNetUsage;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("account,n", value<string>(&account)
            , "The name of account to publish a contract for.")
          ("contract-dir,c", value<string>(&contractDir)
            , "Contract directory, the the path containing the .wast and .abi")          
          ("wast-file", value<string>(&wastFile)
            , "The WAST for the contract relative to the contract dir.")
          ("abi-file", value<string>(&abiFile)->default_value("")
            , "The ABI for the contract relative to the contract dir.")
          ("permission,p", value<string>(&permission)
            ->default_value("")
            ,"An account and permission level to authorize, as in "
              "'account@permission' (defaults to 'account@active')")
          ("expiration,x", value<unsigned>(&expiration)->default_value(30)
            , "The time in seconds before a transaction expires.")
          ("skip-sign,s"
            , "Specify that unlocked wallet keys should not be used to sign "
            "transaction, defaults to false.")
          ("dont-broadcast,d"
            , "Don't broadcast transaction to the network "
              "(just print to stdout).")
          ("force-unique,f"
            , "force the transaction to be unique. this will consume extra "
            "bandwidth and remove any protections against accidently issuing "
            "the same transaction multiple times.")
          ("max-cpu-usage", value<unsigned>(&maxCpuUsage)->default_value(0)
            , "Upper limit on the cpu usage budget, in instructions-retired, "
              "for the execution of the transaction (defaults to 0 which "
              "means no limit).")
          ("max-net-usage", value<unsigned>(&maxNetUsage)->default_value(0)
            ,  "Upper limit on the net usage budget, in bytes, for the "
              "transaction (defaults to 0 which means no limit)");       
          return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("account", 1);
        pos_desc.add("contract-dir", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("account")) {
          reqJson_.put("account", account);
          if (vm.count("contract-dir")) {
            reqJson_.put("contract-dir", contractDir);
            reqJson_.put("wast-file", wastFile);
            reqJson_.put("abi-file", abiFile);
            reqJson_.put("permission", permission);
            reqJson_.put("expiration", expiration);                
            reqJson_.put(
              "skip-sign", skipSignature = vm.count("skip-sign") ? true : false);
            reqJson_.put(
              "dont-broadcast", 
              dontBroadcast = vm.count("dont-broadcast") ? true : false);
            reqJson_.put(
              "force-unique", forceUnique = vm.count("force-unique") ? true : false);
            reqJson_.put("max-cpu-usage", maxCpuUsage);            
            reqJson_.put("max-net-usage", maxNetUsage);                        
            ok = true;
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return SetContract(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("transaction id", "%s", GET_STRING(command, "transaction_id"));
      }
    };
  }
}