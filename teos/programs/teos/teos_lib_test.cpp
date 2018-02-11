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

#ifdef WIN32
extern "C" FILE*  __cdecl __iob_func(void);
#endif // WIN32

int main(int argc, const char *argv[]) {

  using namespace tokenika::teos;

  TeosCommand::host = "localhost";
  TeosCommand::port = "8888";
  string walletName = "default";
  string password = "PW5JbTXTxszm9RU2Kh29MfDuPw7x1FLPHasE9Pz7whJWp71hzPLQ5";
  string initaKeyPriv = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
  string wastFile = "/mnt/hgfs/Workspaces/EOS/eos/build/contracts/currency/currency.wast";
  string abiFile = "/mnt/hgfs/Workspaces/EOS/eos/build/contracts/currency/currency.abi";

  // /*
  // Alice owns account named 'inita' as she possess its private key, which is 
  // 'initaKeyPriv'. She keeps this key in an EOS wallet, in order to prove 
  // (to the blockchain) her rights. 
  
  // She creates a wallet if she does not have any ...
  // */
  // WalletCreate walletCreate(walletName);
  // if (walletCreate.isError()) {
  //  cerr << walletCreate.responseToString() << endl;
  // }
  // cout << "wallet password: " << walletCreate.get<string>("password") << endl;

  // WalletUnlock walletUnlock(password, walletName);
  // if(walletUnlock.isError()){
  //   cerr << walletUnlock.responseToString() << endl;
  // }

  // /*
  // ... and puts the private key into it:
  // */
  // WalletImport walletImportInita(walletName, initaKeyPriv);
  // if (walletImportInita.isError()) {
  //  cerr << walletImportInita.responseToString() << endl;
  // }

  // /*
  // Alice needs another account to keep some budget money. She can create this 
  // account, named 'currency', under the authority of her 'inita' account. Two 
  // pairs of cryptographic keys are needed for the creation. Let us call them 
  // 'owner' and 'active'. 
  // */
  // CreateKey createKeyOwner("owner");
  // CreateKey createKeyActive("active");

  // /*
  // The keys will prove the access permission for Alicia and, perhaps, for 
  // somebody else. The private key of the 'active' pair has to be imported to 
  // the Alicia's wallet:
  // */
  // WalletImport walletImportActive(walletName, 
  //  createKeyActive.get<string>("privateKey"));
  // if (walletImportActive.isError()) {
  //  cerr << walletImportActive.responseToString() << endl;
  // }

  // /*
  // Now, Alicia can create her new 'currency' account:
  // */
  // CreateAccount createAccount("inita", "currency", 
  //  createKeyOwner.get<string>("publicKey"), 
  //  createKeyActive.get<string>("publicKey"));
  // if (createAccount.isError()) {
  //  cerr << createAccount.responseToString() << endl;
  //  return 0;
  // }

  // /*
  // Account 'currency' is operational. This is the ID of the transaction that 
  // has launched it:
  // */
  // cout << "transaction id: " << createAccount.get<string>("transaction_id") 
  //   << endl;
  
  /*
  Alice can inspect her account. For test purposes, 'currency' account has got 
  1EOS, for free.
  */
  GetAccount getAccount("currency");
  cout << "eos balance: " << getAccount.get<string>("eos_balance") << endl;

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
  if (setContract.isError()) {
    cerr << setContract.responseToString() << endl;
    return 0;
  }

  /*
  The contract is registered with the blockchain. This is the ID of the 
  transaction that has launched it:
  */
  cout << "transaction id: " << setContract.get<string>("transaction_id") 
    << endl;

  /*
  Alice can, as she is a rocket scientist, inspect the contract code:
  */
  GetCode getCode("currency");
  cout << "WAST code:\n" << getCode.get<string>("wast")
    << endl;

  /*
  Alice can inspect her account, as well:
  */
  GetTable getTable1("currency", "currency", "account");
  cout << getTable1.responseToString() << endl;

  /*
  Let Alice do a money transfer ...
  */
  PushMessage pushMessage("currency", "transfer", 
    "{\"from\":\"currency\",\"to\":\"inita\",\"quantity\":50}", "currency,inita", "currency@active");
  cout << pushMessage.responseToString() << endl;

  /*
  ... and see the result:
  */
  GetTable getTable2("currency", "currency", "account");
  cout << getTable2.responseToString() << endl;

#ifdef WIN32
  __iob_func(); //A temporary patch for a bug.
#endif // WIN32

  return 1;
}
