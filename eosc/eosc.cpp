#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include "boost/date_time/posix_time/posix_time.hpp"
#include <boost/algorithm/string/join.hpp>
#include <boost/program_options.hpp>

#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/punctuation/comma_if.hpp>

#include "eosc_commands/eosc_get_commands.hpp"
#include "eosc.hpp"

void test()
{
  using namespace std;
  using namespace tokenika::eosc;

  vector<string>

    // args = {"", "--xxx"};
    // cout << boost::algorithm::join(args, ", ") << endl;
    // setOptions<tokenika::eosc::GetInfoOptions>(args);

    // args = {"", "--help", "--raw"};
    // cout << boost::algorithm::join(args, ", ") << endl;
    // setOptions<tokenika::eosc::GetInfoOptions>(args);

    // args = {"", "--example"};
    // cout << boost::algorithm::join(args, ", ") << endl;
    // setOptions<tokenika::eosc::GetInfoOptions>(args);

    // args = {"", "--block_num", "25"};
    // cout << boost::algorithm::join(args, ", ") << endl;
    // setOptions<tokenika::eosc::GetInfoOptions>(args);


    args = { "", "--block_num", "25" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = { "", "25" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = { "", "--help", "--raw" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = { "", "--example" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = { "", "--json",
          R"EOF({"block_num_or_id":"25"})EOF" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<tokenika::eosc::GetBlockOptions>(args);
}

#define IF_ELSE(commandName_, classPrefix)                                      \
  if (commandName == #commandName_)                                             \
  {                                                                             \
    tokenika::eosc::classPrefix##Options(argcLeft, argvLeft).go(); \
  }                                                                             \
  else

#define HELP                  \
  std::cout << usage << endl; \
  std::cout << desc << endl;  \
  std::cout << subcommands << endl;

const char* usage = R"EOF(
Command Line Interface to Eos Daemon
Usage: ./eosc [HOST:PORT] [OPTIONS] SUBCOMMAND [SUBCOMAND OPTIONS]
for example:
192.168.229.140:8888 get block 255
)EOF";

const char* subcommands = R"EOF(
Subcommands:
  create                      Create various items, on and off the blockchain
  get                         Retrieve various items and information from the blockchain
  set                         Set or update blockchain state
  transfer                    Transfer EOS from account to account
  wallet                      Interact with local wallet
  benchmark                   Configure and execute benchmarks
  push                        Push arbitrary transactions to the blockchain
)EOF";

int main(int argc, const char *argv[])
{
  using namespace std;
  using namespace tokenika::eosc;
  using namespace boost::program_options;

  const char* argv0 = argv[0];
  int argcLeft;
  const char** argvLeft;

  options_description desc{ "Options" };
  string first;
  string second;

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
              ("verbose,v", "Output verbose messages on error");

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
      first = to_pass_further[0];

    if (vm.count("help"))
      to_pass_further.push_back("-h");

    argcLeft = max((int)to_pass_further.size() - 2 + 1, 1);

    char** arr = new char*[argcLeft];
    arr[0] = new char[strlen(argv0) + 1];
    strcpy_s(arr[0], strlen(argv0) + 1, argv0);

    for (size_t i = 2; i < to_pass_further.size(); i++) {
      arr[i - 1] = new char[to_pass_further[i].size() + 1];

#ifdef WIN32
      strcpy_s(arr[i - 1], to_pass_further[i].size() + 1,
        to_pass_further[i].c_str());
#else
      strcpy(arr[i - 1], to_pass_further[i].c_str());
#endif

    }
    argvLeft = (const char**)arr;

    if (to_pass_further.size() > 1)
      second = to_pass_further[1];

    if (vm.count("help") && second == "")
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

  if (first == "")
  {
    HELP
      return 0;
  }
  else
  {
    if (first.compare("test") == 0)
    {
      test();
      return 0;  string first;
      string second;

    }
    else if (second != "")
    {
      string commandName = first;
      commandName += "_";
      commandName += second;

      IF_ELSE(get_info, GetInfo)
        IF_ELSE(get_block, GetBlock)
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

