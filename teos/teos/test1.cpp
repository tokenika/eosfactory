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

#include "teoslib.hpp"

#define BOOST_TEST_MODULE test1 test
#include <boost/test/unit_test.hpp>

using namespace std;
using namespace teoslib;
using namespace teos::control;
using namespace teos::command;


BOOST_AUTO_TEST_CASE(test1)
{
  DaemonStart daemonStart(true);
  BOOST_REQUIRE(!daemonStart.isError_);

  AccountEosio eosio;

  Wallet wallet;
  BOOST_REQUIRE(!wallet.isError_);

  Contract contract_eosio_bios(eosio, "eosio.bios", &eosio);
  BOOST_REQUIRE(contract_eosio_bios.deploy()); 
  cout << contract_eosio_bios.console_ << endl;
  //cout << contract_eosio_bios.setContract_->responseToString(true) << endl;

  Key owner_key("owner");
  Key active_key("active");
  BOOST_REQUIRE(!owner_key.isError_ && !active_key.isError_);
  cout << owner_key.responseToString(true) << endl;
  cout << active_key.responseToString(true) << endl;

  wallet.import_key(owner_key);
  wallet.import_key(active_key);

  // BOOST_REQUIRE(wallet.import_key(owner_key));
  // BOOST_REQUIRE(wallet.import_key(active_key));

  wallet.keys(); // Prints wallet keys.

  DaemonStop();
}




