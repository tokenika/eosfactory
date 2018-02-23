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

#include <teos/control/config.hpp>
#include <teos/control/control.hpp>
#include <teos/command/get_commands.hpp>

using namespace boost::process;
using namespace std;

int processEcho(string cmdLine, string& echo)
{
  ipstream pipe_stream;
  child c(cmdLine, std_out > pipe_stream);

  string line;
  stringstream ss;
  string endln;
  while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
    ss << endln;
    ss << line;
    endln = "\n";
  }
  c.wait();
  echo = ss.str();
  return c.exit_code();
}

namespace teos {
  namespace control {

    using namespace teos::config;

    void setEnvironmetVariable(string name, string value)
    {
      string commandLine = "export " + name + "=" + value;
      boost::process::spawn(commandLine);
    }

    void startChainNode(
      string genesis_json,
      string http_server_address,
      string data_dir,
      bool resync_blockchain
    )
    {
      killChainNode();

      string commandLine = (teos::config::EOSIO_INSTALL_DIR() / "bin"
        / CHAIN_NODE()).string()
        + " --genesis-json "
        + genesis_json == "" ? GENESIS_JSON().string() : genesis_json
        + " --http-server-address "
        + http_server_address == "" ? HTTP_SERVER_ADDRESS() : http_server_address
        + " --data-dir "
        + data_dir == "" ? DATA_DIR().string() : data_dir;
      if (resync_blockchain) {
        commandLine +=" --resync-blockchain";
      }

      //cout << commandLine << endl;
      boost::process::spawn(commandLine);

      // Wait until the node is operational:
      teos::command::TeosCommand tc;
      do {
        boost::this_thread::sleep_for(boost::chrono::seconds{ 1 });
        tc = teos::command::GetInfo();
      } while (tc.isError_);
    }

    void killChainNode()
    {
      string pid;
      string processName = teos::config::CHAIN_NODE();
      processEcho(string("pidof ") + processName, pid);
      int count = 10;
      if (!pid.empty()) {
        cout << "killing " << processName << endl;
        boost::process::system(string("kill ") + pid);

        while (!pid.empty() && count > 0) {
          boost::this_thread::sleep(boost::posix_time::milliseconds(1000));
          processEcho(string("pidof ") + processName, pid);
          count--;
        }
      }
      if (count > 0) {
        cout << processName << " stoped.\n";
      }
      else {
        cout << "Failed to kill " << processName << endl;
      }
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
      commandLine += (teos::config::EOSIO_INSTALL_DIR()
        / "bin/abi_gen").string()
        + " -extra-arg=-c"
        + " -extra-arg=--std=c++14"
        + " -extra-arg=--target=wasm32"
        + " -extra-arg=-I" + (teos::config::EOSIO_INSTALL_DIR() / "include").string()
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
      commandLine += teos::config::WASM_CLANG().string()
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
        commandLine += teos::config::WASM_CLANG().string()
          + " -emit-llvm -O3 --std=c++14 --target=wasm32 -ffreestanding -nostdlib"
          + " -fno-threadsafe-statics -fno-rtti -fno-exceptions"
          + " -I " + (teos::config::EOSIO_INSTALL_DIR() / "include").string()
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
        commandLine += teos::config::WASM_LLVM_LINK().string()
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
        commandLine += teos::config::WASM_LLC().string()
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
        commandLine += (teos::config::BINARYEN_BIN() / "s2wasm").string()
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

  }
}


