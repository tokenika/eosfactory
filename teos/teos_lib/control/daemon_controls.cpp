#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>
#include <boost/process.hpp>
#include <boost/format.hpp>
#include <boost/filesystem.hpp>
#include <boost/chrono.hpp>
#include <boost/range/iterator_range.hpp>
#include <boost/range/iterator.hpp>

#include <teoslib/control/config.hpp>
#include <teoslib/control/daemon_controls.hpp>
#include <teoslib/command/get_commands.hpp>
#include <teoslib/utilities.hpp>

namespace  bp = boost::process;
using namespace std;
using namespace std::this_thread; // sleep_for, sleep_until
using namespace std::chrono; // nanoseconds, system_clock, seconds

namespace teos {
  namespace control {

    string getPid()
    {
      bp::ipstream pipe_stream;
      //string cl = string("pidof ") + getDaemonName(nullptr);
      string cl = string("pgrep ") + getDaemonName(nullptr);
      bp::child c(cl, bp::std_out > pipe_stream);

      string line;
      stringstream ss;
      while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
        ss << line;
      }
      c.wait();
      return ss.str();
    }

    //////////////////////////////////////////////////////////////////////////
    // class DaemonIsRunning
    //////////////////////////////////////////////////////////////////////////
    DaemonIsRunning::DaemonIsRunning()
    {
      try {
        string pid = getPid();
        int count = 10;
        if (!pid.empty()) {
          respJson_.put("daemon_pid", pid);
        }
        else {
          respJson_.put("daemon_pid", "");
        }
      }
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    //////////////////////////////////////////////////////////////////////////
    // class DaemonStop
    //////////////////////////////////////////////////////////////////////////
    DaemonStop::DaemonStop()
    {
      try {
        string pid = getPid();
        int count = 10;
        if (!pid.empty()) {
          bp::system(string("kill ") + pid);

          while (!pid.empty() && count > 0) {
            sleep_for(seconds(1));            
            pid = getPid();
            count--;
          }
        }
        if (count <= 0) {
          putError(string("Failed to kill ") + getDaemonName(this) 
            + ". Pid is " + pid);
        }
      }
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    //////////////////////////////////////////////////////////////////////////
    // class DaemonStart
    //////////////////////////////////////////////////////////////////////////
    
    const string DaemonStart::DO_NOT_LAUNCH = "DO_NOT_LAUNCH";
    
    void DaemonStart::action()
    {
      if(configure() && reqJson_.get(DO_NOT_LAUNCH, 0) <= 0)
      {
        launch();
        wait();        
      }
    }

    bool DaemonStart::configure()
    {
      reqJson_.put( "http-server-address", getHttpServerAddress(this));      
      if(isError_){
        return false;
      }
      
      reqJson_.put("data-dir", getDataDir(this));
      if(isError_){
        return false;
      }         
      
      reqJson_.put("config-dir", getConfigDir(this));
      if(isError_){
        return false;
      }

      reqJson_.put("genesis-json", getGenesisJson(this));             
      if(isError_){
        return false;
      }      

      reqJson_.put("daemon_exe", getDaemonExe(this));
      if(isError_){
        return false;
      }
      
      try{
        if(reqJson_.get("delete-all-blocks", false)){
          DaemonStop(); 
        } else if(!getPid().empty()){
          reqJson_.put(DO_NOT_LAUNCH, 1);
          respJson_.put(DO_NOT_LAUNCH, 1);
          respJson_.put("EOSIO_DAEMON_ADDRESS", getHttpServerAddress(this));          
          return false;
        }

        string args = string("")
          + " --http-server-address " 
          + reqJson_.get<string>("http-server-address")
          + " --data-dir " + reqJson_.get<string>("data-dir")
          + " --config-dir " + reqJson_.get<string>("config-dir")
          + " --chain-state-db-size-mb " + getMemorySizeMb()
          + " --contracts-console"
          + " --verbose-http-errors"
          ;
        if(reqJson_.get("delete-all-blocks", false)) {
          args += " --genesis-json " + reqJson_.get<string>("genesis-json")
          + " --delete-all-blocks";
        }
        string commandLine = reqJson_.get<string>("daemon_exe") + args;

        reqJson_.put("command_line", commandLine);
        reqJson_.put("exe", reqJson_.get<string>("daemon_exe"));
        reqJson_.put("args", args);

        respJson_.put("command_line", commandLine);
        respJson_.put("exe", reqJson_.get<string>("daemon_exe"));
        respJson_.put("args", args);
        respJson_.put("uname", uname());
        respJson_.put("is_windows_ubuntu", isWindowsUbuntu());
        respJson_.put("EOSIO_DAEMON_ADDRESS", getHttpServerAddress(this));
      } catch (std::exception& e) {
        putError(e.what(), SPOT);
      }
      return true;
    }

    void DaemonStart::launch()
    { 
      // cout << requestToString(false) << endl;
      cout << reqJson_.get<string>("command_line") <<endl;
      try{
        if(isWindowsUbuntu()) {
          bp::spawn("cmd.exe /c start /MIN bash.exe -c " 
            "'" + reqJson_.get<string>("command_line") + "'");
        } else {
          if(uname() == DARWIN){
            // string cl = "open -a " + reqJson_.get<string>("daemon_exe")
            //   + " --args " + reqJson_.get<string>("args");
            // cout << endl << cl << endl;
            bp::spawn(
              "open -a " + reqJson_.get<string>("daemon_exe") 
              + " --args " + reqJson_.get<string>("args"));
          } else{
            bp::spawn("gnome-terminal -- " + reqJson_.get<string>("command_line"));
          }
        }

      } catch (std::exception& e) {
        putError(e.what());
      }      
    }   

    void DaemonStart::wait()
    { 
      // Wait until the node is operational:
      teos::TeosCommand tc; 
      int count = 10;
      int head_block_num = 2;
      bool OK = false;
      for(;;)
      {
        sleep_for(seconds(1));
        tc = teos::command::GetInfo();
        OK = tc.respJson_.get("head_block_num", -1) >= head_block_num;

        if(OK)
        {
          respJson_ = tc.respJson_; 
          break;          
        }
        if( count-- <= 0)
        {
          if(tc.isError_) {
            putError(tc.errorMsg());
          } else
          {
            putError("timeout");
          }
          break;
        }
      }
    }
  }
}


