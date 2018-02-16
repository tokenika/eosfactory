#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <boost/process.hpp>
#include <boost/thread/thread.hpp>
#include <boost/format.hpp>
#include <boost/filesystem.hpp>

using namespace boost::process;

#define CHAIN_NODE "eosiod"
#define EOSIO_INSTALL_DIR "EOSIO_INSTALL_DIR"
#define EOSIO_GIT_DIR "EOSIO_GIT_DIR"
#define CLANG_BIN "/home/cartman/opt/wasm/bin/"
#define WASM_BIN "/home/cartman/opt/wasm/bin/"
#define BINARYEN_BIN "/home/cartman/opt/binaryen/bin/"

using namespace std;

int processEcho(string cmdLine, string& echo)
{
  ipstream pipe_stream;
  child c(cmdLine, std_out > pipe_stream);

  string line;
  stringstream ss;
  string endln;
  while (pipe_stream && getline(pipe_stream, line) && !line.empty()){
      ss << endln;
      ss << line;
      endln = "\n";
  }
  c.wait();
  echo = ss.str();    
  return c.exit_code();
}

void stopChainNode() 
{
  string pid;
  string echo;
  processEcho(string("pidof ") + CHAIN_NODE, pid);
  int count = 10;
  if (pid != "") { 
    cout <<  "killing " << CHAIN_NODE << endl;
    boost::process::system(string("kill ") + pid);

    while(pid != "" && count > 0){
      boost::this_thread::sleep( boost::posix_time::milliseconds(1000) );
      processEcho(string("pidof ") + CHAIN_NODE, pid);
      count--;
    }
  }   
  if (count > 0) {
    cout << CHAIN_NODE << " stoped.\n";
  }
  else {
    cout << "Failed to kill " << CHAIN_NODE << endl;
  }  
}

void buildContract(
  string targetDir, 
  vector<string> src, 
  vector<string> includeDir, 
  string contractName)
  {
  
  string eosLibDir = string(getenv(EOSIO_GIT_DIR)) + "/contracts";
  boost::filesystem::path workdir 
    = boost::filesystem::temp_directory_path() / boost::filesystem::unique_path();
  boost::filesystem::create_directories(workdir);

  string object = workdir.string() + "/object.o";
  string linked = workdir.string() + "/linked.bc";
  string assembly = workdir.string() + "/assembly.s";

  {
    string commandLine;
    commandLine = string(CLANG_BIN)
      + "clang " 
      + "-emit-llvm -O3 --std=c++14 --target=wasm32 -ffreestanding -nostdlib "
      + "-fno-threadsafe-statics -fno-rtti -fno-exceptions "
      + "-I " + eosLibDir + " ";

    for(string dir : includeDir){
      commandLine += "-I " + dir + " ";
    }
    for(string file : src){
      commandLine += "-c " + file + " ";
    }
    
    commandLine += "-o " + object;

    cout << commandLine << endl;
    boost::process::system(commandLine, 
      boost::process::std_out > stdout, 
      boost::process::std_err > stderr, 
      boost::process::std_in < stdin); 
  }

  {
    string commandLine;
    commandLine = string(WASM_BIN)
      + "lvm-link "
      + "-o " + linked + " "
      + object;
    cout << commandLine << endl;

    /* 
    /home/cartman/opt/wasm/bin/llvm-link 
    -o /tmp/tmp.fXlBIIodY4/linked.bc 
    /tmp/tmp.fXlBIIodY4/built/skeleton.cpp
    */
    boost::process::system(commandLine, 
      boost::process::std_out > stdout, 
      boost::process::std_err > stderr, 
      boost::process::std_in < stdin);    
  }

  {
    string commandLine;
    commandLine = string(WASM_BIN)
      + "llc "
      + "--asm-verbose=false "
      + "-o " + assembly + " "
      + linked;
    cout << commandLine << endl;      
    /* 
    /home/cartman/opt/wasm/bin/llc 
    --asm-verbose=false 
    -o /tmp/tmp.fXlBIIodY4/assembly.s 
    /tmp/tmp.fXlBIIodY4/linked.bc
    */

    boost::process::system(commandLine, 
      boost::process::std_out > stdout, 
      boost::process::std_err > stderr, 
      boost::process::std_in < stdin);   
  }

  {
    string commandLine;
    commandLine = string(BINARYEN_BIN)
      + "s2wasm "
      + "-o " + targetDir + "/" + contractName + ".wast"
      + "-s 16384 "
      + assembly;
    cout << commandLine << endl;
    /* 
    /home/cartman/opt/binaryen/bin/s2wasm 
    -o /tmp/hello.wast 
    -s 16384 
    /tmp/tmp.fXlBIIodY4/assembly.s
    */

    boost::process::system(commandLine, 
      boost::process::std_out > stdout, 
      boost::process::std_err > stderr, 
      boost::process::std_in < stdin);  
  }

  boost::filesystem::remove_all(workdir);

  // /mnt/hgfs/Workspaces/EOS/eos/build/tools/eoscpp -o /tmp/hello.wast \
  // /mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.cpp 
}

int main()
{
  buildContract(
    "/tmp/", 
    {"/mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/skeleton.cpp"},
    {"/mnt/hgfs/Workspaces/EOS/eos/contracts/skeleton/"}, 
    "xxx"
    );
  stopChainNode();
}