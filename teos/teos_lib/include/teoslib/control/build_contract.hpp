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
        string sourceDir, // comma separated list of source c/cpp files
        string includeDir = "", // comma separated list of include dirs
        string codeName = "",
        bool compileOnly = false
      );

    public:
      BuildContract(
        string sourceDir, // comma separated list of source c/cpp files
        string includeDir = "",
        string codeName = "",
        bool compileOnly = false
      )
      {
        buildContract(sourceDir, includeDir, codeName, compileOnly);
      }

      BuildContract(ptree reqJson) : TeosControl(reqJson)
      {
        buildContract(
          reqJson_.get<string>("sourceDir"), 
          reqJson_.get("includeDir", ""),
          reqJson_.get("codeName", ""),
          reqJson_.get("compileOnly", false)

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
Usage: ./teos build contract <source dir> [Options]
Usage: ./teos create key --jarg '{
  "sourceDir":"<source dir>",
  "includeDir":"<comma separated list of include dirs, optional>",
  "codeName":"<name of the WAST file, optional>"
  }' [OPTIONS]
)";
      }

      string sourceDir;
      string includeDir;
      string codeName;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("sourceDir", value<string>(&sourceDir)
            , "Contract source directory.")
          ("includeDir,d", value<string>(&includeDir)->default_value("")
            , "Comma separated list of source c/c++ files.")
          ("codeName,n", value<string>(&codeName)->default_value("")
            , "The name of the WAST file. If not set, it equals to the name "
              "of the contract project.")
          ("compileOnly,c", "Compilation only.");
            
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
          reqJson_.put("includeDir", includeDir);
          reqJson_.put("codeName", codeName);
          if(vm.count("compileOnly")){
            reqJson_.put("compileOnly", 1);
          } else {
            reqJson_.put("compileOnly", 0);
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return BuildContract(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        if(!command.respJson_.get("output", "").empty()) {
          output("WAST", "%s", GET_STRING(command, "output"));
        }
      }    
    };


    /**
     * Generates abi: produces the ABI file.
     */
    class GenerateAbi : public TeosControl
    {
      void generateAbi(
        string sourceDir, // comma separated list of source c/cpp files
        string includeDir = "", // comma separated list of include dirs
        string codeName = ""
      );

    public:
      GenerateAbi(
        string sourceDir, // comma separated list of source c/cpp files
        string includeDir = "",
        string codeName = ""
      )
      {
        generateAbi(sourceDir, includeDir, codeName);
      }

      GenerateAbi(ptree reqJson) : TeosControl(reqJson)
      {
        generateAbi(
          reqJson_.get<string>("sourceDir"),  
          reqJson_.get("includeDir", ""),
          reqJson_.get("codeName", "")
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
Usage: ./teos generate abi <source dir> [Options]
Usage: ./teos create key --jarg '{
  "sourceDir":"<source dir>",
  "includeDir":"<comma separated list of include dirs, optional>",
  "codeName":"<name of the ABI file, optional>"
  }' [OPTIONS]
)";
      }

      string sourceDir;
      string includeDir;
      string codeName;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("sourceDir", value<string>(&sourceDir)
            , "The directory of the contract project.")
          ("includeDir,d", value<string>(&includeDir)->default_value("")
            , "Comma separated list of source c/c++ files.")
          ("codeName,n", value<string>(&codeName)->default_value("")
            , "The name of the ABI file. If not set, it equals to the name "
              "of the contract project.");
            
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
          reqJson_.put("includeDir", includeDir);
          reqJson_.put("codeName", codeName);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return GenerateAbi(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        if(!command.respJson_.get("output", "").empty()) {
          output("ABI", "%s", GET_STRING(command, "output"));
        }
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
        string templateName=TEMPLATE,
        bool removeExisting=false
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
        string templateName=TEMPLATE,
        bool removeExisting=false
      )
      {
        reqJson_.put("name", name);
        reqJson_.put("template", templateName);
        reqJson_.put("remove", removeExisting);
        bootstrapContract(name, templateName, removeExisting);
      }

      BootstrapContract(ptree reqJson) : TeosControl(reqJson)
      {
        bootstrapContract(
          reqJson_.get<string>("name"),
          reqJson_.get("template", TEMPLATE),
          reqJson_.get<bool>("remove")
        );
      }
    };


    /**
     * Command-line driver for the BootstrapContract class.
     */ 
    class BootstrapContractOptions : public ControlOptions
    {
    public:
      BootstrapContractOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

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
      bool removeExisting;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name", value<string>(&name), "Contract name.")
          ("template", value<string>(&templateName)->default_value(TEMPLATE), 
            "Template name.")
          ("remove", value<bool>(&removeExisting)->default_value(false), 
            "Remove existing contract path.");
            
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
          reqJson_.put("remove", removeExisting);
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