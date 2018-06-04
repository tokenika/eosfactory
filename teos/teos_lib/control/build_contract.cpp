#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/process.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>

#include <teoslib/control/config.hpp>
#include <teoslib/control/build_contract.hpp>
#include <teoslib/utilities.hpp>

using namespace std;

namespace teos {
  namespace control {
  
    // File structure relative to the context dir   
    static const string templContractsDir = "templates/contracts";
    static const string contractsDir = "contracts";

    bool process(string command_line, TeosControl* teos_control)
    {
      try{
        namespace bp = boost::process;

        bp::ipstream err;
        bp::child c(command_line, bp::std_err > err);

        string err_line;
        string error_msg;
        while (c.running() && std::getline(err, err_line) && !err_line.empty()){
            error_msg += err_line + "\n";
        }
        c.wait();

        if(!error_msg.empty() && error_msg.find("error") != string::npos){
          teos_control->putError(error_msg);
          return false;
        }
      } catch (exception &e){
        teos_control->putError(e.what());
        return false;
      }  

      return true;
    }

    vector<string> files(string comma_list, set<string> extensions)
    {
      namespace bfs = boost::filesystem;
            
      vector<string> srcs;
      try{
        bfs::path src_path(wslMapWindowsLinux(comma_list));
        if(bfs::is_directory(src_path)) {
          for (bfs::directory_entry& entry 
            : boost::make_iterator_range(
              bfs::directory_iterator(src_path), {})) 
            {
            if (bfs::exists(entry.path()) 
              && bfs::is_regular_file(entry.path())) 
            {
              bfs::path file = entry.path();
              if(extensions.count(file.extension().string())){
                srcs.push_back(file.string());
              }
            }
          } 
        }
      } catch(...){}

      if(srcs.empty()) 
      {
        vector<string> temp;
        boost::split(temp, comma_list, boost::algorithm::is_any_of(","));

        for(const string& comp: temp){
          bfs::path file(comp);
          if(extensions.count(file.extension().string())){
            srcs.push_back(wslMapWindowsLinux(comp));
          }
        }  
      }
      return srcs;      
    }

    void DeleteContract::deleteContract(string contract_dir)
    {
      namespace bfs = boost::filesystem;
      try{
        bfs::path contract_path(getContractDir(this, contract_dir));
        if(isError_){
          return;
        }
        if(bfs::exists(contract_path) && bfs::is_directory(contract_path))
        {
          cout << "deleteContract: " << contract_path.string() << endl;
          // bfs::remove_all(contract_path);
        }
      } catch(exception& e){
        putError(e.what());
        return;
      }
    }

    #define TEMPLATE_TOKEN string("CONTRACT_NAME")

    void BootstrapContract::copy(
      boost::filesystem::path inTemplate,
      boost::filesystem::path inContract,
      string name
      )
    {
      namespace bfs = boost::filesystem; 

      if (bfs::is_regular_file(inTemplate) && !bfs::exists(inContract))
      {       
        string contents;        
        try{
          bfs::ifstream in(inTemplate);
          stringstream ss;
          ss << in.rdbuf();
          in.close();
          contents = ss.str();
          boost::replace_all(contents, "@" + TEMPLATE_TOKEN + "@", name);
          boost::replace_all(contents, "${PYTHONPATH}", getenv("PYTHONPATH"));
        } catch(exception& e){
          putError(e.what());
          return;
        }
        try{
          bfs::ofstream ofs (inContract);
          ofs << contents << endl;
          ofs.flush();
          ofs.close();          
        } catch (bfs::filesystem_error &e){
          putError(e.what());
          return;
        }         
      } else
      {    
        try{
          if(!bfs::exists(inContract)) {
            bfs::create_directory(inContract);          
          }
        } catch (bfs::filesystem_error &e){
          putError(e.what());
          return;
        }  
      }
    }

