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
    cout << e.what() << endl;
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
    arg DATA_DIR = { "data-dir", "build/programs/daemon/data-dir" };
    arg CONFIG_DIR = { "config-dir", "build/programs/daemon/data-dir" };
    arg WALLET_DIR = { "wallet-dir", "wallet"}; // relative to data-dir
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

    string configValue(TeosControl* teosControl, arg configKey) 
    {
      boost::property_tree::ptree json = TeosControl::getConfig(teosControl);
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
        "First, the environmental variable, if any,\n"
        "next, the 'config.json' file that is:\n"
        "\t%1%\n"
        "Finally, the default value in the 'config.cpp' file."
        ) % TeosControl::getConfigJson()
      );
      if(teosControl){
        teosControl->putError(message + "\n" + help);
      } else {
        cout << "ERROR!" << endl << message << endl;
        cout << help << endl;
      }
    }

    string getSourceDir(TeosControl* teosControl)
    {
      string sourceDir = configValue(teosControl, EOSIO_SOURCE_DIR);
      if(sourceDir.empty()){
        onError(teosControl, "Cannot determine the EOSIO source directory.");
      }
      return sourceDir;
    }

    ///////////////////////////////////////////////////////////////////////////
    // getGenesisJson
    ///////////////////////////////////////////////////////////////////////////
    string getGenesisJson(TeosControl* teosControl)
    {
      try
      {
        bfs::path wantedPath(configValue(teosControl, GENESIS_JSON));
        if(!wantedPath.is_absolute()) {
          string configDir = getConfigDir(teosControl);
          if(configDir.empty()){
            return "";
          }
          wantedPath = bfs::path(configDir) / wantedPath;
        }

        if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
          return wantedPath.string();
        }
        
        onError(teosControl, (boost::format("Cannot determine the genesis file:\n%1%\n")
              % wantedPath.string()).str()); 
      } catch (exception& e) {
          onError(teosControl, e.what());               
      }
      return "";  
    }

    ///////////////////////////////////////////////////////////////////////////
    // getContractFile
    ///////////////////////////////////////////////////////////////////////////
    string getContractFile(
        TeosControl* teosControl, string contractDir, string contractFile)
    {
      try
      {
        if(contractFile.empty() || contractDir.empty()) {
          onError(
            teosControl, 
            "Cannot find the contract file. Neither 'contract file' nor "
            "'contract dir' can be empty.");
          return "";
        }

        bfs::path wantedPath;
        {
          wantedPath = bfs::path(contractFile);
          if(wantedPath.is_absolute() && bfs::exists(wantedPath) 
            && bfs::is_regular_file(wantedPath))
          {
            return wantedPath.string();
          }
        }

        {
          wantedPath = bfs::path(contractDir);
          bfs::path contractDirPath;
          if(!wantedPath.is_absolute()) 
          {
            contractDirPath = configValue(teosControl, CONTRACT_BUILD_PATH);
            if(!contractDirPath.is_absolute()) 
            {
              string sourceDir = getSourceDir(teosControl);
              if(sourceDir.empty()){
                return "";
              }
              contractDirPath = bfs::path(sourceDir) / contractDirPath;
            }
            contractDirPath = contractDirPath / wantedPath;
            wantedPath = contractDirPath;
          } 
          wantedPath = wantedPath / contractFile;
          if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
            return wantedPath.string();
          }

          if(contractFile[0] == '.')
          {
            for (bfs::directory_entry& entry 
              : boost::make_iterator_range(
                bfs::directory_iterator(contractDirPath), {})) 
              {
              if (bfs::is_regular_file(entry.path()) 
                && entry.path().extension() == contractFile) {
                  return entry.path().string();
              }
            } 
          }   
        }

        onError(teosControl, (boost::format("Cannot find the contract file:\n%1%\n")
              % wantedPath.string()).str()); 
      } catch (std::exception& e) {
          onError(teosControl, e.what());
      }
      return "";    
    }    

    ///////////////////////////////////////////////////////////////////////////
    // getHttpServerAddress
    ///////////////////////////////////////////////////////////////////////////
    string getHttpServerAddress(TeosControl* teosControl)
    {
      return configValue(teosControl, EOSIO_DAEMON_ADDRESS);
    }
    
    ///////////////////////////////////////////////////////////////////////////
    // getHttpWalletAddress
    ///////////////////////////////////////////////////////////////////////////
    string getHttpWalletAddress(TeosControl* teosControl)
    {
      return configValue(teosControl, EOSIO_WALLET_ADDRESS);
    }
    
    ///////////////////////////////////////////////////////////////////////////
    // getDaemonExe
    ///////////////////////////////////////////////////////////////////////////
    string getDaemonExe(TeosControl* teosControl)
    {
      try
      {
        string sourceDir = getSourceDir(teosControl);
        if(sourceDir.empty()){
          return "";
        }

        bfs::path wantedPath;
        {
          wantedPath 
            = bfs::path(sourceDir)
              / "build/etc/eosio/node_00" 
              / configValue(teosControl, DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }          
        }        
    
        {
          wantedPath 
            = bfs::path(sourceDir)
              / "build/programs/" / configValue(teosControl, DAEMON_NAME)
              / configValue(teosControl, DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }          
        }

        {
          wantedPath = bfs::path("/usr/local/bin")
              / configValue(teosControl, DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }             
        }

        if(!bfs::exists(wantedPath)){
          onError(teosControl,
            (boost::format("Cannot determine the EOS test node "
              "executable file:\n%1%\n") % wantedPath.string()).str());  
          return ""; 
        }
      } catch (std::exception& e) {
          onError(teosControl, e.what());          
          return "";        
      }
    }

    ///////////////////////////////////////////////////////////////////////////
    // getDataDir
    // Is created if argument 'dataDir' reprasents a directory path.
    ///////////////////////////////////////////////////////////////////////////
    string getDataDir(TeosControl* teosControl)
    {
      try
      { 
        bfs::path wantedPath(configValue(teosControl, DATA_DIR));

        if(!wantedPath.is_absolute()){
          string sourceDir = getSourceDir(teosControl);
          if(sourceDir.empty()){
            return "";
          }
          wantedPath = bfs::path(sourceDir) / wantedPath;
        }

        if(bfs::is_directory(wantedPath)) {
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }  
        }

        onError(teosControl,
          (boost::format("Cannot determine the 'data-dir' directory:\n%1%\n")
            % wantedPath.string()).str()); 

      } catch (std::exception& e){
        onError(teosControl, e.what());          
      }
      return "";      
    }

    ///////////////////////////////////////////////////////////////////////////
    // getConfigDir
    // Cannot be created.
    ///////////////////////////////////////////////////////////////////////////
    string getConfigDir(TeosControl* teosControl)
    {
      try
      { 
        bfs::path wantedPath(configValue(teosControl, CONFIG_DIR));
        if(!wantedPath.is_absolute()){
          string sourceDir = getSourceDir(teosControl);
          if(sourceDir.empty()){
            return "";
          }
          wantedPath = bfs::path(sourceDir) / wantedPath;
        } 

        if(bfs::exists(wantedPath) && bfs::is_directory(wantedPath)) {
          return wantedPath.string();
        }

        onError(teosControl,
          (boost::format("Cannot find the 'config-dir' directory:\n%1%\n")
            % wantedPath.string()).str());

      } catch (std::exception& e) {
          onError(teosControl, e.what());
      }
      return "";  
    }

    ///////////////////////////////////////////////////////////////////////////
    // getWalletDir
    ///////////////////////////////////////////////////////////////////////////
    string getWalletDir(
      TeosControl* teosControl)
    {
      try
      {
        bfs::path wantedPath(configValue(teosControl, WALLET_DIR));
        if(!wantedPath.is_absolute()) {
            wantedPath = getDataDir(teosControl) / wantedPath;
        }

        if(bfs::is_directory(wantedPath) && bfs::exists(wantedPath)) {
            return wantedPath.string();
          }  

        onError(teosControl, 
          (boost::format("Cannot find the 'wallet-dir' directory:\n%1%\n")
            % wantedPath.string()).str());

      } catch (std::exception& e) {
          onError(teosControl, e.what());
      }
      return "";        
    }

    ///////////////////////////////////////////////////////////////////////////
    // getDaemonName
    ///////////////////////////////////////////////////////////////////////////
    string getDaemonName(TeosControl* teosControl){
      return configValue(teosControl, DAEMON_NAME);
    }

    ///////////////////////////////////////////////////////////////////////////
    // getWASM_CLANG
    ///////////////////////////////////////////////////////////////////////////
    string getWASM_CLANG(TeosControl* teosControl){
      bfs::path home(getenv("HOME"));
      return (home / configValue(teosControl, WASM_CLANG)).string();
    }

    ///////////////////////////////////////////////////////////////////////////
    // getWASM_LLVM_LINK
    ///////////////////////////////////////////////////////////////////////////
    string getWASM_LLVM_LINK(TeosControl* teosControl){
      bfs::path home(getenv("HOME"));
      return (home / configValue(teosControl, WASM_LLVM_LINK)).string();
    }

    ///////////////////////////////////////////////////////////////////////////
    // getBINARYEN_BIN
    ///////////////////////////////////////////////////////////////////////////
    string getBINARYEN_BIN(TeosControl* teosControl){
      bfs::path home(getenv("HOME"));
      return (home / configValue(teosControl, BINARYEN_BIN)).string();      
    }

    ///////////////////////////////////////////////////////////////////////////
    // getWASM_LLC
    ///////////////////////////////////////////////////////////////////////////
    string getWASM_LLC(TeosControl* teosControl){
      bfs::path home(getenv("HOME"));
      return (home / configValue(teosControl, WASM_LLC)).string();
    }    
  }
}



