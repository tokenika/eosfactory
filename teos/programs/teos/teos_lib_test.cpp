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

#ifdef WIN32
extern "C" FILE*  __cdecl __iob_func(void);
#endif // WIN32

int main(int argc, const char *argv[]) {
#ifdef WIN32
  __iob_func();
#endif // WIN32

//string json = R"EOF(
//{
//    "transaction_id": "173f8663351a76cff55477fed7c98b97fbf3a64810406e0d69d22fb9d1dc31f9",
//    "processed": {
//        "ref_block_num": "398",
//        "ref_block_prefix": "1965811712",
//        "expiration": "2018-02-09T18:58:13",
//        "scope": [
//            "eos",
//            "inita"
//        ],
//        "signatures": [
//            "201c684017f4c481e921a33447997041f67f3f25ba50e1ac11aea8bbe16de7e411717efd814678d90cf3973256a5b02cb3fcf0a76c9843f6b3ea93f3b9c969737e"
//        ],
//        "messages": [
//            {
//                "code": "eos",
//                "type": "newaccount",
//                "authorization": [
//                    {
//                        "account": "inita",
//                        "permission": "active"
//                    }
//                ],
//                "data": {
//                    "creator": "inita",
//                    "name": "currency",
//                    "owner": {
//                        "threshold": "1",
//                        "keys": [
//                            {
//                                "key": "EOS8ccReS2wUNbQjViJXb4GoXP9L5JXKh83Mbz1iFXdVCA3zaLUfT",
//                                "weight": "1"
//                            }
//                        ],
//                        "accounts": ""
//                    },
//                    "active": {
//                        "threshold": "1",
//                        "keys": [
//                            {
//                                "key": "EOS7KuaHugzeNMT3tyYUZNFJRqPBuiH9QasrBpEHsaKvgi2dKoqRu",
//                                "weight": "1"
//                            }
//                        ],
//                        "accounts": ""
//                    },
//                    "recovery": {
//                        "threshold": "1",
//                        "keys": "",
//                        "accounts": [
//                            {
//                                "permission": {
//                                    "account": "inita",
//                                    "permission": "active"
//                                },
//                                "weight": "1"
//                            }
//                        ]
//                    },
//                    "deposit": "0.0001 EOS"
//                },
//                "hex_data": "000000000093dd740000001e4d75af46010000000103eabb35a0f5dc9f60f5beaad955b5b28728db300b28c0177f49e7f1edd1c5864a010000010000000103411b2132013266eb1e087cd06f1c247cec3f85d4a94d513b8ec2f76e3a6708f9010000010000000001000000000093dd7400000000a8ed32320100010000000000000004454f5300000000"
//            }
//        ],
//        "output": [
//            {
//                "notify": "",
//                "deferred_trxs": ""
//            }
//        ]
//    }
//}
//)EOF";
//
//stringstream ss; 
//ss << json;
//ptree tree;
//json_parser::read_json(ss, tree);
//cout << tree.get<string>("transaction_id") << endl;
//cout << boost::format("transaction ID: %1%\n") 
//% tree.get<string>("transaction_id") << endl;
//cout << boost::format("eos balance: %1%\n") % tree.get<string>("eos_balance");


  using namespace tokenika::teos;

  TeosCommand::host = "localhost";
  TeosCommand::port = "8888";
  string walletName = "default";
  string initaKeyPriv = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
  string wastFile = "/mnt/hgfs/Workspaces/EOS/eos/build/contracts/currency/currency.wast";
  string abiFile = "/mnt/hgfs/Workspaces/EOS/eos/build/contracts/currency/currency.abi";

  ///*
  //Alice owns account named 'inita' as she possess its private key, which is 
  //'initaKeyPriv'. She keeps this key in an EOS wallet, in order to prove 
  //(to the blockchain) her rights. 
  //
  //She creates a wallet if she does not have any ...
  //*/
  //WalletCreate walletCreate(walletName);
  //if (walletCreate.isError) {
  //  cerr << walletCreate.toStringRcv() << endl;
  //}

  //WalletUnlock walletUnlock(walletName);

  ///*
  //... and puts the private key into it:
  //*/
  //WalletImport walletImportInita(walletName, initaKeyPriv);
  //if (walletImportInita.isError) {
  //  cerr << walletImportInita.toStringRcv() << endl;
  //}

  ///*
  //Alice needs another account to keep some budget money. She can create this 
  //account, named 'currency', under the authority of her 'inita' account. Two 
  //pairs of cryptographic keys are needed for the creation. Let us call them 
  //'owner' and 'active'. 
  //*/
  //CreateKey createKeyOwner("owner");
  //CreateKey createKeyActive("active");

  ///*
  //The keys will prove the access permission for Alicia and, perhaps, for 
  //somebody else. The private key of the 'active' pair has to be imported to 
  //the Alicia's wallet:
  //*/
  //WalletImport walletImportActive(walletName, 
  //  createKeyActive.get<string>("privateKey"));
  //if (walletImportActive.isError) {
  //  cerr << walletImportActive.toStringRcv() << endl;
  //}

  ///*
  //Now, Alicia can create her new 'currency' account:
  //*/
  //CreateAccount createAccount("inita", "currency", 
  //  createKeyOwner.get<string>("publicKey"), 
  //  createKeyActive.get<string>("publicKey"));
  //if (createAccount.isError) {
  //  cerr << createAccount.toStringRcv() << endl;
  //  return 0;
  //}

  //cout << createAccount.toStringRcv() << endl;

  ///*
  //Account 'currency' is operational. This is the ID of the transaction that has 
  //launched it:
  //*/
  //cout << "transaction id: " << createAccount.get<string>("transaction_id") << endl;
  //
  ///*
  //Alice can inspect her account. For test purposes, 'currency' account has got 
  //1EOS, for free.
  //*/
  //GetAccount getAccount("currency");
  //cout << "eos balance: " << getAccount.get<string>("eos_balance") << endl;

  /*
  Alicia needs means to transfer her money from 'currency' account to 'inita' 
  account. In EOS, such a transfer can be done with a 'smart contract', 
  a specialized chunk of code registered with the blockchain. 
  
  A contract that can satisfy Alice is written in the file 
  eos/contracts/currency/currency.cpp. This C++ source has to be compiled into 
  WebAssembly code (.wast); this is already done, resulting in files 
  eos/build/contracts/currency/currency.wast and 
  eos/build/contracts/currency/currency.abi.
  */
  SetContract setContract("currency", wastFile, abiFile);
  if (setContract.isError) {
    cerr << setContract.toStringRcv() << endl;
    return 0;
  }

  /*
  The contract is registered with the blockchain. This is the ID of the 
  transaction that has launched it:
  */
  cout << "transaction id: " << setContract.get<string>("transaction_id") << endl;

  /*
  Alice can inspect the contract code. The following command prints it into 
  the file /tmp/currency.wast:
  */
  //GetCode getCode("currency", "/tmp/currency.wast");

  /*
  Let Alice do money transfer:
  */


  return 1;
}
