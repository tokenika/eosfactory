#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>
#include <vector>
#include <set>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/format.hpp>
#include <boost/foreach.hpp>
#include <boost/system/error_code.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/dll.hpp>

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

    #define NOT_DEFINED_VALUE ""
    #define CONTRACTS_DIR "contracts/"
    #define TEOS_EXE "teos/build/teos/teos"
    #define EOSIO_CONTRACT_DIR "build/contracts/"
    #define EMPTY ""

    typedef vector<string> arg;

    arg EOSIO_SOURCE_DIR = { "EOSIO_SOURCE_DIR" };
    arg EOSIO_DAEMON_ADDRESS = { "EOSIO_DAEMON_ADDRESS"
        , LOCALHOST_HTTP_ADDRESS };
    arg EOSIO_WALLET_ADDRESS = { "EOSIO_WALLET_ADDRESS", EMPTY };
    arg EOSIO_GENESIS_JSON = { "EOSIO_GENESIS_JSON", "genesis.json" }; 
      //genesis-json: relative to EOSIO_SOURCE_DIR
    arg EOSIO_DATA_DIR = { "EOSIO_DATA_DIR", "build/daemon/data-dir/" };
    arg EOSIO_CONFIG_DIR = { "EOSIO_CONFIG_DIR", "build/daemon/data-dir/" };
    arg EOSIO_WALLET_DIR = { "EOSIO_WALLET_DIR", "wallet/"}; // relative to data-dir
    arg EOSIO_DAEMON_NAME = { "EOSIO_DAEMON_NAME", "nodeos" };
    arg EOSIO_CLI_NAME = { "EOSIO_CLI_NAME", "cleos" };
    arg EOSIO_EOSFACTORY_DIR = { "EOSIO_EOSFACTORY_DIR" };
    arg EOSIO_TEOS_DIR = { "EOSIO_TEOS_DIR", "teos/" };
    arg EOSIO_KEY_PRIVATE = { "EOSIO_KEY_PRIVATE", 
      "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3" };
    arg EOSIO_KEY_PUBLIC = { "EOSIO_KEY_PUBLIC", 
      "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV" };

    arg EOSIO_CONTRACT_WORKSPACE = { 
      "EOSIO_CONTRACT_WORKSPACE", CONTRACTS_DIR };// relative to EOSIO_EOSFACTORY_DIR

    arg EOSIO_SHARED_MEMORY_SIZE_MB = { "EOSIO_SHARED_MEMORY_SIZE_MB", "100" };    
    arg EOSIO_BOOST_INCLUDE_DIR = { "EOSIO_BOOST_INCLUDE_DIR"
      , "${U_HOME}/opt/boost/include", "/usr/local/include/" };
    arg EOSIO_WASM_CLANG = { "EOSIO_WASM_CLANG"
      , "${U_HOME}/opt/wasm/bin/clang", "/usr/local/wasm/bin/clang"};
      // EOSIO_WASM_CLANG: relative to U_HOME dir
    arg EOSIO_WASM_LLVM_LINK = { "EOSIO_WASM_LLVM_LINK"
      , "${U_HOME}/opt/wasm/bin/llvm-link", "/usr/local/wasm/bin/llvm-link" };
      // EOSIO_WASM_LLVM_LINK: relative to U_HOME dir
    arg EOSIO_WASM_LLC = { "EOSIO_WASM_LLC"
      , "${U_HOME}/opt/wasm/bin/llc", "/usr/local/wasm/bin/llc" };
      // EOSIO_WASM_LLC: relative to U_HOME dir

    namespace bfs = boost::filesystem;

    void onError(TeosControl* teosControl, string message, string spot="")
    {
      if(teosControl){
        teosControl->putError(message, spot);
      } else {
        cout << "ERROR!" << endl << message << endl;
      }
    }

    string getTeosConfigJson(TeosControl* teosControl)
    {
      string trace = "";
      try{
        {
          const char* env = getenv(EOSIO_EOSFACTORY_DIR[0].c_str());
          trace += env ? env : "env(EOSIO_EOSFACTORY_DIR) is null";
          trace += "\n";
          if(env != nullptr) {
            bfs::path configPath = bfs::path(env) / "teos" / CONFIG_JSON;
            trace += configPath.string() + "\n";
            if(bfs::exists(configPath)) {
              return configPath.string();
            } 
          } 
        }

        bfs::path programLocation = boost::dll::program_location().parent_path();

        {
          bfs::path configPath = programLocation / CONFIG_JSON;
          trace += configPath.string() + "\n";
          if(bfs::exists(configPath)) {
              return configPath.string();
          }                  
        }

        {
          bfs::path configPath = programLocation.parent_path() / CONFIG_JSON;
          trace += configPath.string() + "\n";
          if(bfs::exists(configPath)) {
              return configPath.string();
          }                  
        }        

        {
          bfs::path configPath = programLocation.parent_path()
            .parent_path() / CONFIG_JSON;
          trace += configPath.string() + "\n";
          if(bfs::exists(configPath)) {
              return configPath.string();
          }                  
        }     

        throw std::exception();

      } catch (std::exception& e) {
        onError(
          teosControl, 
          (boost::format(R"(
Cannot find TEOS config json file. It is expected in the EOSFactory/teos dir.
The EOSFactory has to be set as the EOSIO_EOSFACTORY_DIR environment
variable.
)""\n trace is \n%1%") % trace).str(), 
          SPOT );            
      }
      return "";
    }    

    ptree getConfig(TeosControl* teosControl) 
    {
      ptree config;
      try
      {
        read_json(getTeosConfigJson(teosControl), config);
      }
      catch (exception& e) {
        if(teosControl) {
          teosControl->putError("Cannot read config.json", SPOT);
        } else {
          cout << teos_ERROR << endl << "Cannot read config.json" << endl;
        }
      }
      return config;
    }    

    vector<string> configValues(TeosControl* teosControl, arg configKey) 
    {      
      //First, configure file ...
      boost::property_tree::ptree json = getConfig(teosControl);
      string value = json.get(string(configKey[0]), NOT_DEFINED_VALUE);
      if(value != string(NOT_DEFINED_VALUE)) {
        vector<string> retval = vector<string>();
        retval.push_back(value);
        return retval;
      }
      
      // ... next, environmental variable.
      const char* env = getenv(configKey[0].c_str());
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

      string home = getenv("U_HOME");
      for(auto value : values)
      {
        try{
          boost::replace_all(value, "${U_HOME}", home);
          bfs::path p(value);

          if(bfs::exists(p / findFile)) {
            return p.string();
          }
        } catch(...){}
      }

      return "";
    }

    string getEosFactoryDir(TeosControl* teosControl)
    {
      string config_value = configValue(teosControl, EOSIO_EOSFACTORY_DIR);
      if(config_value.empty()){
        onError(
          teosControl, "Cannot determine the context directory.", SPOT);
      }
      return config_value;
    }

    string getSourceDir(TeosControl* teosControl)
    {
      string config_value = configValue(teosControl, EOSIO_SOURCE_DIR);
      if(config_value.empty()){
        onError(
          teosControl, "Cannot determine the EOSIO source directory.", SPOT);
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
        
        onError(
          teosControl, (boost::format("Cannot determine the genesis file:\n%1%\n")
              % wantedPath.string()).str(), SPOT); 
      } catch (exception& e) {
          onError(teosControl, e.what());               
      }
      return "";  
    }

    /** 
     * getContractDir

    */
    string getContractDir(TeosControl* teosControl, string contractDir)
    {
      string trace = contractDir + SPOT + "\n";      
      contractDir = wslMapWindowsLinux(contractDir);
      try{
        { /*
            Does the given contractDir is absolute, is directory and exists?
          */
          bfs::path contractPath(contractDir);
          trace += contractPath.string() + SPOT + "\n";
          if(contractPath.is_absolute() 
            && bfs::exists(contractPath)) {
              return contractPath.string();
          }
        }
        {
          /*
            Does the given contractDir is an existing subdirectory of the 
            EOSIO_CONTRACT_WORKSPACE entry in the config.json?
          */
          bfs::path contractPath 
            = bfs::path(configValue(teosControl, EOSIO_CONTRACT_WORKSPACE)) 
              / contractDir;
          trace += contractPath.string() + SPOT + "\n";
          if(!contractPath.is_absolute()) {
            bfs::path contextPath(configValue(teosControl, EOSIO_EOSFACTORY_DIR));
            contractPath = contextPath / contractPath;
            trace += contractPath.string() + SPOT + "\n";
          }
          if(bfs::exists(contractPath)) {
            return contractPath.string();
          }
        }
        {
          /*
            Does the given contract directory exists in the 
            eosfactory/contracts directory?
          */
          bfs::path contractPath 
              = bfs::path(configValue(teosControl, EOSIO_EOSFACTORY_DIR)) 
                / CONTRACTS_DIR / contractDir;
          trace += contractPath.string() + SPOT + "\n";
          if(contractPath.is_absolute() && bfs::exists(contractPath)) {
              return contractPath.string();
            }        
        }
        {
          /*
            Does the given contract directory exists in the eos/build/contracts
            directory?
          */
          bfs::path contractPath 
              = bfs::path(configValue(teosControl, EOSIO_SOURCE_DIR)) 
                / EOSIO_CONTRACT_DIR / contractDir;
          trace += contractPath.string() + SPOT + "\n";
          if(contractPath.is_absolute() 
            && bfs::exists(contractPath)) {
              return contractPath.string();
          }
        }

        throw std::exception();

      } catch (std::exception& e) {
        onError(
          teosControl, 
          (boost::format(R"(
Cannot determine the contract directory.
)""\n trace is \n%1%") % trace).str(), 
          SPOT );            
      }
      return "";
    }


    vector<string> getSourceFiles(boost::filesystem::path sourcePath)
    {
      namespace bfs = boost::filesystem;

      vector<string> srcs;
      set<string> extensions({".cpp", ".cxx", ".c", ".abi"});
      for (bfs::directory_entry& entry 
        : boost::make_iterator_range(
          bfs::directory_iterator(sourcePath), {})) 
        {
        if (bfs::is_regular_file(entry.path()) 
          && extensions.find(entry.path().extension().string()) 
              != extensions.end()){
          srcs.push_back(entry.path().string());
        }
      }
      return srcs;
    }
    

    vector<string> getContractSourceFiles(TeosControl* teosControl, string& contractDir)
    {
      contractDir = wslMapWindowsLinux(contractDir);
      contractDir = getContractDir(teosControl, contractDir);
      if(teosControl->isError_){
        return vector<string>();;
      }

      string trace = "contractDir: " + contractDir + SPOT + "\n";
      try{
        {
          bfs::path sourcePath(contractDir);
          trace += sourcePath.string() + SPOT + "\n";
          vector<string> srcs = getSourceFiles(sourcePath);
          if(!srcs.empty()){
            return srcs;            
          }
        }

        {
          bfs::path sourcePath = bfs::path(contractDir) / "src";
          contractDir = sourcePath.string();
          trace += sourcePath.string() + SPOT + "\n";
          vector<string> srcs = getSourceFiles(sourcePath);
          if(!srcs.empty()){
            return srcs;            
          }
        }

        throw std::exception();

      } catch (std::exception& e) {
        onError(
          teosControl, 
          (boost::format(R"(
Cannot find any contract source directory.
)""\n trace is \n%1%") % trace).str(), 
          SPOT );            
      }
      return vector<string>();
    }

    ///////////////////////////////////////////////////////////////////////////
    // getContractFile
    ///////////////////////////////////////////////////////////////////////////
    /**
     * Contract files: WAST, ABI
     */
    string getContractFile(
        TeosControl* teosControl, string contractDir, string contractFile)
    {
      contractDir = wslMapWindowsLinux(contractDir);
      contractFile = wslMapWindowsLinux(contractFile);
      string trace = "";
      try
      {
        if(contractFile.empty() || contractDir.empty()) 
        { 
          /*
            Is it not enough data.
          */
          onError(
            teosControl, 
            "Cannot find the contract file. Neither 'contract file' nor "
            "'contract dir' can be empty.", SPOT);
          return "";
        }

        {
          /*
            Is the contract file absolute?
          */
          bfs::path contractFilePath(contractFile);
          trace += contractFilePath.string() + SPOT + "\n"; 
          if(contractFilePath.is_absolute() && bfs::exists(contractFilePath) 
            && bfs::is_regular_file(contractFilePath))
          {
            return contractFilePath.string();
          }
        }

        {
          /*
            Does the contractDir argument point to a contract directory?
            Try varies internal structures of the contract directories. 
          */
          bfs::path buildPath // Is existing absolute path!
            = bfs::path(getContractDir(teosControl, contractDir));
          trace += buildPath.string() + SPOT + "\n";
          if(teosControl->isError_){
            return "";
          }

          if(bfs::is_regular_file(buildPath))
          {
            return buildPath.string();
          }
          
          /*
            Try contract directory with a 'build' subdirectory:
          */
          if(bfs::exists(buildPath / "build")) {
            buildPath = buildPath / "build";
          }
          trace += buildPath.string() + SPOT + "\n";
          if(contractFile[0] == '.')
          {
            for (bfs::directory_entry& entry 
              : boost::make_iterator_range(
                bfs::directory_iterator(buildPath), {})) 
              {
              trace += entry.path().string() + SPOT + "\n";
              if (bfs::is_regular_file(entry.path()) 
                && entry.path().extension() == contractFile) {
                  return entry.path().string();
              }
            } 
          }   

          bfs::path contractFilePath = buildPath / contractFile;
          trace += contractFilePath.string() + SPOT + "\n";
          if(bfs::exists(contractFilePath) && bfs::is_regular_file(contractFilePath)) {
            return contractFilePath.string();
          }
        }

        throw std::exception();

      } catch (std::exception& e) {
        onError(
          teosControl, 
          (boost::format(R"(
Cannot find any contract file.
)""\n trace is \n%1%") % trace).str(), 
          SPOT ); 
      }

      return "";    
    }

    string getContractWorkspace(TeosControl* teosControl)
    {
      string trace = "";
      try{
        bfs::path workspacePath 
          = bfs::path(configValue(teosControl, EOSIO_CONTRACT_WORKSPACE));
        trace += workspacePath.string() + "\n";
        if(!workspacePath.is_absolute()) {
          bfs::path contextPath(configValue(teosControl, EOSIO_EOSFACTORY_DIR));
          workspacePath = contextPath / workspacePath;
          trace += workspacePath.string() + "\n";
        }
        if(bfs::exists(workspacePath)) {
          trace += "returns " + workspacePath.string() + "\n";
          return workspacePath.string();
        }

        throw std::exception();        
      } catch (std::exception& e) {
        onError(
          teosControl, 
          (boost::format(R"(
Cannot determine the contract workspace.
)""\n trace is \n%1%") % trace).str(),
          SPOT);
      }
      return ""; 
    }

    string getEosioKeyPrivate()
    {
      return configValue(nullptr, EOSIO_KEY_PRIVATE);
    }

    string getEosioKeyPublic()
    {
      return configValue(nullptr, EOSIO_KEY_PUBLIC);
    }    
    
    ///////////////////////////////////////////////////////////////////////////
    // chain-state-db-size-mb
    ///////////////////////////////////////////////////////////////////////////
    string getMemorySizeMb()
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
              "executable file:\n%1%\n") % wantedPath.string()).str(), SPOT);  
          return ""; 
        }
      } catch (exception& e) {
          onError(teosControl, e.what(), SPOT);          
          return "";        
      }
      return "";
    }

    ///////////////////////////////////////////////////////////////////////////
    // getCleosExe
    ///////////////////////////////////////////////////////////////////////////
    string getCleosExe(TeosControl* teosControl)
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
              / "build/programs/" / configValue(teosControl, EOSIO_CLI_NAME)
              / configValue(teosControl, EOSIO_CLI_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }          
        }

        {
          wantedPath = bfs::path("/usr/local/bin")
              / configValue(teosControl, EOSIO_CLI_NAME);
          if(bfs::exists(wantedPath)) {
            return wantedPath.string();
          }             
        }

        if(!bfs::exists(wantedPath)){
          onError(teosControl,
            (boost::format("Cannot determine the EOS test node "
              "executable file:\n%1%\n") % wantedPath.string()).str(), SPOT);  
          return ""; 
        }
      } catch (exception& e) {
          onError(teosControl, e.what(), SPOT);          
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
          string contextDir = configValue(teosControl, EOSIO_EOSFACTORY_DIR);
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
            % wantedPath.string()).str(), SPOT); 

      } catch (std::exception& e){
        onError(teosControl, e.what(), SPOT);          
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
          string contextDir = configValue(teosControl, EOSIO_EOSFACTORY_DIR);
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
            % wantedPath.string()).str(), SPOT);

      } catch (std::exception& e) {
          onError(teosControl, e.what(), SPOT);
      }
      return "";  
    }

    ///////////////////////////////////////////////////////////////////////////
    // getWalletDir
    ///////////////////////////////////////////////////////////////////////////
    string getWalletDir(TeosControl* teosControl)
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
            % wantedPath.string()).str(), SPOT);

      } catch (std::exception& e) {
          onError(teosControl, e.what(), SPOT);
      }
      return "";        
    }

    string getKeosdWalletDir()
    {
      return "${HOME}/eosio-wallet/";
    }

    string getTeosDir(TeosControl* teosControl) {
      try{

        bfs::path wantedPath(configValue(teosControl, EOSIO_TEOS_DIR));
        if(!wantedPath.is_absolute()) {
            wantedPath = 
              bfs::path(configValue(teosControl, EOSIO_EOSFACTORY_DIR)) / wantedPath;
        }
        
        if(bfs::is_directory(wantedPath) && bfs::exists(wantedPath)) {
          return wantedPath.string();
        } 

        onError(teosControl, 
          (boost::format("Cannot find the teos directory:\n%1%\n")
            % wantedPath.string()).str(), SPOT);
      } catch (std::exception& e) {
          onError(teosControl, e.what(), SPOT);
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
      , "${U_HOME}/opt/boost/include", "/usr/local/include/" };
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

    GetConfig::GetConfig(ptree reqJson) : TeosControl(reqJson){
      respJson_.put("EOSIO_SOURCE_DIR", getSourceDir(this));
      respJson_.put("EOSIO_EOSFACTORY_DIR", getEosFactoryDir(this));
      respJson_.put("EOSIO_DATA_DIR", getDataDir(this));
      respJson_.put("EOSIO_CONFIG_DIR", getConfigDir(this));
      respJson_.put("EOSIO_WALLET_DIR", getWalletDir(this));
      respJson_.put("KEOSD_WALLET_DIR", getKeosdWalletDir());
      respJson_.put("nodeExe", getDaemonExe(this));
      respJson_.put("cleosExe", getCleosExe(this));
      respJson_.put("genesisJson", getGenesisJson(this));
      respJson_.put("EOSIO_DAEMON_ADDRESS", getHttpServerAddress(this));
      respJson_.put("EOSIO_KEY_PRIVATE", getEosioKeyPrivate());
      respJson_.put("EOSIO_KEY_PUBLIC", getEosioKeyPublic());

      respJson_.put(
        "EOSIO_WALLET_ADDRESS", 
        getHttpWalletAddress(this).empty() 
          ? getHttpServerAddress(this)
          : getHttpWalletAddress(this));
      respJson_.put("EOSIO_DAEMON_NAME", getDaemonName(this));
      respJson_.put("EOSIO_WASM_CLANG", getEOSIO_WASM_CLANG(this));
      respJson_.put("EOSIO_BOOST_INCLUDE_DIR", getEOSIO_BOOST_INCLUDE_DIR(this));
      respJson_.put("EOSIO_WASM_LLVM_LINK", getEOSIO_WASM_LLVM_LINK(this));
      respJson_.put("EOSIO_WASM_LLC", getEOSIO_WASM_LLC(this));
      respJson_.put("sharedMemory", getMemorySizeMb());
      respJson_.put(
        "contractWorkspace", configValue(this, EOSIO_CONTRACT_WORKSPACE));
      respJson_.put(
        "workspaceEosio", getSourceDir(this) + "/" EOSIO_CONTRACT_DIR );
      if(!reqJson_.get("contract-dir", "").empty())
      {
        respJson_.put("contract-dir", getContractDir(
          this, reqJson_.get<string>("contract-dir")));
        respJson_.put("contract-wast", getContractFile(
          this, reqJson_.get<string>("contract-dir"), ".wast"));
        respJson_.put("contract-abi", getContractFile(
          this, reqJson_.get<string>("contract-dir"), ".abi"));
      }
    }
  }
}
