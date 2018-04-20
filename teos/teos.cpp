#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/program_options.hpp>

#include <teoslib/command/get_commands.hpp>
#include <teoslib/command/wallet_commands.hpp>
#include <teoslib/command/create_commands.hpp>
#include <teoslib/command/set_commands.hpp>
#include <teoslib/command/push_commands.hpp>
#include <teoslib/command/other_commands.hpp>
#include <teoslib/command/subcommands.hpp>

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
  std::cout << desc << endl;  \
  std::cout << commands << endl;

const char* usage = R"EOF(
Command Line Interface to Eos Daemon
Usage: ./teos [HOST:PORT] [OPTIONS] [COMMAND] [SUBCOMMAND] [OPTIONS]
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
  node        Test EOS chain node procedures
)EOF";

std::map<const std::string, const std::string> subcommandMap = {
  { "create", createSubcommands },
  { "get", getSubcommands },
  { "set", setSubcommands },
  { "wallet", walletSubcommands },
  { "benchmark", benchmarkSubcommands },
  { "push", pushSubcommands }
};

int main(int argc, const char *argv[]) {

  using namespace std;
  using namespace teos;
  using namespace teos::command;
  using namespace teos::control;
  using namespace boost::program_options;

  options_description desc{ "Options" };
  string command;
  string subcommand;

  TeosCommand::httpAddress = LOCALHOST_HTTP_ADDRESS;
  TeosCommand::httpWalletAddress = TeosCommand::httpAddress;

  if (argc > 1)
  {
    string httpAddress(argv[1]);
    size_t colon = httpAddress.find(":");

    if (colon != std::string::npos)
    {
      TeosCommand::httpAddress = httpAddress;
      TeosCommand::httpWalletAddress = TeosCommand::httpAddress;
      argv++;
      argc--;
    }

    if (strcmp(argv[1], USE_CONFIG_JSON) == 0)
    {
      TeosCommand::httpAddress = "";
      TeosCommand::httpWalletAddress = TeosCommand::httpAddress;
      argv++;
      argc--;
    }    

    if (strcmp(argv[1], LOCALHOST_ADDRESS) == 0)
    {
      argv++;
      argc--;
    }
    
    if (strcmp(argv[1], TEST_ADDRESS) == 0)
    {
      TeosCommand::httpAddress = TEST_HTTP_ADDRESS;
      TeosCommand::httpWalletAddress = TeosCommand::httpAddress;
      argv++;
      argc--;
    }
  }

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

    IF_ELSE(version_client, VersionClient)
    IF_ELSE(get_info, GetInfo)
    IF_ELSE(get_block, GetBlock)
    IF_ELSE(get_account, GetAccount)
    IF_ELSE(get_accounts, GetAccounts)
    IF_ELSE(get_code, GetCode)
    IF_ELSE(get_table, GetTable)
    IF_ELSE(wallet_create, WalletCreate)
    IF_ELSE(wallet_list, WalletList)
    IF_ELSE(wallet_keys, WalletKeys)
    IF_ELSE(wallet_import, WalletImport)
    IF_ELSE(wallet_open, WalletOpen)
    IF_ELSE(wallet_lock, WalletLock)
    IF_ELSE(wallet_lock_all, WalletLockAll)
    IF_ELSE(wallet_unlock, WalletUnlock)
    IF_ELSE(create_key, CreateKey)
    IF_ELSE(create_account, CreateAccount)
    IF_ELSE(set_contract, SetContract)
    IF_ELSE(push_action, PushAction)
    IF_ELSE(daemon_start, DaemonStart)
    IF_ELSE(daemon_stop, DaemonStop)
    IF_ELSE(build_contract, BuildContract)
    {
      cout << "unknown command!" << endl;
    }    
  } else {
    HELP
    return 0;
  }
  return 0;
}

