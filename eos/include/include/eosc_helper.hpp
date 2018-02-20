#pragma once

#include <stdlib.h>
#include <string>
#include <iostream>

using namespace std;

namespace tokenika{ 
  namespace teos{

    class KeyPair {

    public:

      string privateKey;
      string publicKey;

      KeyPair();
    };
  } 
}