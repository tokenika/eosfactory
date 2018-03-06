#pragma once

#include <stdlib.h>
#include <string>

#include <teos/command/command.hpp>

using namespace std;

namespace teos{ 
  namespace command{

    class KeyPair {

    public:
      static string privateK();
      static string prk;
      string privateKey;
      string publicKey;

      KeyPair();
    };


  TeosCommand createAccount(string creator, string name,
    string ownerKey, string activeKey, long long deposit,
    bool skipSignature, int expiration);

  TeosCommand setContract(std::string wastFile, std::string abiFile,
    string account, bool skipSignature, int expiration);  

  TeosCommand getCode(string accountName, string wastFile, string abiFile);
  
  TeosCommand pushAction(string contract, string action, string data,
    const vector<string> scopes, const vector<string> permissions,
    bool skipSignature, int expiration,
    bool tx_force_unique);
    
  }
}
