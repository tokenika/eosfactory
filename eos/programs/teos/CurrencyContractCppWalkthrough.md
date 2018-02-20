# Example "Currency" Contract Walkthrough with Teos C++ library

## Rationale

Our aim is to provide methods and tools for development of EOS contracts. The construction part of an EOS contract development is currently done with a C++ environment. Therefore we want to have all the contract testing possibilities available within the same C++ IDE.

More, we want to have this all on the MS Visual Studio platform, in order to limit the scope of skills needed for working on smart contracts.          

We have advanced since the previous post:
* We have a trans-system version of a substantial part of the EOS code, corrected to be compatible with Windows;
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

#include <get_commands.hpp>
#include <create_commands.hpp>
#include <set_commands.hpp>
#include <wallet_commands.hpp>
#include <push_commands.hpp>

#ifdef WIN32 // A temporary fix for a bug.
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
  // Alice owns account named 'inita' since she possess its private key, which 
  // is 'initaKeyPriv'. She keeps this key in her EOS wallet, in order to prove 
  // (to the blockchain) her rights. 
  
  // She creates a wallet if she does not have any ...
```
```cpp
  WalletCreate walletCreate(walletName);
  if (walletCreate.isError()) {
   cerr << walletCreate.responseToString() << endl;
  } else {
    cout << "wallet password: " << walletCreate.get<string>("password") << endl;
  }
```
```cpp
// OUTPUT:
// wallet password: "PW5J48ERsPeusMRyEBLLworWTY2LFnB6yR6Fi6nvFhQvRy3BUAcsE"
```
```
  // ... and puts the private key into it:
```
```cpp
  WalletImport walletImportInita(walletName, initaKeyPriv);
  if (walletImportInita.isError()) {
   cerr << walletImportInita.responseToString() << endl;
  } else {
    cout << walletImportInita.responseToString(false) << endl;
  }
```
```cpp
// OUTPUT (empty output means OK here):
// {
// }
```
```
  // The wallet can lock themself later on. Alice can unlock it with the 
  // password:
```
```cpp
  WalletUnlock walletUnlock(password, walletName);
  if(walletUnlock.isError()){
    cerr << walletUnlock.responseToString() << endl;
  } else {
    cout << walletUnlock.responseToString(false) << endl;
  }
```
```cpp
// OUTPUT (empty output means OK here):
// {
// }
```
```
  // Alice needs another account to keep some budget money. She can create 
  // this account, named 'currency', under the authority of her 'inita' account. 
  // Two pairs of cryptographic keys are needed for the creation. Let us call 
  // them 'owner' and 'active'. 
```
```cpp
  CreateKey createKeyOwner("owner");
  cout << createKeyOwner.responseToString(false) << endl; 
```
```
// OUTPUT:
// {
//     "name": "owner",
//     "privateKey": "5JoShiYHAZ5EtmZTiyfBcXXBAjeVTJPx8rujTAg1CUxZEnVBUbb",
//     "publicKey": "EOS7g7Jcnse742LHD96bm34EE8n7CoP19io3uruQv7osobnh7FY1J"
// }

  CreateKey createKeyActive("active");
  cout << createKeyActive.responseToString(false) << endl;
// OUTPUT:
// {
//     "name": "active",
//     "privateKey": "5KVeFdHpXB6ivRXhqRxvegGRB1b6uSNwDEMkSZkXj1qt3w1kkEP",
//     "publicKey": "EOS7jMz68MxycP6fGmXbrtJv8ZMDti2NW3X9MEkLczPuEjm271mcV"
// }

  // The keys will prove access permissions. The private key of the 'active' 
  // pair has to be imported to the owner's wallet:
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
  long long deposit = 1;
  CreateAccount createAccount("inita", "currency", 
   createKeyOwner.get<string>("publicKey"), 
   createKeyActive.get<string>("publicKey"), deposit);
  if (createAccount.isError()) {
   cerr << createAccount.responseToString() << endl;
  } else {
    cout << createAccount.responseToString(false) << endl;
  }
//  OUTPUT:
//   {
//   "transaction_id": "c2a59485fe795f2d6d7a0c44614188a3bdbb0f81ca4945e0cf3c766fdd8e96e3",
//   "processed": {
//     "ref_block_num": 1423,
//     "ref_block_prefix": 2244224674,

// }

  // If the previous creation step was successful, account 'currency' is 
  // operational now. This is the ID of the transaction that has launched it:
  cout << "transaction id: " << createAccount.get<string>("transaction_id") 
    << endl;
