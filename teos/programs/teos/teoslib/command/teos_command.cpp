#include <stdio.h>
#include <iostream>
#include <cstdarg>

#include <boost/property_tree/json_parser.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/filesystem.hpp>
#include <boost/asio.hpp>

#ifdef WIN32
#else
#include <pthread.h>
#endif

#include <teos_command.hpp>
#include <teos_config.h>

using namespace std;
using namespace boost::property_tree;

namespace tokenika
{
  namespace teos
  {

    void output(const char* label, const char* format, ...) {
      printf("## %20s: ", label);

      string f(format);
      f += "\n";

      va_list argptr;
      va_start(argptr, format);
      vprintf(f.c_str(), argptr);
      va_end(argptr);
    }

    void output(const char* text, ...) {
      printf("## %s\n", text);
    }

    template<typename Type> Type getJsonPath(ptree json,
      const ptree::path_type & path) {
      return json.get<Type>(path);
    }

    template<> boost::posix_time::ptime getJsonPath(ptree json,
      const ptree::path_type & path) {
      return strToTime(json.get<string>(path));
    }

    struct InitGetJson {
      /*
      Template function has to be used, in order to force compiler
      to build specific forms needed elsewhere in the program and
      in the library.
      */
      string strVal;
      int intVal;
      float floatVal;
      boost::posix_time::ptime ptime;

      InitGetJson() {
        try {
          ptree json;
          ptree::path_type path;

          strVal = getJsonPath<string>(json, path);
          intVal = getJsonPath<int>(json, path);
          floatVal = getJsonPath<float>(json, path);
          ptime = getJsonPath<boost::posix_time::ptime>(json, path);
        }
        catch (...) {}
      }
    };
    InitGetJson init;

    boost::posix_time::ptime strToTime(const string str) {
      string temp = boost::replace_all_copy(str, "-", "");
      temp = boost::replace_all_copy(temp, ":", "");
      boost::posix_time::ptime t((boost::posix_time::from_iso_string)(temp));
      return t;
    }

    ptree stringToPtree(string json) {
      ptree ptree;
      try {
        stringstream ss;
        ss << json;
        read_json(ss, ptree);
      }
      catch (...) {
        cerr << "argument json is missformatted." << endl;
      }
      return ptree;
    }

/***************************************************************************
Definitions for class TeosCommand.
****************************************************************************/

    ptree TeosCommand::errorRespJson(string sender, string message) {
      ptree respJson;
      string senderEntry = "\"sender\":\"" + sender + "\"";
      string msgEntry = "\"message\":{" + message + "}";
      respJson.put(teos_ERROR, "{" + senderEntry + ", " + msgEntry + "}");
      return respJson;
    }

    void TeosCommand::putError(string sender, string message) {
      respJson_ = errorRespJson(sender, message);
      isError_ = true;
    }

    void TeosCommand::putError(string msg) {
      putError(path_, msg);
    }

    string TeosCommand::normRequest(ptree& reqJson) {
      stringstream ss;
      json_parser::write_json(ss, reqJson, false);
      string postMsg = ss.str();
      boost::trim(postMsg);
      return postMsg;
    }

    void TeosCommand::normResponse(string response, ptree &respJson) {
      stringstream ss;
      ss << response;
      try {
        read_json(ss, respJson);
        stringstream ss1; // Try to write respJson, in order to check it.
        json_parser::write_json(ss1, respJson, false);
      }
      catch (exception& e) {
        putError(e.what());
      }
    }

    ptree TeosCommand::getConfig(bool verbose) {
      ptree config;
      try
      {
        read_json(CONFIG_JSON, config);
      }
      catch (...) {
        boost::filesystem::path full_path(boost::filesystem::current_path());
        if (verbose) {
          printf("ERROR: Cannot read config file %s!\n", CONFIG_JSON);
          printf("Current path is: %s\n", full_path.string().c_str());
          printf("The config json file is expected there!");
        }
      }
      return config;
    }

