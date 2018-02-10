#pragma once

#include <stdlib.h>
#include <string>

#include <teos_command.hpp>

using namespace std;

namespace tokenika{ 
  namespace teos{

    class KeyPair {

    public:
      static string privateK();
      static string prk;
      string privateKey;
      string publicKey;

      KeyPair();
    };


  TeosCommand createAccount(string creator, string name,
    string ownerKey, string activeKey,
    bool skipSignature, int expiration, int deposit);

  TeosCommand setContract(std::string wastPath, std::string abiPath,
    std::string account, bool skipSignature, int expiration);  
  
  } 
}
