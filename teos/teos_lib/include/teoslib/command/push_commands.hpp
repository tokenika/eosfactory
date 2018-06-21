/**
 * @file push_commands.hpp
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

extern const char* pushSubcommands;

namespace teos
{
  namespace command
  {
    /**
     * @ingroup teoslib_raw
     * @brief Push a transaction with a single message
     * 
     */
    class PushAction : public TeosCommand
    {
    public:
      PushAction(
          string CONTRACT_NAME, string action, string data,
          string permission = "",
          unsigned expirationSec = 30, 
          bool skipSignature = false,
          bool dontBroadcast = false,
          bool forceUnique = false,
          unsigned maxCpuUsage = 0,
          unsigned maxNetUsage = 0)
      {
        // copy(pushAction(
        //   CONTRACT_NAME, action, data,
        //   permission,          
        //   expirationSec,
        //   skipSignature, dontBroadcast, forceUnique,
        //   maxCpuUsage, maxNetUsage));
      }

      PushAction(ptree reqJson) : TeosCommand("", reqJson)
      {
        // copy(pushAction(
        //   reqJson_.get<string>("contract"), 
        //   reqJson_.get<string>("action"), 
        //   reqJson_.get<string>("data"),
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

  }
}