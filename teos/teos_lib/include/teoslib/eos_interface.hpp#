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
    unsigned expiration = 30, 
    bool skipSignature = false,
    bool dontBroadcast = false,
    bool forceUnique = false,
    unsigned maxCpuUsage = 0,
    unsigned maxNetUsage = 0);

  TeosCommand setContract(
    string account,
    string contractDir,
    string& wastFile, string& abiFile,
    string permission  = "",
    unsigned expiration = 30,
    bool skipSignature = false,
    bool dontBroadcast = false,
    bool forceUnique = false,
    unsigned maxCpuUsage = 0,
    unsigned maxNetUsage = 0); 
  
  TeosCommand pushAction(
    string contract, string action, string data,
    string permission = "", 
    unsigned expiration = 30,
    bool skipSignature = false,
    bool dontBroadcast = false,
    bool forceUnique = false,
    unsigned maxCpuUsage = 0,
    unsigned maxNetUsage = 0); 

  TeosCommand getCode(
    string accountName, string wastFile, string abiFile);    
  }
}
