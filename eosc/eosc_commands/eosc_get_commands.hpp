/**
 * @file eosc_get_commands.hpp
 *
 * Definitions for get-type commands.
 *
 * Defines command line options.
 */

 // test PS E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug> ./eosc 198.100.148.136:8888 geet block 234
 //  htpc.cpp
 // 63       std::string request = request_stream.str();
 // 64       std::cout << request << std::endln;
 // 
#pragma once

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/property_tree/ptree.hpp>

#include "../eosc_config.h"
#include "eosc_command.hpp"

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

extern const char* getSubcommands;
extern const string getCommandPath;

/* EXAMPLARY TEMPLATE

    class XxxYyy : public EoscCommand
    {
    public:

      XxxYyy(ptree reqJson, bool raw = false) : EoscCommand(
        string(xxxCommandPath + "get_info").c_str(), reqJson, raw) {
          callEosd();
        }
    };

    class XxxYyyOptions : public CommandOptions
    {
    public:
      XxxYyyOptions(int argc, const char **argv)
      : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
      #ifdef WIN32
      return R"EOF(
Lorem ipsum dolor sit amet, consectetur
Usage: ./eosc xxx yyy [positional] [Options]
Usage: ./eosc xxx yyy [-j "{"""argName""":"""argType"""}"] [OPTIONS]
)EOF"; 
#else
return R"EOF(
Create a new wallet locally
Usage: ./eosc xxx yyy [wallet name] [Options]
Usage: ./eosc xxx yyy [-j '{"argName":"argType"}'] [OPTIONS]
)EOF";
#endif
      }

      type1 option1Value;
      type2 option2Value;

      options_description options() {
        options_description special("");
        special.add_options()
          ("option,o", value<type>(&option), "Lorem ipsum dolor sit");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("positional", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("option1")) {
          reqJson.put("option1Name", option1Value);
          if (vm.count("option2Name")) {
            reqJson.put("option2Name", option2Value);
            ok = true;
          }
        }
        return ok;
      }

      EoscCommand getCommand(bool is_raw) {
        return XxxYyy(reqJson, is_raw);
      }

      void getOutput(EoscCommand command) {
        output("block number", "%d", command.get<int>("block_num"));
        output("timestamp", "%s", command.get<string>("timestamp").c_str());
        output("ref block prefix", "%s", command.get<string>("ref_block_prefix").c_str());
      }

      void getExample() {
        cout << R"EOF(
Invoke 'GetInfo' command:
GetInfo GetInfo;
)EOF" << endl;        

        boost::property_tree::ptree reqJson;
        GetInfo GetInfo(reqJson);
        cout << GetInfo.toStringRcv() << endl;
      }
    };

*/

namespace tokenika
{
  namespace eosc
  {

    /**
     * @brief Get current blockchain information.
     *
     * Example:
     *
     * @verbatim
     * #include <stdio.h>
     * #include <stdlib.h>
     * #include <iostream>
     * #include <string>
     * #include <boost/property_tree/ptree.hpp>
     * #include "EoscCommands/eosc_get_commands.hpp"
     *
     * int main(int argc, char *argv[])
     * {
     * boost::property_tree::ptree reqJson;
     * tokenika::eosc::GetInfo GetInfo(getInfoPostJson);
     * std::cout << GetInfo.get<int>("last_irreversible_block_num")) << std::endl;
     * boost::property_tree::ptree rcv_json = GetInfo.getRcvJson();
     * std::cout << GetBlock.toStringRcv() << std::endl; // Print the response json.
     *
     * return 0;
     * }
     * @endverbatim
     */
    class GetInfo : public EoscCommand
    {
    public:

      GetInfo(ptree reqJson, bool raw = false) : EoscCommand(
        string(getCommandPath + "get_info").c_str(), reqJson, raw) {
        callEosd();
      }
    };

