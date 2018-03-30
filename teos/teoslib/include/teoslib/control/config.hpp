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
    boost::filesystem::path getContractFile(
        TeosControl* teosControl, string contractFile = "");
    boost::filesystem::path getConfigDir(
      TeosControl* teosControl, string dataDir = "");
    boost::filesystem::path getWalletDir(
      TeosControl* teosControl, string walletDir = "", string configDir = "");
    boost::filesystem::path getDaemonExe(
      TeosControl* teosControl, string daemonExe = "");
    boost::filesystem::path getGenesisJson(
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