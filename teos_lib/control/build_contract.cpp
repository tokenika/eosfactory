#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include <boost/filesystem.hpp>

#include <teoslib/control/config.hpp>
#include <teoslib/control/build_contract.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>

using namespace std;

namespace teos {
  namespace control {

    void generateAbi(
      string typesHpp,
      string targetAbiFile,
      string includeDir // comma separated list of include dirs
    )
    {
      namespace bfs = boost::filesystem;

      bfs::path typesHppPath(typesHpp);
      string name = typesHppPath.stem().string();
      bfs::path contextFolder = path.parent().string();
      bfs::path output(targetAbiFile);
      if(targetAbiFile.empty()){
        output = contextFolder / (name + ".abi")
      } else {
        output = bfs::path(targetAbiFile);
        if(!output.is_absolute()){
          output = contextFolder / output;
        }
      }

      string commandLine = getSourceDir(this) 
        + "/build/programs/eosio-abigen/eosio-abigen"
        + " -extra-arg=-c -extra-arg=--std=c++14 -extra-arg=--target=wasm32"
        + " -extra-arg=-nostdinc -extra-arg=-nostdinc++ -extra-arg=-DABIGEN"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts/libc++/upstream/include"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts/musl/upstream/include"
        + " -extra-arg=-I" + getBOOST_INCLUDE_DIR(this)
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts"
        + " -extra-arg=-I" + contextFolder.string();

      if(!includeDir.empty())
      {
        vector<string> includeDirs;
        boost::split(includeDirs, includeDir, boost::algorithm::is_any_of(","));
        for (string dir : includeDirs) {
          commandLine += " -extra-arg=-I" + dir;
        }
      }

      commandLine
        += " -extra-arg=-fparse-all-comments"
        + " -destination-file=" + outname.string()
        + " -verbose=0"
        + " -context=" + contextFolder
        + typesHppPath.string() + " --";

      boostProcessSystem(commandLine);
    };

    void wasmClangHelp()
    {
      string commandLine;
      commandLine += getWASM_CLANG(nullptr) + " --help";
      boostProcessSystem(commandLine);
    }


    /*
    See a basic example of the build procedure: https://gist.github.com/yurydelendik/4eeff8248aeb14ce763e#example.
    */
    void BuildContract::buildContract(
      string src, // comma separated list of source c/cpp files
      string targetWastFile,
      string includeDir // comma separated list of include dirs
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
      for (string file : srcs)
      {
        bfs::path srcFile(file);
        string name = srcFile.stem().string();

        bfs::path outputWast(targetWastFile)
        if(outputWast.empty()){
          outputWast = name + "wast";
        } else {
          outputWast = bfs::path(targetAbiFile);
          if(!outputWast.is_absolute()){
            outputWast = contextFolder / outputWast;
          }          
        }


        bfs::path output(build / (name + ".o"));
        objectFileList += output.string() + " ";

        string commandLine;
        commandLine += getWASM_CLANG(this)
          + " -emit-llvm -O3  --std=c++14  --target=wasm32 -nostdinc -nostdlib"
          + " -nostdlibinc -ffreestanding -nostdlib -fno-threadsafe-statics"
          + " -fno-rtti -fno-exceptions"
          + " -I" + getSourceDir(this) + "/contracts"
          + " -I" + getSourceDir(this) + "/contracts/libc++/upstream/include"
          + " -I" + getSourceDir(this) + "/contracts/musl/upstream/include"
          + " -I" + getBOOST_INCLUDE_DIR(this)
          + " -I " + srcFile.parent_path().string();

        vector<string> includeDirs;
        boost::split(includeDirs, includeDir, boost::algorithm::is_any_of(","));
        for (string dir : includeDirs) {
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
        commandLine += getWASM_LLVM_LINK(this)
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
        commandLine += getWASM_LLC(nullptr)
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
        commandLine += getBINARYEN_BIN(nullptr) + "/s2wasm"
          + " -o " + outputWast.string()
          + " -s 16384"
          + " " + assembly;
        cout << commandLine << endl;
        /*
        /home/cartman/opt/binaryen/bin/s2wasm
        -o /tmp/hello.wast
        -s 16384
        /tmp/tmp.fXlBIIodY4/assembly.s
        */
        boostProcessSystem(commandLine);
      }

      bfs::remove_all(workdir);
      /*
      /mnt/hgfs/Workspaces/EOS/eos/build/tools/eoscpp -o /tmp/hello.wast \
      /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.cpp
      */
    }

  }
}