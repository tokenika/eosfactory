#pragma once

#include <stdlib.h>
#include <string>
#include <boost/filesystem.hpp>


using namespace std;
namespace pentagon{
  namespace config{
    boost::filesystem::path get_EOSIO_INSTALL_DIR();
    boost::filesystem::path get_WASM_CLANG();
    boost::filesystem::path get_WASM_LLVM_LINK();
    boost::filesystem::path get_WASM_LLC();
    boost::filesystem::path get_BINARYEN_BIN();
  }
}