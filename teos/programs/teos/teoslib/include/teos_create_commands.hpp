#pragma once

#include <teos_config.h>

#include <teos_command.hpp>
#include <eos_interface.hpp>

using namespace std;

extern const char* createSubcommands;
extern const string createCommandPath;

namespace tokenika
{
  namespace teos
  {
    /**
    Creates a new account on the blockchain.
    */
    class CreateAccount : public TeosCommand
    {
    public:
      CreateAccount(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson, raw) {

        CallChain create = createAccount(
          reqJson.get<string>("creator"), reqJson.get<string>("name"),
          reqJson.get<string>("ownerKey"), reqJson.get<string>("activeKey"),
          reqJson.get<bool>("skip"), reqJson.get<int>("expiration"), 
          reqJson.get<int>("deposit"));
        respJson = create.getRcvJson();
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
      int deposit;


      options_description options() {
        options_description special("");
        special.add_options()
          ("creator,c", value<string>(&creator), "The name of the account creating the new account")
          ("name,n", value<string>(&name), "The name of the new account")
          ("ownerKey,o", value<string>(&ownerKey), "The owner public key for the account")
          ("activeKey,o", value<string>(&activeKey), "The active public key for the account")
          ("skip,s", value<bool>(&skip)->default_value(false),"Specify that unlocked wallet keys should not be used to sign transaction, defaults to false")
          ("expiration,x", value<int>(&expiration)->default_value(30), "The time in seconds before a transaction expires")
          ("deposit,d", value<int>(&deposit)->default_value(1), "The initial deposit");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("creator", 1);
        pos_desc.add("name", 1);
        pos_desc.add("ownerKey", 1);
        pos_desc.add("activeKey", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("creator")) {
          reqJson.put("creator", creator);
          if(vm.count("name")){
            reqJson.put("name", name);
            if (vm.count("ownerKey")) {
              reqJson.put("ownerKey", ownerKey);
              if (vm.count("activeKey")) {
                reqJson.put("activeKey", activeKey);
                reqJson.put("skip", skip);
                reqJson.put("expiration", expiration);
                reqJson.put("deposit", deposit);
                ok = true;
              }
            }
          }
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return CreateAccount(reqJson, is_raw);
      }

      void getExample() {
        cout << R"EOF(
)EOF" << endl;
      }
    };

    class CreateKey : public TeosCommand
    {
    public:
      CreateKey(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson, raw) {
        KeyPair kp;
        respJson.put("name", reqJson.get<string>("name"));
        respJson.put("privateKey", kp.privateKey);
        respJson.put("publicKey", kp.publicKey);
      }

    };

    /**
    * @brief Command-line driver for the CreateKey class
    * Extends the CommandOptions class adding features specific to the
    * 'create key' teos command.
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

      options_description options() {
        options_description special("");
        special.add_options()
          ("name,n", value<string>(&keyName)->default_value("default"),
            "The name of the new key");
        return special;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool setJson(variables_map &vm) {
        bool ok = false;
        if (vm.count("name")) {
          reqJson.put("name", keyName);
          ok = true;
        }
        return ok;
      }

      TeosCommand getCommand(bool is_raw) {
        return CreateKey(reqJson, is_raw);
      }

      void getOutput(TeosCommand command) {
        output("key name", "%s", GET_STRING(command, "name"));
        output("private key", "%s", GET_STRING(command, "privateKey"));
        output("public key", "%s", GET_STRING(command, "publicKey"));
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
reqJson.put("name", "example_key");
CreateKey createKey(reqJson);
cout << createKey.toStringRcv() << endl;

/*
printout:
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        reqJson.put("name", "example_key");
        CreateKey createKey(reqJson);
        cout << createKey.toStringRcv() << endl;

        cout << R"EOF(
*/
)EOF" << endl;
      }
    };

  }
}