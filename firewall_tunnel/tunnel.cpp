//eosc -H 198.100.148.136 -p 8888 get block 330000

#include <iostream>
#include <boost/asio.hpp>
#include <boost/program_options.hpp>

#include "tunnel.hpp"

namespace asio = boost::asio;

std::string serverEosc = "127.0.0.1";
std::string portEosc = "8899";
std::string serverEosd = "198.100.148.136";
std::string portEosd = "8888";
bool isVerbose = false;

std::string readEosc(asio::ip::tcp::socket & socket) {
  asio::streambuf response;
  asio::read_until(socket, response, "}");
  std::string data = asio::buffer_cast<const char*>(response.data());
  return data;
}

void writeEosc(asio::ip::tcp::socket & socket, const std::string& str) {
  const std::string msg = str;
  asio::write(socket, asio::buffer(msg));
}

std::string eosdResp;

void firewallTunnel()
{
  using namespace std;

  asio::io_service ioServiceEosc;

  asio::io_service ioServiceEosd;
  asio::ip::tcp::socket socketEosd(ioServiceEosd);
  asio::ip::tcp::resolver resolver(ioServiceEosd);
  asio::ip::tcp::resolver::query query(serverEosd, portEosd);
  asio::ip::tcp::resolver::iterator iterator = resolver.resolve(query);

  string h = asio::ip::host_name();
  cout << "Host name is " << h << '\n';
  cout << "IP addresses are: \n";
  for_each(resolver.resolve({ h, "" }), {}, [](const auto& re) {
    cout << re.endpoint().address() << '\n';
  });

  while (true)
  {
    asio::ip::tcp::acceptor acc(
      ioServiceEosc,
      asio::ip::tcp::endpoint(asio::ip::address::from_string(serverEosc.c_str()),
        stoi(portEosc.c_str()))
    );

    asio::ip::tcp::socket socketEosc(ioServiceEosc);
    acc.accept(socketEosc);
    asio::io_service ioServiceWrite;

    string request = readEosc(socketEosc);
    if (isVerbose) {
      cout << "request to eosd is:" << endl << request << endl;
    }

    {
      boost::asio::connect(socketEosd, iterator);
      boost::asio::streambuf request_buffer;
      ostream request_stream(&request_buffer);
      request_stream << request;
      boost::system::error_code error;
      boost::asio::write(socketEosd, request_buffer, error);

      if (error) {
        string msg = "writing request to eosd: ";
        msg += error.message();
        eosdResp = msg;
      }
      else {
        // request sent, responce expected.

        boost::asio::streambuf response_buffer;
        boost::asio::read(socketEosd, response_buffer, boost::asio::transfer_all(),
          error);
        if (error && error != boost::asio::error::eof) {
          eosdResp = error.message();
        }
        else
        {
          istream response_stream(&response_buffer);
          eosdResp = string(boost::asio::buffer_cast<const char*>(
            response_buffer.data()));
        }
      }
    }

    writeEosc(socketEosc, eosdResp);
    if (isVerbose) {
      cout << "response from eosd is:" << endl << eosdResp << endl;
    }
  }
}

int main(int argc, const char *argv[])
{

  using namespace std;
  using namespace boost::program_options;

  try
  {
    options_description desc{ "Options" };
    desc.add_options()
      ("help,h", "Help screen")
      ("eosc-host,S", value<string>()->default_value("127.0.0.1"),
        "The host where eosC is running")
        ("eosc-port,P", value<string>()->default_value("8899"),
          "The port where eosC is running")
          ("eosd-host,s", value<string>()->default_value("127.0.0.1"),
            "The host where eosD is running")
            ("eosd-port,p", value<string>()->default_value("8888"),
              "The port where eosD is running")
              ("verbose,V", "Print trafic");

    variables_map vm;
    store(parse_command_line(argc, argv, desc), vm);
    notify(vm);

    if (vm.count("help"))
    {
      cout << desc << '\n';
      return 0;
    }
    if (vm.count("eosc-host")) {
      serverEosc = vm["eosc-host"].as<string>();
    }
    if (vm.count("eosc-port")) {
      portEosc = vm["eosc-port"].as<string>();
    }
    if (vm.count("eosd-host")) {
      serverEosd = vm["eosd-host"].as<string>();
    }
    if (vm.count("eosd-port")) {
      portEosc = vm["eosd-port"].as<string>();
    }
    if (vm.count("verbose")) {
      isVerbose = true;
    }
  }
  catch (const error &ex)
  {
    cerr << ex.what() << '\n';
  }

  firewallTunnel();
  return 0;
}