    void TeosCommand::callEosd()
    {
      using namespace std;
      namespace ip = boost::asio::ip;
      namespace pt = boost::property_tree;

      ptree config = getConfig();

      string host_;
      string port_;

      if (isWalletCommand()) {
        host_ = (walletHost != "") ? walletHost : 
          ((host != "") ? host : config.get("teos.walletServer", HOST_DEFAULT));
        port_ = (walletPort != "") ? walletPort : 
          ((port != "") ? port : config.get("teos.walletPort", PORT_DEFAULT));
      }
      else {
        host_ = (host == "") ? config.get("teos.server", HOST_DEFAULT) : host;
        port_ = (port == "") ? config.get("teos.port", PORT_DEFAULT) : port;
      }
      
      TeosCommand::verbose = (!TeosCommand::verbose) ? config.get("teos.verbose", false) :
        TeosCommand::verbose;

      try {
        boost::asio::io_service io_service;

        ip::tcp::resolver resolver(io_service);
        ip::tcp::resolver::query query(host_, port_);
        ip::tcp::resolver::iterator iterator = resolver.resolve(query);

        ip::tcp::socket socket(io_service);
        boost::asio::connect(socket, iterator);

        string postMsg = normRequest(reqJson_);

        string CRNL = "\r\n";
        string request =
          "POST " + path_ + " HTTP/1.0" + CRNL +
          "Host: " + host_ + CRNL +
          "content-length: " + to_string(postMsg.size()) + CRNL +
          "Accept: */*" + CRNL +
          "Connection: close" + CRNL + CRNL +
          postMsg;

        //cout << request << endl;

        boost::system::error_code error;

        boost::asio::streambuf request_buffer;
        ostream request_stream(&request_buffer);
        request_stream << request;
        boost::asio::write(socket, request_buffer, error);

        if (error) {
          putError(error.message());
          return;
        }

        // request sent, responce expected.

        boost::asio::streambuf response_buffer;
        boost::asio::read(socket, response_buffer, boost::asio::transfer_all(),
          error);
        if (error && error != boost::asio::error::eof) {
          putError(error.message());
          return;
        }

        istream response_stream(&response_buffer);
        string http_version;
        response_stream >> http_version;
        unsigned int status_code;
        response_stream >> status_code;
        string status_message;

        getline(response_stream, status_message);
        if (!(status_code == 200 || status_code == 201 || status_code == 202)) {
          string msg = string("status code is ") + to_string(status_code);
          msg += string("\n eosd response is ") +
            string(boost::asio::buffer_cast<const char*>(
              response_buffer.data()));
          putError(msg);
          return;
        }

        string message(boost::asio::buffer_cast<const char*>(response_buffer.data()));
        string mark = CRNL + CRNL; // header end mark
        size_t found = message.find(mark);
        message = message.substr(found + mark.length(), message.length());
        normResponse(message, respJson_);
      }
      catch (exception& e) {
        putError(e.what());
      }
    }

    TeosCommand::TeosCommand( string path, ptree reqJson, bool isRaw ) 
      : path_(path), reqJson_(reqJson), isRaw_(isRaw) {
    }

    TeosCommand::TeosCommand( string path, bool isRaw ) 
      : path_(path), isRaw_(isRaw) {
    }

    TeosCommand::TeosCommand(bool isError, ptree respJson)
      : isRaw_(true), respJson_(respJson) {
    }
    
    string TeosCommand::requestToString(bool isRaw) const {
      stringstream ss;
      json_parser::
        write_json(ss, reqJson_, !isRaw);
      return ss.str();
    }

    string TeosCommand::requestToString() const {
      return requestToString(isRaw_);
    }

    string TeosCommand::responseToString(bool isRaw) const {
      stringstream ss;
      json_parser::
        write_json(ss, respJson_, !isRaw);
      return ss.str();
    }

    string TeosCommand::responseToString() const {
      return responseToString(isRaw_);
    }

    string TeosCommand::host = "";
    string TeosCommand::port = "";
    string TeosCommand::walletHost = "";
    string TeosCommand::walletPort = "";
    bool TeosCommand::verbose = false;

    /******************************************************************************
      Definitions for class 'command_options'
    ******************************************************************************/

    void CommandOptions::onError(TeosCommand command) {
      std::cerr << "ERROR!" << endl << command.get<string>(teos_ERROR) << endl;
    }

    const string formatUsage(string unixUsage) {
#ifdef WIN32
      string windowsCmndUsage = unixUsage;
      boost::replace_all(windowsCmndUsage, "\"", "\"\"\"");
      boost::replace_all(windowsCmndUsage, "'", "\"");
      return windowsCmndUsage;
#else
      return unixUsage;
#endif
    }

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
          cout << formatUsage(getUsage()) << endl;
          cout << desc << endl;
          return;
        }

        bool is_arg = setJson(vm) || vm.count("json");
        if (vm.count("json")) {
          reqJson = stringToPtree(json_);
        }
        isRaw = vm.count("raw") ? true : false;

        if (vm.count("example")) {
          getExample();
        }
        else if (is_arg) {
          TeosCommand command = getCommand(isRaw);
          if (command.isError()) {
            onError(command);
            return;
          }
           
          if (vm.count("received")) {
            cout << command.responseToString() << endl;
          }
          else {
            getOutput(command);
          }
        }
        else if (vm.count("unreg")) {
          cout << formatUsage(getUsage()) << endl;
          cout << desc << endl;
        }
      }
      catch (const error &ex) {
        cerr << ex.what() << endl;
      }
    }
  }
}