    /**
    * @brief Command-line driver for the GetInfo class
    * Extends the CommandOptions class adding features specific to the
    * 'wallet open_all' eosc command.
    */
    class GetInfoOptions : public CommandOptions
    {
    public:
      GetInfoOptions(int argc, const char **argv) : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
#ifdef WIN32
        return R"EOF(
Get current blockchain information
Usage: ./eosc get info [Options]
Usage: ./eosc get info [-j "{}"] [OPTIONS]
)EOF";
#else
        return R"EOF(
Get current blockchain information
Usage: ./eosc get info [Options]
Usage: ./eosc get info [-j '{}'] [OPTIONS]
)EOF";
#endif
      }

      bool setJson(variables_map &vm) {
        return true;
      }

      EoscCommand getCommand(bool is_raw) {
        return GetInfo(reqJson, is_raw);
      }

      void getOutput(tokenika::eosc::EoscCommand command) {
        output("head block", "%d", command.get<int>("head_block_num"));
        output("head block time", "%s", GET_STRING(command, "head_block_time"));
        output("last irreversible block", "%d", command.get<int>("last_irreversible_block_num"));
      }

      void getExample() {
        boost::property_tree::ptree reqJson;
        GetInfo GetInfo(reqJson);
        cout << R"EOF(
Invoke 'GetInfo' command:
GetInfo GetInfo;
)EOF" << std::endl;
        cout << GetInfo.toStringRcv() << endl;
      }
    };

