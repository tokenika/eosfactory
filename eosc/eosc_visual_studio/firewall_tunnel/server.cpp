#include <iostream>
#include <boost/asio.hpp>

namespace asio = boost::asio;

std::string serverEosc = "localhost";
std::string portEosc = "8899";
std::string serverEosd = "198.100.148.136";
std::string portEosd = "8888";

std::string readline(asio::ip::tcp::socket & socket) {
  asio::streambuf buf;
  asio::read_until(socket, buf, "\n");

  std::string data = asio::buffer_cast<const char*>(buf.data());
  data.erase(--data.end());  // remove the last delimeter
  return data;
}

void sendline(asio::ip::tcp::socket & socket, const std::string& str) {
  const std::string msg = str + "\n";
  asio::write(socket, asio::buffer(msg));
}

int main() {
  asio::io_service ioServiceRead;
  asio::ip::tcp::acceptor acc(
    ioServiceRead,
    asio::ip::tcp::endpoint(asio::ip::tcp::v4(), 31400));
  asio::ip::tcp::socket socketRead(ioServiceRead);
  acc.accept(socketRead);

  asio::io_service ioServiceWrite;

  while (true) {
    std::string str = readline(socketRead);
    std::cout << str << std::endl;




    sendline(socket, "pong");
    std::cout << "sent pong" << std::endl;
  }

  return 0;
}
