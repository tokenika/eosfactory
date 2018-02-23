/**
 * @file get_commands.hpp
 *
 * Definitions for get-type commands.
 *
 * Defines command line options.
 */

#pragma once

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/property_tree/ptree.hpp>

#include <teoslib/config.h>
#include <teos/command/command.hpp>
#include <teos/eos_interface.hpp>

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

extern const char* getSubcommands;
extern const string getCommandPath;

namespace teos
{
  namespace command
  {

    /**
     * @brief Get current blockchain information.
     */
    class GetInfo : public TeosCommand
    {
    public:

      GetInfo(bool raw = false) : TeosCommand(
        string(getCommandPath + "get_info")) {
        callEosd();
      }

      GetInfo(ptree reqJson, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_info"), reqJson) {
        callEosd();
      }
    };

    /**
    * @brief Command-line driver for the GetInfo class.
    */
    class GetInfoOptions : public CommandOptions
    {
    public:
      GetInfoOptions(int argc, const char **argv) : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Get current blockchain information
Usage: ./teos get info [Options]
Usage: ./teos get info [-j '{}'] [OPTIONS]
)EOF";
      }

      bool setJson(variables_map &vm) {
        return true;
      }

      TeosCommand getCommand() {
        return GetInfo(reqJson);
      }

      void getOutput(teos::command::TeosCommand command) {
        output("head block", "%d", command.get<int>("head_block_num"));
        output("head block time", "%s", GET_STRING(command, "head_block_time"));
        output("last irreversible block", "%d", command.get<int>("last_irreversible_block_num"));
      }

    };

    /**
     * @brief Retrieve a full block from a blockchain.
     */
    class GetBlock : public TeosCommand
    {
    public:

      GetBlock(ptree reqJson, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_block"), reqJson) {
        callEosd();
      }
    };

    /**
    * @brief Command-line driver for the GetBlock class.
    */
    class GetBlockOptions : public CommandOptions
    {
    public:
      GetBlockOptions(int argc, const char **argv) : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Retrieve a full block from the blockchain
Usage: ./teos get block [block_num | block_id] [Options]
Usage: ./teos get block [-j '{"block_num_or_id":"<int | string>"}'] [OPTIONS]
)EOF";
      }

      int n;
      string id;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("block_num,n",
            value<int>(&n),
            "Block number")
            ("block_id,i",
              value<string>(&id),
              "Block id");
        return od;
      }

      void
        setPosDesc(positional_options_description&pos_desc) {
        pos_desc.add("block_num", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("block_num")) {
          reqJson.put("block_num_or_id", n);
          ok = true;
        }
        else if (vm.count("block_id")) {
          reqJson.put("block_num_or_id", id);
          ok = true;
        }
        return ok;
      }

      TeosCommand getCommand() {
        return GetBlock(reqJson);
      }

      void getOutput(TeosCommand command) {
        output("block number", "%d", command.get<int>("block_num"));
        output("timestamp", "%s", GET_STRING(command, "timestamp"));
        output("ref block prefix", "%s", GET_STRING(command, "ref_block_prefix"));
      }

    };

    /**
     * @brief Fetch a blockchain account.
    */
    class GetAccount : public TeosCommand
    {
    public:
      GetAccount(string accountName, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_account")) {
        reqJson_.put("account_name", accountName);
        callEosd();
      }

      GetAccount(ptree reqJson, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_account"), reqJson) {
        callEosd();
      }
    };

    /**
    * @brief Command-line driver for the GetAccount class.
    */
    class GetAccountOptions : public CommandOptions
    {
    public:
      GetAccountOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Fetch a blockchain account
Usage: ./teos get account [account_name] [Options]
Usage: ./teos get account [-j '{"account_name":"<account name>"}'] [OPTIONS]
)EOF";
      }

      string name;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n",
            value<string>(&name), "Account name");
        return od;
      }

      void setPosDesc(positional_options_description&pos_desc) {
        pos_desc.add("name", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("account_name", name);
          ok = true;
        }
        return ok;
      }

      TeosCommand getCommand() {
        return GetAccount(reqJson);
      }

      void getOutput(TeosCommand command) {
        output("account name", "%s", GET_STRING(command, "account_name"));
        output("eos balance", "%s", GET_STRING(command, "eos_balance"));
        output("staked balance", "%s", GET_STRING(command, "staked_balance"));
        output("unstaking balance", "%s", GET_STRING(command, "unstaking_balance"));
        output("last unstaking time", "%s", GET_STRING(command, "last_unstaking_time"));
      }

    };

