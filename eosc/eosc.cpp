#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include "boost/date_time/posix_time/posix_time.hpp"
#include <boost/program_options.hpp>

#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/punctuation/comma_if.hpp>

#include "eosc_commands/eosc_get_commands.hpp"
#include "eosc_commands/eosc_wallet_commands.hpp"

#include "eosc.hpp"
#include "eosc_test.hpp"
#include "subcommands.hpp"

#define IF_ELSE(commandName_, classPrefix)                                      \
  if (commandName == #commandName_)                                             \
  {                                                                             \
    tokenika::eosc::classPrefix##Options(argcLeft, argvLeft).go(); \
  }                                                                             \
  else

#define HELP                  \
  std::cout << usage << endl; \
  std::cout << desc << endl;  \
  std::cout << commands << endl;

const char* usage = R"EOF(
Command Line Interface to Eos Daemon
Usage: ./eosc [HOST:PORT] [OPTIONS] [COMMAND] [SUBCOMMAND] [OPTIONS]
for example:
192.168.229.140:8888 get block 255
)EOF";

const char* commands = R"EOF(
Commands:
  create      Create various items, on and off the blockchain
  get         Retrieve various items and information from the blockchain
  set         Set or update blockchain state
  transfer    Transfer EOS from account to account
  wallet      Interact with local wallet
  benchmark   Configure and execute benchmarks
  push        Push arbitrary transactions to the blockchain
  test        Basic test of the application
)EOF";

std::map<const std::string, const std::string> subcommandMap = {
  { "create", create },
  { "get", getSubcommands },
  { "set", setSubcommands },
  { "wallet", wallet },
  { "benchmark", benchmark },
  { "push", push }
};

int main(int argc, const char *argv[])
{
  using namespace std;
  using namespace tokenika::eosc;
  using namespace boost::program_options;

  const char* argv0 = argv[0];
  int argcLeft;
  const char** argvLeft;

  options_description desc{ "Options" };
  string command;
  string subcommand;

  if (argc > 1)
  {
    string ipAddress(argv[1]);
    size_t colon = ipAddress.find(":");
    if (colon != std::string::npos)
    {
      EoscCommand::host = string(ipAddress.substr(0, colon));
      EoscCommand::port = string(ipAddress.substr(colon + 1,
        ipAddress.size()));
      argv++;
      argc--;
    }

    if (strcmp(argv[1], "tokenika") == 0)
    {
      EoscCommand::host = "198.100.148.136";
      EoscCommand::port = "8888";
      argv++;
      argc--;
    }
  }

  try
  {
    options_description desc{ "Options" };
    desc.add_options()
      ("help,h", "Help screen")
      ("host,H", value<string>()->default_value(
        EoscCommand::host == "" ? HOST_DEFAULT : EoscCommand::host),
        "The host where eosd is running")
      ("port,p", value<string>()->default_value(
        EoscCommand::port == "" ? PORT_DEFAULT : EoscCommand::port),
        "The port where eosd is running")
      ("wallet-host", value<string>()->default_value(HOST_DEFAULT),
        "The host where eos-wallet is running")
      ("wallet-port", value<string>()->default_value(PORT_DEFAULT),
        "The port where eos-wallet is running")
      ("verbose,V", "Output verbose messages on error");

    command_line_parser parser{ argc, argv };
    parser.options(desc).allow_unregistered();
    parsed_options parsed_options = parser.run();

    vector<string> to_pass_further = collect_unrecognized(
      parsed_options.options, include_positional);

    variables_map vm;
    store(parsed_options, vm);
    notify(vm);

    if (vm.count("host"))
      EoscCommand::host = string(vm["host"].as<string>());
    if (vm.count("port"))
      EoscCommand::port = string(vm["port"].as<string>());

    if (vm.count("wallet-host"))
      EoscCommand::walletHost = string(vm["wallet-host"].as<string>());
    if (vm.count("wallet-port"))
      EoscCommand::walletPort = string(vm["wallet-port"].as<string>());
    if (vm.count("verbose"))
      EoscCommand::verbose = true;

    if (to_pass_further.size() > 0)
      command = to_pass_further[0];

    if (to_pass_further.size() > 1)
    {
      subcommand = to_pass_further[1];
      to_pass_further.erase(to_pass_further.begin(), to_pass_further.begin() + 2);
    } else
    {
      if (subcommandMap.find(command) != subcommandMap.end())
      {
        cout << subcommandMap.at(command) << endl;
        return(0);
      }
    }

    to_pass_further.insert(to_pass_further.begin(), argv0);    
    if (vm.count("help"))
      to_pass_further.push_back("-h");
    if (vm.count("verbose"))
      to_pass_further.push_back("-V");

    { // Convert to_pass_further std::vector to char** arr:
      argcLeft = (int)to_pass_further.size();
      char** arr = new char*[argcLeft];
      for (size_t i = 0; i < to_pass_further.size(); i++) {
        arr[i] = new char[to_pass_further[i].size() + 1];

#ifdef _MSC_VER
        strcpy_s(arr[i], to_pass_further[i].size() + 1,
          to_pass_further[i].c_str()); 
#else
        strcpy(arr[i], to_pass_further[i].c_str());
#endif
      }
      argvLeft = (const char**)arr;
    }

    if (vm.count("help") && command == "")
    {
      HELP
        return 0;
    }
  }
  catch (const boost::program_options::error &ex)
  {
    std::cerr << ex.what() << '\n';
    exit(-1);
  }

  if (command == "")
  {
    HELP
      return 0;
  }
  else
  {
    if (command.compare("test") == 0)
    {
      test();
      return 0;
    }
    else if (subcommand != "")
    {
      string commandName = command;
      commandName += "_";
      commandName += subcommand;

      IF_ELSE(get_info, GetInfo)
      IF_ELSE(get_block, GetBlock)
      IF_ELSE(get_account, GetAccount)
      {
        cerr << "unknown command!" << endl;
      }
      delete[] argvLeft;
    }
    else
    {
      HELP
        return 0;
    }
  }
  return 0;
}

