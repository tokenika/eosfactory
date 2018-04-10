#pragma once

#include <vector>
#include <boost/algorithm/string.hpp>

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

      CreateAccount(
          string creator, string accountName,
          string ownerKeyPubl, string activeKeyPubl,
          string permission = "",
          unsigned expirationSec = 30, 
          bool skipSignature = false,
          bool dontBroadcast = false,
          bool forceUnique = false,
          unsigned maxCpuUsage = 0,
          unsigned maxNetUsage = 0)
      {
        copy(createAccount(
          creator, accountName,
          ownerKeyPubl, activeKeyPubl, 
          permission,          
          expirationSec,
          skipSignature, dontBroadcast, forceUnique,
          maxCpuUsage, maxNetUsage));
      }

      CreateAccount(ptree reqJson) : TeosCommand("", reqJson)
      {
        copy(createAccount(
          reqJson.get<string>("creator"), reqJson.get<string>("name"),
          reqJson.get<string>("ownerKey"), reqJson.get<string>("activeKey"),
          reqJson.get<string>("permission"), 
          reqJson.get<int>("expiration"),          
          reqJson.get<bool>("skip-sign"),
          reqJson.get<bool>("dont-broadcast"),
          reqJson.get<bool>("force-unique"),
          reqJson.get<unsigned>("max-cpu-usage"),
          reqJson.get<unsigned>("max-net-usage")
          ));
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

      string getTransactionUsage() {
        return string(R"EOF(
  "permission":"<permission list>",
  "expiration":<expiration time sec>,  
  "skip-sign":<true|false>,
  "dont-broadcast":<true|false>,
  "force-unique":<true|false>,
  "max-cpu-usage":"<max cpu usage>",
  "max-net-usage":"<max net usage>"
  }' [OPTIONS]
)EOF");            
      }

      const char* getUsage() {
        return (string( R"EOF(
Create a new account on the blockchain.
Usage: ./teos create account [creator] [name] [ownerKey] 
          [activeKey] [Options]
Usage: ./teos create key --jarg '{
  "creator":"<creator name>",
  "name":"<account name>",
  "ownerKey":"<owner public key>",
  "activeKey":"<active public key>",
)EOF") + getTransactionUsage()).c_str();
      }

      string permission;
      unsigned expiration;      
      bool skipSignature;
      bool dontBroadcast;
      bool forceUnique;
      unsigned maxCpuUsage;
      unsigned maxNetUsage;      
      
      string creator;
      string name;
      string ownerKey;
      string activeKey;

      
      options_description transactionOptions() {
        options_description od("");
        od.add_options();
        od.add_options()
        ("permission,p", value<string>(&permission)
            ->default_value("")
            ,"An account and permission level to authorize, as in "
              "'account@permission' (defaults to 'account')")
          ("expiration,x", value<unsigned>(&expiration)->default_value(30)
            , "The time in seconds before a transaction expires.")
          ("skip-sign,s", value<bool>(&skipSignature)->default_value(false)
            , "Specify that unlocked wallet keys should not be used to sign "
            "transaction, defaults to false.")
          ("dont-broadcast,d", value<bool>(&dontBroadcast)->default_value(false)
            , "Don't broadcast transaction to the network "
              "(just print to stdout).")
          ("force-unique,f", value<bool>(&forceUnique)->default_value(false)
            , "force the transaction to be unique. this will consume extra "
            "bandwidth and remove any protections against accidently issuing "
            "the same transaction multiple times.")
          ("max-cpu-usage", value<unsigned>(&maxCpuUsage)->default_value(0)
            , "Upper limit on the cpu usage budget, in instructions-retired, "
              "for the execution of the transaction (defaults to 0 which "
              "means no limit).")
          ("max-net-usage", value<unsigned>(&maxNetUsage)->default_value(0)
            ,  "Upper limit on the net usage budget, in bytes, for the "
              "transaction (defaults to 0 which means no limit)");
        return od;
      }       

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("creator,c", value<string>(&creator)
            , "The name of the account creating the new account")
          ("name,n", value<string>(&name), "The name of the new account")
          ("ownerKey,o", value<string>(&ownerKey)
            , "The owner public key for the account")
          ("activeKey,a", value<string>(&activeKey)
            , "The active public key for the account");
        od.add(transactionOptions());            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("creator", 1);
        pos_desc.add("name", 1);
        pos_desc.add("ownerKey", 1);
        pos_desc.add("activeKey", 1);
      }

      void transactionArgs(){
        reqJson_.put("permission", permission);
        reqJson_.put("expiration", expiration);                
        reqJson_.put("skip-sign", skipSignature);
        reqJson_.put("dont-broadcast", dontBroadcast);
        reqJson_.put("force-unique", forceUnique);
        reqJson_.put("max-cpu-usage", maxCpuUsage);            
        reqJson_.put("max-net-usage", maxNetUsage);
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
                ok = true;
              }
            }
          }
        }
        transactionArgs();        
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
Usage: ./teos create key --jarg '{"name":"<key name>"}' [OPTIONS]
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

      void printout(TeosControl command, variables_map &vm) {
        output("key name", "%s", GET_STRING(command, "name"));
        output("private key", "%s", GET_STRING(command, "privateKey"));
        output("public key", "%s", GET_STRING(command, "publicKey"));
      }

    };

  }
}