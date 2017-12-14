#include <stdio.h>
#include <iostream>
#include <cstdarg>

#include <boost/property_tree/json_parser.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/filesystem.hpp>
#include <boost/asio.hpp>

#ifdef WIN32
#else
#include <pthread.h>
#endif


#include "eosc_command.hpp"
#include "../eosc_config.h"

namespace tokenika
{
  namespace eosc
  {

    void output(const char* label, const char* format, ...) {
      std::printf("## %20s: ", label);

      std::string f(format);
      f += "\n";

      va_list argptr;
      va_start(argptr, format);
      std::vprintf(f.c_str(), argptr);
      va_end(argptr);
    }

    template<typename Type> Type getJsonPath(boost::property_tree::ptree json,
      const boost::property_tree::ptree::path_type & path) {
      return json.get<Type>(path);
    }

    template<> boost::posix_time::ptime getJsonPath(boost::property_tree::ptree json,
      const boost::property_tree::ptree::path_type & path) {
      return strToTime(json.get<std::string>(path));
    }

    struct InitGetJson {
      /*
      Template function has to be used, in order to force compiler
      to build specific forms needed elsewhere in the program and
      in the library.
      */
      std::string strVal;
      int intVal;
      float floatVal;
      boost::posix_time::ptime ptime;

      InitGetJson() {
        try {
          boost::property_tree::ptree json;
          boost::property_tree::ptree::path_type path;

          strVal = getJsonPath<std::string>(json, path);
          intVal = getJsonPath<int>(json, path);
          floatVal = getJsonPath<float>(json, path);
          ptime = getJsonPath<boost::posix_time::ptime>(json, path);
        }
        catch (...) {}
      }
    };
    InitGetJson init;

    boost::posix_time::ptime strToTime(const std::string str) {
      std::string temp = boost::replace_all_copy(str, "-", "");
      temp = boost::replace_all_copy(temp, ":", "");
      boost::posix_time::ptime t((boost::posix_time::from_iso_string)(temp));
      return t;
    }

    boost::property_tree::ptree stringToPtree(std::string json) {
      boost::property_tree::ptree ptree;
      try {
        std::stringstream ss;
        ss << json;
        boost::property_tree::read_json(ss, ptree);
      }
      catch (...) {
        std::cerr << "argument json is missformatted." << std::endl;
      }
      return ptree;
    }

    void callEosd(
      std::string server,
      std::string port,
      std::string path,
      boost::property_tree::ptree &postJson,
      boost::property_tree::ptree &rcv_json)
    {

      using namespace std;
      namespace ip = boost::asio::ip;
      namespace pt = boost::property_tree;

      try {
        boost::asio::io_service io_service;

        ip::tcp::resolver resolver(io_service);
        ip::tcp::resolver::query query(server, port);
        ip::tcp::resolver::iterator iterator = resolver.resolve(query);

        ip::tcp::socket socket(io_service);
        boost::asio::connect(socket, iterator);

       stringstream ss;
        boost::property_tree::json_parser::write_json(ss, postJson, false);
       string post_msg = ss.str();
        boost::trim(post_msg);

       string CRNL = "\r\n";
       string request =
          "POST " + path + " HTTP/1.0" + CRNL +
          "Host: " + server + CRNL +
          "content-length: " +to_string(post_msg.size()) + CRNL +
          "Accept: */*" + CRNL +
          "Connection: close" + CRNL + CRNL +
          post_msg;
        boost::system::error_code error;

        boost::asio::streambuf request_buffer;
       ostream request_stream(&request_buffer);
        request_stream << request;
        boost::asio::write(socket, request_buffer, error);

        if (error) {
          rcv_json.put(EOSC_ERROR, error.message());
          return;
        }

        // request sent, responce expected.

        boost::asio::streambuf response_buffer;
        boost::asio::read(socket, response_buffer, boost::asio::transfer_all(),
          error);
        if (error && error != boost::asio::error::eof) {
          rcv_json.put(EOSC_ERROR, error.message());
          return;
        }

       istream response_stream(&response_buffer);
       string http_version;
        response_stream >> http_version;
        unsigned int status_code;
        response_stream >> status_code;
       string status_message;

        getline(response_stream, status_message);
        if (status_code != 200) {
          string msg =
            string("status code is ") + to_string(status_code);
          msg += string("\n eosd response is ") +
            string(boost::asio::buffer_cast<const char*>(
              response_buffer.data()));
          rcv_json.put(EOSC_ERROR, msg);
          return;
        }

       string message(boost::asio::buffer_cast<const char*>(response_buffer.data()));
       string mark = CRNL + CRNL; // header end mark
       size_t found = message.find(mark);
        message = message.substr(found + mark.length(), message.length());

       stringstream s_in;
        s_in << message;
        try {
          boost::property_tree::read_json(s_in, rcv_json);
        }
        catch (...) {
          rcv_json.put(EOSC_ERROR, "Failed to read eosc.");
          return;
        }

      }
      catch (std::exception& e) {
        rcv_json.put(EOSC_ERROR, e.what());
        return;
      }
    }

