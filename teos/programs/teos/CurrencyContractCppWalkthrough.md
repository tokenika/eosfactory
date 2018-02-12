# Example "Currency" Contract Walkthrough with Teos C++ library

## Rationale

Our aim is to provide methods and tools for development of EOS contracts. The construction part of an EOS contract development is currently done with a C++ environment. Therefore we want to have all the contract testing possibilities available within the same C++ IDE.

More, we want to have this all on the MS Visual Studio platform, in order to limit the scope of skills needed for working on smart contracts.          

Now, we already have our plan advanced:
* We heve a trans-system version of a substantial part of the EOS code, corrected to be compatible with Windows;
* C++ library for both Windows and Unix systems;
* Command line drivers for this library classes that implement a CLI for EOS.

In this article, we present, in action, our library. It is developed enough to implement an EOS contract testing routine with the Boost Unit Test Framework.

## Walkthrough

We present the library with the *Example Currency Contract Walkthrough* from the EOS README, however we rephrase it, a little bit. It follows the code of a testing program source file, chunked for better readability.

### C++ overhead, skip it
```
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/format.hpp>
#include <boost/property_tree/ptree.hpp>

#include <teos_get_commands.hpp>
#include <teos_create_commands.hpp>
#include <teos_set_commands.hpp>
#include <teos_wallet_commands.hpp>
#include <teos_push_commands.hpp>

#ifdef WIN32 // A temporary fix for a bug
extern "C" FILE*  __cdecl __iob_func(void);
#endif // WIN32

int main(int argc, const char *argv[]) {

  using namespace tokenika::teos;
```

```
  TeosCommand::host = "localhost";
  TeosCommand::port = "8888";
  string walletName = "default";
  string password = "PW5JbTXTxszm9RU2Kh29MfDuPw7x1FLPHasE9Pz7whJWp71hzPLQ5";
  string initaKeyPriv = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
  string wastFile 
    = "/mnt/hgfs/Workspaces/EOS/eos/build/contracts/currency/currency.wast";
  string abiFile 
    = "/mnt/hgfs/Workspaces/EOS/eos/build/contracts/currency/currency.abi";
```
### Walkthrough
```
  // Alice owns account named 'inita' as she possess its private key, which is 
  // 'initaKeyPriv'. She keeps this key in an EOS wallet, in order to prove 
  // (to the blockchain) her rights. 
  // She creates a wallet if she does not have any ...
```
```
  WalletCreate walletCreate(walletName);
  if (walletCreate.isError()) {
   cerr << walletCreate.responseToString() << endl;
  } else {
    cout << "wallet password: " << walletCreate.get<string>("password") << endl;
  }
```
```
  // OUTPUT:
  // wallet password: "PW5HtaVuqrcupUCoAkrbFhU5tpnujoVse5Fo8Jm3AQjFDi1jG9Wmo"
```
```
  WalletUnlock walletUnlock(password, walletName);
  if(walletUnlock.isError()){
    cerr << walletUnlock.responseToString() << endl;
  } else {
    cout << walletUnlock.responseToString(false) << endl;
  }
```
```
  // OUTPUT (empty output means OK here):
  // {
  // }
```
```
  // ... and puts the private key into it:
```
```
  WalletImport walletImportInita(walletName, initaKeyPriv);
  if (walletImportInita.isError()) {
   cerr << walletImportInita.responseToString() << endl;
  } else {
    cout << walletImportInita.responseToString(false) << endl;
  }
  // OUTPUT (empty output means OK here):
  // {
  // }

  // Alice needs another account to keep some budget money. She can create this 
  // account, named 'currency', under the authority of her 'inita' account. Two 
  // pairs of cryptographic keys are needed for the creation. Let us call them 
  // 'owner' and 'active'. 
  CreateKey createKeyOwner("owner");
  CreateKey createKeyActive("active");
  cout << createKeyActive.responseToString(false) << endl;
  // OUTPUT:
  // {
  //   "name": "active",
  //   "privateKey": "5JUJVM9BX69GB3eVCrKdsGX32nPZj52Z8T99CzkG51JWQmLdT1X",
  //   "publicKey": "EOS6iHkQJQyhDd5PWJNSTXcGqWxBWLuyPYPxswPvWXVYMwa16VbN7"
  // }

  /*
  The keys will prove the access permission for Alicia and, perhaps, for 
  somebody else. The private key of the 'active' pair has to be imported to 
  the Alicia's wallet:
  */
  WalletImport walletImportActive(walletName, 
   createKeyActive.get<string>("privateKey"));
  if (walletImportActive.isError()) {
   cerr << walletImportActive.responseToString() << endl;
  } else {
    cout << walletImportActive.responseToString(false) << endl;
  }
  // OUTPUT (empty output means OK here):
  // {
  // }

  // Now, Alicia can create her new 'currency' account. For testing, she can put 
  // any deposit there for free, what is not possible in the reality:
  long long deposit = 50;
  CreateAccount createAccount("inita", "currency", 
   createKeyOwner.get<string>("publicKey"), 
   createKeyActive.get<string>("publicKey"), deposit);
  if (createAccount.isError()) {
   cerr << createAccount.responseToString() << endl;
  } else {
    cout << createAccount.responseToString(false) << endl;
  }

  // If no error output from the previous creation step, account 'currency' is 
  // operational. This is the ID of the transaction that has launched it:
  cout << "transaction id: " << createAccount.get<string>("transaction_id") 
    << endl;
  // OUTPUT:
  // {
  // }
  
  // Alice can inspect her account. For test purposes, 'currency' account has got 
  // 1EOS, for free.
  GetAccount getAccount("currency");
  cout << "eos balance: " << getAccount.get<string>("eos_balance") << endl;

  // Alicia needs means to transfer her money from 'currency' account to 'inita' 
  // account. In EOS, such a transfer can be done with a 'smart contract', 
  // a specialized chunk of code registered with the blockchain. 
  
  // A contract that can satisfy Alice is written in the file 
  // eos/contracts/currency/currency.cpp. This C++ source has to be compiled into 
  // WebAssembly code (.wast); this is already done, resulting in files 
  // eos/build/contracts/currency/currency.wast and 
  // eos/build/contracts/currency/currency.abi.
  SetContract setContract("currency", wastFile, abiFile);
  if (setContract.isError()) {
    cerr << setContract.responseToString() << endl;
    return 0;
  }

  // The contract is registered with the blockchain now. This is the ID of the 
  // transaction that has launched it:
  cout << "transaction id: " << setContract.get<string>("transaction_id") 
    << endl;

  // Alice can inspect the contract code. If the code hash is all-zero, 
  // there is no current contract.
  GetCode getCode("currency");
  cout << "code hash: " << getCode.get<string>("code_hash") << endl;
  // OUTPUT:
  // code hash: "0000000000000000000000000000000000000000000000000000000000000000"

  // Alice can inspect her account, as well:
  {
    GetTable getTable("currency", "currency", "account");
    cout << getTable.responseToString() << endl;
  }

  // Let Alice do a money transfer ...
  PushMessage pushMessage("currency", "transfer", 
    "{\"from\":\"currency\",\"to\":\"inita\",\"quantity\":50}", 
    "currency,inita", "currency@active");
  if(.isError()){
    cout << pushMessage.responseToString() << endl;
  } else {
    cout << pushMessage.responseToString(false) << endl;
  }

  // ... and see the result:
  {
    GetTable getTable("currency", "currency", "account");
    cout << getTable.responseToString() << endl;
  }
```
###  C++ final overhead, skip it
```
#ifdef WIN32
  __iob_func(); //A temporary patch for a bug.
#endif // WIN32

  return 1;
}

```