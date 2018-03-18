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
#include <teoslib/control.hpp>

namespace teos
{
  using namespace std;
  using namespace boost::property_tree;

  string TeosControl::requestToString(bool isRaw) const {
    stringstream ss;
    json_parser::
      write_json(ss, reqJson_, !isRaw);
    return ss.str();
  }

  string TeosControl::responseToString(bool isRaw) const {
    stringstream ss;
    json_parser::
      write_json(ss, respJson_, !isRaw);
    return ss.str();
  }
}