#define WRITE_TO_STDOUT "_"
    /**
    * @brief Retrieves the code and ABI for an account.
    */
    class GetCode : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param wastFile where write the wast code to. If "_", print to stdout.
      * @param abiFile where write the abi code to. If "_", print to stdout.
      * @param getResponse() returns {"account_name":"<account name>", "code_hash":"<code hash>",
      * "wast":"<WAST code>", "abi":"<abi structure>"}.
      */
      GetCode(string accountName, 
        string wastFile = "", string abiFile = "") 
        : TeosCommand(string(getCommandPath + "get_code")) 
      {
        copy(getCode(accountName, 
          wastFile == WRITE_TO_STDOUT ? "" : wastFile, 
          abiFile == WRITE_TO_STDOUT ? "" : abiFile));
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"account_name":"<account name>", 
       * "wast":"<wast file>", "abi":"<abi file>"}
       * @param raw if true, resulting json is not formated.
       */
      GetCode(ptree reqJson, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_code"), reqJson) {
        string wastFile = reqJson.get<string>("code");
        wastFile = wastFile == WRITE_TO_STDOUT ? "" : wastFile;
        string abiFile = reqJson.get<string>("abi");
        abiFile = abiFile == WRITE_TO_STDOUT ? "" : abiFile;
        copy(getCode(reqJson.get<string>("account_name"), wastFile, abiFile));
      }
    };

    /**
    * @brief Command-line driver for the GetCode class.
    */
    class GetCodeOptions : public CommandOptions
    {
    public:
      GetCodeOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Retrieve the code and ABI for an account
Usage: ./teos get code [account_name] [Options]
Usage: ./teos get code [-j '{"account_name":"<account name>", "wast":"<wast file>", 
"abi":"<abi file>"}'] [OPTIONS]
)EOF";
      }

      string accountName;
      string wastFile;
      string abiFile;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&accountName),
            "The name of the account whose code should be retrieved")
            ("wast,c", value<string>(&wastFile)->default_value(""),
              "The name of the file to save the contract .wast to")
              ("abi,a", value<string>(&abiFile)->default_value(""),
                "The name of the file to save the contract .abi to");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("account_name", accountName);
          ok = true;
        }
        reqJson.put("wast", wastFile);
        reqJson.put("abi", abiFile);
        return ok;
      }

      TeosCommand getCommand() {
        return GetCode(reqJson);
      }

      void getOutput(TeosCommand command) {
        output("account name", "%s", GET_STRING(command, "account_name"));
        output("code hash", "%s", GET_STRING(command, "code_hash"));
        if (wastFile == WRITE_TO_STDOUT) {
          output("wast", "%s", GET_STRING(command, "wast"));
        }
        if (abiFile == WRITE_TO_STDOUT) {
          output("abi", "%s", GET_STRING(command, "abi"));
        }
      }

    };

    /**
    * @brief Retrieves the contents of a database table.
    *
    */
    class GetTable : public TeosCommand
    {
    public:
      GetTable(string scope, string contract, string table,
        bool raw = false) : TeosCommand(
        string(getCommandPath + "get_table_rows")) {
        reqJson_.put("json", true);
        reqJson_.put("scope", scope);
        reqJson_.put("code", contract);
        reqJson_.put("table", table);
        callEosd();
      }

      GetTable(ptree reqJson, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_table"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        reqJson.put("json", true);
        return TeosCommand::normRequest(reqJson);
      }

    };

    class GetTableOptions : public CommandOptions
    {
    public:
      GetTableOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Retrieve the contents of a database table
Usage: ./teos get table [scope] [contract] [table] [Options]
Usage: ./teos get table [-j '{"scope":"<scope>","code":"<code>","table":"<table>"}'] [OPTIONS]
)EOF";
      }

      string scope;
      string contract;
      string table;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("scope,e", value<string>(&scope), "The account scope where the table is found")
          ("contract,c", value<string>(&contract), "The contract within scope who owns the table")
          ("table,t", value<string>(&table), "The name of the table as specified by the contract abi");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("scope", 1).add("contract", 1).add("table", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("scope")) {
          reqJson.put("scope", scope);
          if (vm.count("contract")) {
            reqJson.put("code", contract);
            if (vm.count("table")) {
              reqJson.put("table", table);
              ok = true;
            }
          }
        }
        return ok;
      }

      TeosCommand getCommand() {
        return GetTable(reqJson);
      }

      void getOutput(TeosCommand command) {
        output("TO_DO");
      }

    };

  }
}