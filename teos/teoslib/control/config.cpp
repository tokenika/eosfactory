#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/format.hpp>
#include <boost/foreach.hpp>
#include <boost/system/error_code.hpp>

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

vector<string> XXX = {"","fffa"};

#define NOT_DEFINED_VALUE ""
#define EMPTY ""

    enum ConfigKeys { NOT_DEFINED
        , GENESIS_JSON, EOSIO_DAEMON_ADDRESS
        , EOSIO_WALLET_ADDRESS, CONFIG_DIR, WALLET_DIR
        , EOSIO_SOURCE_DIR, DAEMON_NAME, LOGOS_DIR
        , CONTRACT_PATH
        , WASM_CLANG, WASM_LLVM_LINK, WASM_LLC, BINARYEN_BIN
    };

    

    map<ConfigKeys, vector<string>> configMap =
    {
      { EOSIO_DAEMON_ADDRESS,{ "EOSIO_DAEMON_ADDRESS"
        , LOCALHOST_HTTP_ADDRESS} },
      { EOSIO_WALLET_ADDRESS,{ "EOSIO_WALLET_ADDRESS", EMPTY } },
      { GENESIS_JSON,{ "genesis-json", "resources/genesis.json" } },
      { CONFIG_DIR,{ "config-dir" } },
      { WALLET_DIR,{ "wallet-dir" } },
      { EOSIO_SOURCE_DIR,{ "EOSIO_SOURCE_DIR" } },
      { DAEMON_NAME,{ "DAEMON_NAME", "nodeos" } },
      { LOGOS_DIR,{ "LOGOS_DIR" } },
      { CONTRACT_PATH,{ "CONTRACT_PATH" }},
      { WASM_CLANG,{ "WASM_CLANG", "/home/cartman/opt/wasm/bin/clang" } },
      { WASM_LLVM_LINK,{ "WASM_LLVM_LINK"
        , "/home/cartman/opt/wasm/bin/llvm-link" } },
      { WASM_LLC,{ "WASM_LLC", "/home/cartman/opt/wasm/bin/llc" } },
      { BINARYEN_BIN,{ "BINARYEN_BIN", "/home/cartman/opt/binaryen/bin/" } },
    };

    string configValue(ConfigKeys configKey, bool verbose = false);

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

    boost::filesystem::path getContractFile(
        string contractFile, TeosControl& teosControl)
    {
      namespace bfs = boost::filesystem;

      bfs::path contractFilePath(contractFile);
      if(bfs::exists(contractFilePath)){
        return contractFilePath;
      }

      string name = contractFilePath.stem().string();
      contractFilePath = 
        bfs::path(configValue(ConfigKeys::CONTRACT_PATH)) 
        / name / contractFile;
      if(bfs::exists(contractFilePath)){
        return contractFilePath;
      }
      
      contractFilePath = 
        bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
        / "contracts" / name / contractFile;
      if(bfs::exists(contractFilePath)){
        return contractFilePath;
      }

      contractFilePath = 
        bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
        / "build/contracts" / name / contractFile;
      if(bfs::exists(contractFilePath)){
        return contractFilePath;
      }      

      teosControl. putError("Cannot find the path to the contract file.");
      return bfs::path("");
    }    

        string getHttpServerAddress(string address)
    {
      if(!address.empty()) {
        return address;
      }

      return configValue(ConfigKeys::EOSIO_DAEMON_ADDRESS);
    }

    string getHttpWalletAddress(string address)
    {
      if(!address.empty()) {
        return address;
      }
      string walletAddress = configValue(ConfigKeys::EOSIO_WALLET_ADDRESS);
      return walletAddress.empty() 
        ? configValue(ConfigKeys::EOSIO_DAEMON_ADDRESS) : walletAddress;
    }
    

    /*
    Determines the genesis file.
    */
    boost::filesystem::path getGenesisJson(
      string genesisJson, TeosControl& teosControl)
    {
      namespace bfs = boost::filesystem;

      try{
        bfs::path wantedPath;
        
        if(!genesisJson.empty())
        {
          wantedPath = bfs::path(genesisJson);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }
        }

        {
          wantedPath = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
            / "genesis.json";
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }          
        }

        if(!bfs::exists(wantedPath)){
          teosControl.putError("Cannot determine the genesis file.");
          return bfs::path("");
        }         

      } catch (std::exception& e) {
          teosControl.putError(e.what());
          return bfs::path("");        
      }
    }

    /*
    Determines the EOS test node executable file.
    */
    boost::filesystem::path getDaemonExe(
      string daemonExe, TeosControl& teosControl)
    {
      namespace bfs = boost::filesystem;

      try{
        bfs::path wantedPath;
        
        if(!daemonExe.empty())
        {
          wantedPath = bfs::path(daemonExe);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }
        }

        {
          wantedPath 
            = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
              / "build/etc/eosio/node_00" 
              / configValue(ConfigKeys::DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }          
        }        
    
        {
          wantedPath 
            = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
              / "build/programs/" / configValue(ConfigKeys::DAEMON_NAME)
              / configValue(ConfigKeys::DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }          
        }

        {
          wantedPath = bfs::path("/usr/local/bin")
              / configValue(ConfigKeys::DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }             
        }

        if(!bfs::exists(wantedPath)){
          teosControl.putError(
            "Cannot determine the EOS test node executable file."
            );
          return bfs::path("");
        } 

      } catch (std::exception& e) {
          teosControl.putError(e.what());
          return bfs::path("");        
      }
    }

    /*
    Determines 'config-dir' configuration parameter.
    */
    boost::filesystem::path getConfigDir(
      string configDir, TeosControl& teosControl)
    {
      namespace bfs = boost::filesystem;

      try{
        bfs::path wantedPath;

        if(!configDir.empty())
        {
          wantedPath = bfs::path(configDir);
          if(bfs::is_directory(wantedPath))
          {
            if(!bfs::exists(wantedPath)) {
              bfs::create_directories(bfs::path(configDir));           
            }
            return wantedPath;            
          } else
          {
            teosControl.putError(boost::str(boost
              ::format("%1 is not a directory.") % configDir));
            return bfs::path("");
          }
        }
        
        {
          wantedPath = bfs::path(configValue(ConfigKeys::CONFIG_DIR));
          if(bfs::exists(wantedPath) && bfs::is_directory(wantedPath)){
            return wantedPath;
          }            
        }
   
        {
          wantedPath  = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
              / "build/etc/eosio/node_00";
          if(bfs::exists(wantedPath / "config.ini")){
            return wantedPath;
          }           
        }

        if(!bfs::exists(wantedPath)){
          teosControl.putError(
            "Cannot determine the path to 'config-dir' directory."
            );
          return bfs::path("");
        }         
      } catch (std::exception& e)
      {
        teosControl.putError(e.what());
        return bfs::path("");
      }
    }

    /*
    Determines 'wallet-dir' configuration parameter.
    */
    boost::filesystem::path getWalletDir(
      string walletDir, TeosControl& teosControl, string configDir)
    {
      namespace bfs = boost::filesystem;

      try{
        bfs::path configDirPath = getConfigDir(configDir, teosControl);
        bfs::path wantedPath;
        
        if(!walletDir.empty()){
          wantedPath = configDirPath / walletDir;
          boost::system::error_code ec;
          if(bfs::is_directory(wantedPath, ec))
          {
            if(!bfs::exists(wantedPath)) {
              bfs::create_directories(bfs::path(walletDir));           
            }
            return wantedPath;            
          } else
          {
            wantedPath = bfs::path(walletDir);
            if(bfs::is_directory(wantedPath, ec))
              {
                if(!bfs::exists(wantedPath)) {
                  bfs::create_directories(bfs::path(walletDir));           
                }
                return wantedPath;            
              } else
            {
              teosControl.putError(boost::str(boost
                ::format("%1 is not a directory.") % walletDir));
              return bfs::path("");              
            }
          }
        }
        
        wantedPath = bfs::path(configValue(ConfigKeys::WALLET_DIR));
        if(bfs::exists(wantedPath) && bfs::is_directory(wantedPath)) {
          return wantedPath;
        }     

        wantedPath  = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
            / "build/etc/eosio/node_00/wallet-dir";
        if(bfs::exists(wantedPath) && bfs::is_directory(wantedPath)){
          return wantedPath;
        } 

        if(!bfs::exists(wantedPath)){
          teosControl.putError(
            "Cannot determine the path to 'wallet-dir' directory."
            );
          return bfs::path("");
        }         
      } catch (std::exception& e)
      {
        teosControl.putError(e.what());
        return bfs::path("");
      }
    }

    string getDaemonName(){
      return configValue(ConfigKeys::DAEMON_NAME);
    }

    string getWASM_CLANG(){
      return configValue(ConfigKeys::WASM_CLANG);
    }

    string getWASM_LLVM_LINK(){
      return configValue(ConfigKeys::WASM_LLVM_LINK);
    }

    string getBINARYEN_BIN(){
      return configValue(ConfigKeys::BINARYEN_BIN);
    }

    string getWASM_LLC(){
      return configValue(ConfigKeys::WASM_LLC);
    }    
  }
}



