
//#include <stdio.h>
#include <iostream>
#include <cstdarg>
#include <cstdlib>
#include <cstring>

#include "boost/property_tree/json_parser.hpp"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <boost/algorithm/string.hpp>
#include <boost/filesystem.hpp>
#include <boost/asio.hpp>



#define EOSC_ERROR "error" // Error json key

std::string serverLocal = "localhost";
std::string portLocal = "8888";
std::string serwerRemote = "localhost";
std::string portRemote = "8899";

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

    std::stringstream ss;
    boost::property_tree::json_parser::write_json(ss, postJson, false);
    std::string post_msg = ss.str();
    boost::trim(post_msg);

    std::string CRNL = "\r\n";
    std::string request =
      "POST " + path + " HTTP/1.0" + CRNL +
      "Host: " + server + CRNL +
      "content-length: " + std::to_string(post_msg.size()) + CRNL +
      "Accept: */*" + CRNL +
      "Connection: close" + CRNL + CRNL +
      post_msg;
    boost::system::error_code error;

    boost::asio::streambuf request_buffer;
    std::ostream request_stream(&request_buffer);
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

    std::istream response_stream(&response_buffer);
    std::string http_version;
    response_stream >> http_version;
    unsigned int status_code;
    response_stream >> status_code;
    std::string status_message;

    getline(response_stream, status_message);
    if (status_code != 200) {
      rcv_json.put(EOSC_ERROR, status_message);
      return;
    }

    std::string message(boost::asio::buffer_cast<const char*>(response_buffer.data()));
    std::string mark = CRNL + CRNL; // header end mark
    std::size_t found = message.find(mark);
    message = message.substr(found + mark.length(), message.length());

    std::stringstream s_in;
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


using boost::asio::ip::tcp;

enum { max_length = 1024 };

int go(int argc, char* argv[])
{
  try
  {
    if (argc != 3)
    {
      std::cerr << "Usage: blocking_tcp_echo_client <host> <port>\n";
      return 1;
    }

    boost::asio::io_service io_service;

    tcp::resolver resolver(io_service);
    tcp::resolver::query query(tcp::v4(), argv[1], argv[2]);
    tcp::resolver::iterator iterator = resolver.resolve(query);

    tcp::socket socket(io_service);
    boost::asio::connect(socket, iterator);

    using namespace std; // For strlen.
    std::cout << "Enter message: ";
    char request[max_length];
    std::cin.getline(request, max_length);

    boost::asio::write(socket,
      boost::asio::buffer(request, strlen(request)));

    // request sent, responce expected.

    char reply[max_length];
    size_t reply_length = boost::asio::read(socket,
      boost::asio::buffer(reply, strlen(request)));
    std::cout << "Reply is: ";
    std::cout.write(reply, reply_length);
    std::cout << "\n";

    strcat_s(request, max_length, " second request");
    boost::asio::write(socket,
      boost::asio::buffer(request, strlen(request)));
  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
}