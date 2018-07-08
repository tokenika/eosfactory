/**
 * @file config.hpp
 * @copyright defined in LICENSE.txt
 * @author Tokenika
 * @date 30 May 2018
*/

/**
 * @defgroup teoslib_raw Raw function classes
 */
/**
 * @defgroup teoslib_cli Command-line drivers
 */

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

    string getContractWorkspace(TeosControl* teosControl);
    
    string getContractDir(TeosControl* teosControl, string contractDir);

    vector<string> getContractSourceFiles(
      TeosControl* teosControl, string& contractDir);

    string getEosFactoryDir(TeosControl* teosControl);

    string getTeosDir(TeosControl* teosControl);

    string getSourceDir(TeosControl* teosControl);    

    string getDataDir(TeosControl* teosControl);

    string getConfigDir(TeosControl* teosControl);

    string getWalletDir(TeosControl* teosControl);

    string getDaemonExe(TeosControl* teosControl);

    string getCleosExe(TeosControl* teosControl);

    string getGenesisJson(TeosControl* teosControl);

    string getHttpServerAddress(TeosControl* teosControl);

    string getHttpWalletAddress(TeosControl* teosControl);

    string getDaemonName(TeosControl* teosControl);

    string getEOSIO_WASM_CLANG(TeosControl* teosControl);

    string getEOSIO_BOOST_INCLUDE_DIR(TeosControl* teosControl);

    string getEOSIO_WASM_LLVM_LINK(TeosControl* teosControl);

    string getEOSIO_WASM_LLC(TeosControl* teosControl);

    string getMemorySizeMb();

    string getEosioKeyPrivate();

    string getEosioKeyPublic();


    /**
     * @ingroup teoslib_raw
     * @brief Returns the configuration of the runtime.
     * 
     */
    class GetConfig : public TeosControl
    {
    public:
      GetConfig(ptree reqJson);
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
Usage: ./teos get config [<contract dir>]
Usage: ./teos get config --jarg '{
  "contract-dir":"<contract dir>",
  }' [OPTIONS]
)";
      }
      string contractDir;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("contract-dir", value<string>(&contractDir)->default_value(""),
            "Contract directory, possibly relative.");
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("contract-dir", 1);
      } 

      bool checkArguments(variables_map &vm) {
        reqJson_.put("contract-dir", contractDir);
        return true;
      }
               
      TeosControl executeCommand() {
        return GetConfig(reqJson_);
      }
    };    
  }
}