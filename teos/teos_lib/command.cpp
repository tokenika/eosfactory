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

#include <teoslib/config.h>
#include <teoslib/command.hpp>

namespace teos
{
  using namespace std;
  using namespace boost::property_tree;

  string TeosCommand::normRequest(ptree& reqJson) {
    stringstream ss;
    json_parser::write_json(ss, reqJson, false);
    string postMsg = ss.str();
    boost::trim(postMsg);
    return postMsg;
  }

  void TeosCommand::normResponse(string response, ptree &respJson) {
    TeosCommand::validateJsonData(response, respJson);
  }

  void TeosCommand::callEosd()
  {
    using namespace std;
    namespace ip = boost::asio::ip;
    namespace pt = boost::property_tree;  
    namespace control = teos::control;

    string address;
    
    if(isWalletCommand()){
      address = TeosCommand::httpWalletAddress.empty()
        ? teos::control::getHttpWalletAddress(this)
        : TeosCommand::httpWalletAddress;
      if(address.empty()) {
      address = TeosCommand::httpAddress.empty()
        ? teos::control::getHttpServerAddress(this)
        : TeosCommand::httpAddress;        
      }
    } else {
      address = TeosCommand::httpAddress.empty()
        ? teos::control::getHttpServerAddress(this)
        : TeosCommand::httpAddress;
    }
    size_t colon = address.find(":");
    string host = string(address.substr(0, colon));
    string port = string(address.substr(colon + 1, address.size()));

    try {
      boost::asio::io_service io_service;

      ip::tcp::resolver resolver(io_service);
      ip::tcp::resolver::query query(host, port);
      ip::tcp::resolver::iterator iterator = resolver.resolve(query);

      ip::tcp::socket socket(io_service);
      boost::asio::connect(socket, iterator);

      string postMsg = normRequest(reqJson_);

      string CRNL = "\r\n";
      string request =
        "POST " + path_ + " HTTP/1.0" + CRNL +
        "Host: " + host + CRNL +
        "content-length: " + to_string(postMsg.size()) + CRNL +
        "Accept: */*" + CRNL +
        "Connection: close" + CRNL + CRNL +
        postMsg;

      //cout << "callEosd request:\n" << request << endl;

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
      ////cout << message << endl;
      normResponse(message, respJson_);
    }
    catch (exception& e) {
      putError(e.what());
    }
  }

  string TeosCommand::httpAddress = "";
  string TeosCommand::httpWalletAddress = "";

  TeosCommand::TeosCommand( string path, ptree reqJson ) 
    : TeosControl(reqJson), path_(path) {
  }

  TeosCommand::TeosCommand( string path) : path_(path) {
  }

}
