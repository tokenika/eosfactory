#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "teoslib/teos_get_commands.hpp"

#ifdef _MSC_VER
static FILE arr[3];
extern "C" FILE*  __cdecl __iob_func(void) {
  throw std::runtime_error(
    "See https://stackoverflow.com/questions/30412951/unresolved-external-symbol-imp-fprintf-and-imp-iob-func-sdl2");
  return arr;
}
#endif // _MSC_VER

int main() {

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
