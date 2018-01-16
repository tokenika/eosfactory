#pragma once

#include <teos_helper.hpp>
#include "../teos_config.h"
#include "teos_command.hpp"

using namespace std;

extern const char* createSubcommands;
extern const string createCommandPath;

namespace tokenika
{
  namespace teos
  {
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
#ifdef WIN32
        return R"EOF(
Create a new keypair and print the public and private keys.
Usage: ./teos create key [key name] [Options]
Usage: ./teos create key [-j "{"""name""":"""key_name"""}"] [OPTIONS]
)EOF";
#else
        return R"EOF(
Create a new keypair and print the public and private keys.
Usage: ./teos create key [key name] [Options]
Usage: ./teos create key [-j '{"name":"key_name"}'] [OPTIONS]
)EOF";
#endif
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