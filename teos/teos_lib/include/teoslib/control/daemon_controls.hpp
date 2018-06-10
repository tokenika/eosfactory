/**
 * @file daemon_controls.hpp
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

#include <string>

#include <teoslib/control.hpp>

using namespace std;

namespace teos {
  namespace control {

    /**
     * @ingroup teoslib_raw
     * @brief Kill the running local NODEOS process.
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
        return R"(
Kill any running EOS node process.
Usage: ./teos node kill
)";
      }

      TeosControl executeCommand() {
        return DaemonStop();
      }

      void printout(TeosControl command, variables_map &vm){
        sharp() << "Daemon is stopped." << endl;
      }
    };

    /**
     * @ingroup teoslib_raw
     * @brief Start a local NODEOS node, if no one is running.
     * 
     */
    class DaemonStart : public TeosControl
    {
      string nameSuffix_;
      bool configure();
      void launch();
      void wait();
      void action();
      void deleteWallets();
      void deleteDaemonData();
    public:
      static const string DO_NOT_LAUNCH;

      DaemonStart(
        bool clearBlockchain = false,
        string nameSuffix = "11") : nameSuffix_(nameSuffix)
      {
        reqJson_.put("delete-all-blocks", clearBlockchain);
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
        return R"(
Start test EOS node.
Usage: ./teos node start [Options]
)";
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
          reqJson_.put("delete-all-blocks", true);
        } else {
          reqJson_.put("delete-all-blocks", false);
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
        if(command.reqJson_.count(DaemonStart::DO_NOT_LAUNCH) == 0) {
          output("head block number", "%s", command.get<string>("head_block_num").c_str());
          output("head block time", "%s", command.get<string>("head_block_time").c_str());
        }
      }
    };
  }
}