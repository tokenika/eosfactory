/**
 * @file build_contract.hpp
 * @copyright defined in LICENSE.txt
 * @author Tokenika
 * @date 30 May 2018
*/

/**
 * @defgroup teoslib_raw Raw function classes
 */
/**
 * @defgroup teoslib_cli Command-line drivers
 */

#pragma once

#include <boost/filesystem.hpp>
#include <teoslib/control.hpp>

using namespace std;

namespace teos {
  namespace control {


    /**
     * @ingroup teoslib_raw
     * @brief Build a contract: produce the WAST file for the contract.
     */
    class BuildContract : public TeosControl
    {
      void buildContract(
        string sourceDir,
        string includeDir = "", // comma separated list of include dirs
        string codeName = "",
        bool compileOnly = false
      );

    public:
      /**
       * @brief Construct a new Build Contract object
       * 
       * @param sourceDir 
       * @param includeDir 
       * @param codeName 
       * @param compileOnly 
       * 
       * See the description of the BuildContractOptions class for meaning of
       * the parameters.
       */
      BuildContract(
        string sourceDir,
        string includeDir = "", // comma separated list of source c/cpp files
        string codeName = "",
        bool compileOnly = false
      )
      {
        buildContract(sourceDir, includeDir, codeName, compileOnly);
      }

      /**
       * @brief Construct a new Build Contract object
       * 
       * @param reqJson:
       * '{
       *    "sourceDir":"<source dir>",
       *    "includeDir":"<comma separated list of include dirs, optional>",
       *    "codeName":"<name of the WAST file, optional>"
       * }'
       *  
       * See the description of the BuildContractOptions class for meaning of
       * the parameters.
       */
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
     * @ingroup teoslib_cli
     * @brief Build a contract: produce the WAST file for the contract.
     *
     \verbatim
Build smart contract.
Usage: ./teos build contract <source dir> [Options]
Usage: ./teos create key --jarg '{
  "sourceDir":"<source dir>",
  "includeDir":"<comma separated list of include dirs, optional>",
  "codeName":"<name of the WAST file, optional>"
  }' [OPTIONS]

Options:

  --sourceDir arg          Contract source directory, absolute or relative to
                           configured directories.
  -d [ --includeDir ] arg  Comma separated list of include folders.
  -n [ --codeName ] arg    The name of the WAST file. If not set, equals to the
                           name of the contract's project.
  -c [ --compileOnly ]     Compilation only.

  --jarg arg               Json argument.
  --arg                    Print argument.
  -j [ --json ]            Print result as json.
  --both                   For system use.
  -r [ --raw ]             Raw print

  -h [ --help ]            Help screen
  -V [ --verbose ]         Output verbose messages
     \endverbatim 
     */
    class BuildContractOptions : public ControlOptions
    {
    public:
      BuildContractOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"(
Build smart contract: produce the WAST file for the contract.
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
            , "Contract source directory, absolute or relative to configured"
              " directories.")
          ("includeDir,d", value<string>(&includeDir)->default_value("")
            , "Comma separated list of include folders.")
          ("codeName,n", value<string>(&codeName)->default_value("")
            , "The name of the WAST file. If not set, equals to the name "
              "of the contract's project.")
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
     * @ingroup teoslib_raw
     * Generate abi: produce the ABI file for the contract.
     */
    class GenerateAbi : public TeosControl
    {
      void generateAbi(
        string sourceDir, 
        string includeDir = "", // comma separated list of include dirs
        string codeName = ""
      );

    public:
      /**
       * @brief Construct a new Generate Abi object
       * 
       * @param sourceDir 
       * @param includeDir 
       * @param codeName 
       * 
       * See the description of the GenerateAbiOptions class for meaning of
       * the parameters.
       */
      GenerateAbi(
        string sourceDir,
        string includeDir = "",
        string codeName = ""
      )
      {
        generateAbi(sourceDir, includeDir, codeName);
      }

      /**
       * @brief Construct a new Generate Abi object
       * 
       * @param reqJson 
       * '{
       *    "sourceDir":"<source dir>",
       *    "includeDir":"<comma separated list of include dirs, optional>",
       *    "codeName":"<name of the WAST file, optional>"
       * }'
       *  
       * See the description of the GenerateAbiOptions class for meaning of
       * the parameters. 
       */
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
     * @ingroup teoslib_cli
     * @brief Generate abi: produce the ABI file for the contract.
     * 
     \verbatim
Usage: ./teos create key --jarg '{
  "sourceDir":"<source dir>",
  "includeDir":"<comma separated list of include dirs, optional>",
  "codeName":"<name of the ABI file, optional>"
  }' [OPTIONS]

Options:

