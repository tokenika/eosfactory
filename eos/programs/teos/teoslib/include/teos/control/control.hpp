#pragma once

#include <string>
#include <vector>

#include <teos/item.hpp>

using namespace std;

namespace teos {
  namespace control {

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
      string eosiod_exe_;
      string genesis_json_;
      string http_server_address_;
      string data_dir_;
      bool resync_blockchain_;

      NodeStart(
        string eosiod_exe = "",
        string genesis_json = "",
        string http_server_address = "",
        string data_dir = "",
        bool resync_blockchain = true
      );
    };

    class NodeStartOptions : public ItemOptions<NodeStart> {
    public:
      NodeStartOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Start test EOS node
Usage: ./teos node start [Options]
)EOF";
      }
        
      string eosiod;
      string genesis_json;
      string http_server_address;
      string data_dir;
      bool resync_blockchain;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("eosiod.exe", value<string>(&eosiod)
            ->default_value("") , "EOS daemon exe file.")
          ("genesis-json", value<string>(&genesis_json)
            ->default_value(""), "File to read Genesis State from.")
          ("http-server-address", value<string>(&http_server_address)
            ->default_value("127.0.0.1:8888")
              , "The local IP and port to listen for incoming http connections.")
          ("data-dir", value<string>(&data_dir)->default_value("")
            , "Directory containing configuration file config.ini.")
          ("resync-blockchain", value<bool>(&resync_blockchain)
            ->default_value(true)
            , "Clear chain database and block log.");
        return od;
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      NodeStart executeCommand() {
        return NodeStart(
            eosiod,
            genesis_json,
            http_server_address,
            data_dir,
            resync_blockchain
          );
      }

      void printout(NodeStart command) {
        output("eosiod exe file", "%s", command.eosiod_exe_.c_str());
        output("genesis state file", "%s", command.genesis_json_.c_str());
        output("server address", "%s", command.http_server_address_.c_str());
        output("config directory", "%s", command.data_dir_.c_str());
      }

      void printout(NodeStart command, variables_map &vm) {
        if (vm.count("verbose") > 0) {
          printout(command);
        }
      }

      virtual void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          NodeStart command = executeCommand();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            printout(command);
            return;
          }
        printout(command, vm);
        }
      }

    };

  }
}