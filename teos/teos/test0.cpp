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

using namespace std;
using namespace teoslib;
using namespace teos::control;
using namespace teos::command;

int main(int argc, const char *argv[]) {

  using namespace std;
  using namespace teoslib;
  using namespace teos::control;
  using namespace teos::command;

  DaemonStart daemonStart(true);
  AccountEosio eosio;
  Wallet wallet;
  Contract contract_eosio_bios(eosio, "eosio.bios", &eosio);
  cout << contract_eosio_bios.console_ << endl;
  //cout << contract_eosio_bios.setContract_->responseToString(true) << endl;

  Key owner_key("owner");
  Key active_key("active");
  cout << owner_key.responseToString(true) << endl;
  cout << active_key.responseToString(true) << endl;

  wallet.import_key(owner_key);
  wallet.import_key(active_key);

  // vector<string> keys = wallet.keys();
  // cout << keys.size() << endl;
  // for(const string& key: keys)
  // {
  //   cout << key << endl;
  // }

  DaemonStop();  

  return 1;
}