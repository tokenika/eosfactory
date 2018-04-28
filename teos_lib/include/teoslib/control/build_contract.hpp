// #pragma once

#include <boost/filesystem.hpp>
#include <teoslib/control.hpp>

using namespace std;

namespace teos {
  namespace control {
    /**
     * Builds a contract: produces the WAST file.
     */
    class BuildContract : public TeosControl
    {
      void buildContract(
        string src, // comma separated list of source c/cpp files
        string target_wast_file = "",
        string include_dir = "" // comma separated list of include dirs
      );

    public:
      BuildContract(
        string src, // comma separated list of source c/cpp files
        string target_wast_file = "",
        string include_dir = ""
      )
      {
        buildContract(src, target_wast_file, include_dir);
      }

      BuildContract(ptree reqJson) : TeosControl(reqJson)
      {
        buildContract(
          reqJson_.get<string>("src"), 
          reqJson_.get<string>("wast_file"), 
          reqJson_.get<string>("include_dir")
        );
      }
    };


    /**
     * Command-line driver for the BuildContract class.
     */ 
    class BuildContractOptions : public ControlOptions
    {
    public:
      BuildContractOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Build smart contract.
Usage: ./teos build contract src wast_file [Options]
Usage: ./teos create key --jarg '{
  "src":"<comma separated list of c/c++ files>",
  "wast_file":<>,
  "include_dir":"<comma separated list of include dirs>"
  }' [OPTIONS]
)EOF";
      }

      string src;
      string wast_file;
      string include_dir;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("src", value<string>(&src)
            , "Comma separated list of source c/cpp files.")
          ("wast_file,o", value<string>(&wast_file)->default_value("")
            , "Target wast file.")
          ("include_dir,d", value<string>(&include_dir)->default_value("")
            , "Comma separated list of source c/c++ files.");
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("src", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if(vm.count("src")){
          ok = true;
          reqJson_.put("src", src);
          reqJson_.put("wast_file", wast_file);
          reqJson_.put("include_dir", include_dir);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return BuildContract(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("WAST", "%s", GET_STRING(command, "output"));
      }    
    };


    /**
     * Generates abi: produces the ABI file.
     */
    class GenerateAbi : public TeosControl
    {
      void generateAbi(
        string types_hpp, // comma separated list of source c/cpp files
        string abi_file = "",
        string include_dir = "" // comma separated list of include dirs
      );

    public:
      GenerateAbi(
        string types_hpp, // comma separated list of source c/cpp files
        string abi_file = "",
        string include_dir = ""
      )
      {
        generateAbi(types_hpp, abi_file, include_dir);
      }

      GenerateAbi(ptree reqJson) : TeosControl(reqJson)
      {
        generateAbi(
          reqJson_.get<string>("types_hpp"), 
          reqJson_.get<string>("abi_file"), 
          reqJson_.get<string>("include_dir")
        );
      }
    };


    /**
     * Command-line driver for the GenerateAbi class.
     */ 
    class GenerateAbiOptions : public ControlOptions
    {
    public:
      GenerateAbiOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Generate the ABI specification file.
Usage: ./teos generate abi types_hpp [Options]
Usage: ./teos create key --jarg '{
  "types_hpp":"<types.hpp>",
  "abi_file":<target output file>,
  "include_dir":"<comma separated list of include dirs>"
  }' [OPTIONS]
)EOF";
      }

      string types_hpp;
      string abi_file;
      string include_dir;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("types_hpp", value<string>(&types_hpp)
            , "Comma separated list of source c/cpp files.")
          ("abi_file,o", value<string>(&abi_file)->default_value("")
            , "Target wast file. If emmpty, its name is derived from the name of 'types_hpp'")
          ("include_dir,d", value<string>(&include_dir)->default_value("")
            , "Comma separated list of source c/c++ files.");
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("types_hpp", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if(vm.count("types_hpp")){
          ok = true;
          reqJson_.put("types_hpp", types_hpp);
          reqJson_.put("abi_file", abi_file);
          reqJson_.put("include_dir", include_dir);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return GenerateAbi(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("ABI", "%s", GET_STRING(command, "output"));
      }        
    };


    /**
     * BootstrapContract: produces template contract workspace.
    */
    class BootstrapContract : public TeosControl
    {
      void bootstrapContract(
        string name // contract name
      );
      void copyTemplate(
      boost::filesystem::path contract_path, string name, string extension);

    public:
      BootstrapContract(
        string name // contract name
      )
      {
        bootstrapContract(name);
      }

      BootstrapContract(ptree reqJson) : TeosControl(reqJson)
      {
        bootstrapContract(
          reqJson_.get<string>("name")
        );
      }
    };


    /**
     * Command-line driver for the BootstrapContract class.
     */ 
    class BootstrapContractOptions : public ControlOptions
    {
    public:
      BootstrapContractOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Make a workspace for a contract, with a c++ code template.
Usage: ./teos bootstrap contract [Options]
Usage: ./teos create key --jarg '{
  "name":"<contract name>"
  }' [OPTIONS]
)EOF";
      }

      string name;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name", value<string>(&name)
            , "Contract name.");
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if(vm.count("name")){
          ok = true;
          reqJson_.put("name", name);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return BootstrapContract(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("context dir", "%s", GET_STRING(command, "context_dir"));
        output("contracts dir", "%s", GET_STRING(command, "contracts_dir"));        
        output("contract dir", "%s", GET_STRING(command, "contract_dir"));
        output("build_dir", "%s", GET_STRING(command, "build_dir"));        
        output("template.cpp", "%s", GET_STRING(command, "template.cpp"));        
        output("template.hpp", "%s", GET_STRING(command, "template.hpp"));        
      }        
    };
  }
}