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
#include <teoslib/utilities.hpp>
#include <teoslib/item.hpp>

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

namespace teos 
{
  class TeosControl : public Item
  {

  public:
    static ptree errorRespJson(string sender, string message);
    ptree reqJson_;
    ptree respJson_;    

    TeosControl() {}
    TeosControl(ptree reqJson) : reqJson_(reqJson) {}

    string requestToString(bool isRaw) const;
    string responseToString(bool isRaw) const;

    template<typename Type>
    Type get(const ptree::path_type & path) const {
      Type value;
      try {
        value = getJsonPath<Type>(respJson_, path);
      }
      catch (exception& e) {
        cerr << teos_ERROR << "! " << e.what() << endl;
      }
      return value;
    }

    string errorMsg() {
      return get<string>(teos_ERROR);
    }

  };
#define GET_STRING(command, key) command.get<string>(key).c_str()

  class ControlOptions : public ItemOptions<TeosControl>
  {
    int argc_;
    const char **argv_;
    string json_;

  protected:

    ptree reqJson_;

    options_description groupOptionDescription() {
      options_description od("");
      od.add_options()
        ("json,j", value<string>(&json_), "Json argument.")
        ("received,v", "Print received json.")
        ("both,b", "For system use.")
        ("raw,r", "Raw print");
      return od;
    }

    virtual void
      setPosDesc(positional_options_description&
        pos_descr) {}

    virtual void printout(TeosControl command, variables_map &vm) {
      output(command.responseToString(false));
    }

    virtual void parseGroupVariablesMap(variables_map& vm) 
    {
      if(!checkArguments(vm)) {
        std::cerr << teos_ERROR << endl << "Wrong argument." << endl;
        return;
      }

      if (vm.count("json")) {
        reqJson_ = stringToPtree(json_);
      }

      TeosControl command = executeCommand();
      if (command.isError_) {
        std::cerr << teos_ERROR << endl << command.errorMsg() << endl;
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
    ControlOptions(int argc, const char *argv[]) : ItemOptions(argc, argv) {}
  };
}