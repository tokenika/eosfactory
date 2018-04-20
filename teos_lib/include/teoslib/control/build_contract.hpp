#pragma once

#include <string>

#include <teoslib/control.hpp>

using namespace std;

namespace teos {
  namespace control {

    class BuildContract : public TeosControl
    {
      TeosControl buildContract(
        string src, // comma separated list of source c/cpp files
        string target_wast_file,
        string include_dir = "" // comma separated list of include dirs
      );

    public:
      BuildContract(
        string src, // comma separated list of source c/cpp files
        string target_wast_file,
        string include_dir = ""
      )
      {
        copy(buildContract(src, target_wast_file, include_dir));
      }

      BuildContract(ptree reqJson) : TeosControl(reqJson)
      {
        copy(buildContract(
          reqJson_.get<string>("src"), 
          reqJson_.get<string>("wast_file"), 
          reqJson_.get<string>("include_dir")
        ));
      }
    };

    class BuildContractOptions : public ControlOptions
    {
    public:
      BuildContractOptions(int argc, const char **argv) : ControlOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Build smart contract.
Usage: ./teos build contract src wast_file [Options]
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
          ("wast_file", value<string>(&wast_file)
            , "Target wast file.")
          ("include_dir,d", value<string>(&wast_file)->default_value("")
            , "Comma separated list of source c/cpp files.");
            
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("src", 1);
        pos_desc.add("wast_file", 1);
      }      

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if(vm.count("src")){
          reqJson_.put("src", src);
          if(vm.count("wast_file")){
            ok = true;
            reqJson_.put("include_dir", include_dir);
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return BuildContract(reqJson_);
      }
    };
  }
}