#pragma once

#include <string>
#include <vector>

using namespace std;

namespace teos {
  namespace control {

    class CyberCommand {
    public:
      CyberCommand() {}
      string responseToString() const;
    };

//    class CyberOptions {
//
//      /**
//      * @brief List of options common to all commands.
//      *
//      * @param common boost program options description object.
//      */
//      void basicOptionDescription(options_description& common)
//      {
//        using namespace std;
//        using namespace boost::program_options;
//
//        common.add_options()
//          ("help,h", "Help screen")
//          ("verbose,V", "Output verbose messages on error");
//      }
//
//    protected:
//
//      /**
//      * @brief Command 'usage' instruction.
//      *
//      * @return const char* usage text
//      */
//      virtual const char* getUsage() { return ""; }
//
//      /**
//      * @brief List of the command options.
//      *
//      * @return boost::program_options::options_description command options
//      */
//      virtual options_description  argumentDescription() {
//        options_description od("");
//        return od;
//      }
//
//      /**
//      * @brief Positional options.
//      *
//      * @param pos_descr positional options
//      */
//      virtual void
//        setPosDesc(positional_options_description&
//          pos_descr) {}
//
//      /**
//      * @brief Placeholder for printout instructions.
//      *
//      * Placeholder for printout instructions. Printout should be composed
//      * with the ::output(const char*, const char*, ...) function.
//      *
//      * @param command command object, containing a responce from the blockchain.
//      */
//      virtual void getOutput(CyberCommand command) {
//        cout << command.responseToString() << endl;
//      }
//
//      virtual void onError(CyberCommand command);
//
//      /**
//      * @brief Returns command object, containing a responce from the blockchain.
//      *
//      * @param isRaw raw or pretty printout flag
//      * @return TeosCommand command object
//      */
//      virtual CyberCommand getCommand(bool isRaw) {
//        return CyberCommand();
//      }
//
//    public:
//      CyberOptions(int argc, const char *argv[]) : argc_(argc), argv_(argv) {}
//      void go();
//    };
//
//    /**
//    * @brief Wrapper for CommandOptions descendants, for tests.
//    *
//    * Descendants of the CommandOptions class take arguments of the `main` function.
//    * The setOptions() template wrapper takes `std::vector<std::string>` argument
//    * and converts it to its client standard.
//    *
//    * @tparam T
//    * @param strVector
//    */
//    template<class T> static void setOptions(vector<string> strVector) {
//
//      int argc = (int)strVector.size();
//      char** argv = new char*[argc];
//      for (int i = 0; i < argc; i++) {
//        argv[i] = new char[strVector[i].size() + 1];
//
//#ifdef _MSC_VER
//        strcpy_s(argv[i], strVector[i].size() + 1,
//          strVector[i].c_str());
//#else
//        strcpy(argv[i], strVector[i].c_str());
//#endif
//      }
//
//      T(argc, (const char**)argv).go();
//      delete[] argv;
//    }

    void startChainNode();
    void killChainNode();

    void buildContract(
      vector<string> src, // list of source c/cpp files
      string targetWastFile,
      vector<string> includeDir = {}
    );

    void generateAbi(
      string typesHpp,
      string targetAbiFile,
      vector<string> includeDir = {} // list of header files  
    );

    void wasmClangHelp();

  }
}