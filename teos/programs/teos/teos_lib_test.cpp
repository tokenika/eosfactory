#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "teoslib/teos_get_commands.hpp"

int main()
{
  using namespace tokenika::teos;

  TeosCommand::host = "198.100.148.136";
  TeosCommand::port = "8888";

  ptree getInfoJson;

  // Invoke GetInfo command:
  GetInfo getInfo(getInfoJson);
  cout << getInfo.toStringRcv() << endl;

  if (getInfo.isError()) {
    return -1;
  }

  ptree getBlockJson;

  // Use reference to the last block:
  getBlockJson.put("block_num_or_id",
    getInfo.get<int>("last_irreversible_block_num"));

  // Invoke GetBlock command:
  GetBlock getBlock(getBlockJson);
  cout << getBlock.toStringRcv() << endl;

  if (getBlock.isError()) {
    return -1;
  }

  return 0;
}