  --sourceDir arg          The directory of the contract project.
  -d [ --includeDir ] arg  Comma separated list of source c/c++ files.
  -n [ --codeName ] arg    The name of the ABI file. If not set, it equals to
                           the name of the contract project.

  --jarg arg               Json argument.
  --arg                    Print argument.
  -j [ --json ]            Print result as json.
  --both                   For system use.
  -r [ --raw ]             Raw print

  -h [ --help ]            Help screen
  -V [ --verbose ]         Output verbose messages
     \endverbatim
     */
    class GenerateAbiOptions : public ControlOptions
    {
    public:
      GenerateAbiOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"(
Generate the ABI file for the contract.
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
     * @ingroup teoslib_raw
     * @brief TemplateCreate: produce contract workspace from a 
     * given template.
     * 
     * If the template is not set, a default one is used.
     */
    class TemplateCreate : public TeosControl
    {
      void bootstrapContract(
        string name, // contract name
        string templateName =TEMPLATE,
        string workspace="",
        bool removeExisting=false,
        bool vsc=false
      );
      void copy(
        boost::filesystem::path inTemplateCreate,
        boost::filesystem::path inContract,
        string name);

    public:
    /**
     * @brief Construct a new Bootstrap Contract object.
     * 
     * @param name name of the bootstrapped contract.
     * @param templateName chosen template.
     */
      TemplateCreate(
        string name, // contract name
        string templateName=TEMPLATE,
        string workspace="",
        bool removeExisting=false,
        bool vsc=false
      )
      {
        reqJson_.put("name", name);
        reqJson_.put("template", templateName);
        reqJson_.put("workspace", workspace);
        reqJson_.put("remove", removeExisting);
        reqJson_.put("vsc", vsc);
        bootstrapContract(name, templateName, workspace, removeExisting, vsc);
      }

      TemplateCreate(ptree reqJson) : TeosControl(reqJson)
      {
        bootstrapContract(
          reqJson_.get<string>("name"),
          reqJson_.get("template", TEMPLATE),
          reqJson_.get("workspace", ""),
          reqJson_.get("remove", false),
          reqJson_.get("vsc", false)
        );
      }
    };


    /**
     * Command-line driver for the TemplateCreate class.
     */ 
    class TemplateCreateOptions : public ControlOptions
    {
    public:
      TemplateCreateOptions(int argc, const char **argv) 
        : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"(
Produce contract workspace from a given template.
Usage: ./teos bootstrap contract [Options] name template [Options]
Usage: ./teos create key --jarg '{
  "name": "<contract name>",
  "template": "<template name>",
  "workspace": "<user workspace dir>",
  "removeExisting": "<true|false>"
  "vsc":"<true|false>"
  }' [OPTIONS]
)";
      }

      string name;
      string templateName;
      string workspace;
      bool removeExisting;
      bool vsc;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("name", value<string>(&name), "Contract name.")
          ("template", value<string>(&templateName)->default_value(TEMPLATE), 
            "TemplateCreate name.")
          ("workspace", value<string>(&workspace)->default_value(""),
            "User workspace where contract file-system is placed.")
          ("remove", "Remove existing contract path.")
          ("vsc,c", "Launch Visual Studio Code.")
          ;
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("name", 1);
        pos_desc.add("template", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        removeExisting = false;
        vsc = false;

        if(vm.count("name")){
          ok = true;
          reqJson_.put("name", name);
          reqJson_.put("template", templateName);
          reqJson_.put("workspace", workspace);
          if(vm.count("remove")){
            removeExisting = true;
          } 
          reqJson_.put("remove", removeExisting);
          if(vm.count("vsc")){
            vsc = true;
          }
          reqJson_.put("vsc", vsc);
        }
        return ok;
      }

      TeosControl executeCommand() {
        return TemplateCreate(reqJson_);
      }

      void printout(TeosControl command, variables_map &vm) {
        output("template contract", "%s", GET_STRING(command, "contract_dir"));              
      }        
    };

    /**
     * @ingroup teoslib_raw
     * Deletes the workspace directory of a contract.
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