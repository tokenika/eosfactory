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

#define NOT_DEFINED_VALUE ""
  #define EMPTY ""
    typedef vector<string> arg;

/*
  --genesis-json arg (="genesis.json")  File to read Genesis State from
  --resync-blockchain                   clear chain database and block log
  --http-server-address arg (=127.0.0.1:8888)
                                        The local IP and port to listen for
                                        incoming http connections.
  --wallet-dir arg (=".")               The path of the wallet files (absolute
                                        path or relative to application data
                                        dir)

  -d [ --data-dir ] arg                 Directory containing program runtime
                                        data
  --config-dir arg                      Directory containing configuration
                                        files such as config.ini
  -c [ --config ] arg (="config.ini")   Configuration file name relative to
                                        config-dir

daemon_exe: 

config-dir: E:\Workspaces\EOS\eos\build\etc\eosio\node_00/
E:\Workspaces\EOS\eos\build\etc\eosio\node_00/config.ini
E:\Workspaces\EOS\eos\build\etc\eosio\node_00/genesis.json

data-dir: E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00/
E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00\blocks
E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00\shared_mem

wallet-dir: .
E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00/default.wallet

*/   

    arg EOSIO_SOURCE_DIR = { "EOSIO_SOURCE_DIR" };
    arg EOSIO_DAEMON_ADDRESS = { "EOSIO_DAEMON_ADDRESS"
        , LOCALHOST_HTTP_ADDRESS };
    arg EOSIO_WALLET_ADDRESS = { "EOSIO_WALLET_ADDRESS", EMPTY };
    arg GENESIS_JSON = { "genesis-json", "resources/genesis.json" };
    arg CONFIG_DIR = { "config-dir" };
    arg WALLET_DIR = { "wallet-dir" };
    arg DAEMON_NAME = { "DAEMON_NAME", "nodeos" };
    arg LOGOS_DIR = { "LOGOS_DIR" };
    arg CONTRACT_PATH = { "CONTRACT_PATH" };
    arg WASM_CLANG = { "WASM_CLANG", "/home/cartman/opt/wasm/bin/clang" };
    arg WASM_LLVM_LINK = { "WASM_LLVM_LINK"
        , "/home/cartman/opt/wasm/bin/llvm-link" };
    arg WASM_LLC = { "WASM_LLC", "/home/cartman/opt/wasm/bin/llc" };
    arg BINARYEN_BIN = { "BINARYEN_BIN", "/home/cartman/opt/binaryen/bin/" };

    namespace bfs = boost::filesystem;

    string configValue(arg configKey, bool verbose = false) 
    {
      boost::property_tree::ptree json = TeosControl::getConfig(verbose);
      string value = json.get(configKey[0], NOT_DEFINED_VALUE);

      if(value != NOT_DEFINED_VALUE) {
        return value;
      } else {
        char* env = getenv(configKey[0].c_str());
        if(env == nullptr){
          return configKey.size() > 1 ? configKey[1] : NOT_DEFINED_VALUE;          
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
        bfs::path(configValue(CONTRACT_PATH)) 
        / name / contractFile;
      if(bfs::exists(contractFilePath)){
        return contractFilePath;
      }
      
      contractFilePath = 
        bfs::path(configValue(EOSIO_SOURCE_DIR))
        / "contracts" / name / contractFile;
      if(bfs::exists(contractFilePath)){
        return contractFilePath;
      }

      contractFilePath = 
        bfs::path(configValue(EOSIO_SOURCE_DIR))
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

      return configValue(EOSIO_DAEMON_ADDRESS);
    }

    string getHttpWalletAddress(string address)
    {
      if(!address.empty()) {
        return address;
      }
      string walletAddress = configValue(EOSIO_WALLET_ADDRESS);
      return walletAddress.empty() 
        ? configValue(EOSIO_DAEMON_ADDRESS) : walletAddress;
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
          wantedPath = bfs::path(configValue(EOSIO_SOURCE_DIR))
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
            = bfs::path(configValue(EOSIO_SOURCE_DIR))
              / "build/etc/eosio/node_00" 
              / configValue(DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }          
        }        
    
        {
          wantedPath 
            = bfs::path(configValue(EOSIO_SOURCE_DIR))
              / "build/programs/" / configValue(DAEMON_NAME)
              / configValue(DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath;
          }          
        }

        {
          wantedPath = bfs::path("/usr/local/bin")
              / configValue(DAEMON_NAME);
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
          wantedPath = bfs::path(configValue(CONFIG_DIR));
          if(bfs::exists(wantedPath) && bfs::is_directory(wantedPath)){
            return wantedPath;
          }            
        }
   
        {
          wantedPath  = bfs::path(configValue(EOSIO_SOURCE_DIR))
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
        
        wantedPath = bfs::path(configValue(WALLET_DIR));
        if(bfs::exists(wantedPath) && bfs::is_directory(wantedPath)) {
          return wantedPath;
        }     

        wantedPath  = bfs::path(configValue(EOSIO_SOURCE_DIR))
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
      return configValue(DAEMON_NAME);
    }

    string getWASM_CLANG(){
      return configValue(WASM_CLANG);
    }

    string getWASM_LLVM_LINK(){
      return configValue(WASM_LLVM_LINK);
    }

    string getBINARYEN_BIN(){
      return configValue(BINARYEN_BIN);
    }

    string getWASM_LLC(){
      return configValue(WASM_LLC);
    }    
  }
}



