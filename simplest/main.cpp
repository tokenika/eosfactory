#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "boost/property_tree/ptree.hpp"
#include "boost/property_tree/json_parser.hpp"

#include <boost/log/core.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/sinks/text_file_backend.hpp>
#include <boost/log/utility/setup/file.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>
#include <boost/log/sources/severity_logger.hpp>
#include <boost/log/sources/record_ostream.hpp>

#include <pthread.h>
#include <config.h>

using namespace std;
using boost::format;

string errorJson (string message){
   stringstream re;
   re << format("{\"error\":\"%1%\"}") % message;
   return re.str();
}

struct info{
   int head_block_num;
   int last_irreversible_block_num;
   string head_block_id;
   string head_block_time;
   string head_block_producer;
   string recent_slots;
   long participation_rate;
   void load(const std::string &filename);
   void save(const std::string &filename);
};

void initLog(){
   namespace pt = boost::property_tree;
   namespace logging = boost::log;
   namespace src = boost::log::sources;
   namespace sinks = boost::log::sinks;
   namespace keywords = boost::log::keywords;

   pt::ptree tree;
   pt::read_json(CONFIG_JSON, tree);
   boost::log::trivial::severity_level severity = 
      (boost::log::trivial::severity_level)tree.get("logging.severity",4);
   logging::core::get()->set_filter
      (
         logging::trivial::severity >= severity
      );
   string logFile = tree.get("logging.logFile","");
   if(logFile.length() > 0)
   {
      logging::add_file_log
      (
         keywords::file_name = "",
         keywords::rotation_size = 10 * 1024 * 1024//,
         // keywords::format = 
         //    tree.get("logging.format","[%TimeStamp%]: %Message%")
         
      );
   }   
}

int main (int argc, char *argv[]) {
   initLog();
   
   BOOST_LOG_TRIVIAL(trace) << "A trace severity message";
   BOOST_LOG_TRIVIAL(debug) << "A debug severity message";
   BOOST_LOG_TRIVIAL(info) << "An informational severity message";
   BOOST_LOG_TRIVIAL(warning) << "A warning severity message";
   BOOST_LOG_TRIVIAL(error) << "An error severity message";
   BOOST_LOG_TRIVIAL(fatal) << "A fatal severity message";


   // const string server = "localhost";
   // const string port = "8888";
   // const string path = "/v1/chain/get_info";
   // const string postjson = "";

   //printf("", server, port, );
   // string json = callEosd(server, port, path, postjson);
   // cout <<json << "\n";

   return 0;
}