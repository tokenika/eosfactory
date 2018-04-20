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
      boost::filesystem::path typesHppPath(typesHpp);
      string name = typesHppPath.stem().string();

      // string commandLine;
      // commandLine += configValue( "/bin/abi_gen" )
      //   + " -extra-arg=-c"
      //   + " -extra-arg=--std=c++14"
      //   + " -extra-arg=--target=wasm32"
      //   + " -extra-arg=-I" + configValue("/include"
      //   + " -extra-arg=-I" + typesHppPath.parent_path().string();

      // vector<string> includeDirs
      // boost::split(includeDirs, includeDir, boost::is_any_of(","));
      // for (string dir : includeDirs) {
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
    TeosControl BuildContract::buildContract(
      string src, // comma separated list of source c/cpp files
      string targetWastFile,
      string includeDir // comma separated list of include dirs
    )
    {
      boost::filesystem::path workdir
        = boost::filesystem::temp_directory_path()
        / boost::filesystem::unique_path();
      boost::filesystem::create_directories(workdir);
      boost::filesystem::path build(workdir / "build");
      boost::filesystem::create_directory(build);

      vector<string> srcs;
      boost::split(srcs, src, boost::algorithm::is_any_of(","));
      string objectFileList;
      for (string file : srcs)
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
        commandLine += getWASM_LLVM_LINK(nullptr)
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