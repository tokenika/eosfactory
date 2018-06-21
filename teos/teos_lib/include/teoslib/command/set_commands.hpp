/**
 * @file set_commands.hpp
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

#include <teoslib/config.h>
#include <teoslib/command.hpp>

using namespace std;

extern const char* setSubcommands;
extern const string setCommandPath;

namespace teos
{
  namespace command
  {
    /**
     * @ingroup teoslib_raw
     * @brief Create or update the contract on an account.
     * 
     */
    class SetContract : public TeosCommand
    {
    public:
      SetContract(
          string accountName,
          string contractDir,
          string wastFile = "", string abiFile = "",
          string permission  = "",
          unsigned expiration = 30,
          bool skipSignature = false,
          bool dontBroadcast = false,
          bool forceUnique = false,
          unsigned maxCpuUsage = 0,
          unsigned maxNetUsage = 0)
      {
        // copy(setContract(
        //   accountName, contractDir, wastFile, abiFile, permission, 
        //   expiration, skipSignature, dontBroadcast, forceUnique,
        //   maxCpuUsage, maxNetUsage));

        reqJson_.put("wast-file", wastFile);
        reqJson_.put("abi-file", abiFile);
      }

      SetContract(ptree reqJson) : TeosCommand("", reqJson)
      {
        string wastFile = reqJson.get<string>("wast-file");
        string abiFile = reqJson.get<string>("abi-file");
        // copy(setContract(
        //   reqJson.get<string>("account"),
        //   reqJson.get<string>("contract-dir"),
        //   wastFile, abiFile,
        //   reqJson.get<string>("permission"),
        //   reqJson.get<unsigned>("expiration"),
        //   reqJson.get<bool>("skip-sign"),
        //   reqJson.get<bool>("dont-broadcast"),
        //   reqJson.get<bool>("force-unique"),
        //   reqJson.get<unsigned>("max-cpu-usage"),
        //   reqJson.get<unsigned>("max-net-usage")
        //   ));
        
        reqJson_.put("wast-file", wastFile);
        reqJson_.put("abi-file", abiFile);
      }
    };
  }
}