// OUTPUT:
// {
// transaction id: "b0f42ee1a50604ce2d1d1b4b3e069912952906014a2bdbe4107d7c8d4ab8b87b"
// }
  
  // Alice can inspect her account:
  {
    GetAccount getAccount("currency");
    cout << "eos balance: " << getAccount.get<string>("eos_balance") << endl;
    cout << "staked balance: " << getAccount.get<string>("staked_balance") << endl;
    cout << "unstaking balance: " << getAccount.get<string>("unstaking_balance") 
      << endl;
  }
// OUTPUT:
// {
// eos balance: 0.0000 EOS
// staked balance: 0.0001 EOS
// eos balance: 0.0000 EOS
// }

  // Alicia needs means to transfer her money from 'currency' account to 'inita' 
  // account. In EOS, such a transfer can be done with a 'smart contract', 
  // a specialized chunk of code registered with the blockchain. 
  
  // A contract that can satisfy Alice is written in the file 
  // eos/contracts/currency/currency.cpp. This C++ source has to be compiled into 
  // WebAssembly code (.wast); this is already done, resulting in files 
  // eos/build/contracts/currency/currency.wast and 
  // eos/build/contracts/currency/currency.abi.

  // Alicia uploads the contract:
  SetContract setContract("currency", wastFile, abiFile);
  if (setContract.isError()) {
    cerr << setContract.responseToString() << endl;
  }

  // The contract is registered with the blockchain now. This is the ID of the 
  // transaction that has launched it:
  cout << "transaction id: " << setContract.get<string>("transaction_id") 
    << endl;
// OUTPUT:
// transaction id: c450a6803e9f0266b3416ed0ee3c9fe36504ecc8181a1ed7489a1ea5d3df5848

  // Alice can inspect the contract code. If the code hash is not all-zero, 
  // the contract exists:
  GetCode getCode("currency");
  cout << "code hash: " << getCode.get<string>("code_hash") << endl;
  // OUTPUT:
  // code hash: "9b9db1a7940503a88535517049e64467a6e8f4e9e03af15e9968ec89dd794975"

  // Alice can inspect her account, as well:
  {
    GetTable getTable("currency", "currency", "account");
    cout << getTable.responseToString() << endl;
  }
// OUTPUT:
// {
//     "rows": [
//         {
//             "key": "account",
//             "balance": "1000000000"
//         }
//     ],
//     "more": "true"
// }

  // Let Alice do a money transfer ...
  PushMessage pushMessage("currency", "transfer", 
    "{\"from\":\"currency\",\"to\":\"inita\",\"quantity\":50}", 
    "currency,inita", "currency@active");
  if(pushMessage.isError()){
    cout << pushMessage.responseToString() << endl;
  } else {
    cout << pushMessage.responseToString(false) << endl;
  }
// OUTPUT:
// {
//     "transaction_id": "2cbb4d211f27500ad63792b61a5d3ce46733f7d90d3bc97b3ef1cb80d876fd28",
//     "processed": {
//         "ref_block_num": "3356",
//         "ref_block_prefix": "2746369842",
//         "expiration": "2018-02-13T09:30:45",
//         "scope": [
//             "currency",
//             "inita"
//         ],
//         "signatures": [
//             "1f7db39cd4be19714988e8f3174ec6170ea2740170aeff05ae3a6bf586fe38a43c35502670ac5c752f2de5973d9281458ae05decfb0d5f339e68e86222b9e0c654"
//         ],
//         "messages": [
//             {
//                 "code": "currency",
//                 "type": "transfer",
//                 "authorization": [
//                     {
//                         "account": "currency",
//                         "permission": "active"
//                     }
//                 ],
//                 "data": {
//                     "from": "currency",
//                     "to": "inita",
//                     "quantity": "50"
//                 },
//                 "hex_data": "0000001e4d75af46000000000093dd743200000000000000"
//             }
//         ],
//         "output": [
//             {
//                 "notify": [
//                     {
//                         "name": "inita",
//                         "output": {
//                             "notify": "",
//                             "deferred_trxs": ""
//                         }
//                     }
//                 ],
//                 "deferred_trxs": ""
//             }
//         ]
//     }
// }

  // ... and see the result:
  {
    GetTable getTable("inita", "currency", "account");
    cout << getTable.responseToString() << endl;
  }
// OUTPUT:
// {
//     "rows": [
//         {
//             "key": "account",
//             "balance": "50"
//         }
//     ],
//     "more": "true"
// }

  {
    GetTable getTable("currency", "currency", "account");
    cout << getTable.responseToString() << endl;
  }
// OUTPUT:
// {
//     "rows": [
//         {
//             "key": "account",
//             "balance": "999999950"
//         }
//     ],
//     "more": "true"
// }

```
###  C++ final overhead, skip it
```
#ifdef WIN32
  __iob_func(); //A temporary patch for a bug.
#endif // WIN32

  return 1;
}

```