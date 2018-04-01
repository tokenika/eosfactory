
#include <cstdarg>
#include <teoslib/utilities.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>


namespace teos 
{
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
    ptree ptree;
    try {
      stringstream ss;
      ss << json;
      read_json(ss, ptree);
    }
    catch (...) {
      cout << "argument json is missformatted." << endl;
    }
    return ptree;
  }
  
}