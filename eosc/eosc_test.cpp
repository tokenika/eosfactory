#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/algorithm/string/join.hpp>

#include "eosc_commands/eosc_get_commands.hpp"

void test()
{
  using namespace std;
  using namespace tokenika::eosc;

  vector<string>

  args = {"", "--xxx"};
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetInfoOptions>(args);

  args = {"", "--help", "--raw"};
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetInfoOptions>(args);

  args = {"", "--example"};
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetInfoOptions>(args);

  args = {"", "--block_num", "25"};
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetInfoOptions>(args);


    args = { "", "--block_num", "25" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetBlockOptions>(args);

  args = { "", "25" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetBlockOptions>(args);

  args = { "", "--help", "--raw" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetBlockOptions>(args);

  args = { "", "--example" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetBlockOptions>(args);

  args = { "", "--json",
    R"EOF({"block_num_or_id":"25"})EOF" };
  cout << boost::algorithm::join(args, ", ") << endl;
  setOptions<GetBlockOptions>(args);
}