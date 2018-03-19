#pragma once

#include <teoslib/config.h>
#include <teoslib/eos_interface.hpp>
#include <teoslib/command.hpp>

using namespace std;

extern const char* createSubcommands;
extern const string createCommandPath;

namespace teos
{
  namespace command
  {
    /**
    Creates a new account on the blockchain.
    */
    class CreateAccount : public TeosCommand
    {
    public:
      /**
       * @brief A constructor.
       * @param creator authorising account name.
       * @param accountName new account name.
       * @param ownerKeyPubl 'owner' public key.
       * @param activeKeyPubl 'active' public key.
       * @param skip if true, unlocked wallet keys should not be used to sign transaction.
       * @param expirationSec time in seconds before a transaction expires.
       * @param depositEos initial deposit.
       * @param raw if true, resulting json is not formated.
       * @param getResponse() returns a push-transaction json.
      */
      CreateAccount(string creator, string accountName,
        string ownerKeyPubl, string activeKeyPubl, uint64_t depositEos = 1,
        bool skip = false, int expirationSec = 30,
        bool raw = false) : TeosCommand("")
      {
        copy(createAccount(
          creator, accountName,
          ownerKeyPubl, activeKeyPubl, depositEos,
          skip, expirationSec));
      }

      /**
       * @brief A constructor.
       * @param reqJson json tree argument: {"creator":"<creator name>" "name":"<account name>"
       * "ownerKey":"<owner public key>" "activeKey":"<active public key>"
       * "skip":<false|true> "expiration":<int> "deposit":<int>}.
       * @param getResponse() returns a push-transaction json.
      */
      CreateAccount(ptree reqJson) : TeosCommand("", reqJson)
      {
        copy(createAccount(
          reqJson.get<string>("creator"), reqJson.get<string>("name"),
          reqJson.get<string>("ownerKey"), reqJson.get<string>("activeKey"),
          reqJson.get<uint64_t>("deposit"),
          reqJson.get<bool>("skip"), reqJson.get<int>("expiration")));
      }
    };

    /**
    * @brief Command-line driver for the CreateAccount class.
    */
    class CreateAccountOptions : public CommandOptions
    {
    public:
      CreateAccountOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Create a new account on the blockchain.
Usage: ./teos create account [creator] [name] [ownerKey] [activeKey] [Options]
Usage: ./teos create key [-j '{
  "creator":"<creator name>"
  "name":"<account name>"
  "ownerKey":"<owner public key>"
  "activeKey":"<active public key>"
  "skipSignature":<true|false>
  "expiration":<expiration time sec>
  "deposit":<initial deposit EOS>
  }'] [OPTIONS]
)EOF";
      }

      string creator;
      string name;
      string ownerKey;
      string activeKey;
      bool skip;
      int expiration;
      uint64_t deposit;


      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("creator,c", value<string>(&creator), "The name of the account creating the new account")
          ("name,n", value<string>(&name), "The name of the new account")
          ("ownerKey,o", value<string>(&ownerKey), "The owner public key for the account")
          ("activeKey,o", value<string>(&activeKey), "The active public key for the account")
          ("skip,s", value<bool>(&skip)->default_value(false), "Specify that unlocked wallet keys should not be used to sign transaction, defaults to false")
          ("expiration,x", value<int>(&expiration)->default_value(30), "The time in seconds before a transaction expires")
          ("deposit,d", value<uint64_t>(&deposit)->default_value(1), "The initial deposit");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("creator", 1);
        pos_desc.add("name", 1);
        pos_desc.add("ownerKey", 1);
        pos_desc.add("activeKey", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("creator")) {
          reqJson_.put("creator", creator);
          if (vm.count("name")) {
            reqJson_.put("name", name);
            if (vm.count("ownerKey")) {
              reqJson_.put("ownerKey", ownerKey);
              if (vm.count("activeKey")) {
                reqJson_.put("activeKey", activeKey);
                reqJson_.put("skip", skip);
                reqJson_.put("expiration", expiration);
                reqJson_.put("deposit", deposit);
                ok = true;
              }
            }
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return CreateAccount(reqJson_);
      }

      void getExample() {
        cout << R"EOF(
)EOF" << endl;
      }
    };

    /**
     * @brief Create a new keypair and print the public and private keys.
     */
    class CreateKey : public TeosCommand
    {
    public:
      /**
       * @brief A constructor.
       * @param keyName key-pair id.
       * @param getResponse() returns {"keyName":"<key name"
       * "privateKey":"<private key>" "publicKey":"<public key>"}.
       */
      CreateKey(string keyName, bool raw = false) : TeosCommand("") {
        KeyPair kp;
        respJson_.put("name", keyName);
        respJson_.put("privateKey", kp.privateKey);
        respJson_.put("publicKey", kp.publicKey);
      }

      /**
       * @brief A constructor.
       * @param reqJson a boost json tree argument: {"keyName":"<key name>"}.
       * @param getResponse() returns {"keyName":"<key name"
       * "privateKey":"<private key>" "publicKey":"<public key>"}.
       */
      CreateKey(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson) {
        KeyPair kp;
        respJson_.put("name", reqJson.get<string>("name"));
        respJson_.put("privateKey", kp.privateKey);
        respJson_.put("publicKey", kp.publicKey);
      }
    };

    /**
    * @brief Command-line driver for the CreateKey class
    */
    class CreateKeyOptions : public CommandOptions
    {
    public:
      CreateKeyOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Create a new keypair and print the public and private keys.
Usage: ./teos create key [key name] [Options]
Usage: ./teos create key [-j '{"name":"<key name>"}'] [OPTIONS]
)EOF";
      }

      string keyName;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&keyName)->default_value("default"),
            "The name of the new key");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson_.put("name", keyName);
          ok = true;
        }
        return ok;
      }

      TeosControl executeCommand() {
        return CreateKey(reqJson_);
      }

      void printout(TeosCommand command, variables_map &vm) {
        output("key name", "%s", GET_STRING(command, "name"));
        output("private key", "%s", GET_STRING(command, "privateKey"));
        output("public key", "%s", GET_STRING(command, "publicKey"));
      }

    };

  }
}