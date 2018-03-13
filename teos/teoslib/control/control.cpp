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

#include <teos/control/config.hpp>
#include <teos/control/control.hpp>
#include <teos/command/get_commands.hpp>

using namespace boost::process;
using namespace std;

namespace teos {
  namespace control {

    using namespace teos::config;

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

    DaemonKill::DaemonKill()
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
          isError_ = true;
          errorMsg("Failed to kill " + configValue(ConfigKeys::DAEMON_NAME));
        }
      }
      catch (std::exception& e) {
        isError_ = true;
        errorMsg(e.what());
      }
    }

    DaemonStart::DaemonStart(
      bool resync_blockchain,
      string eosiod_exe,
      string genesis_json,
      string http_server_address,
      string data_dir

    ) : eosiod_exe_(eosiod_exe.empty()
        ? configValue(ConfigKeys::EOSIO_INSTALL_DIR) + "/bin/" + configValue(ConfigKeys::DAEMON_NAME)
        : eosiod_exe)
      , genesis_json_(genesis_json.empty() ? configValue(ConfigKeys::GENESIS_JSON) 
        : genesis_json)
      , http_server_address_(http_server_address.empty() 
        ? configValue(ConfigKeys::HTTP_SERVER_ADDRESS) : http_server_address)
      , data_dir_(data_dir.empty() ? configValue(ConfigKeys::DATA_DIR) : data_dir)
      , resync_blockchain_(resync_blockchain)

    {
      try{
        DaemonKill();

        string commandLine = eosiod_exe_
          + " --" + configValue(ConfigKeys::GENESIS_JSON) + " " + genesis_json_
          + " --" + configValue(ConfigKeys::HTTP_SERVER_ADDRESS) + " " + http_server_address_
          + " --" + configValue(ConfigKeys::DATA_DIR) + " " + data_dir_;
        if (resync_blockchain_) {
          commandLine += " --resync-blockchain";
        }

        cout << commandLine <<endl;
        boost::process::system("gnome-terminal -- " + commandLine);

        // Wait until the node is operational:
        teos::command::TeosCommand tc;
        teos::command::TeosCommand::ipAddress(http_server_address_);
        int count = 10;
        do {
          boost::this_thread::sleep_for(boost::chrono::seconds{ 1 });
          tc = teos::command::GetInfo();
          if(count-- == 0){
            isError_ = true;
            errorMsg(tc.errorMsg());
          }
        } while (tc.isError_ && count > 0);
      }
      catch (std::exception& e) {
        isError_ = true;
        errorMsg(e.what());
      }
    }

    DaemonDeleteWallets::DaemonDeleteWallets()
    {
      namespace bfs = boost::filesystem;

      bfs::path p(configValue(ConfigKeys::DATA_DIR));

      try {
        for (bfs::directory_entry& entry : boost::make_iterator_range(bfs::directory_iterator(p), {})) {
          if (bfs::is_regular_file(entry.path()) 
            && entry.path().extension() == ".wallet") {
            bfs::remove(entry.path());
          }
        }
      }
      catch (std::exception& e) {
        isError_ = true;
        errorMsg(e.what());
      }
    }

  }
}