    void BootstrapContract::bootstrapContract(
      string name, string templateName, bool removeExisting, bool vsc)
    {
      namespace bfs = boost::filesystem;

      bfs::path workspacePath(getContractWorkspace(this));
      if(isError_){
        return;
      }

      bfs::path eosFactoryDir(getEosFactoryDir(this));
      if(isError_){
        return;
      }
      
      bfs::path templContractPath 
        = eosFactoryDir / templContractsDir / templateName;
      if(!bfs::exists(templContractPath))
      {
        putError((boost::format("Template '%1%' does not exist.\n")
              % templateName).str(), SPOT);
        return;
      }
      
      bfs::path contractPath = workspacePath / name;
      if(bfs::exists(contractPath)){
        if(removeExisting)
        {
          bfs::remove_all(contractPath);
        } else
        {
          cout << (boost::format(
            "NOTE:\n"
            "Contract \n%1%\n workspace already exists. Cannot owerwrite it.") 
              % contractPath.string()).str() << endl;
          putError("");
          return;
        }
      }

      { // make contract directory and its build directory:
        try{
          bfs::create_directories(contractPath / "build");
        } catch (bfs::filesystem_error &e){
          putError(e.what());
        }
        if(isError_){
          return;
        }
      }

      respJson_.put("contract_dir", contractPath.string());           

      for (const auto& dirEnt : bfs::recursive_directory_iterator{templContractPath})
      {
        try{
          const auto& inTemplate = dirEnt.path();
          auto relativePathStr = inTemplate.string();
          boost::replace_first(relativePathStr, templContractPath.string(), "");
          boost::replace_all(relativePathStr, TEMPLATE_TOKEN, name);

          bfs::path dest = contractPath / relativePathStr;
          copy(inTemplate, contractPath / relativePathStr, name);

        } catch (exception &e){
          putError(e.what());
        }
        if(isError_){
          return;
        }
      }

      if(vsc)
      {
        namespace bp = boost::process;

        if(isWindowsUbuntu()) 
        {            
          bp::ipstream pipe_stream;
          string cl = string(
R"(reg.exe query HKLM\Software\Classes\Applications\Code.exe\shell\open\command /ve)");
          bp::child c(cl, bp::std_out > pipe_stream);

          string line;
          stringstream ss;
          while (pipe_stream && getline(pipe_stream, line) && !line.empty()) {
            ss << line;
          }
          c.wait();
          
          string value = ss.str();
          if( value.find("Code.exe") != string::npos)
          {
            size_t pos = value.find("\"");
            value = value.substr(pos + 1);
            pos = value.find("\\Code");
            string codePath = value.substr(0, pos);
            cout << "VSCode path: " << value << endl;

            string commandLine 
              = string("cmd.exe /c start /D \"") + codePath + "\" Code.exe "
              + wslMapLinuxWindows(contractPath.string());
            cout << "commandLine\n" << commandLine << endl;
            bp::spawn(commandLine);
          }else
          {
            cout << 
            "NOTE!\n"
            "Cannot find the Visual Studio Code in the Registry."
            "Is it installed?" << endl;
          }
        } else 
        {
          if(uname() == DARWIN){
            bp::spawn(
              string("open -a code --args ") + contractPath.string());
          } else{
            bp::spawn(
              string("code ") + contractPath.string());
          }
        }
      }
    }


    /**
     * @brief Get the target (build) directory.
     * 
     * Given a source directory, tries varies contract IDE structure models
     * and returns the first existing one.
     * 
     * @param sourceDir source directory, where C/C++ files come from.
     * @return boost::filesystem::path 
     */
    boost::filesystem::path getTargetDirPath(string sourceDir)
    {
      namespace bfs = boost::filesystem;
      bfs::path sourceDirPath(sourceDir);
      bfs::path targetPath;
      
      if(targetPath.empty())
      {
        bfs::path td = sourceDirPath / ("../build");
        if(bfs::exists(td)){
          targetPath = td;
        }
      }
      if(targetPath.empty())
      {
        bfs::path td = sourceDirPath / "build";
        if(bfs::exists(td)){
          targetPath = td;
        }
      }
      if(targetPath.empty())
      {
        targetPath = sourceDirPath;
      } 
      return targetPath;
    }

    void GenerateAbi::generateAbi(
      string sourceDir,
      string include_dir, // comma separated list of include dirs
      string codeName
    )
    {
      namespace bfs = boost::filesystem;

      vector<string> srcs = getContractSourceFiles(this, sourceDir);
      bfs::path targetDirPath = getTargetDirPath(sourceDir);

      for(string src: srcs){
        bfs::path srcPath(src);
        if(srcPath.extension().string() == ".abi"){
          cout << (boost::format(
            "NOTE:\n"
            "An ABI exists in the source directory. Cannot overwrite it:\n%1%\n"
            "\tJust copying it to the target directory.")
              % srcPath.string()).str() << endl;
          putError("");

          bfs::copy_file(
            srcPath, targetDirPath / srcPath.filename(), 
            bfs::copy_option::overwrite_if_exists);
          return;
        }
      }
      if(srcs.empty()){
        putError((boost::format("The source is empty. The imput is:\n%1%\n")
              % sourceDir).str(), SPOT);
        return;
      }

      bfs::path sourcePath(srcs[0]);
      string name = codeName.empty() ? sourcePath.stem().string() : codeName;
      bfs::path targetPath = targetDirPath / (name  + ".abi");

      string command_line = getSourceDir(this) 
        + "/build/programs/eosio-abigen/eosio-abigen"
        + " -extra-arg=-c -extra-arg=--std=c++14 -extra-arg=--target=wasm32"
        + " -extra-arg=-nostdinc -extra-arg=-nostdinc++ -extra-arg=-DABIGEN"
        + " -extra-arg=-I" + getEOSIO_BOOST_INCLUDE_DIR(this)
        + " -extra-arg=-I" + getSourceDir(this) + "/externals/magic_get/include"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts/libc++/upstream/include"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts/musl/upstream/include"
        + " -extra-arg=-I" + getSourceDir(this) + "/contracts"
        + " -extra-arg=-I" + sourcePath.string();

      if(!include_dir.empty())
      {
        vector<string> include_dirs;
        boost::split(include_dirs, include_dir, boost::algorithm::is_any_of(","));
        for (string dir : include_dirs) {
          command_line += " -extra-arg=-I" + dir;
        }
      }

      command_line = command_line
        + " -extra-arg=-fparse-all-comments"
        + " -destination-file=" + targetPath.string()
        + " -verbose=0"
        + " -context=" + sourcePath.string()
        + " " + sourcePath.string() + " --";
      
      //cout << command_line << endl;

      if(process(command_line, this)){  
        boost::property_tree::ptree abi;
        boost::property_tree::read_json(targetPath.string(), abi);
        respJson_.add_child("ABI", abi);
        respJson_.put("output", targetPath.string());
          //cout << responseToString();        
      }
    }

