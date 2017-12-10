#pragma once

#include <stdlib.h>
#include <string>
#include <boost/property_tree/ptree.hpp>

#define ERROR "error" // Error json key

namespace pentagon{

   extern std::string eos_name(
      const unsigned long long ull);

   extern unsigned long long eos_name(
      const char* str);

   extern void callEosd(
      std::string server, 
      std::string port, 
      std::string path,
      std::string postjson,
      boost::property_tree::ptree &tree);
}