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
    string getHttpServerAddress(string address = "");
    string getHttpWalletAddress(string address = "");
    string getDaemonName();
    string getWASM_CLANG();
    string getWASM_LLVM_LINK();
    string getBINARYEN_BIN();
    string getWASM_LLC();
  };
}