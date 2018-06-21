/**
 * @file get_commands.hpp
 * @copyright defined in LICENSE.txt
 * @author Tokenika
 * @date 30 May 2018
*/

/**
 * @defgroup teoslib_raw Raw function classes
 */
/**
 * @defgroup teoslib_cli Command-line drivers
 */

#pragma once

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/property_tree/ptree.hpp>

#include <teoslib/config.h>
#include <teoslib/command.hpp>

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
     * @ingroup teoslib_raw
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
     * @ingroup teoslib_raw
     * @brief Retrieve a full block from a blockchain.
     */
    class GetBlock : public TeosCommand
    {
    public:

      GetBlock(ptree reqJson) : TeosCommand(
        string(getCommandPath + "get_block"), reqJson) {
        callEosd();
      }
    };


    /**
     * @ingroup teoslib_raw
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
     * @ingroup teoslib_raw
     * @brief Retrieve accounts associated with a public key.
    */
    class GetAccounts : public TeosCommand
    {
      #define GET_ACCOUNTS_PATH "/v1/account_history/get_key_accounts"      
    public:
      GetAccounts(string publicKey) 
        : TeosCommand(GET_ACCOUNTS_PATH) 
      {
        reqJson_.put("public_key", publicKey);
        callEosd();
      }
      
      GetAccounts(ptree reqJson) 
        : TeosCommand(GET_ACCOUNTS_PATH, reqJson) 
      {
        callEosd();
      }

    };


    /**
    * @ingroup teoslib_raw
    * @brief Retrieves the code and ABI for an account.
    */
    class GetCode : public TeosCommand
    {
      #define WRITE_TO_STDOUT "stdout"
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
        // copy(getCode(
        //   accountName, 
        //   wastFile == WRITE_TO_STDOUT ? "" : wastFile, 
        //   abiFile == WRITE_TO_STDOUT ? "" : abiFile));
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"account_name":"<account name>", 
       * "wast":"<wast file>", "abi":"<abi file>"}
       * @param raw if true, resulting json is not formated.
       */
      GetCode(ptree reqJson) : TeosCommand(
        string(getCommandPath + "get_code"), reqJson) {
        string wastFile = reqJson.get<string>("wast");
        wastFile = wastFile == WRITE_TO_STDOUT ? "" : wastFile;
        string abiFile = reqJson.get<string>("abi");
        abiFile = abiFile == WRITE_TO_STDOUT ? "" : abiFile;
        // copy(getCode(reqJson.get<string>("account_name"), wastFile, abiFile));
      }
    };


    /**
    * @ingroup teoslib_raw
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

  }
}