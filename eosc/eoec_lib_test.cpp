#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "eosclib/eosc_get_commands.hpp"

int main()
{
  using namespace tokenika::eosc;

  EoscCommand::host = "198.100.148.136";
  EoscCommand::port = "8888";

  ptree getInfoJson;

  // Invoke 'GetInfo' command:
  GetInfo getInfo(getInfoJson);
  cout << getInfo.toStringRcv() << endl;

  ptree getBlockJson;

  // Use reference to the last block:
  getBlockJson.put("block_num_or_id",
    getInfo.get<int>("last_irreversible_block_num"));
  GetBlock getBlock(getBlockJson);
  cout << getBlock.toStringRcv() << endl;

  return 0;
}
