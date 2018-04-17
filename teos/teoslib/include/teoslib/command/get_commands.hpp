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
#include <teoslib/command.hpp>
#include <teoslib/eos_interface.hpp>

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
Usage: ./teos get info --jarg '{}' [OPTIONS]
)EOF";
      }

      TeosControl executeCommand() {
        return GetInfo(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
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
Usage: ./teos get block --jarg '{"block_num_or_id":"<int | string>"}' [OPTIONS]
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

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("block_num")) {
          reqJson_.put("block_num_or_id", n);
          ok = true;
        }
        else if (vm.count("block_id")) {
          reqJson_.put("block_num_or_id", id);
          ok = true;
        }
        return ok;
      }

      TeosControl executeCommand() {
        return GetBlock(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
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
Usage: ./teos get account --jarg '{"account_name":"<account name>"}' [OPTIONS]
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

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson_.put("account_name", name);
          ok = true;
        }
        return ok;
      }

      TeosControl executeCommand() {
        return GetAccount(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("account name", "%s", GET_STRING(command, "account_name"));
      }
    };

    // /**
    //  * @brief Retrieve accounts associated with a public key.
    // */
    // class GetAccounts : public TeosCommand
    // {

    // public:
    //   GetAccounts(string publicKey) : TeosCommand(
    //     string("/v1/account_history/get_key_accounts")) {
    //     reqJson_.put("public_key", publicKey);
    //     callEosd();
    //   }

    //   GetAccount(ptree reqJson, bool raw = false) : TeosCommand(
    //     string(getCommandPath + "get_account"), reqJson) {
    //     callEosd();
    //   }
    // };

#define WRITE_TO_STDOUT "stdout"
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
      * "wast":"<WAST code>", "abi":"<abi structure>"}.
      */
      GetCode(string accountName, 
        string wastFile = "", string abiFile = "") 
        : TeosCommand(string(getCommandPath + "get_code")) 
      {
        copy(getCode(
          accountName, 
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
        string wastFile = reqJson.get<string>("wast");
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
Usage: ./teos get code --jarg '{"account_name":"<account name>", "wast":"<wast file>", 
"abi":"<abi file>"}' [OPTIONS]
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

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson_.put("account_name", accountName);
          ok = true;
        }
        reqJson_.put("wast", wastFile);
        reqJson_.put("abi", abiFile);
        return ok;
      }

      TeosControl executeCommand() {
        return GetCode(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("code hash", "%s", GET_STRING(command, "code_hash"));
      }

    };

    /**
    * @brief Retrieves the contents of a database table.
    *
    */
    class GetTable : public TeosCommand
    {
    public:
      GetTable(
          string contract, string scope, string table,
          unsigned limit = 10, string key = "", 
          string lower = "", string upper = ""
      ) : TeosCommand(
        string(getCommandPath + "get_table_rows")) {
        reqJson_.put("json", true);
        reqJson_.put("code", contract);        
        reqJson_.put("scope", scope);
        reqJson_.put("table", table);
        reqJson_.put("limit", limit);
        reqJson_.put("table_key", key);
        reqJson_.put("lower_bound", lower);
        reqJson_.put("upper_bound", upper);
        callEosd();
      }

      GetTable(ptree reqJson, bool raw = false) : TeosCommand(
        string(getCommandPath + "get_table_rows"), reqJson) {
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
Usage: ./teos get table --jarg '{
  "code":"<contract>",  
  "scope":"<scope>",
  "table":"<table>",
  "limit":"<row count limit>",
  "table_key":"<table key>",
  "lower_bound":"<lower bound>",
  "upper_bound":"upper bound",      
  }' [OPTIONS]
)EOF";
      }

      string contract;      
      string scope;
      string table;
      unsigned limit;
      string key;
      string lower;
      string upper;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("contract", value<string>(&contract)
            , "The contract who owns the table.")
          ("scope", value<string>(&scope)
            , "The scope within the contract in which the table is found.")
          ("table", value<string>(&table)
            , "The name of the table as specified by the contract abi.")         
          ("limit,l", value<unsigned>(&limit)->default_value(10)
            , "The maximum number of rows to return.")                
          ("key,k", value<string>(&key)->default_value("")
            , "The name of the key to index by as defined by the abi, defaults "
              "to primary key.")                
          ("lower,L", value<string>(&lower)->default_value("")
            , "JSON representation of lower bound value of key, defaults "
              "to first.")    
          ("upper,U", value<string>(&upper)->default_value("")
            , "JSON representation of upper bound value value of key, "
              "defaults to last.");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("contract", 1).add("scope", 1).add("table", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("contract")) {
          reqJson_.put("code", contract);
          if (vm.count("scope")) {
            reqJson_.put("scope", scope);
            if (vm.count("table")) {
              reqJson_.put("table", table);
              reqJson_.put("limit", limit);
              reqJson_.put("table_key", key);
              reqJson_.put("lower_bound", lower);
              reqJson_.put("upper_bound", upper);
              ok = true;
            }
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return GetTable(reqJson_);
      }
    };
  }
}