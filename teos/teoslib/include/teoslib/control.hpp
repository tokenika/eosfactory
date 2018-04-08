/**
 * @file command.hpp
 * @copyright defined in resources/LICENSE.txt
 * @brief Tool for sending transactions and querying state from EOS blockchain
 *
 * @brief Base definitions.
 *
 * Defines base classes of the project, and helper methods.
 */

#pragma once

#include <stdlib.h>
#include <string>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/program_options.hpp>
#include <boost/format.hpp>
#include <teoslib/utilities.hpp>

#define teos_ERROR "ERROR!" // Error json key

extern std::string formatUsage(std::string unixUsage);

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

namespace teos 
{
  /**
  * @brief Printout formater.
  *
  * For example, `output("timestamp", "%s", "2017-07-18T20:16:36")` produces
  * `##           timestamp: 2017-07-18T20:16:36`
  *
  * @param label
  * @param format
  * @param ...
  */
  extern void output(const char* label, const char* format, ...);
  extern void output(const char* text, ...); 
  extern void output(string text);
  extern boost::format output(string label, string format);
  extern ostream& sharp();

  class TeosControl
  {
  public:
    static string getConfigJson();
    static ptree getConfig(TeosControl* teosControl = nullptr);

    bool isError_ = false;
    ptree reqJson_;
    ptree respJson_;
    void errorRespJson(string sender, string message);
    void putError(string msg, string sender = "");   

    TeosControl() {}
    TeosControl(ptree reqJson) : reqJson_(reqJson) {}

    string errorMsg() {
      return get<string>(teos_ERROR);
    }
    string requestToString(bool isRaw) const;
    string responseToString(bool isRaw) const;

    template<typename Type>
    Type get(const ptree::path_type & path) const {
      Type value;
      try {
        value = getJsonPath<Type>(respJson_, path);
      }
      catch (exception& e) {
        cout << teos_ERROR << endl << e.what() << endl;
        exit(-1);
      }
      return value;
    }

  };
#define GET_STRING(command, key) command.get<string>(key).c_str()

  class ControlOptions
  {
    int argc_;
    const char **argv_;
    
  protected:
    string json_;
    ptree reqJson_;

    options_description basicOptionDescription()
    {
      options_description od("");
      od.add_options()
        ("help,h", "Help screen")
        ("verbose,V", "Output verbose messages");
      return od;
    }

    virtual options_description  argumentDescription() {
      options_description od("");
      return od;
    }

    virtual options_description groupOptionDescription() {
      options_description od("");
      od.add_options()      
        ("jarg", value<string>(&json_), "Json argument.")
        ("json,j", "Print result as json.")
        ("both", "For system use.")
        ("raw,r", "Raw print");
      return od;
    }
    /**
    * @brief Command 'usage' instruction.
    * @return usage text
    */
    virtual const char* getUsage() { return ""; }

    virtual void
      setPosDesc(positional_options_description&
        pos_descr) {}

    virtual void printout(TeosControl command, variables_map &vm) {
      output(command.responseToString(false));
    }

    virtual bool checkArguments(variables_map &vm) {
      return true;
    }

    virtual void parseGroupVariablesMap(variables_map& vm) 
    {
      if (vm.count("json")) {
        reqJson_ = stringToPtree(json_);
      } else {
        if(!checkArguments(vm)) {
          std::cout << teos_ERROR << endl << "Wrong argument." << endl;
          return;
        }        
      }
      
      TeosControl command = executeCommand();
      if (command.isError_) {       
        cout << teos_ERROR << endl << command.errorMsg() << endl;
        return;
      }

      bool isRaw = vm.count("raw") ? true : false;
      if(vm.count("both")) {
        cerr << command.responseToString(isRaw) << endl;
        printout(command, vm);
      } else {
        if (vm.count("received")) {
          cout << command.responseToString(isRaw) << endl;
        }
        else {
          printout(command, vm);
        }
      }
    }

    virtual TeosControl executeCommand() {
      return TeosControl(reqJson_);
    }

  public:    
    ControlOptions(int argc, const char *argv[]) : argc_(argc), argv_(argv) {}

    void go()
    {
      using namespace boost::program_options;

      options_description desc{"Options"};      
      try {
        desc.add(argumentDescription()).add(groupOptionDescription())
          .add(basicOptionDescription());
        positional_options_description pos_desc;
        setPosDesc(pos_desc);
        command_line_parser parser{argc_, argv_};
        parser.options(desc).positional(pos_desc);
        parsed_options parsed_options = parser.run();

        variables_map vm;
        store(parsed_options, vm);
        notify(vm);

        if (vm.count("help")) {
          cout << formatUsage(getUsage()) << endl;
          cout << desc << endl;
          return;
        }

        parseGroupVariablesMap(vm);
      }
      catch (const error &ex) {
        cout << "ERROR: " << ex.what() << endl;
        cout << formatUsage(getUsage()) << endl;
        cout << desc << endl;        
      }
    }
  };
}