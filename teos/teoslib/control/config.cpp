#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/filesystem.hpp>
#include <boost/format.hpp>
#include <boost/foreach.hpp>

#include <teoslib/config.h>
#include <teoslib/control/config.hpp>

#define _CRT_SECURE_NO_WARNINGS

using namespace std;

void saveConfigJson(boost::property_tree::ptree json){
  try {
    write_json(CONFIG_JSON, json);
  }
  catch (exception& e) {
    cerr << e.what() << endl;
  }
}

namespace teos {
  namespace control {

    map<ConfigKeys, vector<string>> configMap =
    {
      { NOT_DEFINED,{ "not_defined", "not_defined" } },
      { GENESIS_JSON,{ "genesis-json", "resources/genesis.json" } },
      { HTTP_SERVER_ADDRESS,{ "http-server-address", "127.0.0.1:8888" } },
      { HTTP_SERVER_WALLET_ADDRESS,{ "http-server-wallet-address", "127.0.0.1:8888" } },
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
      boost::property_tree::ptree ConfigTeos = TeosControl::getConfig();
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

    //////////////////////////////////////////////////////////////////////////

    void ConfigTeos::action() 
    {
      boost::property_tree::ptree config = TeosControl::getConfig();

      if(reqJson_.count(CONFIG_TEOS_ACTION) != 0)
      {
        if(reqJson_.get<string>(CONFIG_TEOS_ACTION) == CONFIG_TEOS_PATH_ACTION)
        {
          respJson_.put("config json file", 
            boost::filesystem::current_path() / CONFIG_JSON);
        } else if(reqJson_.get<string>(CONFIG_TEOS_ACTION) 
            == CONFIG_TEOS_RESET_ACTION)
        {
          config.clear();
          for(map<ConfigKeys, vector<string>>::iterator 
          entry = configMap.begin(); entry != configMap.end(); ++entry) {
            config.put(entry->second[0], configValue(entry->first));
          }
          saveConfigJson(config);
          respJson_ = config;
        } else if(reqJson_.get<string>(CONFIG_TEOS_ACTION) 
            == CONFIG_TEOS_REVIEW_ACTION)
        {
          for(map<ConfigKeys, vector<string>>::iterator 
            entry = configMap.begin(); entry != configMap.end(); ++entry) 
            {
              string value = configValue(entry->first);
              string newValue;
              while(true)
              {
                if(entry->first == ConfigKeys::NOT_DEFINED){
                  break;
                }
                cout << entry->second[0] << ": " << value  << endl;
                cout << "Enter a new value, or 'y' to confirm, 'yy' to escape."
                  << endl;
                cin >> newValue;
                if(newValue == "y" || newValue == "yy") {
                  break;
                } else {
                  value = newValue;
                }
              }
              if(newValue == "yy"){
                break;
              }
              config.put(entry->second[0], value);
            }
            saveConfigJson(config);
            respJson_ = config;
          }
      } else 
      {
        BOOST_FOREACH(auto& update, reqJson_) {
          config.put_child(update.first, update.second);
        }
        saveConfigJson(config);
        respJson_ = config;
      }

        
    }

    void ConfigTeosOptions::printout(TeosControl command, variables_map &vm  )
    {
      if(reqJson_.count(CONFIG_TEOS_ACTION) != 0)
      {
        if(reqJson_.get<string>(CONFIG_TEOS_ACTION) == CONFIG_TEOS_PATH_ACTION)
        {
          sharp() << "Config file is: " 
            << (boost::filesystem::current_path() / CONFIG_JSON).string() << endl;
          return;
        }
        return;
      }

      boost::filesystem::path configJsonPath
        = boost::filesystem::current_path() / CONFIG_JSON;
      ptree config = TeosControl::getConfig();
      
      if (config.empty()) {
        sharp() << "A config file is expected to be:" << endl;
        sharp() << configJsonPath.string() << endl;
        sharp() << "None is there." << endl;
      }

      sharp() << "## Environmental variables:" << endl;
      for (const auto &entry : configMap) {
        string value = getEnv(entry.first);
        if(value != configMapValue(ConfigKeys::NOT_DEFINED)[0])
        sharp() << entry.second[0] << ": " << value << endl;
      }
      sharp() <<  endl;

      sharp() << "## Definitions in the config json file, "
        "which is expected to be " << endl;
      sharp() << "   " << configJsonPath.string() << endl;
      sharp() << "overcome the environmental ones." << endl;

      sharp() <<  endl;
      sharp() << "## Resulting configuration is:" << endl;
      for (const auto &entry : configMap) {
        sharp() << entry.second[0] << ": " << configValue(entry.first)  
          << endl;
      }
    }
  }
}



