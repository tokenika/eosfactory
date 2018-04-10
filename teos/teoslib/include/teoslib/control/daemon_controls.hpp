#pragma once

#include <string>
#include <vector>

#include <teoslib/control.hpp>

using namespace std;

namespace teos {
  namespace control {

    /**
     * @brief Delete opened locally walets.
     */
    class DaemonDeleteWallets : public  TeosControl
    {
      void action();
      public:
        static const char* DELETE_ALL;
        static const char* WALLET_EXT;
        DaemonDeleteWallets(string name = "")
        {
          reqJson_.put("name", name);
          action();
        }

        DaemonDeleteWallets(ptree reqJson) : TeosControl(reqJson){
          action();
        }
    };

    /**
     * @brief Delete locally opened walets,#include <teoslib/control/config.hpp>
     * Usage: ./teos daemon delete_wallets
     */
    class DaemonDeleteWalletsOptions : public ControlOptions
    {
    public:
      DaemonDeleteWalletsOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Delete locally opened walets.
Usage: ./teos [] daemon delete_wallets [name]
)EOF";
      }

      string name;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name,n", value<string>(&name)
            ->default_value(DaemonDeleteWallets::DELETE_ALL)
            ,"The name of the wallet. Default is 'all names'.");

        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }

      bool checkArguments(variables_map &vm) {
        if (vm.count("name")) {
          reqJson_.put("name", name);
        }      
        return true;
      }

      TeosControl executeCommand() {
        return DaemonDeleteWallets(reqJson_);
      }  

      void printout(TeosControl command, variables_map &vm); 

    };

    /**
     * @brief Kill a running EOS node process.
     */
    class DaemonStop : public TeosControl
    {
    public:
      DaemonStop();
    };

    class DaemonStopOptions : public ControlOptions
    {
    public:
      DaemonStopOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Kill any running EOS node process.
Usage: ./teos node kill
)EOF";
      }

      TeosControl executeCommand() {
        return DaemonStop();
      }

      void printout(TeosControl command, variables_map &vm){
        sharp() << "Daemon is stopped." << endl;
      }
    };

    /**
     * @brief Start a test EOSIO daemon if no one is running.
     * 
     */
    class DaemonStart : public TeosControl
    {
      void action();

    public:
      static const string DO_NOT_WAIT;
      static const string DO_NOT_LAUNCH;

      DaemonStart(
        bool resync_blockchain = false)
      {
        reqJson_.put("resync-blockchain", resync_blockchain);
        action();
      }

      DaemonStart(ptree reqJson){
        reqJson_ = reqJson;
        action();
      }
    };

    class DaemonStartOptions : public ControlOptions 
    {
    public:
      DaemonStartOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Start test EOS node.
Usage: ./teos node start [Options]
)EOF";
      }

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("clear,c", "Clear chain database and block log.");
            
        return od;
      }

      bool checkArguments(variables_map &vm) {
        bool ok = true;
        if(vm.count("clear")){
          reqJson_.put("resync-blockchain", true);
        } else {
          reqJson_.put("resync-blockchain", false);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return DaemonStart(reqJson_);
      } 

      void printout(TeosControl command, variables_map &vm) {
        output("nodeos exe file", "%s"
          , command.reqJson_.get<string>("daemon_exe").c_str());
        output("genesis state file", "%s"
          , command.reqJson_.get<string>("genesis-json").c_str());
        output("server address", "%s"
          , command.reqJson_.get<string>("http-server-address").c_str());
        output("config directory", "%s"
          , command.reqJson_.get<string>("config-dir").c_str());
        output("wallet directory", "%s"
          , command.reqJson_.get<string>("wallet-dir").c_str());
        if(command.reqJson_.count(DaemonStart::DO_NOT_WAIT) == 0) {
          output("head block number", "%s", command.get<string>("head_block_num").c_str());
          output("head block time", "%s", command.get<string>("head_block_time").c_str());
        }
      }
    };
  }
}