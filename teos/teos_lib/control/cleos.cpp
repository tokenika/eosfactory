#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

#include <boost/asio.hpp>
#include <boost/process.hpp>

#include <teoslib/control/config.hpp>
#include <teoslib/control.hpp>
#include <teoslib/control/cleos.hpp>

namespace teos {
  namespace control {

      Cleos::Cleos(
        vector<string> args, string first, string second,
        bool isVerbose, pair<string, string> okSubstring )
      {
        boost::asio::boost::asio::io_service ios;
        


        string cleosExe = getCleosExe(this);


        int result = boost::process::system(
          "/usr/bin/g++", 
          "main.cpp"
          );
      }

  }
}