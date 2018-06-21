/**
 * @file wallet_commands.hpp
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
#include <boost/foreach.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/replace.hpp>

#include <teoslib/config.h>
#include <teoslib/command.hpp>

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

extern const char* walletSubcommands;
extern const string walletCommandPath;

namespace teos
{
  namespace command
  {
#define DEFAULT_WALLET_NAME "default"
    /**
     * @ingroup teoslib_raw
     * @brief Create a new wallet locall.
     */
    class WalletCreate : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param name wallet ID.
      */
      WalletCreate(string name = DEFAULT_WALLET_NAME) : TeosCommand(
        string(walletCommandPath + "create")) {
        reqJson_.put("name", name);
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"name":"<wallet name>"}.
       */
      WalletCreate(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "create"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("\"") + reqJson.get<string>("name") + "\"";
      }

      void normResponse(string response, ptree &respJson) {
        respJson.put("password", boost::replace_all_copy(response, "\"", ""));
      }

    };


    /**
     * @ingroup teoslib_raw
     * @brief Import private key into wallet.
     * 
     */
    class WalletImport : public TeosCommand
    {
    public:
      /**
       * @brief A constructor.
       * @param name wallet ID.
       * @param keyPrivate private key, proving authorities.
       */
      WalletImport(string name, string keyPrivate) : TeosCommand(
          string(walletCommandPath + "import_key")) {
        reqJson_.put("name", name);
        reqJson_.put("key", keyPrivate);
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"name":"<wallet name>", "key":"<private key>"}.
       */
      WalletImport(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "import_key"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("[\"") + reqJson.get<string>("name") + "\",\"" + reqJson.get<string>("key") + "\"]";
      }

      void normResponse(string response, ptree &respJson) {}
    };


    /**
     * @ingroup teoslib_raw
     * @brief List opened wallets, * = unlocked
     * 
     */
    class WalletList : public TeosCommand
    {
    public:
      WalletList() : TeosCommand(
        string(walletCommandPath + "list_wallets")) {
        callEosd();
      }

      WalletList(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "list_wallets"), reqJson) {
        callEosd();
      }

      void normResponse(string response, ptree &respJson) 
      {
        boost::replace_all(response, "[", "{\"wallets\":[");
        boost::replace_all(response, "]", "]}");
        TeosCommand::normResponse(response, respJson);
      }

    };


    /**
    * @ingroup teoslib_raw
    * @brief Open an existing wallet.
    */
    class WalletOpen : public TeosCommand
    {
    public:
      WalletOpen(string name = DEFAULT_WALLET_NAME) : TeosCommand(
        string(walletCommandPath + "open")) {
        reqJson_.put("name", name);
        callEosd();
      }

      WalletOpen(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "open"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("\"") + reqJson.get<string>("name") + "\"";
      }

      void normResponse(string response, ptree &respJson) {}

    };


    /**
    * @ingroup teoslib_raw
    * @brief Lock wallet
    */
    class WalletLock : public TeosCommand
    {
    public:

      WalletLock(string name = DEFAULT_WALLET_NAME) : TeosCommand(
        string(walletCommandPath + "lock")) {
        callEosd();
      }

      WalletLock(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "lock"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("\"") + reqJson.get<string>("name") + "\"";
      }

      void normResponse(string response, ptree &respJson) {}

    };


    /**
    * @ingroup teoslib_raw
    * @brief Lock all unlocked wallets
    */
    class WalletLockAll : public TeosCommand
    {
    public:

      WalletLockAll() : TeosCommand(
        string(walletCommandPath + "lock_all")) {
        callEosd();
      }

      WalletLockAll(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "lock_all"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("");
      }

      void normResponse(string response, ptree &respJson) {}

    };


    /**
    * @ingroup teoslib_raw
    * @brief Unlock wallet
    *
    */
    class WalletUnlock : public TeosCommand
    {
    public:

      WalletUnlock(string password, string name = DEFAULT_WALLET_NAME) 
        : TeosCommand(string(walletCommandPath + "unlock")) 
      {
        reqJson_.put("password", password);
        reqJson_.put("name", name);
        callEosd();
      }

      WalletUnlock(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "unlock"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("[\"") + reqJson.get<string>("name") 
          + "\",\"" + reqJson.get<string>("password") + "\"]";
      }

      void normResponse(string response, ptree &respJson) {}
    };


    /**
    * @ingroup teoslib_raw
    * @brief List opened wallets, *= unlocked
    *
    */
    class WalletKeys : public TeosCommand
    {
    public:

      WalletKeys() : TeosCommand(
        string(walletCommandPath + "list_keys")) {
        callEosd();
      }

      WalletKeys(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "list_keys"), reqJson) {
        callEosd();
      }     
    };
  }
}