#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <teos_get_commands.hpp>

#ifdef WIN32
extern "C" FILE*  __cdecl __iob_func(void);
#endif // WIN32

int main(int argc, const char *argv[]) {
#ifdef WIN32
  __iob_func();
#endif // WIN32

  using namespace tokenika::teos;

  TeosCommand::host = TEST_HOST;
  TeosCommand::port = TEST_PORT;

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
