#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/process.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>

#include <teoslib/control/config.hpp>
#include <teoslib/control/build_contract.hpp>

using namespace std;

namespace teos {
  namespace control {

    void GenerateAbi::generateAbi(
      string types_hpp,
      string target_abi_file,
      string include_dir // comma separated list of include dirs
    )
    {
      namespace bfs = boost::filesystem;

      bfs::path types_pth(types_hpp);
      string name = types_pth.stem().string();
      bfs::path contextFolder = types_pth.parent_path();

      bfs::path target_path(target_abi_file);
      if(target_abi_file.empty()){
        target_path = contextFolder / (name + ".abi");
      } else {
        target_path = bfs::path(target_abi_file);
        if(!target_path.is_absolute()){
          target_path = contextFolder / target_path;
        }
      }

      string command_line = getSourceDir(this) 
        + "/build/programs/eosio-abigen/eosio-abigen"
        + " -extra-arg=-c -extra-arg=--std=c++14 -extra-arg=--target=wasm32"
        + " -extra-arg=-nostdinc -extra-arg=-nostdinc++ -extra-arg=-DABIGEN"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts/libc++/upstream/include"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts/musl/upstream/include"
        + " -extra-arg=-I" + getBOOST_INCLUDE_DIR(this)
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts"
        + " -extra-arg=-I" + contextFolder.string();

      if(!include_dir.empty())
      {
        vector<string> includeDirs;
        boost::split(includeDirs, include_dir, boost::algorithm::is_any_of(","));
        for (string dir : includeDirs) {
          command_line += " -extra-arg=-I" + dir;
        }
      }

      command_line = command_line
        + " -extra-arg=-fparse-all-comments"
        + " -destination-file=" + target_path.string()
        + " -verbose=0"
        + " -context=" + contextFolder.string()
        + " " + types_pth.string() + " --";
      
      //cout << command_line << endl;

      {
        namespace bp = boost::process;
        namespace pt = boost::property_tree;

        bp::ipstream err;
        bp::child c(command_line, bp::std_err > err);

        string err_line;
        string error_msg;
        while (c.running() && std::getline(err, err_line) && !err_line.empty()){
            error_msg += err_line + "\n";
        }
        c.wait();

        if(!error_msg.empty()){
          putError(error_msg);
        } else {
          pt::read_json(target_path.string(), respJson_);
          //cout << responseToString();
        }
      }
    };

    void wasmClangHelp()
    {
      string command_line;
      command_line += getWASM_CLANG(nullptr) + " --help";
      boostProcessSystem(command_line);
    }


    /*
    See a basic example of the build procedure: 
      https://gist.github.com/yurydelendik/4eeff8248aeb14ce763e#example.
    */
    void BuildContract::buildContract(
      string src, // comma separated list of source c/cpp files
      string target_wast_file,
      string include_dir // comma separated list of include dirs
    )
    {
      namespace bfs = boost::filesystem;

      bfs::path workdir= bfs::temp_directory_path()
        / bfs::unique_path();
      bfs::create_directories(workdir);
      bfs::path build(workdir / "build");
      bfs::create_directory(build);

      vector<string> srcs;
      boost::split(srcs, src, boost::algorithm::is_any_of(","));
      string objectFileList;
      bfs::path target_path(target_wast_file);

      for (string file : srcs)
      {
        bfs::path srcFile(file);
        string name = srcFile.stem().string();

        if(target_wast_file.empty()){
          target_path = name + "wast";
        } else {
          target_path = bfs::path(target_wast_file);
          if(!target_path.is_absolute()){
            target_path = srcFile.parent_path() / target_path;
          }          
        }


        bfs::path output(build / (name + ".o"));
        objectFileList += output.string() + " ";

        string command_line;
        command_line += getWASM_CLANG(this)
          + " -emit-llvm -O3  --std=c++14  --target=wasm32 -nostdinc -nostdlib"
          + " -nostdlibinc -ffreestanding -nostdlib -fno-threadsafe-statics"
          + " -fno-rtti -fno-exceptions"
          + " -I" + getSourceDir(this) + "/contracts"
          + " -I" + getSourceDir(this) + "/contracts/libc++/upstream/include"
          + " -I" + getSourceDir(this) + "/contracts/musl/upstream/include"
          + " -I" + getBOOST_INCLUDE_DIR(this)
          + " -I " + srcFile.parent_path().string();

        vector<string> includeDirs;
        boost::split(includeDirs, include_dir, boost::algorithm::is_any_of(","));
        for (string dir : includeDirs) {
          command_line += " -I " + dir;
        }

        command_line += " -c " + file
          + " -o " + output.string();

        cout << command_line << endl;
        boostProcessSystem(command_line);
      }

      string linked = workdir.string() + "/linked.bc";
      {
        string command_line;
        command_line += getWASM_LLVM_LINK(this)
          + " -o " + linked
          + " " + objectFileList;
        cout << command_line << endl;
        /*
        /home/cartman/opt/wasm/bin/llvm-link
        -o /tmp/tmp.fXlBIIodY4/linked.bc
        /tmp/tmp.fXlBIIodY4/built/skeleton.cpp
        */
        boostProcessSystem(command_line);
      }

      string assembly = workdir.string() + "/assembly.s";
      {
        string command_line;
        command_line += getWASM_LLC(nullptr)
          + " --asm-verbose=false"
          + " -o " + assembly
          + " " + linked;
        cout << command_line << endl;
        /*
        /home/cartman/opt/wasm/bin/llc
        --asm-verbose=false
        -o /tmp/tmp.fXlBIIodY4/assembly.s
        /tmp/tmp.fXlBIIodY4/linked.bc
        */
        boostProcessSystem(command_line);
      }

      {
        string command_line;
        command_line += getBINARYEN_BIN(nullptr) + "/s2wasm"
          + " -o " + target_path.string()
          + " -s 16384"
          + " " + assembly;
        cout << command_line << endl;
        /*
        /home/cartman/opt/binaryen/bin/s2wasm
        -o /tmp/hello.wast
        -s 16384
        /tmp/tmp.fXlBIIodY4/assembly.s
        */
        boostProcessSystem(command_line);
      }

      bfs::remove_all(workdir);
      /*
      /mnt/hgfs/Workspaces/EOS/eos/build/tools/eoscpp -o /tmp/hello.wast \
      /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.cpp
      */
    }

  }
}