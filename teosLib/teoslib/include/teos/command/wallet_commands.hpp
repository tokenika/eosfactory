#pragma once

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>
#include <boost/property_tree/json_parser.hpp>

#include <teoslib/config.h>
#include <teos/command/command.hpp>

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
     * @brief Create a new wallet locall.
     */
    class WalletCreate : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param name wallet ID.
      * @param getResponse() returns {"password":"<password>"}.
      */
      WalletCreate(string name = DEFAULT_WALLET_NAME) : TeosCommand(
        string(walletCommandPath + "create")) {
        reqJson_.put("name", name);
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"name":"<wallet name>"}.
       * @param getResponse() returns {"password":"<password>"}.
       */
      WalletCreate(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "create"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("\"") + reqJson.get<string>("name") + "\"";
      }

      void normResponse(string response, ptree &respJson) {
        respJson.put("password", response);
      }

    };

    /**
     * @brief Command-line driver for the WalletCreate class
     */
    class WalletCreateOptions : public CommandOptions
    {
    public:
      WalletCreateOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Create a new wallet locally
Usage: ./teos wallet create [wallet name] [Options]
Usage: ./teos wallet create [-j '{"name":"<wallet name>"}'] [OPTIONS]
)EOF";
      }

      string name;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&name)->default_value(DEFAULT_WALLET_NAME),
            "The name of the new wallet");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", name);
          ok = true;
        }
        return ok;
      }

      TeosCommand executeCommand() {
        return WalletCreate(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("password", "%s", GET_STRING(command, "password"));
        output("You need to save this password to be able to lock/unlock the wallet!");
      }

    };

    /**
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
       * @param getResponse() returns {}.
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
       * @param getResponse() returns {}.
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
     * @brief Command-line driver for the WalletImport class.
     */
    class WalletImportOptions : public CommandOptions
    {
    public:
      WalletImportOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Import private key into wallet
Usage: ./teos wallet import [name] [key] [Options]
Usage: ./teos wallet import [-j '{"name":"<wallet name>", "key":"<private key>"}'] [OPTIONS]
)EOF";
      }

      string name;
      string key;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&name), 
            "The name of the wallet to import key into")
          ("key,k", value<string>(&key), "Private key in WIF format to import");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1).add("key", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", name);
          if (vm.count("key")) {
            reqJson.put("key", key);
            ok = true;
          }
        }
        return ok;
      }

      TeosCommand executeCommand() {
        return WalletImport(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("wallet", "%s", name.c_str());
        output("key imported", "%s", key.c_str());
      }

    };

    /**
    * @brief List opened wallets, *= unlocked
    *wallets
    */
    class WalletList : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param getResponse() returns {"":"<wallet1 name>" "":"<wallet2 name>" ...}.
      */
      WalletList() : TeosCommand(
        string(walletCommandPath + "list_wallets")) {
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {}.
       * @param raw if true, resulting json is not formated.
       * @param getResponse() returns {"":"<wallet1 name>" "":"<wallet2 name>" ...}.
       */
      WalletList(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "list_wallets"), reqJson) {
        callEosd();
      }
    };

    /**
     * @brief Command-line driver for the WalletList class
     */
    class WalletListOptions : public CommandOptions
    {
    public:
      WalletListOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
List opened wallets, *= unlocked
Usage: ./teos wallet list [Options]
Usage: ./teos wallet list [-j '{}'] [OPTIONS]
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      TeosCommand executeCommand() {
        return WalletList(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        ptree rcvJson = command.getResponse();
        BOOST_FOREACH(ptree::value_type &v, rcvJson)
        {
          assert(v.first.empty()); // array elements have no names
          output("wallet", "%s", v.second.data().c_str());
        }
      }

    };

    /**
    * @brief Open an existing wallet.
    */
    class WalletOpen : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param name wallet ID.
      * @param getResponse() returns {}.
      */
      WalletOpen(string name = DEFAULT_WALLET_NAME) : TeosCommand(
        string(walletCommandPath + "open")) {
        reqJson_.put("name", name);
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"name":"<wallet name>"}.
       * @param raw if true, resulting json is not formated.
       * @param getResponse() returns {}.
       */
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
    * @brief Command-line driver for the WalletList class
    * Extends the CommandOptions class adding features specific to the
    * 'wallet open' teos command.
    *
    */
    class WalletOpenOptions : public CommandOptions
    {
    public:
      WalletOpenOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Open an existing wallet
Usage: ./teos wallet open [name] [Options]
Usage: ./teos wallet open [-j '{"name":"<wallet name>"}'] [OPTIONS]
)EOF";
      }

      string name;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&name), "The name of the wallet to open");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", name);
            ok = true;
        }
        return ok;
      }

      TeosCommand executeCommand() {
        return WalletOpen(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("wallet opened", "%s", name.c_str());
      }

    };

    /**
    * @brief Lock wallet
    */
    class WalletLock : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param name wallet ID.
      * @param raw a boolean argument:
      * if true, resulting json is not formated.
      * @param getResponse() returns {}.
      */
      WalletLock(string name = DEFAULT_WALLET_NAME) : TeosCommand(
        string(walletCommandPath + "lock")) {
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"name":"<wallet name>"}.
       * @param getResponse() returns {}.
       */
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
    * @brief Command-line driver for the WalletList class.
    */
    class WalletLockOptions : public CommandOptions
    {
    public:
      WalletLockOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Lock wallet
Usage: ./teos wallet lock [name] [Options]
Usage: ./teos wallet lock [-j '{"name":"<wallet name>"}'] [OPTIONS]
)EOF";
      }

      string name;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&name), "The name of the wallet to lock");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", name);
          ok = true;
        }
        return ok;
      }

      TeosCommand executeCommand() {
        return WalletLock(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("wallet lock", "%s", name.c_str());
      }

    };

    /**
    * @brief Lock all unlocked wallets
    */
    class WalletLockAll : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param raw if true, resulting json is not formated.
      * @param getResponse() returns {}.
      */
      WalletLockAll() : TeosCommand(
        string(walletCommandPath + "lock_all")) {
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {}.
       * @param raw if true, resulting json is not formated.
       * @param getResponse() returns {}.
       */
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
    * @brief Command-line driver for the WalletLockAll class
    */
    class WalletLockAllOptions : public CommandOptions
    {
    public:
      WalletLockAllOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Lock all unlocked wallets
Usage: ./teos wallet lock_all [Options]
Usage: ./teos wallet lock_all [-j '{}'] [OPTIONS]
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      TeosCommand executeCommand() {
        return WalletLockAll(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("wallets lock", "%s", "all");
      }

    };

    /**
    * @brief Unlock wallet
    *
    */
    class WalletUnlock : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param password the password returned by wallet create.
      * @param name the name of the wallet to unlock.
      * @param raw if true, resulting json is not formated.
      * @param getResponse() returns {}.
      */
      WalletUnlock(string password, string name = DEFAULT_WALLET_NAME) 
        : TeosCommand(string(walletCommandPath + "unlock")) 
      {
        reqJson_.put("password", password);
        reqJson_.put("name", name);
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"name":"<wallet name>"}.
       * @param getResponse() returns {}.
       */
      WalletUnlock(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "unlock"), reqJson) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("[\"") + reqJson.get<string>("name") + "\",\"" + reqJson.get<string>("password") + "\"]";
      }

      void normResponse(string response, ptree &respJson) {}
    };

    /**
    * @brief Command-line driver for the WalletUnlock class
    */
    class WalletUnlockOptions : public CommandOptions
    {
    public:
      WalletUnlockOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Unlock wallet
Usage: ./teos wallet import [password] [name] [Options]
Usage: ./teos wallet import [-j '{"password":"<password>", name":"<wallet name>"}'] [OPTIONS]
)EOF";
      }

      string name;
      string password;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("password", value<string>(&password), "The password returned by wallet create");        
          ("name,n", value<string>(&name), "The name of the wallet to unlock");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("password", 1);
        pos_desc.add("name", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", name);
          if (vm.count("password")) {
            reqJson.put("password", password);
            ok = true;
          }
        }
        return ok;
      }

      TeosCommand executeCommand() {
        return WalletUnlock(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("wallet unlocked", "%s", name.c_str());
      }

    };

    /**
    * @brief List opened wallets, *= unlocked
    *
    */
    class WalletKeys : public TeosCommand
    {
    public:
      /**
      * @brief A constructor.
      * @param raw if true, resulting json is not formated.
      * @param getResponse() returns {"":"<key1>" "":"<key2>" ...}.
      */
      WalletKeys() : TeosCommand(
        string(walletCommandPath + "list_keys"), reqJson_) {
        callEosd();
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {}.
       * @param getResponse() returns {"":"<key1>" "":"<key2>" ...}.
       */
      WalletKeys(ptree reqJson) : TeosCommand(
        string(walletCommandPath + "list_keys"), reqJson) {
        callEosd();
      }
    };

    /**
     * @brief Command-line driver for the WalletKeys class
     */
    class WalletKeysOptions : public CommandOptions
    {
    public:
      WalletKeysOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
List opened wallets, *= unlocked
Usage: ./teos wallet list [Options]
Usage: ./teos wallet list [-j '{}'] [OPTIONS]
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      TeosCommand executeCommand() {
        return WalletKeys(reqJson);
      }

      void printout(TeosCommand command, variables_map &vm) {
        ptree rcvJson = command.getResponse();
        BOOST_FOREACH(ptree::value_type &v, rcvJson)
        {
          assert(v.first.empty()); // array elements have no names
          output("wallet", "%s", v.second.data().c_str());
        }
      }

    };
  }
}