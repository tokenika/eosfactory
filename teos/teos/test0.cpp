#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>


#include <teoslib/control/daemon_controls.hpp>
#include <teoslib/command/get_commands.hpp>
#include <teoslib/command/create_commands.hpp>
#include <teoslib/command/set_commands.hpp>
#include <teoslib/command/wallet_commands.hpp>
#include <teoslib/command/push_commands.hpp>

#include "teostestlib.hpp"


using namespace std;
using namespace teoslib;

int main(int argc, const char *argv[]) {

  using namespace std;
  using namespace teoslib;

  AccountEosio* eosio;
  Wallet* wallet;
  Key* key_owner; 
  Key* key_active;
  Account* alice;
  Account* bob;
  Account* carol;
  
  setup(eosio, wallet, key_owner, key_active, alice, bob, carol);
  Account account_contract(*eosio, "contract", *key_owner, *key_active);
  cout << "code: " << account_contract.code() << endl;

  Contract contract(account_contract, "eosio.token");
  contract.deploy();
  cout << "transaction ID: " 
    << contract.setContract_->respJson_.get<string>("transaction_id") << endl;
  cout << "code: " << account_contract.code() << endl;

  contract.push_action(
    "create", 
    R"({"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0})");
  cout << "create action transaction ID: " 
    << contract.action_->respJson_.get<string>("transaction_id") << endl;
  cout << contract.console_ << endl;

  contract.push_action(
    "issue", 
    R"({"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"})", eosio);
  cout << "issue action transaction ID: " 
    << contract.action_->respJson_.get<string>("transaction_id") << endl;    
  cout << contract.console_ << endl;

  contract.push_action(
    "transfer", 
    R"({"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"})", 
    alice);
  cout << "transfer action transaction ID: " 
    << contract.action_->respJson_.get<string>("transaction_id") << endl;  
  cout << contract.console_ << endl;

  contract.push_action(
    "transfer", 
    R"({"from":"carol", "to":"bob", "quantity":"13.0000 EOS", "memo":"memo"})", 
    carol);
  cout << "transfer action transaction ID: " 
    << contract.action_->respJson_.get<string>("transaction_id") << endl;
  cout << contract.console_ << endl;
    
  contract.push_action(
    "transfer", 
    R"({"from":"bob", "to":"alice", "quantity":"2.0000 EOS", "memo":"memo"})", bob);
  cout << "transfer action transaction ID: " 
    << contract.action_->respJson_.get<string>("transaction_id") << endl;
  cout << contract.console_ << endl;
  
  teardown(eosio, wallet, key_owner, key_active, alice, bob, carol); 

  return 1;
}