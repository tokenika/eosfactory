#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/property_tree/ptree.hpp>

#include <teoslib/control/build_contract.hpp>
#include <teoslib/command/get_commands.hpp>
#include <teoslib/command/create_commands.hpp>
#include <teoslib/command/set_commands.hpp>
#include <teoslib/command/wallet_commands.hpp>
#include <teoslib/command/push_commands.hpp>
#include <teoslib/teoslib.hpp> 

using namespace std;
using namespace boost::property_tree;


namespace teoslib
{  

  bool setup(
    AccountEosio*& eosio, Wallet*& wallet,
    Key*& key_owner, Key*& key_active,
    Account*& alice, Account*& bob, Account*& carol
  )
  {
    bool ok = true;
    DaemonStart daemonStart(true);
    ok &= !daemonStart.isError_;

    eosio = new AccountEosio();
    wallet = new Wallet();
    ok &= !wallet->isError_; 

    Contract contract_eosio_bios(*eosio, "eosio.bios", eosio);
    //cout << contract_eosio_bios.console_ << endl;
    //cout << contract_eosio_bios.setContract_->responseToString(true) << endl;

    key_owner = new Key("owner");
    ok &= !key_owner->isError_;

    key_active = new Key("active");
    ok &= !key_active->isError_;

    // cout << key_owner->responseToString(true);
    // cout << key_active->responseToString(true);

    ok &= wallet->import_key(*key_owner);
    ok &= wallet->import_key(*key_active);
    // ok &= wallet->keys(); // Prints wallet keys.

    alice = new Account(*eosio, "alice", *key_owner, *key_active);
    ok &= !alice->isError_;
    // cout << alice->responseToString(true);
    bob = new Account(*eosio, "bob", *key_owner, *key_active);
    ok &= !bob->isError_;
    carol = new Account(*eosio, "carol", *key_owner, *key_active);
    ok &= !carol->isError_;

    return ok;  
  }

  void teardown(
    AccountEosio* eosio, Wallet* wallet,
    Key* key_owner, Key* key_active,
    Account* alice, Account* bob, Account* carol
  )
  {
    DaemonStop();
    if(eosio)
    {
      delete eosio;
    }
    if(wallet)
    {
      delete wallet;
    }
    if(key_owner)
    {
      delete key_owner;
    }
    if(key_active)
    {
      delete key_active;
    }
    if(alice)
    {
      delete alice;
    }
    if(bob)
    {
      delete bob;
    }
    if(carol)
    {
      delete carol;
    }
  }
}