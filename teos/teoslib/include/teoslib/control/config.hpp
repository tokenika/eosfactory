#pragma once

#include <stdlib.h>
#include <string>
#include <boost/filesystem.hpp>

#include <teoslib/control.hpp>

namespace teos {
  namespace control {
    using namespace std;

    boost::filesystem::path getContractFile(
        string contractFile, TeosControl& teosControl);
    boost::filesystem::path getConfigDir(
      string dataDir, TeosControl& teosControl);
    boost::filesystem::path getWalletDir(
      string walletDir, TeosControl& teosControl, string configDir = "");
    boost::filesystem::path getDaemonExe(
      string daemonExe, TeosControl& teosControl);
    boost::filesystem::path getGenesisJson(
      string genesisJson, TeosControl& teosControl);
    string getHttpServerAddress(string address = "");
    string getHttpWalletAddress(string address = "");
    string getDaemonName();
    string getWASM_CLANG();
    string getWASM_LLVM_LINK();
    string getBINARYEN_BIN();
    string getWASM_LLC();
  };
}