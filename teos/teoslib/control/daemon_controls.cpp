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

using namespace boost::process;
using namespace std;

namespace teos {
  namespace control {

    string getPid()
    {
      ipstream pipe_stream;
      child c(string("pidof ") + getDaemonName() 
        , std_out > pipe_stream);

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
      ipstream pipe_stream;
      child c(string("cat /proc/version"), std_out > pipe_stream);

      string line;
      stringstream ss;
      while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
        ss << line;
      }
      c.wait();
      string resp = ss.str();
      return resp.find("Microsoft") != string::npos;
    }

    void boostProcessSystem(string commandLine) {
      boost::process::system(commandLine,
        boost::process::std_out > stdout,
        boost::process::std_err > stderr,
        boost::process::std_in < stdin);
    }

    void generateAbi(
      string typesHpp,
      string targetAbiFile,
      vector<string> includeDir // list of header files  
    )
    {
      boost::filesystem::path typesHppPath(typesHpp);
      string name = typesHppPath.stem().string();

      // string commandLine;
      // commandLine += configValue( "/bin/abi_gen" )
      //   + " -extra-arg=-c"
      //   + " -extra-arg=--std=c++14"
      //   + " -extra-arg=--target=wasm32"
      //   + " -extra-arg=-I" + configValue("/include"
      //   + " -extra-arg=-I" + typesHppPath.parent_path().string();

      // for (string dir : includeDir) {
      //   commandLine += "-extra-arg=-I" + dir;
      // }

      // commandLine +=
      //   string(" -extra-arg=-fparse-all-comments")
      //   + " -destination-file=" + targetAbiFile
      //   + " -verbose=0"
      //   + " -context=/mnt/hgfs/Workspaces/EOS/eos/contracts/eoslib"
      //   + " " + typesHpp
      //   + " --";

      // cout << commandLine << endl;
      // boostProcessSystem(commandLine);

      /*
      call:
      /mnt/hgfs/Workspaces/EOS/eos/build/tools/eoscpp
      -g /tmp/skeleton.abi
      /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.hpp

      context folder:
      /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton

      /mnt/hgfs/Workspaces/EOS/eos/build/install//bin/abi_gen
      -extra-arg=-c
      -extra-arg=--std=c++14
      -extra-arg=--target=wasm32
      -extra-arg=-I/mnt/hgfs/Workspaces/EOS/eos/build/install//include
      -extra-arg=-I/mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton
      -extra-arg=-fparse-all-comments
      -destination-file=/tmp/skeleton.abi
      -verbose=0
      -context=/mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton
      /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.hpp
      --
      */
    }

    void wasmClangHelp()
    {
      string commandLine;
      commandLine += getWASM_CLANG() + " --help";
      boostProcessSystem(commandLine);
    }

    /*
    See a basic example of the build procedure: https://gist.github.com/yurydelendik/4eeff8248aeb14ce763e#example.
    */
    void buildContract(
      vector<string> src, // list of source c/cpp files
      string targetWastFile,
      vector<string> includeDir
    ) // list of header files
    {

      boost::filesystem::path workdir
        = boost::filesystem::temp_directory_path()
        / boost::filesystem::unique_path();
      boost::filesystem::create_directories(workdir);
      boost::filesystem::path build(workdir / "build");
      boost::filesystem::create_directory(build);

      string objectFileList;
      for (string file : src)
      {
        boost::filesystem::path srcFile(file);

        string name = srcFile.stem().string();
        boost::filesystem::path output(build / (name + ".o"));
        objectFileList += output.string() + " ";

        string commandLine;
        // commandLine += configValue(ConfigKeys::WASM_CLANG)
        //   + " -emit-llvm -O3 --std=c++14 --target=wasm32 -ffreestanding -nostdlib"
        //   + " -fno-threadsafe-statics -fno-rtti -fno-exceptions"
        //   + " -I " + configValue("/include"
        //   + " -I " + srcFile.parent_path().string();

        for (string dir : includeDir) {
          commandLine += " -I " + dir;
        }

        commandLine += " -c " + file
          + " -o " + output.string();

        cout << commandLine << endl;
        boostProcessSystem(commandLine);
      }

      string linked = workdir.string() + "/linked.bc";
      {
        string commandLine;
        commandLine += getWASM_LLVM_LINK()
          + " -o " + linked
          + " " + objectFileList;
        cout << commandLine << endl;
        /*
        /home/cartman/opt/wasm/bin/llvm-link
        -o /tmp/tmp.fXlBIIodY4/linked.bc
        /tmp/tmp.fXlBIIodY4/built/skeleton.cpp
        */
        boostProcessSystem(commandLine);
      }

      string assembly = workdir.string() + "/assembly.s";
      {
        string commandLine;
        commandLine += getWASM_LLC()
          + " --asm-verbose=false"
          + " -o " + assembly
          + " " + linked;
        cout << commandLine << endl;
        /*
        /home/cartman/opt/wasm/bin/llc
        --asm-verbose=false
        -o /tmp/tmp.fXlBIIodY4/assembly.s
        /tmp/tmp.fXlBIIodY4/linked.bc
        */
        boostProcessSystem(commandLine);
      }

      {
        string commandLine;
        commandLine += getBINARYEN_BIN() + "/s2wasm"
          + " -o " + targetWastFile
          + " -s 16384"
          + " " + assembly;
        //cout << commandLine << endl;
        /*
        /home/cartman/opt/binaryen/bin/s2wasm
        -o /tmp/hello.wast
        -s 16384
        /tmp/tmp.fXlBIIodY4/assembly.s
        */
        boostProcessSystem(commandLine);
      }

      boost::filesystem::remove_all(workdir);
      /*
      /mnt/hgfs/Workspaces/EOS/eos/build/tools/eoscpp -o /tmp/hello.wast \
      /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.cpp
      */
    }

