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

std::string formatUsage(std::string unixUsage) {
#ifdef WIN32
  std::string windowsCmndUsage = unixUsage;
  boost::replace_all(windowsCmndUsage, "\"", "\"\"\"");
  boost::replace_all(windowsCmndUsage, "'", "\"");
  return windowsCmndUsage;
#else
  return unixUsage;
#endif
}

namespace teos
{
  using namespace std;
  using namespace boost::property_tree;

#define SHARP "#  "
#define INDENT "15"
  boost::format output(string label, string format) {
    string header = (boost::format(SHARP "%1$" INDENT "s: ") % label).str();
    return boost::format(header + format);
  }

  void output(const char* label, const char* format, ...) {
    printf(SHARP "%" INDENT "s: ", label);

    string f(format);
    f += "\n";

    va_list argptr;
    va_start(argptr, format);
    vprintf(f.c_str(), argptr);
    va_end(argptr);
  }

  void output(const char* text, ...) {
    printf(SHARP "%s\n", text);
  }

  ostream& sharp() {
    cout << SHARP;
    return cout;
  }

  void output(string text){
    text = SHARP + text;
    boost::replace_all<string>(text, "\n", "\n" SHARP);
    cout << text << endl;
  }  

  string TeosControl::requestToString(bool isRaw) const {
    stringstream ss;
    json_parser::
      write_json(ss, reqJson_, !isRaw);
    
    string temp = ss.str();
    boost::replace_all(temp, "\\/", "/");
    return temp;
  }

  string TeosControl::responseToString(bool isRaw) const {
    stringstream ss;
    json_parser::
      write_json(ss, respJson_, !isRaw);
    
    string temp = ss.str();
    boost::replace_all(temp, "\\/", "/");
    return temp;
  }

  bool TeosControl::printError() {
    if(isError_) {
      cout << responseToString(true) << endl;
    }
    return isError_;
  }

  string TeosControl::executable = "";
  /*
    The config file is expected in the application directory, or two
    levels above.
  */
  string TeosControl::getConfigJson(){
    namespace bfs = boost::filesystem;
    /*The path to the application directory, relative to the working dir:*/
    bfs::path dirPath = (bfs::path(TeosControl::executable)).parent_path();
    
    if(bfs::exists(dirPath / CONFIG_JSON)) {
      return (dirPath / CONFIG_JSON).string();
    }

    if(bfs::exists(dirPath / "../../" / CONFIG_JSON)) {
      return (dirPath / "../../" / CONFIG_JSON).string();
    }

    return "";
  }

  void TeosControl::validateJsonData(string data, ptree &json) {
    stringstream ss;
    ss << data;
    try {
      read_json(ss, json);
      stringstream ss1; // Try to write json, in order to check it.
      json_parser::write_json(ss1, json, false);
    }
    catch (exception& e) {
      putError("Data is not a json.");
    }      
  }

  ptree TeosControl::getConfig(TeosControl* teosControl) {
    ptree config;
    try
    {
      read_json(getConfigJson(), config);
    }
    catch (exception& e) {
      if(teosControl) {
        teosControl->putError(e.what());
      } else {
        cout << teos_ERROR << endl << e.what() << endl;
      }
    }
    return config;
  }

  void TeosControl::errorRespJson(string sender, string message) 
  {
    if(respJson_.count(teos_ERROR) != 0) {
      return;
    }
    
    if(!sender.empty()) {
      string senderEntry = "\"sender\":\"" + sender + "\"";
      string msgEntry = "\"message\":{" + message + "}";
      respJson_.put(teos_ERROR, "{" + senderEntry + ", " + msgEntry + "}");
    } else {
      respJson_.put(teos_ERROR, message);
    }
    isError_ = true;  
  }

  void TeosControl::putError(string message, string sender) {
    errorRespJson(sender, message);
  }
}