/**
 * @brief Retrieve a full block from a blockchain.
 *
 * Given a `boost::property_tree::ptree json`, conforms ([after eosjs-json]
 * (#https://github.com/EOSIO/eosjs-json/blob/master/api/v1/chain.json)) this
 * pattern:
 * @verbatim
 * {"block_num_or_id":"uint32 | string"}.
 * @endverbatim
 *
 * the constructor posts it to
 * an EOS block socket, specified in the `eosc_config.json` file. The responce
 * of the blockchain is, again, a `boost::property_tree::ptree json`. On error,
 * the reaponce json is `{"error":"error message"}`, otherwise it conforms
 * ([after eosjs-json]
 * (#https://github.com/EOSIO/eosjs-json/blob/master/api/v1/chain.json)) this
 * pattern:
 * @verbatim
 * {
 * "previous":"uint32",
 * "timestamp":"2017-07-18T20:16:36",
 * "transaction_merkle_root":"uint32",
 * "producer":"uint16",
 * "producer_changes":"map<account_name, account_name>[]",
 * "producer_signature":"signature",
 * "cycles":"thread[]",
 * "id":"fixed_bytes33",
 * "block_num":"uint32",
 * "refBlockPrefix":"uint32"
 * }
 * @endverbatim
 *account
 * It is available with the \ref tokenika::eosc::EoscCommand::getRcvJson() method.
 *
 * Note that time is a string. For processing, it has to be expressed as a
 * structure and afterwords back to a string. Helper functions, namely
 * ::strToTime(const string)
 *
 * Example:
 *
 * @verbatim
 * #include <stdio.h>
 * #include <stdlib.h>
 * #include <iostream>
 * #include <string>
 *
 * #include <boost/property_tree/ptree.hpp>
 * #include "boost/date_time/posix_time/posix_time.hpp"
 *
 * #include "EoscCommands/eosc_get_commands.hpp"
 *
 * int main(int argc, char *argv[])
 * {
 * boost::property_tree::ptree reqJson;
 * reqJson.put("block_num_or_id", 25);
 * tokenika::eosc::GetBlock getBlock(getInfoPostJson);
 * if(!getBlock.isError())
 * {
 *    std::cout << getBlock.get<int>("last_irreversible_block_num")) << std::endl;
 *    boost::posix_time::ptime time = GetInfo.get<boost::posix_time::ptime>("timestamp");
 *    std::cout << time << std::endl;
 *    boost::posix_time::ptime t1 = time + boost::posix_time::seconds(900);
 *    cout << (boost::posix_time::to_iso_extended_string)(t1) << endl;
 * } else
 * {
 *    std::cerr << getBlock.get<string>("error")) << std::endl;
 * }
 *
 * return 0;
 * }
 * @endverbatim
 */
    class GetBlock : public EoscCommand
    {
    public:

      GetBlock(ptree reqJson, bool raw = false) : EoscCommand(
        string(getCommandPath + "get_block").c_str(), reqJson, raw) {
        callEosd();
      }
    };
    
    /**
    * @brief Command-line driver for the GetBlock class.
    * Extends the CommandOptions class adding features specific to the
    * 'wallet open_all' eosc command.
    */
    class GetBlockOptions : public CommandOptions
    {
    public:
      GetBlockOptions(int argc, const char **argv) : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
#ifdef WIN32
        return R"EOF(
Retrieve a full block from the blockchain
Usage: ./eosc get block [block_num | block_id] [Options]
Usage: ./eosc get block [-j "{"""block_num_or_id""":"""int | string"""}"] [OPTIONS]
)EOF";
#else
        return R"EOF(
Retrieve a full block from the blockchain
Usage: ./eosc get block [block_num | block_id] [Options]
Usage: ./eosc get block [-j '{"block_num_or_id":"int | string"}'] [OPTIONS]
)EOF";
#endif

      }

      int n;
      string id;

      options_description options() {
        options_description special("");
        special.add_options()
          ("block_num,n",
            value<int>(&n),
            "Block number")
            ("block_id,i",
              value<string>(&id),
              "Block id");
        return special;
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

      EoscCommand getCommand(bool is_raw) {
        return GetBlock(reqJson, is_raw);
      }

      void getOutput(EoscCommand command) {
        output("block number", "%d", command.get<int>("block_num"));
        output("timestamp", "%s", GET_STRING(command, "timestamp"));
        output("ref block prefix", "%s", GET_STRING(command, "ref_block_prefix"));
      }

      void getExample() {
        ptree getInfoPostJson;
        GetInfo GetInfo(getInfoPostJson);
        cout << R"EOF(
Invoke 'GetInfo' command:
GetInfo getInfo;
)EOF" << endl;

        cout << GetInfo.toStringRcv() << endl;
        ptree GetBlock_post_json;
        GetBlock_post_json.put("block_num_or_id", 25);
        GetBlock GetBlock(GetBlock_post_json);
        cout << R"EOF(
Use reference to the last block:
GetBlock GetBlock(
  GetInfo.get<int>("last_irreversible_block_num"));
)EOF" << endl;
        cout << GetBlock.toStringRcv() << endl;
      }
    };

    /**
     * @brief Fetch a blockchain account
     * 
     * Extends the EoscCommand class so that it addresses the 'get account' command
     * to the blockchain.
    */
    class GetAccount : public EoscCommand
    {
    public:

      GetAccount(ptree reqJson, bool raw = false) : EoscCommand(
        string(getCommandPath + "get_account").c_str(), reqJson, raw) {
        callEosd();
      }
    };

    /**
    * @brief Command-line driver for the GetAccount class
    * Extends the CommandOptions class adding features specific to the
    * 'wallet open_all' eosc command.
    */
    class GetAccountOptions : public CommandOptions
    {
    public:
      GetAccountOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
#ifdef WIN32
        return R"EOF(
Fetch a blockchain account
Usage: ./eosc get account [account_name] [Options]
Usage: ./eosc get account [-j "{"""account_name""":"""string"""}"] [OPTIONS]
)EOF";
#else
        return R"EOF(
Fetch a blockchain account
Usage: ./eosc get account [account_name] [Options]
Usage: ./eosc get account [-j '{"account_name":"string"}'] [OPTIONS]
)EOF";
#endif

      }

      string name;

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n",
            value<string>(&name), "Account name");
        return special;
      }

      void
        setPosDesc(positional_options_description&pos_desc) {
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

      EoscCommand getCommand(bool is_raw) {
        return GetAccount(reqJson, is_raw);
      }

      void getOutput(EoscCommand command) {
        output("account name", "%s", GET_STRING(command, "account_name"));
        output("eos balance", "%s", GET_STRING(command, "eos_balance"));
        output("staked balance", "%s", GET_STRING(command, "staked_balance"));
        output("unstaking balance", "%s", GET_STRING(command, "unstaking_balance"));
        output("last unstaking time", "%s", GET_STRING(command, "last_unstaking_time"));
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
reqJson.put("account_name", "int");
GetAccount getAccount(reqJson);
cout << getAccount.toStringRcv() << endl;
)EOF" << endl;
        ptree reqJson;
        reqJson.put("account_name", "inita");
        GetAccount getAccount(reqJson);
        cout << getAccount.toStringRcv() << endl;
      }
    };
      /**
      * @brief Retrieve the code and ABI for an account
      *
      * Extends the EoscCommand class so that it addresses the 'get account' command
      * to the blockchain.
      */
      class GetCode : public EoscCommand
      {
      public:

        GetCode(ptree reqJson, bool raw = false) : EoscCommand(
          string(getCommandPath + "get_code").c_str(), reqJson, raw) {
          callEosd();
        }
      };

      /**
      * @brief Command-line driver for the GetCode class
      * Extends the CommandOptions class adding features specific to the
      * 'wallet open_all' eosc command.
      */
      class GetCodeOptions : public CommandOptions
      {
      public:
        GetCodeOptions(int argc, const char **argv)
          : CommandOptions(argc, argv) {}

      protected:
        const char* getUsage() {
#ifdef WIN32
          return R"EOF(
Retrieve the code and ABI for an account
Usage: ./eosc get code [account_name] [Options]
Usage: ./eosc get code [-j "{"""account_name""":"""string"""}"] [OPTIONS]
)EOF";
#else
          return R"EOF(
Retrieve the code and ABI for an account
Usage: ./eosc get code [account_name] [Options]
Usage: ./eosc get code [-j '{"account_name":"string"}'] [OPTIONS]
)EOF";
#endif
        }

        string accountName;

        options_description options() {
          options_description special("");
          special.add_options()
            ("name,n", value<string>(&accountName), "The name of the account whose code should be retrieved");
          return special;
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
          return ok;
        }

        EoscCommand getCommand(bool is_raw) {
          return GetCode(reqJson, is_raw);
        }

        void getOutput(EoscCommand command) {
          output("account name", "%s", GET_STRING(command, "account_name"));
          output("code hash", "%s", GET_STRING(command, "code_hash"));
          output("wast", "%s", GET_STRING(command, "wast"));
        }

        void getExample() {
          cout << R"EOF(
boost::property_tree::ptree reqJson;
reqJson.put("account_name", "inita");
GetCode getCode(reqJson);
cout << getCode.toStringRcv() << endl; 
)EOF" << endl;

          boost::property_tree::ptree reqJson;
          reqJson.put("account_name", "inita");
          GetCode getCode(reqJson);
          cout << getCode.toStringRcv() << endl;
        }
      };

      /**
      * @brief Retrieve the contents of a database table.
      *
      * Extends the EoscCommand class so that it addresses the 'get account' command
      * to the blockchain.
      */
      class GetTable : public EoscCommand
      {
      public:

        GetTable(ptree reqJson, bool raw = false) : EoscCommand(
          string(getCommandPath + "get_table").c_str(), reqJson, raw) {
          callEosd();
        }

        string normRequest(ptree& reqJson) {
          reqJson.put("json", true);          
          return EoscCommand::normRequest(reqJson);
        }

      };

      class GetTableOptions : public CommandOptions
      {
      public:
        GetTableOptions(int argc, const char **argv)
          : CommandOptions(argc, argv) {}

      protected:
        const char* getUsage() {
#ifdef WIN32
          return R"EOF(
Retrieve the contents of a database table
Usage: ./eosc get table [scope] [contract] [table] [Options]
Usage: ./eosc get table [-j "{"""scope""":"""string""","""code""":"""string""","""table""":"""table"""}"] [OPTIONS]
)EOF";
#else
          return R"EOF(
Retrieve the contents of a database table
Usage: ./eosc get table [scope] [contract] [table] [Options]
Usage: ./eosc xxx yyy [-j '{"argName":"argType"}'] [OPTIONS]
Usage: ./eosc get table [-j '{"scope""":"string","code":"string","table":"table"}'] [OPTIONS]
)EOF";
#endif
        }

        string scope;
        string contract;
        string table;

        options_description options() {
          options_description special("");
          special.add_options()
            ("scope,e", value<string>(&scope), "The account scope where the table is found")
            ("contract,c", value<string>(&contract), "The contract within scope who owns the table")
            ("table,t", value<string>(&table), "The name of the table as specified by the contract abi");
          return special;
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

        EoscCommand getCommand(bool is_raw) {
          return GetTable(reqJson, is_raw);
        }

        void getOutput(EoscCommand command) {
          output("TO_DO");
        }

        void getExample() {
          cout << R"EOF(
boost::property_tree::ptree reqJson;
reqJson.put("scope", "inita");
reqJson.put("code", "currency");
reqJson.put("table", "account");
GetInfo GetInfo(reqJson);
cout << GetInfo.toStringRcv() << endl;
)EOF" << endl;

          boost::property_tree::ptree reqJson;
          reqJson.put("scope", "inita");
          reqJson.put("code", "currency");
          reqJson.put("table", "account");
          GetTable getTable(reqJson);
          cout << getTable.toStringRcv() << endl;
        }
      };

