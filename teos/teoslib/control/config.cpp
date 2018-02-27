
#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/filesystem.hpp>

#include <teoslib/config.h>
#include <teos/control/config.hpp>
#include <teos/item.hpp>

#define _CRT_SECURE_NO_WARNINGS

using namespace std;

boost::property_tree::ptree getConfigJson()
{
  boost::property_tree::ptree json;
  try {
    read_json(CONFIG_JSON, json);
  }
  catch (...) {
  }
  return json;
}

namespace teos {
  namespace config {

    map<ConfigKeys, vector<string>> configMap =
    {
      { NOT_DEFINED,{ "not_defined", "not_defined" } },
      { GENESIS_JSON,{ "genesis-json", "resources/genesis.json" } },
      { HTTP_SERVER_ADDRESS,{ "http-server-address", "127.0.0.1:8888" } },
      { DATA_DIR,{ "data-dir", "workdir/data-dir" } },
      { EOSIO_INSTALL_DIR,{ "EOSIO_INSTALL_DIR" } },
      { EOSIO_GIT_DIR,{ "EOSIO_GIT_DIR" } },
      { CHAIN_NODE,{ "CHAIN_NODE", "eosiod" } },
      { PENTAGON_DIR,{ "PENTAGON_DIR" } },
      { WASM_CLANG,{ "WASM_CLANG", "/home/cartman/opt/wasm/bin/clang" } },
      { WASM_LLVM_LINK,{ "WASM_LLVM_LINK", "/home/cartman/opt/wasm/bin/llvm-link" } },
      { WASM_LLC,{ "WASM_LLC", "/home/cartman/opt/wasm/bin/llc" } },
      { BINARYEN_BIN,{ "BINARYEN_BIN", "/home/cartman/opt/binaryen/bin/" } },
    };

    namespace bfs = boost::filesystem;

    vector<string> configMapValue(ConfigKeys configKey) {
      auto it = configMap.find(configKey);
      return (it != configMap.end()) ? configMap.at(configKey)
        : configMapValue(ConfigKeys::NOT_DEFINED);
    }

    string getEnv(ConfigKeys configKey) {
      vector<string> temp = configMapValue(configKey);
      return getenv(temp[0].c_str()) == 0 ? configMapValue(ConfigKeys::NOT_DEFINED)[0]
        : getenv(temp[0].c_str());
    }

    string getJson(ConfigKeys configKey) {
      vector<string> temp = configMapValue(configKey);
      boost::property_tree::ptree configJson = getConfigJson();
      return configJson.get(temp[0], temp[1]);
    }

    string configValue(ConfigKeys configKey) {
      string temp = getJson(configKey);
      if (temp != configMapValue(ConfigKeys::NOT_DEFINED)[0]) {
        return temp;
      }
      return getEnv(configKey);
    }

    teos::config::ConfigJson::ConfigJson()
    {
      try {
        boost::property_tree::ptree config = getConfigJson();
        boost::property_tree::write_json(cout, config);
      }
      catch (std::exception& e) {
        isError_ = true;
        errorMsg(e.what());
      }
    }

  }
}//namespace pentagon



