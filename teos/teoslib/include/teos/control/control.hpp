#pragma once

#include <string>
#include <vector>

#include <teos/item.hpp>

using namespace std;

namespace teos {
  namespace control {

    class DaemonDeleteWallets : public Item
    {
    public:
      DaemonDeleteWallets();
    };

    class DaemonDeleteWalletsOptions : public ItemOptions<DaemonDeleteWallets>
    {
    public:
      DaemonDeleteWalletsOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

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
          DaemonDeleteWallets command = DaemonDeleteWallets();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }
        }
      }
    };

    class DaemonKill : public Item
    {
    public:
      DaemonKill();
    };

    class DaemonKillOptions : public ItemOptions<DaemonKill>
    {
    public:
      DaemonKillOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

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
          DaemonKill command = DaemonKill();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }
        }
      }
    };


    class DaemonStart : public Item
    {

    public:
      bool resync_blockchain_;
      string eosiod_exe_;
      string genesis_json_;
      string http_server_address_;
      string data_dir_;

      DaemonStart(
        bool resync_blockchain = false,
        string eosiod_exe = "",
        string genesis_json = "",
        string http_server_address = "",
        string data_dir = ""
      );
    };

    class DaemonStartOptions : public ItemOptions<DaemonStart> 
    {
    public:
      DaemonStartOptions(int argc, const char **argv) : ItemOptions(argc, argv) {}

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

      void printout(DaemonStart command) {
        output("eosiod exe file", "%s", command.eosiod_exe_.c_str());
        output("genesis state file", "%s", command.genesis_json_.c_str());
        output("server address", "%s", command.http_server_address_.c_str());
        output("config directory", "%s", command.data_dir_.c_str());
      }

      void printout(DaemonStart command, variables_map &vm) {
        if (vm.count("verbose") > 0) {
          printout(command);
        }
      }

      void parseGroupVariablesMap(variables_map& vm) {
        if (checkArguments(vm)) {
          DaemonStart command = DaemonStart(resync_blockchain);

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