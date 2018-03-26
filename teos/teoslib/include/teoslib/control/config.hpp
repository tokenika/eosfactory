#pragma once

#include <stdlib.h>
#include <string>
#include <boost/filesystem.hpp>

#include <teoslib/control.hpp>

namespace teos {
  namespace control {
    using namespace std;

    enum ConfigKeys { NOT_DEFINED
        , GENESIS_JSON, EOSIO_DAEMON_ADDRESS
        , EOSIO_WALLET_ADDRESS, DATA_DIR
        , EOSIO_INSTALL_DIR, EOSIO_SOURCE_DIR, DAEMON_NAME, LOGOS_DIR
        , CONTRACT_PATH
        , WASM_CLANG, WASM_LLVM_LINK, WASM_LLC, BINARYEN_BIN
    };
    string configValue(ConfigKeys configKey, bool verbose = false);
    boost::filesystem::path getContractFile(
        string contractFile, TeosControl& teosControl);
    boost::filesystem::path getDataDir(
      string dataDir, TeosControl& teosControl);


#define CONFIG_TEOS_ACTION "action"
#define CONFIG_TEOS_RESET_ACTION "reset"
#define CONFIG_TEOS_REVIEW_ACTION "review"
#define CONFIG_TEOS_PATH_ACTION "path"
    /**
     * @brief Review or reset the configure json tree.
    */
    class ConfigTeos : public  TeosControl
    {
      void action();

      public:
        ConfigTeos(string actionName) {
          reqJson_.put(CONFIG_TEOS_ACTION, actionName);
          action();
        }

        ConfigTeos(ptree reqJson) : TeosControl(reqJson) {
          action();
        }
    };

    /**
     * @brief Review or reset the configure json tree.
     * Usage: ./teos [http address] config teos [{review | reset | path}] [Options]
     * Usage: ./teos [http address] [-j '{
     *  ["action":"action name"], ["key1":"value1"], ["key2":"value2"] ...
     * }]
     */
    class ConfigTeosOptions : public ControlOptions
    {
    public:
      ConfigTeosOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Review or reset the configure json tree.
Usage: ./teos [http address] config teos [{review | reset | path}] [Options]
Usage: ./teos [http address] [-j '{
  ["action":"action name"]
}] [OPTIONS]
)EOF";
      }

      string action;
      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
        (CONFIG_TEOS_ACTION",a", value<string>(&action), 
          "The name the action requested.");
        return od;
      }   

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add(CONFIG_TEOS_ACTION, 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count(CONFIG_TEOS_ACTION)) {
          if(action == CONFIG_TEOS_RESET_ACTION 
            || action == CONFIG_TEOS_REVIEW_ACTION
            || action == CONFIG_TEOS_PATH_ACTION){
            reqJson_.put(CONFIG_TEOS_ACTION, action);
            ok = true;
          }
        } else {
          return true;
        }
        return ok;
      }      

      TeosControl executeCommand() {
        return ConfigTeos(reqJson_);
      }  

      void printout(TeosControl command, variables_map &vm);
    };
  };
}