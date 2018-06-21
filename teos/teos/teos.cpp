#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/program_options.hpp>

#include <teoslib/control.hpp>
#include <teoslib/control/build_contract.hpp>
#include <teoslib/control/daemon_controls.hpp>
#include <teoslib/control/config.hpp>

#include <teos/teos.hpp>

#define IF_ELSE(commandName_, classPrefix) \
  if (commandName == #commandName_) \
  { \
    classPrefix##Options(argc, argv).go(); \
  } \
  else

#define HELP                  \
  std::cout << usage << endl; \
  std::cout << desc << endl; 

const char* usage = R"(
Command Line Interface to teos
Usage: ./teos [COMMAND] [SUBCOMMAND] [OPTIONS]
)";

int main(int argc, const char *argv[]) {

  using namespace std;
  using namespace teos;
  using namespace teos::control;
  using namespace boost::program_options;

  options_description desc("Options");
  string command;
  string subcommand;

  if (argc > 1){
    command = argv[1];
    argv++;
    argc--;    
  } else {
    HELP
    return 0;
  }

  if (argc > 1){
    subcommand = argv[1];
    argv++;
    argc--;

    string commandName = command + "_" + subcommand;

    IF_ELSE(daemon_start, DaemonStart)
    IF_ELSE(daemon_stop, DaemonStop)
    IF_ELSE(build_contract, BuildContract)
    IF_ELSE(generate_abi, GenerateAbi)
    IF_ELSE(bootstrap_contract, BootstrapContract) 
    IF_ELSE(delete_contract, DeleteContract)    
    IF_ELSE(get_config, GetConfig)    
    {
      cout << "unknown command!" << endl;
    }    
  } else {
    HELP
    return 0;
  }
  return 0;
}