    /***************************************************************************
      Definitions for class EoscCommand.
    ****************************************************************************/

    EoscCommand::EoscCommand(
      std::string path,
      boost::property_tree::ptree postJson,
      bool isRaw) : path(path), postJson(postJson), isRaw(isRaw)
    {
      std::string host_(host);
      std::string port_(port);

      boost::property_tree::ptree config;
      try 
      {
        boost::property_tree::read_json(CONFIG_JSON, config);
      }
      catch (...) {
        boost::filesystem::path full_path(boost::filesystem::current_path());
        printf("ERROR: Cannot read config file %s!\n", CONFIG_JSON);
        printf("Current path is: %s\n", full_path.string().c_str());
        printf("The config json file is expected there!");
        exit(-1);
      }    
      
      if(host == "")
        host_ = config.get("eosc.server", HOST_DEFAULT);
      if(port == "")
        port_ = config.get("eosc.port", PORT_DEFAULT);
      if(EoscCommand::walletHost == "")
        EoscCommand::walletHost = config.get("eosc.walletServer", HOST_DEFAULT);
      if(EoscCommand::walletPort == "")
        EoscCommand::walletPort = config.get("eosc.walletPort", PORT_DEFAULT);
      if(!EoscCommand::verbose)
        EoscCommand::verbose = config.get("eosc.verbose", false);

      callEosd(host_, port_, path, postJson, jsonRcv);
      try {
        jsonRcv.get<std::string>(EOSC_ERROR);
        isErrorSet = true;
        return;
      }
      catch (...) {}
    }

    std::string EoscCommand::toStringPost() const {
      std::stringstream ss;
      boost::property_tree::json_parser::
        write_json(ss, postJson, !isRaw);
      return ss.str();
    }

    std::string EoscCommand::toStringRcv() const {
      std::stringstream ss;
      boost::property_tree::json_parser::
        write_json(ss, jsonRcv, !isRaw);
      return ss.str();
    }
    
    std::string EoscCommand::host = "";
    std::string EoscCommand::port = "";
    std::string EoscCommand::walletHost = "";
    std::string EoscCommand::walletPort = "";
    bool EoscCommand::verbose = false;

    /******************************************************************************
      Definitions for class 'command_options'
    ******************************************************************************/

    void CommandOptions::go() 
    {
      using namespace boost::program_options;

      try {
        bool isRaw = false;

        options_description desc{ "Options" };
        options_description common("");
        commonOptions(common);
        desc.add(options()).add(common);
        positional_options_description pos_desc;
        setPosDesc(pos_desc);
        command_line_parser parser{ argc_, argv_ };
        parser.options(desc).positional(pos_desc);//.allow_unregistered();
        parsed_options parsed_options = parser.run();

        variables_map vm;
        store(parsed_options, vm);
        notify(vm);

        if (vm.count("help")) {
          std::cout << getUsage() << std::endl;
          std::cout << desc << std::endl;
          return;
        }        
        
        bool is_arg = setJson(vm) || vm.count("json");
        if (vm.count("json")) {
          postJson = stringToPtree(json_);
        }
        isRaw = vm.count("raw") ? true : false;

        if (vm.count("example")) {
          getExample();
        }
        else if (is_arg) {
          EoscCommand command = getCommand(isRaw);
          if (command.isError())
          {
            std::cerr << "ERROR!"  << std::endl
              << command.get<std::string>(EOSC_ERROR) << std::endl;
            return;
          }
          if (vm.count("received")) {
            std::cout << command.toStringRcv() << std::endl;
          }
          else {
             getOutput(command);
          }
        }
        else if (vm.count("unreg")) {
          std::cout << getUsage() << std::endl;
          std::cout << desc << std::endl;
        }
      }
      catch (const error &ex) {
        std::cerr << ex.what() << std::endl;
      }
    }
  }
}
