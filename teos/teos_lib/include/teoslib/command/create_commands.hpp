/**
 * @file create_commands.hpp
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
     * @ingroup teoslib_raw
     * @brief Create an account, buy ram, stake for bandwidth for the account.
     */
    class CreateAccount : public TeosCommand
    {
    public:
      /**
       * @brief Create a Account object
       * 
       * @return respJson_ transaction json
       */
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

      /**
       * @brief Create a Account object
       * 
       * @param reqJson json:
       * '{
       *    "creator":"<creator name>",
       *    "name":"<account name>",
       *    "ownerKey":"<owner public key>",
       *    "activeKey":"<active public key>",
       *    "permission":"<permission list>",
       *    "expiration":<expiration time sec>,
       *    "skip-sign":<true|false>,
       *    "dont-broadcast":<true|false>,
       *    "force-unique":<true|false>,
       *    "max-cpu-usage":"<max cpu usage>",
       *    "max-net-usage":"<max net usage>"
       * }'
       * @return respJson_ transaction json
       */
      CreateAccount(ptree reqJson) : TeosCommand("", reqJson)
      {
        copy(createAccount(
          reqJson_.get<string>("creator"), reqJson_.get<string>("name"),
          reqJson_.get<string>("ownerKey"), reqJson_.get<string>("activeKey"),
          reqJson_.get<string>("permission"), 
          reqJson_.get<int>("expiration"),          
          reqJson_.get<bool>("skip-sign"),
          reqJson_.get<bool>("dont-broadcast"),
          reqJson_.get<bool>("force-unique"),
          reqJson_.get<unsigned>("max-cpu-usage"),
          reqJson_.get<unsigned>("max-net-usage")
          ));
      }
    };

    /**
    * @ingroup teoslib_cli
    * @brief Create an account, buy ram, stake for bandwidth for the account.
    * 
    \verbatim
    Usage: ./teos create account [creator] [name] [ownerKey] [activeKey] 
    [Options]
    Usage: ./teos create key --jarg '{
    "creator":"<creator name>",
    "name":"<account name>",
    "ownerKey":"<owner public key>",
    "activeKey":"<active public key>",
    "permission":"<permission list>",
    "expiration":<expiration time sec>,
    "skip-sign":<true|false>,
    "dont-broadcast":<true|false>,
    "force-unique":<true|false>,
    "max-cpu-usage":"<max cpu usage>",
    "max-net-usage":"<max net usage>"
    }' [OPTIONS]
    
    Options:
    
    -c [ --creator ] arg                  The name of the account creating the
                                            new account
    -n [ --name ] arg                     The name of the new account
    -o [ --ownerKey ] arg                 The owner public key for the account
    -a [ --activeKey ] arg                The active public key for the account
    -p [ --permission ] arg               An account and permission level to
                                            authorize, as in 'account@permission'
                                            (defaults to 'account')
    -x [ --expiration ] arg (=30)         The time in seconds before a
                                            transaction expires.
    -s [ --skip-sign ]                    Specify that unlocked wallet keys
                                            should not be used to sign 
                                            transaction,defaults to false.
    -d [ --dont-broadcast ]               Don't broadcast transaction to the
                                            network (just print to stdout).
    -f [ --force-unique ]                 Force the transaction to be unique.
                                            this will consume extra bandwidth and
                                            remove any protections against
                                            accidentally issuing the same 
                                            transaction multiple times.
    --max-cpu-usage arg (=0)              Upper limit on the cpu usage budget, in
                                            instructions-retired, for the execution
                                            of the transaction (defaults to 0 which
                                            means no limit).
    --max-net-usage arg (=0)              Upper limit on the net usage budget, in
                                            bytes, for the transaction (defaults to
                                            0 which means no limit)
    
    -a [ --address ] arg (=127.0.0.1:8888)
                                          The http address (host:port) of the
                                            EOSIO node.
    -w [ --wallet ] arg (=127.0.0.1:8888) The http address (host:port) where
                                            eos-wallet is running.
    
    --jarg arg                            Json argument.
    --arg                                 Print argument.
    -j [ --json ]                         Print result as json.
    --both                                For system use.
    -r [ --raw ]                          Raw print
    
    -h [ --help ]                         Help screen
    -V [ --verbose ]                      Output verbose messages
    \endverbatim
    */
    class CreateAccountOptions : public CommandOptions
    {
    public:
      CreateAccountOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:

      string getTransactionUsage() {
        return string(R"(
  "permission":"<permission list>",
  "expiration":<expiration time sec>,  
  "skip-sign":<true|false>,
  "dont-broadcast":<true|false>,
  "force-unique":<true|false>,
  "max-cpu-usage":"<max cpu usage>",
  "max-net-usage":"<max net usage>"
  }' [OPTIONS]
)");            
      }

      const char* getUsage() {
        return (string( R"(
Create a new account on the blockchain.
Usage: ./teos [Options] create account creator name ownerKey 
          [activeKey] [Options]
Usage: ./teos create key --jarg '{
  "creator":"<creator name>",
  "name":"<account name>",
  "ownerKey":"<owner public key>",
  "activeKey":"<active public key>",
)") + getTransactionUsage()).c_str();
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
          ("skip-sign,s"
            , "Specify that unlocked wallet keys should not be used to sign "
            "transaction, defaults to false.")
          ("dont-broadcast,d"
            , "Don't broadcast transaction to the network "
              "(just print to stdout).")
          ("force-unique,f"
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
                reqJson_.put("permission", permission);
                reqJson_.put("expiration", expiration);        
                reqJson_.put(
                  "skip-sign", 
                  skipSignature = vm.count("skip-sign") ? true : false);
                reqJson_.put(
                  "dont-broadcast", 
                  dontBroadcast = vm.count("dont-broadcast") ? true : false);
                reqJson_.put(
                  "force-unique", 
                  forceUnique = vm.count("force-unique") ? true : false);
                reqJson_.put("max-cpu-usage", maxCpuUsage);            
                reqJson_.put("max-net-usage", maxNetUsage);                
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

      void printout(TeosControl command, variables_map &vm) {
        output("transaction id", "%s", GET_STRING(command, "transaction_id"));
      }
    };

    /**
     * @ingroup teoslib_raw
     * @brief Create a new keypair and print the public and private keys.
     */
    class CreateKey : public TeosCommand
    {
    public:
      /**
       * @brief A constructor.
       * @param keyName key-pair id.
       * @return respJson_ = json({
       *    "privateKey":"<private key>",
       *    "publicKey":"<public key>"
       * })
       */
      CreateKey(string keyName) : TeosCommand("") {
        KeyPair kp;
        respJson_.put("name", keyName);
        respJson_.put("privateKey", kp.privateKey);
        respJson_.put("publicKey", kp.publicKey);
      }

      /**
       * @brief A constructor.
       * @param reqJson a boost json tree argument: {"keyName":"<key name>"}.
       * @return respJson_ = json({ "privateKey":"<private key>", 
       * "publicKey":"<public key>"
       * })
       */
      CreateKey(ptree reqJson) : TeosCommand(
        "", reqJson) {
        KeyPair kp;
        respJson_.put("name", reqJson.get<string>("name"));
        respJson_.put("privateKey", kp.privateKey);
        respJson_.put("publicKey", kp.publicKey);
      }
    };

    /**
    * @ingroup teoslib_cli
    * @brief Create a new keypair and print the public and private keys.
    * 
    \verbatim
    Usage: ./teos create key [key name] [Options]
    Usage: ./teos create key --jarg '{"name":"<key name>"}' [OPTIONS]
    
    Options:
    
    -n [ --name ] arg (=default)          The name of the new key
    
    -a [ --address ] arg (=127.0.0.1:8888)
                                            The http address (host:port) of the
                                            EOSIO daemon.
    -w [ --wallet ] arg (=127.0.0.1:8888) The http address (host:port) where
                                            eos-wallet is running.
    
    --jarg arg                            Json argument.
    --arg                                 Print argument.
    -j [ --json ]                         Print result as json.
    --both                                For system use.
    -r [ --raw ]                          Raw print
    
    -h [ --help ]                         Help screen
    -V [ --verbose ]                      Output verbose messages
    \endverbatim
    */
    class CreateKeyOptions : public CommandOptions
    {
    public:
      CreateKeyOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"(
Create a new keypair and print the public and private keys.
Usage: ./teos create key [key name] [Options]
Usage: ./teos create key --jarg '{"name":"<key name>"}' [OPTIONS]
)";
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