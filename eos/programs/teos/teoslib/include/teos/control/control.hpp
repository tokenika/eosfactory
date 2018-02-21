#pragma once

#include <string>
#include <vector>

using namespace std;

namespace teos{
  namespace control{

    void startChainNode();
    void killChainNode();

    void buildContract(
      vector<string> src, // list of source c/cpp files
      string targetWastFile,
      vector<string> includeDir = {}
    );

    void generateAbi(
      string typesHpp,
      string targetAbiFile,
      vector<string> includeDir = {} // list of header files  
    );

    void wasmClangHelp();

  }
}