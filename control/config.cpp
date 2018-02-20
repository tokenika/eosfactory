
#include <stdlib.h>
#include <string>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <config.h>
#include <control/config.hpp>

#define _CRT_SECURE_NO_WARNINGS

using namespace std;

const char* configJsonDefault = R"EOF(
"EOSIO_GIT_DIR":"",
"EOSIO_INSTALL_DIR":"",
"WASM_CLANG":"",
"WASM_LLVM_LINK":"",
"WASM_LLC":"",
"BINARYEN_BIN":""
)EOF";

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

string getFromConfigOrFromEnv(string name, string defaultValue = "")
{
  boost::property_tree::ptree config = getConfigJson();
  string temp;
  temp = config.get(name, "");
  temp = temp != "" 
    ? temp 
    : getenv(name.c_str()) == 0 ? "" : getenv(name.c_str());
  if(temp != ""){
    return temp;
  }
  return defaultValue == "" ? name + "_is_not_defined." : defaultValue;
}

namespace pentagon {
  namespace config {

    using namespace std;
    using namespace boost::filesystem; 

    string CHAIN_NODE(){ 
      return getFromConfigOrFromEnv("CHAIN_NODE", "eosiod");
    }

    path GENESIS_JSON(){
      path retval(getFromConfigOrFromEnv("GENESIS_JSON", 
        (PENTAGON_DIR() / "resources/genesis.json").string()));
      return retval;
    }

    string HTTP_SERVER_ADDRESS(){
      return getFromConfigOrFromEnv("HTTP_SERVER_ADDRESS", "127.0.0.1:8888");
    }

    path DATA_DIR(){
      path retval(getFromConfigOrFromEnv("DATA_DIR", 
        (PENTAGON_DIR() / "workdir/data-dir").string()));
      return retval;
    }    

    path EOSIO_GIT_DIR(){
      path retval(getFromConfigOrFromEnv("EOSIO_GIT_DIR"));
      return retval;
    }

    path EOSIO_INSTALL_DIR(){
      path retval(getFromConfigOrFromEnv("EOSIO_INSTALL_DIR"));
      return retval;
    }
    
    path PENTAGON_DIR(){
      path retval(getFromConfigOrFromEnv("PENTAGON_DIR"));
      return retval;
    }        
    
    path WASM_CLANG(){
      path retval(getFromConfigOrFromEnv("WASM_CLANG"
        , "/home/cartman/opt/wasm/bin/clang"));
      return retval;
    }

    path WASM_LLVM_LINK(){
      path retval(getFromConfigOrFromEnv("WASM_LLVM_LINK"
        , "/home/cartman/opt/wasm/bin/llvm-link"));
      return retval;  
    } 

    path WASM_LLC(){
      path retval(getFromConfigOrFromEnv("WASM_LLC"
        , "/home/cartman/opt/wasm/bin/llc"));
      return retval;      
    }
    
    path BINARYEN_BIN(){
      path retval(getFromConfigOrFromEnv("BINARYEN_BIN"
        , "/home/cartman/opt/binaryen/bin/"));
      return retval;
    } 
            
  }
}//namespace pentagon



