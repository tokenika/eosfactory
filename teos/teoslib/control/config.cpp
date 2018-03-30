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

Jast after build, facts are:

daemon_exe: ${EOSIO_SOURCE_DIR}/build/programs/nodeos/nodeos

config-dir: ${EOSIO_SOURCE_DIR}\build\etc\eosio\node_00/
${EOSIO_SOURCE_DIR}\build\etc\eosio\node_00/config.ini
${EOSIO_SOURCE_DIR}\build\etc\eosio\node_00/genesis.json

data-dir: ${EOSIO_SOURCE_DIR}\build\var\lib\eosio\node_00/
    ${EOSIO_SOURCE_DIR}\build\var\lib\eosio\node_00\blocks
    ${EOSIO_SOURCE_DIR}\build\var\lib\eosio\node_00\shared_mem

wallet-dir: .
    ${EOSIO_SOURCE_DIR}\build\var\lib\eosio\node_00/default.wallet
*/   

    #define NOT_DEFINED_VALUE ""
    #define EMPTY ""

    typedef vector<string> arg;

    arg EOSIO_SOURCE_DIR = { "EOSIO_SOURCE_DIR" };
    arg EOSIO_DAEMON_ADDRESS = { "EOSIO_DAEMON_ADDRESS"
        , LOCALHOST_HTTP_ADDRESS };
    arg EOSIO_WALLET_ADDRESS = { "EOSIO_WALLET_ADDRESS", EMPTY };
    arg GENESIS_JSON = { "genesis-json", "genesis.json" }; 
      //genesis-json: relative to EOSIO_SOURCE_DIR
    arg DATA_DIR = { "data-dir", "build/var/lib/eosio/node_00/" };
    arg CONFIG_DIR = { "config-dir", "build/etc/eosio/node_00/" };
    arg WALLET_DIR = { "wallet-dir" "."}; // relative to data-dir
    arg DAEMON_NAME = { "DAEMON_NAME", "nodeos" };
    arg LOGOS_DIR = { "LOGOS_DIR" };
    arg CONTRACT_BUILD_PATH = { "CONTRACT_BUILD_PATH", "build/contracts" };
      //CONTRACT_BUILD_PATH: relative to EOSIO_SOURCE_DIR
    arg WASM_CLANG = { "WASM_CLANG", "opt/wasm/bin/clang" };
      // WASM_CLANG: relative to HOME dir
    arg WASM_LLVM_LINK = { "WASM_LLVM_LINK", "opt/wasm/bin/llvm-link" };
      // WASM_LLVM_LINK: relative to HOME dir
    arg WASM_LLC = { "WASM_LLC", "opt/wasm/bin/llc" };
      // WASM_LLC: relative to HOME dir
    arg BINARYEN_BIN = { "BINARYEN_BIN", "opt/binaryen/bin/" };
      // BINARYEN_BIN: relative to HOME dir

    namespace bfs = boost::filesystem;

    string configValue(arg configKey) 
    {
      boost::property_tree::ptree json = TeosControl::getConfig(false);
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

    void onError(TeosControl* teosControl, string message)
    {
      string help = boost::str(boost::format(
        "%1 is not a directory.") % TeosControl::getConfigJson()
      );
      if(teosControl){
        teosControl->putError(message);
      } else {
        cerr << "ERROR!" << endl << message << endl;
      }
    }

    boost::filesystem::path getContractFile(
        TeosControl* teosControl, string contractFile)
    {
      namespace bfs = boost::filesystem;

      string name;
      {// Is it passed as 'contractFile' argument?
        bfs::path wantedPath(contractFile);
        if(bfs::exists(wantedPath)){
          return wantedPath;
        }
        name = wantedPath.stem().string();
      }

      {// Is it defined with the 'configValue' function?
        bfs::path contractDir = bfs::path(configValue(CONTRACT_BUILD_PATH));

        bfs::path wantedPath = contractDir.is_absolute()
          ? contractDir / name / contractFile
          : bfs::path(configValue(EOSIO_SOURCE_DIR))
            / contractDir / name / contractFile;
        if(bfs::exists(wantedPath)) {
          return wantedPath;
        }
      }

      onError(teosControl, "Cannot find the path to the contract file.");
      return bfs::path("");
    }    


    string getHttpServerAddress(string address)
    {
      if(address != EMPTY) {
        return address;
      }
      return configValue(EOSIO_DAEMON_ADDRESS);
    }

    string getHttpWalletAddress(string address)
    {
      if(address != EMPTY) {
        return address;
      }
      string walletAddress = configValue(EOSIO_WALLET_ADDRESS);
      return walletAddress.empty() 
        ? configValue(EOSIO_DAEMON_ADDRESS) : walletAddress;
    }
    

    boost::filesystem::path getGenesisJson(
      TeosControl* teosControl, string genesisJson)
    {
      namespace bfs = boost::filesystem;

      try{
        bfs::path wantedPath;
        
        if(!genesisJson.empty())
        {
          wantedPath = bfs::path(genesisJson);
          if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
            return wantedPath;
          }
          wantedPath = bfs::path(configValue(EOSIO_SOURCE_DIR)) / wantedPath;
            if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
            return wantedPath;
          }
        } else
        {
          wantedPath = bfs::path(configValue(GENESIS_JSON));
          if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
            return wantedPath;
          }
          wantedPath = bfs::path(configValue(EOSIO_SOURCE_DIR)) 
            / bfs::path(configValue(GENESIS_JSON));
          if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
            return wantedPath;
          }                    
        }

        if(!bfs::exists(wantedPath)){
          teosControl->putError("Cannot determine the genesis file.");
          return bfs::path("");
        }         

      } catch (std::exception& e) {
          onError(teosControl, e.what());
          return bfs::path("");        
      }
    }

    /*
    Determines the EOS test node executable file.
    */
    boost::filesystem::path getDaemonExe(
      TeosControl* teosControl, string daemonExe)
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
          onError(
            teosControl, 
            "Cannot determine the EOS test node executable file.");
          return bfs::path(""); 
        }
      } catch (std::exception& e) {
          onError(teosControl, e.what());          
          return bfs::path("");        
      }
    }

    boost::filesystem::path getConfigDir(
      TeosControl* teosControl, string configDir)
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
            onError(teosControl, boost::str(boost
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

        if(!bfs::exists(wantedPath) && teosControl){
          onError(
            teosControl,
            "Cannot determine the path to 'config-dir' directory.");
          return bfs::path("");
        }         
      } catch (std::exception& e)
      {
        onError(teosControl, e.what());          
        return bfs::path("");
      }
    }

    boost::filesystem::path getWalletDir(
      TeosControl* teosControl, string walletDir, string configDir)
    {
      namespace bfs = boost::filesystem;

      try{
        bfs::path configDirPath = getConfigDir(teosControl, configDir);
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
              teosControl->putError(boost::str(boost
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
          onError(
            teosControl, 
            "Cannot determine the path to 'wallet-dir' directory.");
          return bfs::path("");
        }         
      } catch (std::exception& e)
      {
        onError(teosControl, e.what());
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
      string home = getenv("HOME");
      return configValue(WASM_LLC);
    }    
  }
}



