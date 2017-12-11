#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/algorithm/string.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include "boost/date_time/posix_time/posix_time.hpp"
#include <boost/algorithm/string/join.hpp>

#include <boost/preprocessor/repetition/repeat.hpp>
#include <boost/preprocessor/punctuation/comma_if.hpp>

#include "eosc_commands/eosc_get_commands.hpp"
#include "eosc.hpp"

using namespace std;

void test()
{
  vector<string>

      args = {"tokenika::eosc::command_options", "--xxx"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetInfoOptions>(args);

  args = {"tokenika::eosc::command_options", "--help", "--raw"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetInfoOptions>(args);

  args = {"tokenika::eosc::command_options", "--example"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetInfoOptions>(args);

  args = {"tokenika::eosc::command_options", "--block_num", "25"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetInfoOptions>(args);

  args = {"tokenika::eosc::command_options", "--help", "--raw"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = {"tokenika::eosc::command_options", "--example"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = {"tokenika::eosc::command_options", "--block_num", "25"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetBlockOptions>(args);

  args = {"tokenika::eosc::command_options", "--json",
          R"EOF({"block_num_or_id":"25"})EOF"};
  cout << boost::algorithm::join(args, ", ") << endl;
  tokenika::eosc::setOptions<tokenika::eosc::GetBlockOptions>(args);
}

#define IF_ELSE(commandName_, classPrefix)                 \
  if (command_name == #commandName_)                       \
  {                                                        \
    tokenika::eosc::classPrefix##Options(argc, argv).go(); \
  }                                                        \
  else

int main(int argc, const char *argv[])
{
  if (argc > 1)
  {
    string ipAddress(argv[1]);
    size_t colon = ipAddress.find(":");
    if (colon != std::string::npos)
    {
      tokenika::eosc::EoscCommand::host = string(ipAddress.substr(0, colon));
      tokenika::eosc::EoscCommand::port = string(ipAddress.substr(colon + 1, 
        ipAddress.size()));
      argv++;
      argc--;
    }
  }

  string command_name;
  if (argc > 1)
  {
    command_name = argv[1];
    if (command_name.compare("test") == 0)
    {
      test();
      return 0;
    }
    argv++;
    argc--;
    if (argc > 1)
    {
      command_name += "_";
      command_name += argv[1];
      argv++;
      argc--;

      IF_ELSE(get_info, GetInfo)
      IF_ELSE(get_block, GetBlock)
      {
        cerr << "unknown command!";
      }
    }
  }
  return 0;
}
/*
Testing with VMware Ubuntu:
Virtual Machine Settings > Network Adapter :
  Bridget, Replicate physical network connection state

ifconfig

ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
inet6 fe80::e6a5:d11:3cab:ec93  prefixlen 64  scopeid 0x20<link>
ether 00:0c:29:e3:76:b8  txqueuelen 1000  (Ethernet)
RX packets 183  bytes 16810 (16.8 KB)
RX errors 0  dropped 0  overruns 0  frame 0
TX packets 191  bytes 22942 (22.9 KB)
TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

SSH session, 
Remote host: 192.168.1.100
User name: cartman
Port: 22

OK

The same works with 
Virtual Machine Settings > Network Adapter :
Host-only: A provate network shared with the host

*/
