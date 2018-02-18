
#include <stdlib.h>
#include <string>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <config.h>
#include <control/config.hpp>

#define _CRT_SECURE_NO_WARNINGS

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

using namespace std;
namespace pentagon {
  namespace config {

    boost::filesystem::path get_EOSIO_INSTALL_DIR()
    {
      boost::filesystem::path retval(getFromConfigOrFromEnv("EOSIO_INSTALL_DIR"));
      return retval;
    }
    
    boost::filesystem::path get_WASM_CLANG()
    {
      boost::filesystem::path retval(getFromConfigOrFromEnv("WASM_CLANG"
        , "/home/cartman/opt/wasm/bin/clang"));
      return retval;
    }

    boost::filesystem::path get_WASM_LLVM_LINK()
    {
      boost::filesystem::path retval(getFromConfigOrFromEnv("WASM_LLVM_LINK"
        , "/home/cartman/opt/wasm/bin/llvm-link"));
      return retval;  
    } 

    boost::filesystem::path get_WASM_LLC()
    {
      boost::filesystem::path retval(getFromConfigOrFromEnv("WASM_LLC"
        , "/home/cartman/opt/wasm/bin/llc"));
      return retval;      
    }
    
    boost::filesystem::path get_BINARYEN_BIN()
    {
      boost::filesystem::path retval(getFromConfigOrFromEnv("BINARYEN_BIN"
        , "/home/cartman/opt/binaryen/bin/"));
      return retval;
    } 
            
  }
}//namespace pentagon



