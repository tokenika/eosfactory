//
// async_tcp_echo_server.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2011 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <cstdlib>
#include <iostream>
#include <string>
#include <boost/thread/thread.hpp>
#include <boost/bind.hpp>
#include <boost/asio.hpp>
#include <boost/process.hpp>
#include <boost/format.hpp>

using boost::asio::ip::tcp;
#define CLEAR_CHAIN_DATABASE_AND_BLOCK_LOG "--resync-blockchain"
#define MAX_LENGTH  1024
#define CHAIN_NODE "eosiod"

namespace pentagon {
  namespace control {
    void stopChain() {
      auto pid = boost::process::system("echo", "$(pidof eosiod)");
      int count = 10;
      while (pid > 0 && count > 0) {
        boost::this_thread::sleep( boost::posix_time::milliseconds(1000) );
        pid = boost::process::system("echo", "$(pidof eosiod)");
        count--;
      }
      if (count > 0) {
        std::cout << boost::format("%1% killed.\n") % CHAIN_NODE;
      }
      else {
        std::cout << boost::format("Failed to kill %1%.\n") % CHAIN_NODE;
      }
    }


  }
}

class session
{
public:
  session(boost::asio::io_service& io_service)
    : socket_(io_service)
  {
  }

  tcp::socket& socket()
  {
    return socket_;
  }

  void start()
  {
    socket_.async_read_some(boost::asio::buffer(data_, MAX_LENGTH),
        boost::bind(&session::handle_read, this,
          boost::asio::placeholders::error,
          boost::asio::placeholders::bytes_transferred));
  }

void parse()
{
  if (std::string(data_) == CLEAR_CHAIN_DATABASE_AND_BLOCK_LOG) {
    boost::process::ipstream pipe_stream;
    boost::process::child c("gcc --version", boost::process::std_out > pipe_stream);

    std::string line;

    while (pipe_stream && std::getline(pipe_stream, line) && !line.empty()) {
        std::cerr << line << std::endl;
    }

    c.detach();
  }
}

private:
  void handle_read(const boost::system::error_code& error,
      size_t bytes_transferred)
  {
    if (!error)
    {
      parse();
      boost::asio::async_write(socket_,
          boost::asio::buffer(data_, bytes_transferred),
          boost::bind(&session::handle_write, this,
            boost::asio::placeholders::error));
    }
    else
    {
      delete this;
    }
  }

  void handle_write(const boost::system::error_code& error)
  {
    if (!error)
    {
      socket_.async_read_some(boost::asio::buffer(data_, MAX_LENGTH),
          boost::bind(&session::handle_read, this,
            boost::asio::placeholders::error,
            boost::asio::placeholders::bytes_transferred));
    }
    else
    {
      delete this;
    }
  }

  tcp::socket socket_;
  char data_[MAX_LENGTH];
};

class server
{
public:
  server(boost::asio::io_service& io_service, short port)
    : io_service_(io_service),
      acceptor_(io_service, tcp::endpoint(tcp::v4(), port))
  {
    start_accept();
  }

private:
  void start_accept()
  {
    session* new_session = new session(io_service_);
    acceptor_.async_accept(new_session->socket(),
        boost::bind(&server::handle_accept, this, new_session,
          boost::asio::placeholders::error));
  }

  void handle_accept(session* new_session,
      const boost::system::error_code& error)
  {
    if (!error)
    {
      new_session->start();
    }
    else
    {
      delete new_session;
    }

    start_accept();
  }

  boost::asio::io_service& io_service_;
  tcp::acceptor acceptor_;
};

int runServer(int argc, char* argv[]) 
{
  try
  {
    if (argc != 2)
    {
      std::cerr << "Usage: async_tcp_echo_server <port>\n";
      return 1;
    }

    boost::asio::io_service io_service;

    using namespace std; // For atoi.
    server s(io_service, atoi(argv[1]));

    io_service.run();
  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
};

int runClient(int argc, char* argv[])
{
  try
  {
    if (argc != 3)
    {
      std::cerr << "Usage: blocking_tcp_echo_client <host> <port>\n";
      return 1;
    }

    boost::asio::io_service io_service;

    tcp::socket s(io_service);
    tcp::resolver resolver(io_service);
    boost::asio::connect(s, resolver.resolve({ argv[1], argv[2] }));

    std::cout << "Enter message: ";
    char request[MAX_LENGTH];
    std::cin.getline(request, MAX_LENGTH);
    size_t request_length = std::strlen(request);
    boost::asio::write(s, boost::asio::buffer(request, request_length));

    char reply[MAX_LENGTH];
    size_t reply_length = boost::asio::read(s,
      boost::asio::buffer(reply, request_length));
    std::cout << "Reply is: ";
    std::cout.write(reply, reply_length);
    std::cout << "\n";
  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
}

int main(int argc, char* argv[])
{
  pentagon::control::stopChain();
}