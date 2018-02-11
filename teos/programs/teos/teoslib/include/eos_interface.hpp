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

  TeosCommand setContract(std::string wastFile, std::string abiFile,
    string account, bool skipSignature, int expiration);  

  TeosCommand getCode(string accountName, string wastFile, string abiFile);
  
  TeosCommand pushMessage(string contract, string action, string data,
    const vector<string> scopes, const vector<string> permissions,
    bool skipSignature, int expiration,
    bool tx_force_unique);
    
  }
}
