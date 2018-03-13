#pragma once

#include <stdlib.h>
#include <string>

#include <teos/item.hpp>

namespace teos {
  namespace config {
    using namespace std;

    enum ConfigKeys {
      NOT_DEFINED, GENESIS_JSON, HTTP_SERVER_ADDRESS, DATA_DIR
      , EOSIO_INSTALL_DIR, EOSIO_SOURCE_DIR, DAEMON_NAME, LOGOS_DIR
      , WASM_CLANG, WASM_LLVM_LINK, WASM_LLC, BINARYEN_BIN
    };
    string configValue(ConfigKeys configKey);

    /**
    */
    class ConfigTeos : public Item {
      public:
        ConfigTeos();
    };

    class ConfigTeosOptions : public ItemOptions<ConfigTeos>
    {
    public:
      ConfigTeosOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Review the configure json tree.
Usage: ./teos config teos
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      void printout(ConfigTeos command, variables_map &vm);

      void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          ConfigTeos command = ConfigTeos();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }
          printout(command, vm);
        }
      }
    };

  }
}