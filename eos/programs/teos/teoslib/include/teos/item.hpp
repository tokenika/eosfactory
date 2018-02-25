#pragma once

#include <stdlib.h>
#include <string>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/program_options.hpp>

extern std::string formatUsage(std::string unixUsage);

namespace teos {

  using namespace std;
  using namespace boost::property_tree;
  using namespace boost::program_options;

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

  class Item
  {
    string errorMsg_ = "";
  public:
    static bool verbose;
    static ptree getConfig(bool verbose = false);
    bool isError_ = false;

    void errorMsg(string errorMsg) {
      errorMsg_ += "\n" + errorMsg;
    }
    virtual string errorMsg() {
      return errorMsg_;
    }
  };

  /**
  * @brief Command-line wrapper for Item commands.
  *
  * A prototype for command-line wrappers for Item commands. Defines
  * common options like 'help', 'verbose'.
  *
  * Also, the class defines virtual methods that are placeholders for
  * specific definitions of the command that is wrapped.
  */
  template<class T>
  class ItemOptions
  {
    int argc_;
    const char **argv_;

    /**
    * @brief List of options common to all commands.
    */
    options_description basicOptionDescription()
    {
      options_description od("");
      od.add_options()
        ("help,h", "Help screen")
        ("verbose,V", "Output verbose messages");
      return od;
    }

  protected:

    /**
    * @brief Command 'usage' instruction.
    * @return usage text
    */
    virtual const char* getUsage() { return ""; }

    /**
    * @brief List of the command options that are common for a command group.
    * @return  a command description object.
    */
    virtual options_description groupOptionDescription() {
      options_description od("");
      return od;
    }

    /**
    * @brief List of the command arguments.
    * @return  a command description object.
    */
    virtual options_description  argumentDescription() {
      options_description od("");
      return od;
    }

    /**
    * @brief Ordering o the positional options.
    * @param pos_descr positional options description object.
    */
    virtual void
      setPosDesc(positional_options_description& pos_descr) {}

    /**
    * @brief Placeholder for printout instructions.
    * Printout should be composed
    * with the ::output(const char*, const char*, ...) function.
    * @param command Item object, containing a command response.
    */
    virtual void printout(Item command, variables_map &vm) {};

    /**
    * @brief Returns Item object, containing a command response.
    * @return Item object.
    */
    T executeCommand();

    /**
    * @brief Sets arguments if the command according to options.
    * @param option-variable map.
    * @return true if all the arguments are set.
    */
    virtual bool checkArguments(variables_map &vm) {
      return false;
    }

    virtual void parseGroupVariablesMap(variables_map& vm) {
    }

  public:
    ItemOptions(int argc, const char *argv[]) : argc_(argc), argv_(argv) {}
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

  /**
  * @brief Wrapper for CommandOptions descendants, for tests.
  *
  * Descendants of the CommandOptions class take arguments of the `main` function.
  * The setOptions() template wrapper takes `std::vector<std::string>` argument
  * and converts it to its client standard.
  *
  * @tparam T
  * @param strVector
  */
  template<class T> static void setOptions(vector<string> strVector) {

    int argc = (int)strVector.size();
    char** argv = new char*[argc];
    for (int i = 0; i < argc; i++) {
      argv[i] = new char[strVector[i].size() + 1];

#ifdef _MSC_VER
      strcpy_s(argv[i], strVector[i].size() + 1,
        strVector[i].c_str());
#else
      strcpy(argv[i], strVector[i].c_str());
#endif
    }

    T(argc, (const char**)argv).go();
    delete[] argv;
  }
}