//      class XxxYyy : public EoscCommand
//      {
//      public:
//
//        XxxYyy(ptree reqJson, bool raw = false) : EoscCommand(
//          string(xxxCommandPath + "get_info").c_str(), reqJson, raw) {
//          callEosd();
//        }
//      };
//
//      /**
//      * @brief Command-line driver for the GetInfo class
//      * Extends the CommandOptions class adding features specific to the
//      * 'wallet open_all' eosc command.
//      */
//      class XxxYyyOptions : public CommandOptions
//      {
//      public:
//        XxxYyyOptions(int argc, const char **argv)
//          : CommandOptions(argc, argv) {}
//
//      protected:
//        const char* getUsage() {
//#ifdef WIN32
//          return R"EOF(
//Lorem ipsum dolor sit amet, consectetur
//Usage: ./eosc xxx yyy [positional] [Options]
//Usage: ./eosc xxx yyy [-j "{"""argName""":"""argType"""}"] [OPTIONS]
//)EOF";
//#else
//          return R"EOF(
//Create a new wallet locally
//Usage: ./eosc xxx yyy [wallet name] [Options]
//Usage: ./eosc xxx yyy [-j '{"argName":"argType"}'] [OPTIONS]
//)EOF";
//#endif
//        }
//
//        type1 option1Value;
//        type2 option2Value;
//
//        options_description options() {
//          options_description special("");
//          special.add_options()
//            ("option,o", value<type>(&option), "Lorem ipsum dolor sit");
//          return special;
//        }
//
//        void setPosDesc(positional_options_description& pos_desc) {
//          pos_desc.add("positional", 1);
//        }
//
//        bool setJson(variables_map &vm) {
//          bool ok = false;
//          if (vm.count("option1")) {
//            reqJson.put("option1Name", option1Value);
//            if (vm.count("option2Name")) {
//              reqJson.put("option2Name", option2Value);
//              ok = true;
//            }
//          }
//          return ok;
//        }
//
//        EoscCommand getCommand(bool is_raw) {
//          return XxxYyy(reqJson, is_raw);
//        }
//
//        void getOutput(EoscCommand command) {
//          output("block number", "%d", command.get<int>("block_num"));
//          output("timestamp", "%s", command.get<string>("timestamp").c_str());
//          output("ref block prefix", "%s", command.get<string>("ref_block_prefix").c_str());
//        }
//
//        void getExample() {
//          cout << R"EOF(
//Invoke 'GetInfo' command:
//GetInfo GetInfo;
//)EOF" << endl;
//
//          boost::property_tree::ptree reqJson;
//          GetInfo GetInfo(reqJson);
//          cout << GetInfo.toStringRcv() << endl;
//        }
//      };
  }
}