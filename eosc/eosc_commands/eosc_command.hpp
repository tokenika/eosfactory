/**
 * @file eosc_command.hpp
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
#include "boost/date_time/posix_time/posix_time.hpp"
#include <boost/program_options.hpp>

#define EOSC_ERROR "error" // Error json key
#define HOST_DEFAULT "localhost"
#define PORT_DEFAULT "8888"

namespace tokenika
{
  namespace eosc
  {

    /**
     * @brief Converts EOS time string to 'boost::posix_time'.
     *
     * EOS time is a string, for example `2017-07-18T20:16:36`. For processing,
     * it is converted to the boost `ptime`.
     *
     * @param str EOS time string.
     * @return boost::posix_time::ptime
     */
    extern boost::posix_time::ptime strToTime(const std::string str);

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

    /**
     * @brief Given a json, eoscCommandJsongets EOS blockchain responce.
     *
     * Given a json tree and a command path (for example `/v1/chain/GetInfo`),
     * and EOS blockchain communication port (for example `8888`),
     * and EOS blockchain server name (for example `localhost`),
     * gets EOS blockchain responce.
     *
     * @param server EOS blockchain server name
     * @param port EOS blockchain communication port
     * @param path command path
     * @param postJson json eoscCommandJsonto be posted
     * @param jsonRcv json to be filled with received data
     */
    extern void callEosd(
      std::string server,
      std::string port,
      std::string path,
      boost::property_tree::ptree &postJson,
      boost::property_tree::ptree &jsonRcv);

    /**
     * @brief Given a json teoscCommandJsonree, returns the <Type>value of a given path.
     *
     * @tparam Type type of the called value
     * @param json json tree
     * @param path path of the given tree
     * @return Type
     */
    template<typename Type>
    Type getJsonPath(boost::property_tree::ptree json,
      const boost::property_tree::ptree::path_type & path);

    /**
     * @brief Given a text json tree, returns the equivalent `boost ptree`.
     *
     * @param json
     * @return boost::property_tree::ptree
     */
    extern boost::property_tree::ptree stringToPtree(
      std::string json);

    /**
     * @brief Basic connection to the blockchain.
     *
     * Given a command path (for example `/v1/chain/GetBlock`), and a json tree
     * (for example {"block_num_or_id"="25"}),
     * connects to the blockchain and receives a json reflacting an aspect of the
     * blockchain state.
     *
     * `EoscCommand` is the superclass for any specific command class in this
     * library.
     *
     * Parameters of the connection used are specified in file `eosc_config.json`,
     * in the root directory of the project.
     *
     */
    class EoscCommand
    {
      std::string path;
      boost::property_tree::ptree jsonRcv;
      bool isErrorSet = false;
      bool isRaw;

    protected:
      boost::property_tree::ptree postJson;

    public:
      static std::string host;
      static std::string port;
      static std::string walletHost;
      static std::string walletPort;
      static bool verbose;

      /**
       * @brief Initiates members, and calls the blockchain
       *
       * @param path command path, for example `/v1/chain/GetBlock`
       * @param postJson json tree, for example {"block_num_or_id"="25"}
       * @param isRaw boolean, determines printout of the to-string methods
       */
      EoscCommand(
        std::string path,
        boost::property_tree::ptree postJson,
        bool isRaw = false);

      /**
       * @brief Error flag.
       *
       * @return true if EOS blockchain responce is normal
       * @return false if EOS blockchain responce is not normal
       */
      bool isError() const {
        return isErrorSet;
      }

      /**
       * @brief Blockchain responce
       *
       * @return boost::property_tree::ptree blockchain responce
       */
      boost::property_tree::ptree getRcvJson() const {
        return jsonRcv;
      }

      /**
       * @brief Post json string representation
       *
       * Returns post json string representation. I can be pretty or raw,
       * depending ib the `isRaw` flag.
       *
       * @return std::string post json string representation
       */
      std::string toStringPost() const;

      /**
       * @brief Received json string representation
       *
       * Returns received json string representation. I can be pretty or raw,
       * depending ib the `isRaw` flag.
       *
       * @return std::string received json string representation
       */
      std::string toStringRcv() const;

      /**
       * @brief Returns a value of a path of the received json.
       *
       * @tparam Type type of the value
       * @param path json tree path to the value
       * @return Type the value of the given path
       */
      template<typename Type>
      Type get(const boost::property_tree::ptree::path_type & path) const {
        return getJsonPath<Type>(jsonRcv, path);
      }
    };

    //http://boost.cowic.de/rc/pdf/program_options.pdf
    /**
     * @brief Command-line wrapper for eosc commands.
     *
     * The prototype for command-line wrappers for eosc commands. Defines
     * common options like 'help', 'example'.
     *
     * Also, the class defines virtual methods that are placeholders for
     * specific definitions of the command that is wrapped.
     */
    class CommandOptions
    {
      int argc_;
      const char **argv_;
      std::string json_;

      /**
       * @brief List of options common to all commands.
       *
       * @param common boost program options description object.
       */
      void commonOptions(boost::program_options::options_description& common)
      {
        using namespace std;
        using namespace boost::program_options;

        common.add_options()
          ("help,h", "Help screen")
          ("wallet-host", value<string>()->default_value(HOST_DEFAULT),
            "The host where eos-wallet is running")
            ("wallet-port", value<string>()->default_value(PORT_DEFAULT),
              "The port where eos-wallet is running")
              ("verbose,v", "Output verbose messages on error")
          ("json,j",
            value<string>(&json_),
            "Json argument")
            ("received,v", "Print received json")
          ("raw,r", "Not pretty print")
          ("example,e", "Usage example");
      }

    protected:

      /**
       * @brief json tree to be filled with blockchain responce.
       */
      boost::property_tree::ptree postJson;

      /**
       * @brief Command 'usage' instruction.
       *
       * @return const char* usage text
       */
      virtual const char* getUsage() { return ""; }

      /**
       * @brief List of the command options.
       *
       * @return boost::program_options::options_description command options
       */
      virtual boost::program_options::options_description options() {
        boost::program_options::options_description special("");
        return special;
      }

      /**
       * @brief Positional options.
       *
       * @param pos_descr positional options
       */
      virtual void
        setPosDesc(boost::program_options::positional_options_description&
          pos_descr) {}

      /**
       * @brief Fills the post json tree according to options.
       *
       * @param vm boost program options variable map
       * @return true if post json is set completely
       * @return false if post json cannot be set completely
       */
      virtual bool setJson(boost::program_options::variables_map &vm) {
        return false;
      }

      /**
       * @brief Returns command object, containing a responce frosource /mnt/hgfs/Workspaces/EOS/eoscBash/eoscBash $EOSIO_INSTALL_DIR m the blockchain.
       *
       * @param isRaw raw or pretty printout flag
       * @return EoscCommand command object
       */
      virtual EoscCommand getCommand(bool isRaw) {
        return EoscCommand("", postJson);
      }

      /**source /mnt/hgfs/Workspaces/EOS/eoscBash/eoscBash $EOSIO_INSTALL_DIR
       * @brief Placeholder for any exemplary code snippet.
       *
       */
      virtual void getExample() {}

      /**
       * @brief Placeholder for printout instructions.
       *
       * Placeholder for printout instructions. Printout should be composed
       * with the ::output(const char*, const char*, ...) function.
       *
       * @param command command object, containing a responce from the blockchain.
       */
      virtual void getOutput(EoscCommand command) {
        std::cout << command.toStringRcv() << std::endl;
      }

    public:
      CommandOptions(int argc, const char *argv[]) : argc_(argc), argv_(argv) {}
      void go();
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
    template<class T> static void setOptions(std::vector<std::string> strVector) {

      int argc = (int)strVector.size();
      char** argv = new char*[argc];
      for (int i = 0; i < argc; i++) {
        argv[i] = new char[strVector[i].size() + 1];

#ifdef WIN32
        strcpy_s(argv[i], strVector[i].size() + 1,
          strVector[i].c_str());
#else
        strcpy(argv[i], strVector[i].c_str());
#endif
        strcpy_s(argv[i], strVector[i].size() + 1,
          strVector[i].c_str());
      }

      T(argc, (const char**)argv).go();
      delete[] argv;
    }
  }
}