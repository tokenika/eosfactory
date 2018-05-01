#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <boost/process.hpp>
#include <boost/thread/thread.hpp>
#include <boost/format.hpp>
#include <boost/filesystem.hpp>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>
#include <boost/range/iterator_range.hpp>
#include <boost/range/iterator.hpp>

#include <teoslib/control/config.hpp>
#include <teoslib/control/daemon_controls.hpp>
#include <teoslib/command/get_commands.hpp>

namespace  bp = boost::process;
using namespace std;

namespace teos {
  namespace control {

    string getPid()
    {
      bp::ipstream pipe_stream;
      string cl = string("pidof ") + getDaemonName(nullptr);
      bp::child c(cl, bp::std_out > pipe_stream);

      string line;
      stringstream ss;
      while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
        ss << line;
      }
      c.wait();
      return ss.str();
    }

    bool isWindowsUbuntu()
    {
      bp::ipstream pipe_stream;
      bp::child c(string("cat /proc/version"), bp::std_out > pipe_stream);

      string line;
      stringstream ss;
      while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
        ss << line;
      }
      c.wait();
      string resp = ss.str();
      return resp.find("Microsoft") != string::npos;
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
            boost::this_thread::sleep(boost::posix_time::milliseconds(1000));
            pid = getPid();
            count--;
          }
        }
        if (count <= 0) {
          putError(string("Failed to kill ") + getDaemonName(this) + " pid:");
        }
      }
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    //////////////////////////////////////////////////////////////////////////
    // class DaemonStart
    //////////////////////////////////////////////////////////////////////////
    
    const string DaemonStart::DO_NOT_WAIT = "DO_NOT_WAIT";
    const string DaemonStart::DO_NOT_LAUNCH = "DO_NOT_LAUNCH";

    void DaemonStart::action()
    { 

      reqJson_.put( "http-server-address", getHttpServerAddress(this));      
      if(isError_){
        return;
      }
      
      reqJson_.put("data-dir", getDataDir(this));
      if(isError_){
        return;
      }         
      
      reqJson_.put("config-dir", getConfigDir(this));
      if(isError_){
        return;
      }

      reqJson_.put("genesis-json", getGenesisJson(this));             
      if(isError_){
        return;
      }      
      
      reqJson_.put("wallet-dir", getWalletDir(this));
      if(isError_){
        return;
      }

      reqJson_.put("daemon_exe", getDaemonExe(this));
      if(isError_){
        return;
      }
      
      try{
        if(reqJson_.get("resync-blockchain", false)){
          DaemonStop();
          deleteDaemonData();
          deleteWallets();          
        } else if(!getPid().empty()){
          teos::TeosCommand tc = teos::command::GetInfo(); 
          respJson_ = tc.respJson_;
          return;
        }

        string commandLine = reqJson_.get<string>("daemon_exe")
          + " --genesis-json " + reqJson_.get<string>("genesis-json")
          + " --http-server-address " 
          + reqJson_.get<string>("http-server-address")
          + " --data-dir " + reqJson_.get<string>("data-dir")
          + " --config-dir " + reqJson_.get<string>("config-dir")
          + " --wallet-dir " + reqJson_.get<string>("wallet-dir")
          ;
        if(reqJson_.get("resync-blockchain", false)) {
          commandLine += " --resync-blockchain";
        }

        bool isWU;
        respJson_.put("command_line", commandLine);
        respJson_.put("is_windows_ubuntu", isWU = isWindowsUbuntu());

        // cout << commandLine <<endl;
        if(reqJson_.count(DO_NOT_LAUNCH) == 0) {
          if(isWU) {
            bp::spawn("cmd.exe /c start /MIN bash.exe -c " 
              "'" + commandLine + "'");
          } else {
            bp::spawn("gnome-terminal -- " + commandLine);
          }
        }
        
        // Wait until the node is operational:
        if(reqJson_.count(DO_NOT_WAIT) == 0) {
          teos::TeosCommand tc;
          teos::TeosCommand::httpAddress 
            = reqJson_.get<string>("http-server-address");
          int count = 10;
          do {
            tc = teos::command::GetInfo(); 
            respJson_ = tc.respJson_;                   
            boost::this_thread::sleep_for(boost::chrono::seconds{ 1 });
            if(count-- == 0){
              putError(tc.errorMsg());
            }
          } while (tc.isError_ && count > 0);
        }
      }
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    void DaemonStart::deleteDaemonData(){
      namespace bfs = boost::filesystem;  

      bfs::path dataDir(getDataDir(this));
      int count = 10;
      while (true)
      {
        try{
          count--;
          bfs::remove_all(dataDir / "blocks");
          bfs::remove_all(dataDir / "shared_mem");
          break;
        } catch (std::exception& e) {
          if(count){
            putError(e.what());
            break;
          }
          boost::this_thread::sleep_for(boost::chrono::seconds{ 1 });
        }
      }
    }

    void DaemonStart::deleteWallets()
    {
      namespace bfs = boost::filesystem;      
      try{
        bfs::path walletDir(getWalletDir(this));

        for (bfs::directory_entry& entry 
            : boost::make_iterator_range(
              bfs::directory_iterator(walletDir), {})) 
        {
          if (bfs::is_regular_file(entry.path())){
            bfs::remove(entry.path());
          }
        }
      } catch (std::exception& e) {
        putError(e.what());
      }  
    }
  }
}


