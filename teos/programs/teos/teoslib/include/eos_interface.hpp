#pragma once

#include <stdlib.h>
#include <string>
#include <iostream>

#include <boost/range/algorithm/sort.hpp>

#include <fc/variant.hpp>
#include <fc/io/json.hpp>
#include <eos/chain_plugin/chain_plugin.hpp>

#include <teos_command.hpp>
#include <teos_get_commands.hpp>
#include <teos_wallet_commands.hpp>

using namespace std;

namespace tokenika{ 
  namespace teos{

    class KeyPair {

    public:
      static string privateK();
      static string prk;
      string privateKey;
      string publicKey;

      KeyPair();
    };

    class CallChain : public TeosCommand
    {
      std::string requestStr;
    public:
      fc::variant fcVariant;

      bool fcaVariant2ptree(const fc::variant& postData) {
        if (!postData.is_null()) {
          requestStr = fc::json::to_string(postData);
          stringstream ss;
          ss << requestStr;
          try {
            read_json(ss, reqJson);
            stringstream ss1;
            json_parser::write_json(ss1, reqJson, false);
            return true;
          }
          catch (exception& e) {
            reqJson.put(teos_ERROR, e.what());
            return false;
          }
        }
        return true;
      }

      CallChain(std::string path, const fc::variant& postData = fc::variant()) : TeosCommand(path, true) {
        if (fcaVariant2ptree(postData)) {
          callEosd();
        }
        //std::cout << path << std::endl;
        //std::cout << requestStr << std::endl;
        //std::cout << fc::json::to_pretty_string(fcVariant) << std::endl;
        if (isError()) {
          //std::cout << toStringRcv() << std::endl;
        }
      }

      std::string normRequest(ptree &regJson) { return requestStr; }
      void normResponse(std::string response, ptree &respJson);
    };

  } 
}

tokenika::teos::CallChain createAccount(string creator, string name,
  string ownerKey, string activeKey,
  bool skipSignature, int expiration, int deposit);