#pragma once

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>

#include <boost/property_tree/json_parser.hpp>

#include <teos_config.h>
#include <teos_command.hpp>

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

extern const char* walletSubcommands;
extern const string walletCommandPath;

namespace tokenika
{
  namespace teos
  {
    /**
     * @brief Create a new wallet locally
     * 
     */
    class WalletCreate : public TeosCommand
    {
    public:

      WalletCreate(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "create"), reqJson, raw) {
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
     * Extends the CommandOptions class adding features specific to the
     * 'wallet create' teos command.
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

      string walletName;

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n", value<string>(&walletName)->default_value("default"), 
            "The name of the new wallet");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", walletName);
          ok = true;
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletCreate(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("password", "%s", GET_STRING(command, "password"));
        output("You need to save this password to be able to lock/unlock the wallet!");
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
ptree config = TeosCommand::getConfig();
reqJson.put("name", config.get("teos.tokenikaWallet", TOKENIKA_WALLET));
WalletCreate walletCreate(reqJson);
cout << walletCreate.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        ptree config = TeosCommand::getConfig();
        reqJson.put("name", config.get("teos.tokenikaWallet", TOKENIKA_WALLET));
        WalletCreate walletCreate(reqJson);
        cout << walletCreate.toStringRcv() << endl;

        cout << R"EOF(
*/
)EOF" << endl;
      }
    };

    /**
     * @brief Import private key into wallet
     * 
     */
    class WalletImport : public TeosCommand
    {
    public:

      WalletImport(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "import_key"), reqJson, raw) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("[\"") + reqJson.get<string>("name") + "\",\"" + reqJson.get<string>("key") + "\"]";
      }

      void normResponse(string response, ptree &respJson) {}
    };

    /**
     * @brief Command-line driver for the WalletImport class
     * Extends the CommandOptions class adding features specific to the
     * 'wallet import' teos command.
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
Usage: ./teos wallet import [walet name] [key] [Options]
Usage: ./teos wallet import [-j '{"name":"<name>", "key":"private key"}'] [OPTIONS]
)EOF";
      }

      string walletName;
      string key;

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n", value<string>(&walletName), 
            "The name of the wallet to import key into")
          ("key,k", value<string>(&key), "Private key in WIF format to import");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1).add("key", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", walletName);
          if (vm.count("key")) {
            reqJson.put("key", key);
            ok = true;
          }
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletImport(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("wallet", "%s", walletName.c_str());
        output("key imported", "%s", key.c_str());
      }

      void getExample() {
        output("Not available yet.");
      }
    };

    /**
    * @brief List opened wallets, *= unlocked
    *wallets
    */
    class WalletList : public TeosCommand
    {
    public:

      WalletList(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "list_wallets"), reqJson, raw) {
        callEosd();
      }
    };

    /**
     * @brief Command-line driver for the WalletList class
     * Extends the CommandOptions class adding features specific to the
     * 'wallet list' teos command.
     * 
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

      bool setJson(variables_map &vm) {
        //reqJson.put(NSON, NSON);
        return true;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletList(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        ptree rcvJson = command.getRcvJson();
        BOOST_FOREACH(ptree::value_type &v, rcvJson)
        {
          assert(v.first.empty()); // array elements have no names
          output("wallet", "%s", v.second.data().c_str());
        }
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
WalletList walletList(reqJson);
cout << walletList.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        WalletList walletList(reqJson);
        cout << walletList.toStringRcv() << endl;

        cout << R"EOF(
*/      
)EOF" << endl;
}

    };

    /**
    * @brief Open an existing wallet.
    */
    class WalletOpen : public TeosCommand
    {
    public:

      WalletOpen(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "open"), reqJson, raw) {
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
Usage: ./teos wallet open [wallet name] [Options]
Usage: ./teos wallet open [-j '{"name":"<name>"}'] [OPTIONS]
)EOF";
      }

      string walletName;

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n", value<string>(&walletName), "The name of the wallet to open");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", walletName);
            ok = true;
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletOpen(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("wallet opened", "%s", walletName.c_str());
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
ptree config = TeosCommand::getConfig();
reqJson.put("name", config.get("teos.tokenikaWallet", TOKENIKA_WALLET));
WalletOpen walletOpen(reqJson);
cout << walletOpen.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        ptree config = TeosCommand::getConfig();
        reqJson.put("name", config.get("teos.tokenikaWallet", TOKENIKA_WALLET));
        WalletOpen walletOpen(reqJson);
        cout << walletOpen.toStringRcv() << endl;

        cout << R"EOF(
*/
)EOF" << endl;
      }
    };

    /**
    * @brief Lock wallet
    */
    class WalletLock : public TeosCommand
    {
    public:

      WalletLock(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "lock"), reqJson, raw) {
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
    class WalletLockOptions : public CommandOptions
    {
    public:
      WalletLockOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Lock wallet
Usage: ./teos wallet lock [wallet name] [Options]
Usage: ./teos wallet lock [-j '{"name":"<name>"}'] [OPTIONS]
)EOF";
      }

      string walletName;

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n", value<string>(&walletName), "The name of the wallet to lock");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", walletName);
          ok = true;
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletLock(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("wallet lock", "%s", walletName.c_str());
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
ptree config = TeosCommand::getConfig();
reqJson.put("name", config.get("teos.tokenikaWallet", TOKENIKA_WALLET));
WalletLock walletLock(reqJson);
cout << walletLock.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        ptree config = TeosCommand::getConfig();
        reqJson.put("name", config.get("teos.tokenikaWallet", TOKENIKA_WALLET));
        WalletLock walletLock(reqJson);
        cout << walletLock.toStringRcv() << endl;

        cout << R"EOF(
*/
)EOF" << endl;
      }
    };

    /**
    * @brief Lock all unlocked wallets
    */
    class WalletLockAll : public TeosCommand
    {
    public:

      WalletLockAll(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "lock_all"), reqJson, raw) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("");
      }

      void normResponse(string response, ptree &respJson) {}

    };

    /**
    * @brief Command-line driver for the WalletLockAll class
    * Extends the CommandOptions class adding features specific to the
    * 'wallet open_all' teos command.
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
Usage: ./teos wallet lock_all [wallet name] [Options]
Usage: ./teos wallet lock_all [-j '{}'] [OPTIONS]
)EOF";
      }

      bool setJson(variables_map &vm) {
        return true;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletLockAll(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("wallets lock", "%s", "all");
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
WalletLockAll walletLock(reqJson);
cout << walletLock.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        WalletLockAll walletLock(reqJson);
        cout << walletLock.toStringRcv() << endl;

        cout << R"EOF(
*/
)EOF" << endl;
      }
    };

    /**
    * @brief Unlock wallet
    *
    */
    class WalletUnlock : public TeosCommand
    {
    public:

      WalletUnlock(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "unlock"), reqJson, raw) {
        callEosd();
      }

      string normRequest(ptree& reqJson) {
        return string("[\"") + reqJson.get<string>("name") + "\",\"" + reqJson.get<string>("password") + "\"]";
      }

      void normResponse(string response, ptree &respJson) {}
    };

    /**
    * @brief Command-line driver for the WalletUnlock class
    * Extends the CommandOptions class adding features specific to the
    * 'wallet import' teos command.
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
Usage: ./teos wallet import [walet name] [password] [Options]
Usage: ./teos wallet import [-j '{"name":"<wallet name>"}'] [OPTIONS]
)EOF";
      }

      string walletName;
      string password;

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n", value<string>(&walletName), "The name of the wallet to import key into")
          ("password", value<string>(&password), "Private key in WIF format to import");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1).add("password", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", walletName);
          if (vm.count("password")) {
            reqJson.put("password", password);
            ok = true;
          }
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletUnlock(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("wallet unlocked", "%s", walletName.c_str());
      }

      void getExample() {
        output("Not available yet.");
      }
    };

    /**
    * @brief List opened wallets, *= unlocked
    *
    */
    class WalletKeys : public TeosCommand
    {
    public:

      WalletKeys(ptree reqJson, bool raw = false) : TeosCommand(
        string(walletCommandPath + "list_keys"), reqJson, raw) {
        callEosd();
      }
    };

    /**
     * @brief Command-line driver for the WalletKeys class
     * Extends the CommandOptions class adding features specific to the
     * 'wallet keys' teos command.
     * 
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

      bool setJson(variables_map &vm) {
        //reqJson.put(NSON, NSON);
        return true;
      }

      TeosCommand getCommand(bool is_raw) {
        return WalletKeys(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        ptree rcvJson = command.getRcvJson();
        BOOST_FOREACH(ptree::value_type &v, rcvJson)
        {
          assert(v.first.empty()); // array elements have no names
          output("wallet", "%s", v.second.data().c_str());
        }
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
WalletKeys walletKeys(reqJson);
cout << walletKeys.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        WalletKeys walletKeys(reqJson);
        cout << walletKeys.toStringRcv() << endl;

        cout << R"EOF(
*/
)EOF" << endl;
      }
    };
  }
}