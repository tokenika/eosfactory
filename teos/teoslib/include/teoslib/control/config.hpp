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
        TeosControl* teosControl, string contractFile = "");
    string getDataDir(
      TeosControl* teosControl, string dataDir = "");        
    string getConfigDir(
      TeosControl* teosControl, string dataDir = "");
    string getWalletDir(
      TeosControl* teosControl, string walletDir = "", string dataDir = "");
    string getDaemonExe(
      TeosControl* teosControl, string daemonExe = "");
    string getGenesisJson(
      TeosControl* teosControl, string genesisJson = "");
    string getHttpServerAddress(TeosControl* teosControl, string address = "");
    string getHttpWalletAddress(TeosControl* teosControl, string address = "");
    string getDaemonName(TeosControl* teosControl);
    string getWASM_CLANG(TeosControl* teosControl);
    string getWASM_LLVM_LINK(TeosControl* teosControl);
    string getBINARYEN_BIN(TeosControl* teosControl);
    string getWASM_LLC(TeosControl* teosControl);
  };
}