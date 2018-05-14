#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/format.hpp>
#include <boost/foreach.hpp>
#include <boost/system/error_code.hpp>
#include <boost/algorithm/string/replace.hpp>

#include <teoslib/config.h>
#include <teoslib/control/config.hpp>
#include <teoslib/utilities.hpp>

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
    #define CONTRACTS_DIR "contracts"
    #define EOSIO_CONTRACT_DIR "build/contracts"
    #define EMPTY ""

    typedef vector<string> arg;

    arg EOSIO_SOURCE_DIR = { "EOSIO_SOURCE_DIR" };
    arg EOSIO_DAEMON_ADDRESS = { "EOSIO_DAEMON_ADDRESS"
        , LOCALHOST_HTTP_ADDRESS };
    arg EOSIO_WALLET_ADDRESS = { "EOSIO_WALLET_ADDRESS", EMPTY };
    arg EOSIO_GENESIS_JSON = { "EOSIO_GENESIS_JSON", "genesis.json" }; 
      //genesis-json: relative to EOSIO_SOURCE_DIR
    arg EOSIO_DATA_DIR = { "EOSIO_DATA_DIR", "build/daemon/data-dir" };
    arg EOSIO_CONFIG_DIR = { "EOSIO_CONFIG_DIR", "build/daemon/data-dir" };
    arg EOSIO_WALLET_DIR = { "EOSIO_WALLET_DIR", "wallet"}; // relative to data-dir
    arg EOSIO_DAEMON_NAME = { "EOSIO_DAEMON_NAME", "nodeos" };
    arg EOSIO_CONTEXT_DIR = { "EOSIO_CONTEXT_DIR" };
    arg EOSIO_CONTRACT_WORKSPACE = { 
      "EOSIO_CONTRACT_WORKSPACE", CONTRACTS_DIR };// relative to EOSIO_CONTEXT_DIR

    arg EOSIO_SHARED_MEMORY_SIZE_MB = { "EOSIO_SHARED_MEMORY_SIZE_MB", "100" };    
    arg EOSIO_BOOST_INCLUDE_DIR = { "EOSIO_BOOST_INCLUDE_DIR"
      , "${HOME}/opt/boost_1_66_0/include", "/usr/local/include/" };
    arg EOSIO_WASM_CLANG = { "EOSIO_WASM_CLANG"
      , "${HOME}/opt/wasm/bin/clang", "/usr/local/wasm/bin/clang"};
      // EOSIO_WASM_CLANG: relative to HOME dir
    arg EOSIO_WASM_LLVM_LINK = { "EOSIO_WASM_LLVM_LINK"
      , "${HOME}/opt/wasm/bin/llvm-link", "/usr/local/wasm/bin/llvm-link" };
      // EOSIO_WASM_LLVM_LINK: relative to HOME dir
    arg EOSIO_WASM_LLC = { "EOSIO_WASM_LLC"
      , "${HOME}/opt/wasm/bin/llc", "/usr/local/wasm/bin/llc" };
      // EOSIO_WASM_LLC: relative to HOME dir

    namespace bfs = boost::filesystem;

    vector<string> configValues(TeosControl* teosControl, arg configKey) 
    {      
      //First, configure file ...
      boost::property_tree::ptree json = TeosControl::getConfig(teosControl);
      string value = json.get(string(configKey[0]), NOT_DEFINED_VALUE);
      if(value != string(NOT_DEFINED_VALUE)) {
        vector<string> retval = vector<string>();
        retval.push_back(value);
        return retval;
      }
      
      // ... next, environmental variable.
      char* env = getenv(configKey[0].c_str());
      if(env != nullptr) {
        vector<string> retval = vector<string>();
        retval.push_back(string(env));        
        return retval;
      } 

      // Finally, hard-codded value, if any.
      if(configKey.size() > 1) {
        vector<string> retval = vector<string>();        
        for(int i = 1; i < configKey.size(); i++) {
          retval.push_back(configKey[i]);
        }
        return retval;          
      }      
      
      vector<string> retval;
      retval.push_back(string(NOT_DEFINED_VALUE));
      return retval;
    }

    string configValue(TeosControl* teosControl, arg configKey) {
      return configValues(teosControl, configKey)[0];
    }

    string getValidPath(TeosControl* teosControl, arg configKey, string findFile)
    {
      vector<string> values = configValues(teosControl, configKey);
      bfs::path absolute(values[0]);
      if(absolute.is_absolute()) {
        if(bfs::exists(absolute / findFile)) {
          return absolute.string();
        }
      }

      string home = getenv("HOME");
      for(auto value : values)
      {
        try{
          boost::replace_all(value, "${HOME}", home);
          bfs::path p(value);

          if(bfs::exists(p / findFile)) {
            return p.string();
          }
        } catch(...){}
      }

      return "";
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

    string getContextDir(TeosControl* teosControl)
    {
      string config_value = configValue(teosControl, EOSIO_CONTEXT_DIR);
      if(config_value.empty()){
        onError(teosControl, "Cannot determine the context directory.");
      }
      return config_value;
    }

    string getSourceDir(TeosControl* teosControl)
    {
      string config_value = configValue(teosControl, EOSIO_SOURCE_DIR);
      if(config_value.empty()){
        onError(teosControl, "Cannot determine the EOSIO source directory.");
      }
      return config_value;
    }

    ///////////////////////////////////////////////////////////////////////////
    // getGenesisJson
    ///////////////////////////////////////////////////////////////////////////
    string getGenesisJson(TeosControl* teosControl)
    {
      try
      {
        bfs::path wantedPath(configValue(teosControl, EOSIO_GENESIS_JSON));
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

    string getContractDir(TeosControl* teosControl, string contract_dir)
    {
      bfs::path contract_path(contract_dir);
      if(!contract_path.is_absolute())
      {
        bfs::path workspacePath 
          = configValue(teosControl, EOSIO_CONTRACT_WORKSPACE);

        if(!workspacePath.is_absolute()) 
        {
          workspacePath = bfs::path(getContextDir(teosControl)) 
            / workspacePath;
        }
        contract_path = workspacePath / contract_dir / contract_dir;
      }
      if(bfs::is_regular_file(contract_path))
      {
        return contract_path.parent_path().string();
      } else
      {
        return contract_path.string();
      }
    }

    ///////////////////////////////////////////////////////////////////////////
    // getContractFile
    ///////////////////////////////////////////////////////////////////////////
    /**
     * Contract files: WAST, ABI
     */
    string getContractFile(
        TeosControl* teosControl, string contract_dir, string contractFile)
    {
      try
      {
        if(contractFile.empty() || contract_dir.empty()) {
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
          contract_dir = wslMapWindowsLinux(contract_dir);
          bfs::path contractDirPath(contract_dir);
          if(!contractDirPath.is_absolute()) 
          {
            bfs::path workspacePath 
              = configValue(teosControl, EOSIO_CONTRACT_WORKSPACE);

            if(!workspacePath.is_absolute()) 
            {
              string eosioContextDir = getContextDir(teosControl);
              workspacePath = bfs::path(eosioContextDir) 
                / workspacePath;
            }
            contractDirPath = workspacePath / contract_dir / "build";
            
            if(!bfs::exists(contractDirPath))
            {
              bfs::path workspacePathEosio = bfs::path(getSourceDir(teosControl)) 
                / EOSIO_CONTRACT_DIR;

              if(!bfs::exists(workspacePathEosio))
              {
                onError(
                  teosControl, 
                  (boost::format(
                    "Cannot find any contract directory: \n"
                    "neither\n%1%\n nor\n%1%\n is valid path.")
                  % contractDirPath.string() % workspacePathEosio.string()).str());
                return "";
              }
              contractDirPath = workspacePathEosio / contract_dir;
            }
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

          wantedPath = contractDirPath / contractFile;
          if(bfs::exists(wantedPath) && bfs::is_regular_file(wantedPath)) {
            return wantedPath.string();
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
    // shared-memory-size-mb
    ///////////////////////////////////////////////////////////////////////////
    string getSharedMemorySizeMb()
    {
      return configValue(nullptr, EOSIO_SHARED_MEMORY_SIZE_MB);
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
              / configValue(teosControl, EOSIO_DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }          
        }        
    
        {
          wantedPath 
            = bfs::path(sourceDir)
              / "build/programs/" / configValue(teosControl, EOSIO_DAEMON_NAME)
              / configValue(teosControl, EOSIO_DAEMON_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }          
        }

        {
          wantedPath = bfs::path("/usr/local/bin")
              / configValue(teosControl, EOSIO_DAEMON_NAME);
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
      } catch (exception& e) {
          onError(teosControl, e.what());          
          return "";        
      }
      return "";
    }

    ///////////////////////////////////////////////////////////////////////////
    // getDataDir
    // Is created if argument 'dataDir' reprasents a directory path.
    ///////////////////////////////////////////////////////////////////////////
    string getDataDir(TeosControl* teosControl)
    {
      try
      { 
        bfs::path wantedPath(configValue(teosControl, EOSIO_DATA_DIR));

        if(!wantedPath.is_absolute()){
          string contextDir = configValue(teosControl, EOSIO_CONTEXT_DIR);
          if(contextDir.empty()){
            return "";
          }
          wantedPath = bfs::path(contextDir) / wantedPath;
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
        bfs::path wantedPath(configValue(teosControl, EOSIO_CONFIG_DIR));
        if(!wantedPath.is_absolute()){
          string contextDir = configValue(teosControl, EOSIO_CONTEXT_DIR);
          if(contextDir.empty()){
            return "";
          }
          wantedPath = bfs::path(contextDir) / wantedPath;
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
        bfs::path wantedPath(configValue(teosControl, EOSIO_WALLET_DIR));
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
      return configValue(teosControl, EOSIO_DAEMON_NAME);
    }

    /*/////////////////////////////////////////////////////////////////////////
    // getEOSIO_BOOST_INCLUDE_DIR
        arg EOSIO_BOOST_INCLUDE_DIR = { "EOSIO_BOOST_INCLUDE_DIR"
      , "${HOME}/opt/boost_1_66_0/include", "/usr/local/include/" };
    /////////////////////////////////////////////////////////////////////////*/
    string getEOSIO_BOOST_INCLUDE_DIR(TeosControl* teosControl){
      return getValidPath(teosControl, EOSIO_BOOST_INCLUDE_DIR, "boost/version.hpp");
    }   

    ///////////////////////////////////////////////////////////////////////////
    // getEOSIO_WASM_CLANG
    ///////////////////////////////////////////////////////////////////////////
    string getEOSIO_WASM_CLANG(TeosControl* teosControl){
      return getValidPath(teosControl, EOSIO_WASM_CLANG, "");
    }

    ///////////////////////////////////////////////////////////////////////////
    // getEOSIO_WASM_LLVM_LINK
    ///////////////////////////////////////////////////////////////////////////
    string getEOSIO_WASM_LLVM_LINK(TeosControl* teosControl){
      return getValidPath(teosControl, EOSIO_WASM_LLVM_LINK, "");      
    }

    ///////////////////////////////////////////////////////////////////////////
    // getEOSIO_WASM_LLC
    ///////////////////////////////////////////////////////////////////////////
    string getEOSIO_WASM_LLC(TeosControl* teosControl){
      return getValidPath(teosControl, EOSIO_WASM_LLC, "");       
    }    

    GetConfig::GetConfig(){
        respJson_.put("contextDir", getContextDir(this));
        respJson_.put("sourceDir", getSourceDir(this));
        respJson_.put("dataDir", getDataDir(this));
        respJson_.put("configDir", getConfigDir(this));
        respJson_.put("walletDir", getWalletDir(this));
        respJson_.put("daemonExe", getDaemonExe(this));
        respJson_.put("genesisJson", getGenesisJson(this));
        respJson_.put("httpServer", getHttpServerAddress(this));
        respJson_.put(
          "httpWallet", 
          getHttpWalletAddress(this).empty() 
            ? getHttpServerAddress(this)
            : getHttpWalletAddress(this));
        respJson_.put("daemonName", getDaemonName(this));
        respJson_.put("wsmClang", getEOSIO_WASM_CLANG(this));
        respJson_.put("boostInclude", getEOSIO_BOOST_INCLUDE_DIR(this));
        respJson_.put("wasmLink", getEOSIO_WASM_LLVM_LINK(this));
        respJson_.put("wasmLlc", getEOSIO_WASM_LLC(this));
        respJson_.put("sharedMemory", getSharedMemorySizeMb());
        respJson_.put(
          "contractWorkspace", configValue(this, EOSIO_CONTRACT_WORKSPACE));
        respJson_.put(
          "workspaceEosio", getSourceDir(this) + "/" EOSIO_CONTRACT_DIR );
    }
  }
}



