#pragma once

#include <stdlib.h>
#include <string>
#include <boost/filesystem.hpp>

#include <teoslib/control.hpp>

namespace teos {
  namespace control {
    using namespace std;
    /*
     * All the links with the environmen are defined here:
     */
    string getContractFile(
        TeosControl* teosControl, string contractDir, 
        string contractFile = "");

    string getSourceDir(TeosControl* teosControl);    

    string getDataDir(TeosControl* teosControl);

    string getConfigDir(TeosControl* teosControl);

    string getWalletDir(TeosControl* teosControl);

    string getDaemonExe(TeosControl* teosControl);

    string getGenesisJson(TeosControl* teosControl);

    string getHttpServerAddress(TeosControl* teosControl);

    string getHttpWalletAddress(TeosControl* teosControl);

    string getDaemonName(TeosControl* teosControl);

    string getWASM_CLANG(TeosControl* teosControl);

    string getBOOST_INCLUDE_DIR(TeosControl* teosControl);

    string getWASM_LLVM_LINK(TeosControl* teosControl);

    string getBINARYEN_BIN(TeosControl* teosControl);

    string getWASM_LLC(TeosControl* teosControl);
  };
}