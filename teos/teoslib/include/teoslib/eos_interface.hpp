#pragma once

#include <stdlib.h>
#include <string>

#include <teoslib/command.hpp>

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


  TeosCommand createAccount(
    string creator, string name,
    string ownerKey, string activeKey, 
    string permission  = "",
    int expiration = 30, 
    bool skipSignature = false,
    bool dontBroadcast = false,
    bool forceUnique = false);

  TeosCommand setContract(
    string account,
    string wastFile, string abiFile = "",
    string permission  = "",
    int expiration = 30,
    bool skipSignature = false,
    bool dontBroadcast = false,
    bool forceUnique = false); 

  TeosCommand getCode(
    string accountName, string wastFile, string abiFile);
  
  TeosCommand pushAction(
    string contract, string action, string data,
    string permission = "", 
    int expiration = 30,
    bool skipSignature = false,
    bool dontBroadcast = false,
    bool forceUnique = false);    
  }
}
