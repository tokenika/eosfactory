#pragma once

#include <stdlib.h>
#include <string>

#include <teos/item.hpp>

namespace teos {
  namespace config {
    using namespace std;

    enum ConfigKeys {
      NOT_DEFINED, GENESIS_JSON, HTTP_SERVER_ADDRESS, DATA_DIR
      , EOSIO_INSTALL_DIR, EOSIO_SOURCE_DIR, CHAIN_NODE, PENTAGON_DIR
      , WASM_CLANG, WASM_LLVM_LINK, WASM_LLC, BINARYEN_BIN
    };
    string configValue(ConfigKeys configKey);

    /**
    */
    class ConfigJson : public Item
    {
    public:
      ConfigJson();
    };

    class ConfigJsonOptions : public ItemOptions<ConfigJson>
    {
    public:
      ConfigJsonOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Show the configure json tree.
Usage: ./teos config json
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          ConfigJson command = ConfigJson();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }
        }
      }
    };

  }
}