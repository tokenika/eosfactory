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
#include <teos/item.hpp>

#define teos_ERROR "error" // Error json key
#define HOST_DEFAULT "localhost"
#define PORT_DEFAULT "8888"
#define TOKENIKA_WALLET "tokenikaWallet"

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

extern const string walletCommandPath;

namespace teos {
  namespace command {

    /**
     * @brief Converts EOS time string to 'boost::posix_time'.
     *
     * EOS time is a string, for example `2017-07-18T20:16:36`. For processing,
     * it is converted to the boost `ptime`.
     *
     * @param str EOS time string.
     * @return boost::posix_time::ptime
     */
    extern boost::posix_time::ptime strToTime(const string str);

    /**
     * @brief Given a json tteosCommandJsonree, returns the <Type>value of a given path.
     *
     * @tparam Type type of the called value
     * @param json json tree
     * @param path path of the given tree
     * @return Type
     */
    template<typename Type>
    Type getJsonPath(ptree json,
      const ptree::path_type & path);

    /**
     * @brief Given a text json tree, returns the equivalent `boost ptree`.
     *
     * @param json
     * @return boost::property_tree::ptree
     */
    extern ptree stringToPtree(
      string json);

    /**
     * @brief Basic connection to the blockchain.
     *
     * Given a command path (for example `/v1/chain/GetBlock`), and a json tree
     * (for example {"block_num_or_id"="25"}),
     * connects to the blockchain and receives a json reflacting an aspect of the
     * blockchain state.
     *
     * `TeosCommand` is the superclass for any specific command class in this
     * library.
     *
     * Parameters of the connection used are specified in file `teos_config.json`,
     * in the root directory of the project.
     *
     */
    class TeosCommand : public Item
    {
    protected:
      string path_;
      ptree reqJson_;
      ptree respJson_;

      /**
      * @brief Given a json, teosCommandJsongets EOS blockchain responce.
      *
      * Given a json tree and a command path (for example `/v1/chain/GetInfo`),
      * and EOS blockchain communication port (for example `8888`),
      * and EOS blockchain server name (for example `localhost`),
      * gets EOS blockchain responce.
      *
      * @param server EOS blockchain server name
      * @param port EOS blockchain communication port
      * @param path command path
      * @param reqJson json teosCommandJsonto be posted
      * @param respJson json to be filled with received data
      */
      void callEosd();
      void putError(string sender, string msg);
      void putError(string msg);
      virtual string normRequest(ptree& reqJson);
      virtual void normResponse(string response, ptree &respJson);
      virtual bool isWalletCommand() { return path_.find(walletCommandPath) != std::string::npos; };

    public:
      static string host;
      static string port;
      static string walletHost;
      static string walletPort;
      static ptree errorRespJson(string sender, string message);
      static bool ipAddress(string ipAddress);

      /**
       * @brief A constructor.
       * @param path command path, for example `/v1/chain/GetBlock`
       * @param reqJson json tree, for example {"block_num_or_id"="25"}
       * @param isRaw if true, the resulting json is not formated.
       */
      TeosCommand(string path, ptree reqJson);
      TeosCommand(string path);
      TeosCommand(bool isError, ptree respJson);
      TeosCommand() {}

      void copy(TeosCommand teosCommand) {
        path_ = teosCommand.path_;
        reqJson_ = teosCommand.reqJson_;
        respJson_ = teosCommand.respJson_;
        isError_ = teosCommand.isError_;
      }

      ptree getResponse() const {
        return respJson_;
      }

      string errorMsg() {
        return get<string>(teos_ERROR);
      }

      /**
       * @brief Post json string representation
       * I can be pretty or raw, depending ib the `isRaw` flag.
       */
      string requestToString() const;

      string requestToString(bool isRaw) const;

      /**
       * @brief Received json string representation
       * I can be pretty or raw, depending ib the `isRaw` flag.
       */
      string responseToString(bool isRaw) const;

      /**
       * @brief Returns a value of a path of the received json.
       *
       * @tparam Type type of the value
       * @param path json tree path to the value
       * @return Type the value of the given path
       */
      template<typename Type>
      Type get(const ptree::path_type & path) const {
        Type value;
        try {
          value = getJsonPath<Type>(respJson_, path);
        }
        catch (exception& e) {
          cerr << "ERROR: " << e.what() << endl;
        }
        return value;
      }

    };
#define GET_STRING(command, key) command.get<string>(key).c_str()

    //http://boost.cowic.de/rc/pdf/program_options.pdf
    /**
     * @brief Command-line wrapper for teos commands.
     *
     * The prototype for command-line wrappers for teos commands. Defines
     * common options like 'help', 'example'.
     *
     * Also, the class defines virtual methods that are placeholders for
     * specific definitions of the command that is wrapped.
     */
    class CommandOptions : public ItemOptions<TeosCommand>
    {
      int argc_;
      const char **argv_;
      string json_;

    protected:

      options_description groupOptionDescription() {
        options_description od("");
        od.add_options()
          ("wallet-host", value<string>()->default_value(HOST_DEFAULT),
            "The host where eos-wallet is running")
            ("wallet-port", value<string>()->default_value(PORT_DEFAULT),
              "The port where eos-wallet is running")
              ("json,j", value<string>(&json_), "Json argument")
          ("received,v", "Print received json")
          ("raw,r", "Raw print");
        return od;
      }

      /**
      * @brief Positional options.
      *
      * @param pos_descr positional options
      */
      virtual void
        setPosDesc(positional_options_description&
          pos_descr) {}

      /**
      * @brief Placeholder for printout instructions.
      *
      * Placeholder for printout instructions. Printout should be composed
      * with the ::output(const char*, const char*, ...) function.
      *
      * @param command command object, containing a responce from the blockchain.
      */
      virtual void printout(TeosCommand command, variables_map &vm) {
        cout << command.responseToString(false) << endl;
      }

      virtual void parseGroupVariablesMap(variables_map& vm) 
      {
        bool is_arg = checkArguments(vm) || vm.count("json");
        if (vm.count("json")) {
          reqJson = stringToPtree(json_);
        }
        bool isRaw = vm.count("raw") ? true : false;

        if (is_arg) {
          TeosCommand command = executeCommand();
          if (command.isError_) {
            std::cerr << "ERROR!" << endl << command.errorMsg() << endl;
            return;
          }

          if (vm.count("received")) {
            cout << command.responseToString(isRaw) << endl;
          }
          else {
            printout(command, vm);
          }
        }
      }

      /**
      * @brief Returns command object, containing a responce from the blockchain.
      *
      * @param isRaw raw or pretty printout flag
      * @return TeosCommand command object
      */

      virtual TeosCommand executeCommand() {
        return TeosCommand("", reqJson);
      }
      /**
       * @brief Fills the post json tree according to options.
       *
       * @param vm boost program options variable map
       * @return true if post json is set completely
       * @return false if post json cannot be set completely
       */
      virtual bool checkArguments(variables_map &vm) {
        return false;
      }

      /**
       * @brief json tree to be filled with blockchain responce.
       */
      ptree reqJson;


    public:
      CommandOptions(int argc, const char *argv[]) : ItemOptions(argc, argv) {}
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
}