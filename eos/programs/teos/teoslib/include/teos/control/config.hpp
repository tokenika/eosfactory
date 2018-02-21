#pragma once

#include <stdlib.h>
#include <string>
#include <boost/filesystem.hpp>

namespace teos{
  namespace config{

    using namespace std;
    using namespace boost;

    filesystem::path EOSIO_GIT_DIR();
    filesystem::path EOSIO_INSTALL_DIR();
    filesystem::path PENTAGON_DIR();
    
    string CHAIN_NODE();
    filesystem::path GENESIS_JSON();
    string HTTP_SERVER_ADDRESS();
    filesystem::path DATA_DIR();

    filesystem::path WASM_CLANG();
    filesystem::path WASM_LLVM_LINK();
    filesystem::path WASM_LLC();
    filesystem::path BINARYEN_BIN();
  }
}