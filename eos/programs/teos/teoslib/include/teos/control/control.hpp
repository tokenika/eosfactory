#pragma once

#include <string>
#include <vector>
#include <teos/control/config.hpp>
#include <teos/item.hpp>

using namespace std;

namespace teos {
  namespace control {

    void startChainNode(
      string genesis_json = "",
      string http_server_address = "",
      string data_dir = "",
      bool resync_blockchain = true
    );
    void killChainNode();

    void buildContract(
      vector<string> src, // list of source c/cpp files
      string targetWastFile,
      vector<string> includeDir = {}
    );

    void generateAbi(
      string typesHpp,
      string targetAbiFile,
      vector<string> includeDir = {} // list of header files  
    );

    void wasmClangHelp();

    class NodeStart : public Item
    {
    public:
      NodeStart(
        string genesis_json = "",
        string http_server_address = "",
        string data_dir = "",
        bool resync_blockchain = true
      ) {
        try {
          startChainNode(
            genesis_json,
            http_server_address,
            data_dir,
            resync_blockchain
          );
        }
        catch (std::exception& e) {
          isError_ = true;
          errorMsg_ = e.what();
        }
      }
    };

    class NodeStartOptions : public ItemOptions<Item> {
    public:
      NodeStartOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Start test EOS node
Usage: ./teos node start [Options]
)EOF";
      }
        
      string genesis_json;
      string http_server_address;
      string data_dir;
      bool resync_blockchain;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("genesis-json", value<string>(&genesis_json)
            ->default_value(teos::config::GENESIS_JSON().string())
            , "File to read Genesis State from.")
          ("http-server-address", value<string>(&http_server_address)
            ->default_value(teos::config::HTTP_SERVER_ADDRESS())
            , "The local IP and port to listen for incoming http connections.")
          ("data-dir", value<string>(&data_dir)
            ->default_value(teos::config::DATA_DIR().string())
            , "Directory containing configuration file config.ini.")
          ("resync-blockchain", value<bool>(&resync_blockchain)
            ->default_value(true)
            , "Clear chain database and block log.");
        return od;
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      Item executeCommand() {
        return NodeStart(
            genesis_json,
            http_server_address,
            data_dir,
            resync_blockchain
          );
      }

      void printout(Item command, variables_map &vm) {
        if (vm.count("verbose") > 0) {
          output("genesis state file", "%s", genesis_json);
          output("server address", "%s", http_server_address);
          output("config directory", "%s", data_dir);
        }
      }

      virtual void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          Item command = executeCommand();
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