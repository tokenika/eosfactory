#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/filesystem.hpp>
#include <boost/format.hpp>

#include <teoslib/config.h>
#include <teos/control/config.hpp>
#include <teos/item.hpp>

#define _CRT_SECURE_NO_WARNINGS

using namespace std;

boost::filesystem::path getConfigFilePath(){
  return boost::filesystem::canonical(
    boost::filesystem::path(CONFIG_JSON));
}

boost::property_tree::ptree getConfigJson()
{
  boost::property_tree::ptree json;
  try {
    read_json(getConfigFilePath().string(), json);
  }
  catch (exception& e) {
    //cout << e.what() << endl;
  }
  return json;
}

void saveConfigJson(boost::property_tree::ptree json){
  try {
    write_json(getConfigFilePath().string(), json);
  }
  catch (exception& e) {
    cerr << e.what() << endl;
  }
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
      { EOSIO_SOURCE_DIR,{ "EOSIO_SOURCE_DIR" } },
      { DAEMON_NAME,{ "DAEMON_NAME", "eosiod" } },
      { LOGOS_DIR,{ "LOGOS_DIR" } },
      { WASM_CLANG,{ "WASM_CLANG", "/home/cartman/opt/wasm/bin/clang" } },
      { WASM_LLVM_LINK,{ "WASM_LLVM_LINK", "/home/cartman/opt/wasm/bin/llvm-link" } },
      { WASM_LLC,{ "WASM_LLC", "/home/cartman/opt/wasm/bin/llc" } },
      { BINARYEN_BIN,{ "BINARYEN_BIN", "/home/cartman/opt/binaryen/bin/" } },
    };

    namespace bfs = boost::filesystem;

    vector<string> configMapValue(ConfigKeys configKey) {
      auto it = configMap.find(configKey);
      return (it != configMap.end()) 
        ? configMap.at(configKey)
        : configMapValue(ConfigKeys::NOT_DEFINED);
    }

    string getEnv(ConfigKeys configKey) {
      vector<string> temp = configMapValue(configKey);
      return getenv(temp[0].c_str()) == 0 
        ? configMapValue(ConfigKeys::NOT_DEFINED)[0]
        : getenv(temp[0].c_str());
    }

    string getJson(ConfigKeys configKey) {
      vector<string> temp = configMapValue(configKey);
      boost::property_tree::ptree ConfigTeos = getConfigJson();
      return ConfigTeos.get(temp[0], temp.size() > 1 
        ? temp[1]
        : configMapValue(ConfigKeys::NOT_DEFINED)[0]);
    }

    string configValue(ConfigKeys configKey) {
      string temp = getJson(configKey);
      if (temp != configMapValue(ConfigKeys::NOT_DEFINED)[0]) {
        return temp;
      }
      return getEnv(configKey);
    }

    ostream& sharp() {
      cout << "#  ";
      return cout;
    }

    ConfigTeos::ConfigTeos(){
      boost::property_tree::ptree config = getConfigJson();

      for(map<ConfigKeys, vector<string>>::iterator 
        entry = configMap.begin(); entry != configMap.end(); ++entry) 
        {
          string value = configValue(entry->first);
          while(true)
          {
            if(entry->first == ConfigKeys::NOT_DEFINED){
              break;
            }
            cout << entry->second[0] << ": " << value  << endl;
            cout << "Enter a new value, or 'y' to confirm, 'yy' to escape."
              << endl;
            string newValue;
            cin >> newValue;
            if(newValue == "yy"){
              entry = configMap.end();
              break;
            }
            if(newValue == "y") {
              break;
            } else {
              value = newValue;
            }
          }
          config.put(entry->second[0], value);
        }
        saveConfigJson(config);
        cout << "Config file is:\n" << getConfigFilePath().string() << endl;
    }

    void ConfigTeosOptions::printout(ConfigTeos command, variables_map &vm)
    {
      string header = "#  ";
      boost::filesystem::path configJsonPath
        = boost::filesystem::current_path() / CONFIG_JSON;

      boost::property_tree::ptree config = getConfigJson();
      if (config.empty()) {
        sharp() << "A config file is expected to be:" << endl;
        sharp() << configJsonPath.string() << endl;
        sharp() << "None is there." << endl;
      }

      sharp() << "Environmental variables:" << endl;
      for (const auto &entry : configMap) {
        string value = getEnv(entry.first);
        if(value != configMapValue(ConfigKeys::NOT_DEFINED)[0])
        sharp() << entry.second[0] << ": " << value << endl;
      }
      sharp() <<  endl;

      sharp() << "Definitions in the config json file, which is expected to be " << endl;
      sharp() << configJsonPath.string() << endl;
      sharp() << "beat the environmental ones." << endl;

      sharp() <<  endl;
      sharp() << "Resulting configuration is:" << endl;
      for (const auto &entry : configMap) {
        sharp() << entry.second[0] << ": " << configValue(entry.first)  << endl;
      }
    }

  }
}//namespace pentagon



