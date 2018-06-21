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
       * 
       * See the description of the CreateAccountOptions class for meaning of
       * the parameters.
       * 
       * @return respJson_ object member kips EOSIO node's response.
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
        // copy(createAccount(
        //   creator, accountName,
        //   ownerKeyPubl, activeKeyPubl, 
        //   permission,          
        //   expirationSec,
        //   skipSignature, dontBroadcast, forceUnique,
        //   maxCpuUsage, maxNetUsage));
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
       * 
       * See the description of the CreateAccountOptions class for meaning of
       * the parameters.
       * 
       * @return respJson_ object member kips EOSIO node's response.
       */
      CreateAccount(ptree reqJson) : TeosCommand("", reqJson)
      {
        // copy(createAccount(
        //   reqJson_.get<string>("creator"), reqJson_.get<string>("name"),
        //   reqJson_.get<string>("ownerKey"), reqJson_.get<string>("activeKey"),
        //   reqJson_.get<string>("permission"), 
        //   reqJson_.get<int>("expiration"),          
        //   reqJson_.get<bool>("skip-sign"),
        //   reqJson_.get<bool>("dont-broadcast"),
        //   reqJson_.get<bool>("force-unique"),
        //   reqJson_.get<unsigned>("max-cpu-usage"),
        //   reqJson_.get<unsigned>("max-net-usage")
        //   ));
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
       *       
       * See the description of the CreateAccountOptions class for meaning of
       * the parameters.
       * 
       * @return respJson_  object member is json({ "privateKey":"<private key>", 
       * "publicKey":"<public key>"
       */
      CreateKey(string keyName) : TeosCommand("") {
        // KeyPair kp;
        // respJson_.put("name", keyName);
        // respJson_.put("privateKey", kp.privateKey);
        // respJson_.put("publicKey", kp.publicKey);
      }

      /**
       * @brief A constructor.
       * @param reqJson a boost json tree argument: {"keyName":"<key name>"}.
       *       
       * See the description of the CreateAccountOptions class for meaning of
       * the parameters.
       * 
       * @return respJson_  object member is json({ "privateKey":"<private key>", 
       * "publicKey":"<public key>"
       * })
       */
      CreateKey(ptree reqJson) : TeosCommand(
        "", reqJson) {
        // KeyPair kp;
        // respJson_.put("name", reqJson.get<string>("name"));
        // respJson_.put("privateKey", kp.privateKey);
        // respJson_.put("publicKey", kp.publicKey);
      }
    };
  }
}