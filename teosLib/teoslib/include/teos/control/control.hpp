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






    class NodeDeleteAllWallets : public Item
    {
    public:
      NodeDeleteAllWallets();
    };

    class NodeDeleteAllWalletsOptions : public ItemOptions<NodeDeleteAllWallets>
    {
    public:
      NodeDeleteAllWalletsOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Delete all walets in the data-dir directory.
Usage: ./teos node deleteAllWallets
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          NodeDeleteAllWallets command = NodeDeleteAllWallets();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }
        }
      }
    };

    class NodeKill : public Item
    {
    public:
      NodeKill();
    };

    class NodeKillOptions : public ItemOptions<NodeKill>
    {
    public:
      NodeKillOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Kill any running EOS node process.
Usage: ./teos node kill
)EOF";
      }

      bool checkArguments(variables_map &vm) {
        return true;
      }

      void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          NodeKill command = NodeKill();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }
        }
      }
    };


    class NodeStart : public Item
    {

    public:
      bool resync_blockchain_;
      string eosiod_exe_;
      string genesis_json_;
      string http_server_address_;
      string data_dir_;

      NodeStart(
        bool resync_blockchain = false,
        string eosiod_exe = "",
        string genesis_json = "",
        string http_server_address = "",
        string data_dir = ""
      );
    };

    class NodeStartOptions : public ItemOptions<NodeStart> 
    {
    public:
      NodeStartOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Start test EOS node.
Usage: ./teos node start [Options]
)EOF";
      }
        
      bool resync_blockchain;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("resync-blockchain", value<bool>(&resync_blockchain)
            ->default_value(false)
            , "Clear chain database and block log.");
        return od;
      }

      bool checkArguments(variables_map &vm) {
        return true;
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

      void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          NodeStart command = NodeStart(resync_blockchain);

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