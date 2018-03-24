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

    void setEnvironmetVariable(string name, string value)
    {
      string commandLine = "export " + name + "=" + value;
      boost::process::spawn(commandLine);
    }

    string getPid()
    {
      ipstream pipe_stream;
      child c(string("pidof ") + configValue(ConfigKeys::DAEMON_NAME), std_out > pipe_stream);

      string line;
      stringstream ss;
      while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
        ss << line;
      }
      c.wait();
      return ss.str();
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

      string commandLine;
      commandLine += configValue(ConfigKeys::EOSIO_INSTALL_DIR) + "/bin/abi_gen"
        + " -extra-arg=-c"
        + " -extra-arg=--std=c++14"
        + " -extra-arg=--target=wasm32"
        + " -extra-arg=-I" + configValue(ConfigKeys::EOSIO_INSTALL_DIR) + "/include"
        + " -extra-arg=-I" + typesHppPath.parent_path().string();

      for (string dir : includeDir) {
        commandLine += "-extra-arg=-I" + dir;
      }

      commandLine +=
        string(" -extra-arg=-fparse-all-comments")
        + " -destination-file=" + targetAbiFile
        + " -verbose=0"
        + " -context=/mnt/hgfs/Workspaces/EOS/eos/contracts/eoslib"
        + " " + typesHpp
        + " --";

      cout << commandLine << endl;
      boostProcessSystem(commandLine);

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
      commandLine += configValue(ConfigKeys::WASM_CLANG)
        + " --help";
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
        commandLine += configValue(ConfigKeys::WASM_CLANG)
          + " -emit-llvm -O3 --std=c++14 --target=wasm32 -ffreestanding -nostdlib"
          + " -fno-threadsafe-statics -fno-rtti -fno-exceptions"
          + " -I " + configValue(ConfigKeys::EOSIO_INSTALL_DIR) + "/include"
          + " -I " + srcFile.parent_path().string();

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
        commandLine += configValue(ConfigKeys::WASM_LLVM_LINK)
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
        commandLine += configValue(ConfigKeys::WASM_LLC)
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
        commandLine += configValue(ConfigKeys::BINARYEN_BIN) + "/s2wasm"
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
          putError(string("Failed to kill ") + configValue(ConfigKeys::DAEMON_NAME));
        }
      }
      catch (std::exception& e) {
        putError(e.what());
      }
    }

    void DaemonStart::action()
    {
      namespace bfs = boost::filesystem;
      if(reqJson_.get("http-server-address", "").empty())
      {
        reqJson_.put("http-server-address"
          , configValue(ConfigKeys::EOSIO_DAEMON_ADDRESS));
      }
      if(reqJson_.get("eosiod_exe", "").empty())
      {
        bfs::path path 
          = bfs::path(configValue(ConfigKeys::EOSIO_INSTALL_DIR)) 
            / "/bin/" / configValue(ConfigKeys::DAEMON_NAME);

        if(!bfs::exists(path)){
          path = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
          / "build/programs" / configValue(ConfigKeys::DAEMON_NAME)
          / configValue(ConfigKeys::DAEMON_NAME);
        }
        if(!bfs::exists(path)){
          putError("Cannot deduce the path to the daemon executable.");
        } else {
          reqJson_.put("eosiod_exe", path.string());
        }
      }

      if(reqJson_.get("genesis-json", "").empty()){
        bfs::path path(configValue(ConfigKeys::GENESIS_JSON));
        if(!bfs::exists(path)){
          path = bfs::path(configValue(ConfigKeys::EOSIO_INSTALL_DIR)) 
            / "genesis.json";
        }
        if(!bfs::exists(path)){
          path = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
            / "genesis.json";
        }
        if(!bfs::exists(path)){
          putError("Cannot deduce the path to the genesis.json file.");
        } else {
          reqJson_.put("genesis-json", path.string());
        }
      }

      if(reqJson_.get("data-dir", "").empty()){
        bfs::path path(configValue(ConfigKeys::DATA_DIR));
        if(!bfs::exists(path)){
          path = bfs::path(configValue(ConfigKeys::EOSIO_INSTALL_DIR)) 
            / "data-dir";
        }
        if(!bfs::exists(path)){
          path = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
            / "build/programs" / configValue(ConfigKeys::DAEMON_NAME) 
            / "data-dir";
        }
        if(!bfs::exists(path)){
          putError("Cannot deduce the path to the data-dir directory.");
        } else {
          reqJson_.put("data-dir", path.string());
        }
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

        string commandLine = reqJson_.get<string>("eosiod_exe")
          + " --genesis-json " + reqJson_.get<string>("genesis-json")
          + " --http-server-address " + reqJson_.get<string>("http-server-address")
          + " --data-dir " + reqJson_.get<string>("data-dir");
        if(reqJson_.get("resync-blockchain", false)) {
          commandLine += " --resync-blockchain";
        }

        //cout << commandLine <<endl;
        boost::process::system("gnome-terminal -- " + commandLine);

        if(reqJson_.get("wait", true))
        {
          // Wait until the node is operational:
          teos::TeosCommand tc;
          teos::TeosCommand::httpAddress = reqJson_.get<string>("http-server-address");
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

    void DaemonDeleteWallets::action()
    {
      namespace bfs = boost::filesystem;
      bfs::path dataDir;
      if(reqJson_.get("data-dir", "").empty())
      {
        dataDir = bfs::path(configValue(ConfigKeys::DATA_DIR));
        if(!bfs::exists(dataDir)){
          dataDir = bfs::path(configValue(ConfigKeys::EOSIO_INSTALL_DIR)) 
            / "data-dir";
        }
        if(!bfs::exists(dataDir)){
          dataDir = bfs::path(configValue(ConfigKeys::EOSIO_SOURCE_DIR))
            / "build/programs" / configValue(ConfigKeys::DAEMON_NAME) 
            / "data-dir";
        }
      } else
      {
        dataDir = bfs::path(reqJson_.get("data-dir", ""));
      }
      if(!bfs::exists(dataDir)){
        putError("Cannot find the path to the data-dir directory.");
        return;
      } 

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


