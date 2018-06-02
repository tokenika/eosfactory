/**
 * @file unittest1.cpp
 * @copyright defined in LICENSE.txt
 * @author Tokenika
 * @date 30 May 2018
*/

/**
 * @defgroup teoslib_usage Usage examples
 */

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

#define BOOST_TEST_MODULE test1 test
#include <boost/test/unit_test.hpp>

using namespace std;
using namespace teoslib;
using namespace teos::control;
using namespace teos::command;
using namespace boost::property_tree;

/**
 * @ingroup teoslib_usage
 * @brief unittest1.cpp: Unittest the *eosio.token* smart contract example.
 \verbatim
BOOST_AUTO_TEST_CASE(test1)
{
  printf(
    R"(
    First test of the TEOS library (C++).
    The library is to assist development of EOSIO smart contracts.
    Please, see the documentation.
    
    )"
    );

  AccountEosio* eosio;
  Wallet* wallet;
  Key* key_owner; 
  Key* key_active;
  Account* alice;
  Account* bob;
  Account* carol;

  BOOST_REQUIRE(setup(
    eosio, wallet, key_owner, key_active, alice, bob, carol));

  string name = "eosio.token";
  Account account_contract(*eosio, name, *key_owner, *key_active);

  Contract contract(account_contract, name);
  
  BOOST_REQUIRE(contract.deploy());
  BOOST_REQUIRE(contract.push_action(
    "create", 
    R"({"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", 
    "can_freeze":0, "can_recall":0, "can_whitelist":0})")
  );
  
  BOOST_REQUIRE(contract.push_action(
    "issue", 
    R"({"to":"alice", "quantity":"100.0000 EOS", 
    "memo":"memo"})", eosio));

  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"alice", "to":"carol", "quantity":"25.0000 EOS", 
    "memo":"memo"})", 
    alice));

  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"carol", "to":"bob", "quantity":"13.0000 EOS", 
    "memo":"memo"})", 
    carol));
    
  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"bob", "to":"alice", "quantity":"2.0000 EOS", 
    "memo":"memo"})", bob));

  BOOST_REQUIRE(
    contract.get_table("accounts", alice).get("rows..balance", "ERROR!") 
      == "77.0000 EOS"
  );
  BOOST_REQUIRE(
    contract.get_table("accounts", bob).get("rows..balance", "ERROR!") 
      == "11.0000 EOS"
  );
  BOOST_REQUIRE(
    contract.get_table("accounts", carol).get("rows..balance", "ERROR!") 
      == "12.0000 EOS"
  );

  teardown(eosio, wallet, key_owner, key_active, alice, bob, carol); 
}

 \endverbatim 
 */
BOOST_AUTO_TEST_CASE(test1)
{
  printf(
    R"(
    First test of the TEOS library (C++).
    The library is to assist development of EOSIO smart contracts.
    Please, see the documentation.
    
    )"
    );

  AccountEosio* eosio;
  Wallet* wallet;
  Key* key_owner; 
  Key* key_active;
  Account* alice;
  Account* bob;
  Account* carol;

  BOOST_REQUIRE(setup(
    eosio, wallet, key_owner, key_active, alice, bob, carol));

  string name = "eosio.token";
  Account account_contract(*eosio, name, *key_owner, *key_active);

  Contract contract(account_contract, name);
  
  BOOST_REQUIRE(contract.deploy());
  BOOST_REQUIRE(contract.push_action(
    "create", 
    R"({"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", 
    "can_freeze":0, "can_recall":0, "can_whitelist":0})")
  );
  
  BOOST_REQUIRE(contract.push_action(
    "issue", 
    R"({"to":"alice", "quantity":"100.0000 EOS", 
    "memo":"memo"})", eosio));

  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"alice", "to":"carol", "quantity":"25.0000 EOS", 
    "memo":"memo"})", 
    alice));

  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"carol", "to":"bob", "quantity":"13.0000 EOS", 
    "memo":"memo"})", 
    carol));
    
  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"bob", "to":"alice", "quantity":"2.0000 EOS", 
    "memo":"memo"})", bob));

  BOOST_REQUIRE(
    contract.get_table("accounts", alice).get("rows..balance", "ERROR!") 
      == "77.0000 EOS"
  );
  BOOST_REQUIRE(
    contract.get_table("accounts", bob).get("rows..balance", "ERROR!") 
      == "11.0000 EOS"
  );
  BOOST_REQUIRE(
    contract.get_table("accounts", carol).get("rows..balance", "ERROR!") 
      == "12.0000 EOS"
  );

  teardown(eosio, wallet, key_owner, key_active, alice, bob, carol); 
}