    void wasmClangHelp()
    {
      string command_line;
      command_line += getEOSIO_WASM_CLANG(nullptr) + " --help";
      boostProcessSystem(command_line);
    }

    /*
    See a basic example of the build procedure: 
      https://gist.github.com/yurydelendik/4eeff8248aeb14ce763e#example.
    */
    void BuildContract::buildContract(
      string sourceDir, // contract source directory
      string include_dir, // comma separated list of include dirs
      string codeName,
      bool compile_only
    )
    {
      namespace bfs = boost::filesystem;

      vector<string> srcs = getContractSourceFiles(this, sourceDir);
      if(srcs.empty()){
        putError((boost::format("The source is empty. The imput is:\n%1%\n")
              % sourceDir).str());
        return;
      }

      string objectFileList;
      bfs::path target_dir_path;
      bfs::path targetPath;
      bfs::path workdir;
      bfs::path workdir_build;

      for (string file : srcs)
      {  
        bfs::path src_file(file);
        string name = codeName.empty() ? src_file.stem().string() : codeName;

        if(targetPath.empty()) 
        { // Define target path once.
          targetPath = getTargetDirPath(sourceDir) / (name + ".wast");

          workdir = target_dir_path / "working_dir";
          bfs::create_directories(workdir);
          workdir_build = bfs::path(workdir / "build");
          bfs::create_directory(workdir_build);
        }

        bfs::path output(workdir_build / (name + ".o"));
        objectFileList += output.string() + " ";

        string command_line;
        command_line += getEOSIO_WASM_CLANG(this)
          + " -emit-llvm -O3 --std=c++14 --target=wasm32 -nostdinc -nostdlib"
          + " -nostdlibinc -ffreestanding -nostdlib -fno-threadsafe-statics"
          + " -fno-rtti -fno-exceptions"
          + " -I" + getEOSIO_BOOST_INCLUDE_DIR(this)          
          + " -I" + getSourceDir(this) + "/externals/magic_get/include"
          + " -I" + getSourceDir(this) + "/contracts/libc++/upstream/include"
          + " -I" + getSourceDir(this) + "/contracts/musl/upstream/include"
          + " -I" + getSourceDir(this) + "/contracts"
          + " -I" + src_file.parent_path().string();

        if(!include_dir.empty())
        {
          vector<string> include_dirs;
          boost::split(include_dirs, include_dir, boost::algorithm::is_any_of(","));
          for (string dir : include_dirs) {
            command_line += " -I " + dir;
          }
        }        

        command_line += " -c " + file + " -o " + output.string();

        //cout << "command line clang:" << endl << command_line << endl;

        if(!process(command_line, this)){
          bfs::remove_all(workdir);
          return;
        }
      }

      if(!compile_only)
      {
        {
          string command_line;
          command_line += getEOSIO_WASM_LLVM_LINK(this)
            + " -only-needed" 
            + " -o "  + workdir.string() + "/linked.bc"
            + " " + objectFileList // $workdir/built/* DOES NOT WORK
            + " " + getSourceDir(this) + "/build/contracts/musl/libc.bc"
            + " " + getSourceDir(this) + "/build/contracts/libc++/libc++.bc"
            + " " + getSourceDir(this) + "/build/contracts/eosiolib/eosiolib.bc";

          //cout << "command line llvm-link:" << endl << command_line << endl;

          if(!process(command_line, this)){
            return;
          }   
        }
        
        {
          string command_line;
          command_line += getEOSIO_WASM_LLC(this)
            + " -thread-model=single --asm-verbose=false"
            + " -o " + workdir.string() + "/assembly.s"
            + " " + workdir.string() + "/linked.bc";
          //cout << "command line llc:" << endl << command_line << endl;

          if(!process(command_line, this)){
            return;
          } 
        }

        {
          string command_line;
          command_line += getSourceDir(this) + "/build/externals/binaryen/bin/eosio-s2wasm"
            + " -o " + targetPath.string()
            + " -s 16384"
            + " " + workdir.string() + "/assembly.s";

          //cout << "command line eosio-s2wasm:" << endl << command_line << endl;

          if(!process(command_line, this)){
            return;
          } 
        }
        bfs::remove_all(workdir);

        ifstream ifs(targetPath.string());
        stringstream ss;
        ss << ifs.rdbuf();
        respJson_.put("WAST", ss.str());
        respJson_.put("output", targetPath.string());
      }
    }
  }
}