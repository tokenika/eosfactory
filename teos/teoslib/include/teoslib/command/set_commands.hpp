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
      SetContract(string accountName,
        string wastFile, string abiFile = "",
        bool skip = false, int expiration = 30)
        : TeosCommand("")
      {
        copy(setContract(accountName, wastFile, abiFile, skip, expiration));
      }

      SetContract(ptree reqJson) : TeosCommand(
        "", reqJson)
      {
        copy(setContract(
            reqJson.get<string>("account"),
            reqJson.get<string>("wast"), reqJson.get<string>("abi"),
            reqJson.get<bool>("skip"), reqJson.get<int>("expiration")));
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
  }'] [OPTIONS]
)EOF";
      }

      string account;
      string wast;
      string abi;
      bool skip;
      int expiration;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("account,n", value<string>(&account)
            , "The name of account to publish a contract for")
          ("wast,o", value<string>(&wast), "The WAST file for the contract")
          ("abi,a", value<string>(&abi)->default_value("")
            , "The ABI file for the contract")
          ("skip,s", value<bool>(&skip)->default_value(false)
            , "Specify that unlocked wallet keys should not be used to "
              "sign transaction, defaults to false")
          ("expiration,x", value<int>(&expiration)->default_value(30)
            , "The time in seconds before a transaction expires");
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
            ok = true;
          }
        }
        reqJson_.put("abi", abi);
        reqJson_.put("skip", skip);
        reqJson_.put("expiration", expiration);
        return ok;
      }

      TeosControl executeCommand() {
        return SetContract(reqJson_);
      }

    };
  }
}