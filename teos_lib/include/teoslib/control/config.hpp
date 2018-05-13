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

    string getContractDir(TeosControl* teosControl, string contractDir);

    string getContextDir(TeosControl* teosControl);

    string getSourceDir(TeosControl* teosControl);    

    string getDataDir(TeosControl* teosControl);

    string getConfigDir(TeosControl* teosControl);

    string getWalletDir(TeosControl* teosControl);

    string getDaemonExe(TeosControl* teosControl);

    string getGenesisJson(TeosControl* teosControl);

    string getHttpServerAddress(TeosControl* teosControl);

    string getHttpWalletAddress(TeosControl* teosControl);

    string getDaemonName(TeosControl* teosControl);

    string getEOSIO_WASM_CLANG(TeosControl* teosControl);

    string getEOSIO_BOOST_INCLUDE_DIR(TeosControl* teosControl);

    string getEOSIO_WASM_LLVM_LINK(TeosControl* teosControl);

    string getEOSIO_BINARYEN_BIN(TeosControl* teosControl);

    string getEOSIO_WASM_LLC(TeosControl* teosControl);

    string getSharedMemorySizeMb();

    class GetConfig : public TeosControl
    {
    public:
      GetConfig();
    };

    class GetConfigOptions : public ControlOptions
    {
    public:
      GetConfigOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"(
Get Teos configuration.
Usage: ./teos get config
)";
      }

      TeosControl executeCommand() {
        return GetConfig();
      }
    };    
  }
}