    DaemonStop::DaemonStop()
    {
      try {
        string pid = getPid();
        int count = 10;
        if (!pid.empty()) {
          boost::process::system(string("kill ") + pid);

          while (!pid.empty() && count > 0) {
            boost::this_thread::sleep(boost::posix_time::milliseconds(1000));
            pid = getPid();
            count--;
          }
        }
        if (count < 0) {
          putError(string("Failed to kill ") + getDaemonName());
        }
      }
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    void DaemonStart::action()
    {
      reqJson_.put(
        "http-server-address"
        , getHttpServerAddress(reqJson_.get("http-server-address", ""))) ;      
      if(isError_){
        return;
      }
      
      reqJson_.put(
        "daemon_exe"
        , getDaemonExe(this, reqJson_.get("daemon_exe", "")));
      if(isError_){
        return;
      }
      
      reqJson_.put(
        "genesis-json"
        , getGenesisJson(this, reqJson_.get("genesis-json", "")));             
      if(isError_){
        return;
      }
      
      reqJson_.put(
        "config-dir"
        , getConfigDir(this, reqJson_.get("config-dir", "")));
      if(isError_){
        return;
      }

      reqJson_.put(
        "data-dir"
        , getDataDir(this, reqJson_.get("data-dir", "")));
      if(isError_){
        return;
      }      

      reqJson_.put(
        "wallet-dir"
        , getWalletDir(this, reqJson_.get("wallet-dir", "")));
      if(isError_){
        return;
      }

      try{
        if(reqJson_.get("resync-blockchain", false)){
          DaemonStop();
          DaemonDeleteWallets();          
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

        cout << commandLine <<endl;

        if(isWindowsUbuntu()) {
          boost::process::system("cmd.exe /c start bash.exe -c " 
            "'" + commandLine + "'");
        } else {
          boost::process::system("gnome-terminal -- " + commandLine);
        }
        
        // Wait until the node is operational:
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
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    void DaemonDeleteWallets::action()
    {
      namespace bfs = boost::filesystem;
      bfs::path dataDir = getConfigDir(this, reqJson_.get("config-dir", ""));
      
      int count = 0; 
      try{
        if(!reqJson_.get("name", "").empty()){
          bfs::path walletFile = dataDir / (reqJson_.get("name", "") + ".wallet");
          if(bfs::exists(walletFile)){
            bfs::remove(walletFile);
            count++;            
          }
        } else
        {
          for (bfs::directory_entry& entry 
              : boost::make_iterator_range(bfs::directory_iterator(dataDir), {})) 
            {
            if (bfs::is_regular_file(entry.path()) 
              && entry.path().extension() == ".wallet") {
              bfs::remove(entry.path());
              count++;
            }
          }       
        }
      } catch (std::exception& e) {
        putError(e.what());
      }
      respJson_.put("count", count);      
    }

    void DaemonDeleteWalletsOptions::printout(TeosControl command, variables_map &vm) {
      output("deleted wallet count", "%d", command.get<int>("count"));
    }
  }
}


