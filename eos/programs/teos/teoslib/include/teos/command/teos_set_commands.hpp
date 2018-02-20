#pragma once

#include <teoslib/config.h>
#include <teos/eos_interface.hpp>
#include <teos/command/teos_command.hpp>

using namespace std;

extern const char* setSubcommands;
extern const string setCommandPath;

namespace tokenika
{
  namespace teos
  {
    /**
    Create or update the contract on an account.
    */
    class SetContract : public TeosCommand
    {
    public:
      SetContract(string accountName,
        string wastFile, string abiFile = "",
        bool skip = false, int expiration = 30, bool raw = false)
        : TeosCommand("", raw)
      {
        copy(setContract(accountName, wastFile, abiFile, skip, expiration));
      }

      SetContract(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson, raw)
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
Usage: ./teos set contract [account] [wast] [abi] [Options]
Usage: ./teos create key [-j '{
  "account":"<account name>"
  "wast":"<wast file>"
  "abi":"<abi file>"
  }'] [OPTIONS]
)EOF";
      }

      string account;
      string wast;
      string abi;
      string activeKey;
      bool skip;
      int expiration;
      int deposit;


      options_description options() {
        options_description special("");
        special.add_options()
          ("account,n", value<string>(&account), "The name of account to publish a contract for")
          ("wast,o", value<string>(&wast), "The WAST file for the contract")
          ("abi,a", value<string>(&abi)->default_value(""), "The ABI file for the contract")
          ("skip,s", value<bool>(&skip)->default_value(false), "Specify that unlocked wallet keys should not be used to sign transaction, defaults to false")
          ("expiration,x", value<int>(&expiration)->default_value(30), "The time in seconds before a transaction expires")
          ("deposit,d", value<int>(&deposit)->default_value(1), "The initial deposit");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("account", 1);
        pos_desc.add("wast", 1);
        pos_desc.add("abi", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("account")) {
          reqJson.put("account", account);
          if (vm.count("wast")) {
            reqJson.put("wast", wast);
            ok = true;
          }
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return SetContract(reqJson, is_raw);
      }

      void getExample() {
        cout << R"EOF(
)EOF" << endl;
      }
    };
  }
}