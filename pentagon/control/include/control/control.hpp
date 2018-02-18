#pragma once

#include <string>
#include <vector>

using namespace std;

void buildContract(
  vector<string> src, // list of source c/cpp files
  string targetWastFile,
  vector<string> includeDir = {}
  );