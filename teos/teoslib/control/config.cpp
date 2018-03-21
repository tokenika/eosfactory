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

#define NOT_DEFINED_VALUE ""
#define EMPTY ""

    map<ConfigKeys, vector<string>> configMap =
    {
      { EOSIO_DAEMON_ADDRESS,{ "EOSIO_DAEMON_ADDRESS"
        , LOCALHOST_HTTP_ADDRESS} },
      { EOSIO_WALLET_ADDRESS,{ "EOSIO_WALLET_ADDRESS", EMPTY } },
      { GENESIS_JSON,{ "genesis-json", "resources/genesis.json" } },
      { DATA_DIR,{ "data-dir" } },
      { EOSIO_INSTALL_DIR,{ "EOSIO_INSTALL_DIR" } },
      { EOSIO_SOURCE_DIR,{ "EOSIO_SOURCE_DIR" } },
      { DAEMON_NAME,{ "DAEMON_NAME", "eosiod" } },
      { LOGOS_DIR,{ "LOGOS_DIR" } },
      { WASM_CLANG,{ "WASM_CLANG", "/home/cartman/opt/wasm/bin/clang" } },
      { WASM_LLVM_LINK,{ "WASM_LLVM_LINK"
        , "/home/cartman/opt/wasm/bin/llvm-link" } },
      { WASM_LLC,{ "WASM_LLC", "/home/cartman/opt/wasm/bin/llc" } },
      { BINARYEN_BIN,{ "BINARYEN_BIN", "/home/cartman/opt/binaryen/bin/" } },
    };

    namespace bfs = boost::filesystem;
    
    vector<string> configMapValue(ConfigKeys configKey) {
      auto it = configMap.find(configKey);
      return (it != configMap.end()) 
        ? configMap.at(configKey)
        : vector<string>({NOT_DEFINED_VALUE});
    }

    string configValue(ConfigKeys configKey, bool verbose) 
    {
      vector<string> entry = configMapValue(configKey);
      boost::property_tree::ptree json = TeosControl::getConfig(verbose);
      string value = json.get(entry[0], NOT_DEFINED_VALUE);

      if(value != NOT_DEFINED_VALUE) {
        return value;
      } else {
        char* env = getenv(entry[0].c_str());
        if(env == nullptr){
          return entry.size() > 1 ? entry[1] : NOT_DEFINED_VALUE;          
        }
        return string(env);
      } 
    }

    //////////////////////////////////////////////////////////////////////////

    void ConfigTeos::action() 
    {
      boost::property_tree::ptree config = TeosControl::getConfig();

      if(reqJson_.count(CONFIG_TEOS_ACTION) != 0)
      {
        if(reqJson_.get<string>(CONFIG_TEOS_ACTION) == CONFIG_TEOS_PATH_ACTION)
        {// Output path to the config.json:
          respJson_.put("config json file", 
            boost::filesystem::current_path() / CONFIG_JSON);
        } else if(reqJson_.get<string>(CONFIG_TEOS_ACTION) 
            == CONFIG_TEOS_RESET_ACTION)
        {// Fill the config.json with the configValue(...) data:
          config.clear();
          BOOST_FOREACH(auto &entry, configMap) 
          {
            config.put(entry.second[0], configValue(entry.first));
          }
          saveConfigJson(config);
          respJson_ = config;
        } else if(reqJson_.get<string>(CONFIG_TEOS_ACTION) 
            == CONFIG_TEOS_REVIEW_ACTION)
        {// Iterate over the configMap entries, propose changes, and save
         // everything in the config.json:
          BOOST_FOREACH(auto &entry, configMap) 
          {
            string value = configValue(entry.first);
            string newValue;
            while(true)
            {
              cout << entry.second[0] << ": " << value  << endl;
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
            config.put(entry.second[0], value);
          }
          saveConfigJson(config);
          respJson_ = config;
        }
      } else if(!reqJson_.empty())
      {//Merge the config.json with json argument.
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
        char* value = getenv(entry.second[0].c_str());
        if(value != nullptr)
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



