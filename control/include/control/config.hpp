#pragma once

#include <stdlib.h>
#include <string>
#include <boost/filesystem.hpp>

namespace pentagon{
  namespace config{

    using namespace std;
    using namespace boost::filesystem;

    path EOSIO_GIT_DIR();
    path EOSIO_INSTALL_DIR();
    path PENTAGON_DIR();    
    
    string CHAIN_NODE();
    path GENESIS_JSON();
    string HTTP_SERVER_ADDRESS();
    path DATA_DIR();

    path WASM_CLANG();
    path WASM_LLVM_LINK();
    path WASM_LLC();
    path BINARYEN_BIN();
  }
}