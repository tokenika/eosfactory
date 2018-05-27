#pragma once

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
        string include_dir = "", // comma separated list of include dirs
        bool compile_only = false
      );

    public:
      BuildContract(
        string src, // comma separated list of source c/cpp files
        string include_dir = "",
        bool compile_only = false
      )
      {
        buildContract(src, include_dir, compile_only);
      }

      BuildContract(ptree reqJson) : TeosControl(reqJson)
      {
        buildContract(
          reqJson_.get<string>("src"), 
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
        return R"(
Build smart contract.
Usage: ./teos build contract src [Options]
Usage: ./teos create key --jarg '{
  "src":"<comma separated list of c/c++ files>",
  "include_dir":"<comma separated list of include dirs>"
  }' [OPTIONS]
)";
      }

      string src;
      string include_dir;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("src", value<string>(&src)
            , "Contract source directory.")
          ("include_dir,d", value<string>(&include_dir)->default_value("")
            , "Comma separated list of source c/c++ files.")
          ("compile_only,c", "Compilation only.");
            
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
          reqJson_.put("include_dir", include_dir);
          if(vm.count("compile_only")){
            reqJson_.put("compile_only", 1);
          } else {
            reqJson_.put("compile_only", 0);
          }
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
        string sourceDir, // comma separated list of source c/cpp files
        string include_dir = "" // comma separated list of include dirs
      );

    public:
      GenerateAbi(
        string sourceDir, // comma separated list of source c/cpp files
        string include_dir = ""
      )
      {
        generateAbi(sourceDir, include_dir);
      }

      GenerateAbi(ptree reqJson) : TeosControl(reqJson)
      {
        generateAbi(
          reqJson_.get<string>("sourceDir"),  
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
        return R"(
Generate the ABI specification file.
Usage: ./teos generate abi sourceDir [Options]
Usage: ./teos create key --jarg '{
  "sourceDir":"<types.hpp>",
  "include_dir":"<comma separated list of include dirs>"
  }' [OPTIONS]
)";
      }

      string sourceDir;
      string include_dir;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("sourceDir", value<string>(&sourceDir)
            , "Comma separated list of source c/cpp files.")
          ("include_dir,d", value<string>(&include_dir)->default_value("")
            , "Comma separated list of source c/c++ files.");
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("sourceDir", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if(vm.count("sourceDir")){
          ok = true;
          reqJson_.put("sourceDir", sourceDir);
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

    #define TEMPLATE "skeleton"
    /**
     * @brief BootstrapContract: produce contract workspace from a 
     * given template.
     * 
     * If the template is not set, a default one is used.
     */
    class BootstrapContract : public TeosControl
    {
      void bootstrapContract(
        string name, // contract name
        string templateName=TEMPLATE
      );
      void copy(
        boost::filesystem::path inTemplate,
        boost::filesystem::path inContract,
        string name);

    public:
    /**
     * @brief Construct a new Bootstrap Contract object.
     * 
     * @param name name of the bootstrapped contract.
     * @param templateName chosen template.
     */
      BootstrapContract(
        string name, // contract name
        string templateName=TEMPLATE
      )
      {
        reqJson_.put("name", name);
        reqJson_.put("template", templateName);
        bootstrapContract(name, templateName);
      }

      BootstrapContract(ptree reqJson) : TeosControl(reqJson)
      {
        bootstrapContract(
          reqJson_.get<string>("name"),
          reqJson_.get("template", TEMPLATE)
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
        return R"(
Produce contract workspace from a given template.
Usage: ./teos bootstrap contract [Options] name template [Options]
Usage: ./teos create key --jarg '{
  "name":"<contract name>",
  "template":"<template name>"
  }' [OPTIONS]
)";
      }

      string name;
      string templateName;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name", value<string>(&name), "Contract name.")
          ("template", value<string>(&templateName)->default_value(TEMPLATE), 
            "Template name.");
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
        pos_desc.add("template", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if(vm.count("name")){
          ok = true;
          reqJson_.put("name", name);
          reqJson_.put("template", templateName);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return BootstrapContract(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("template contract", "%s", GET_STRING(command, "contract_dir"));              
      }        
    };

        /**
     * BootstrapContract: produces template contract workspace.
    */
    class DeleteContract : public TeosControl
    {
      void deleteContract(
        string name // contract name
      );

    public:
      DeleteContract(
        string name // contract name
      )
      {
        deleteContract(name);
      }

      DeleteContract(ptree reqJson) : TeosControl(reqJson)
      {
        deleteContract(
          reqJson_.get<string>("name")
        );
      }
    };


    /**
     * Command-line driver for the DeleteContract class.
     */ 
    class DeleteContractOptions : public ControlOptions
    {
    public:
      DeleteContractOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"(
Deletes the workspace of a contract.
Usage: ./teos delete contract [Options]
Usage: ./teos delete contract --jarg '{
  "name":"<contract name>"
  }' [OPTIONS]
)";
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
        return DeleteContract(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("template contract", "%s", GET_STRING(command, "contract_dir"));              
      }        
    };
  }
}