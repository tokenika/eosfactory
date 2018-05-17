
#include <cstdarg>
#include <cstdlib>
#include <iostream>

#include <boost/process.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string.hpp> 

#include "c-callstack.h"
#include <teoslib/utilities.hpp>

using namespace std;

namespace teos 
{
  void boostProcessSystem(string commandLine) {
    namespace  bp = boost::process;
    bp::system(commandLine,
      bp::std_out > stdout,
      bp::std_err > stderr,
      bp::std_in < stdin);
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
    to build specific forms needed elsewhere.
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
    boost::replace_all(json, "\\\"", "\"");
    ptree ptree;
    try {
      stringstream ss;
      ss << json;
      read_json(ss, ptree);
    }
    catch (...) {
      cout << "argument json is missformatted:" << endl;
      cout << json << endl;
      //NL_RETURN(ptree);
    }
    return ptree;
  }
  
  string wslMapWindowsLinux(string path) {
      if( !path.empty() && path.find(":\\") != string::npos)
        {
          boost::replace_all(path, "\\", "/");
          string drive(1, path[0]);
          boost::replace_all(
            path, 
            drive + ":/"
            , "/mnt/" + boost::algorithm::to_lower_copy(drive) + "/");
        }
      return path;
    }           
}