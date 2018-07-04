# python3 ./tests/test2.py

import json
import time
from termcolor import cprint
import setup
import eosf

cprint("""
Use `setup.use_keosd(False)` instruction, then the wallets are not
managed by the EOSIO keosd and, hence, can be safely manipulated.

If `setup.set_verbose(True)`, print the response messages of the
issued commands.
""", 'magenta')

setup.use_keosd(False)
setup.set_verbose(True)

def test():

    cprint("""
Start a local test EOSIO node, use `eosf.reset()`:
    """, 'magenta')

    reset = eosf.reset()
    
    cprint("""
Create a local wallet, use `wallet = eosf.Wallet()`:
    """, 'magenta')

    wallet = eosf.Wallet()

    cprint("""
Implement the `eosio` master account as a `eosf.AccountMaster` object,
use `account_master = eosf.AccountMaster()` 
and `wallet.import_key(account_master)`:
    """, 'magenta')

    account_master = eosf.AccountMaster()
    wallet.import_key(account_master)

    cprint("""
Deploy the `eosio.bios` contract, 
use `eosf.Contract(account_master, "eosio.bios").deploy()`:
    """, 'magenta')

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios").deploy()


    cprint("""
Create an account to be equipped with a smart contract, namely:
"tic_tac_toe" from the EOSIO repository, 
use `account_test = eosf.account()`:
    """, 'magenta')

    account_test = eosf.account(name="tic.tac.toe")

    cprint("""
Put the account into the wallet, use `wallet.import_key(account_test)`:
    """, 'magenta')
    
    wallet.import_key(account_test)

    cprint("""
Create a smart contract object:
    """, 'magenta')

    contract_test = eosf.Contract(account_test, "tic_tac_toe")

    cprint("""
Deploy the contract:
    """, 'magenta')
    deployed = contract_test.deploy()
                
    cprint("""
See the response of the node, use `print(contract.contract_test)`:
    """, 'magenta')

    print(contract_test.contract)

    cprint("""
See the response of the node, use `print(contract.contract_test)`:
    """, 'magenta')

    cprint("""
Confirm that the account `account_test` contains the contract code:
    """, 'magenta')

    code = account_test.code()
    print("code hash: {}".format(code.code_hash))

    time.sleep(1)

    cprint("""
Create accounts `alice`and `bob`, 
use `alice = eosf.account()` and `wallet.import_key(alice)`:
    """, 'magenta')

    alice = eosf.account()
    wallet.import_key(alice)

    bob = eosf.account()
    wallet.import_key(bob)        

    cprint("""
Inspect the account, use `bob.info()`:
    """, 'magenta')
    
    print(bob.info())

    cprint("""
Push actions to the contract. Begin with the `create` action:
    """, 'magenta')
    action_create = contract_test.push_action(
        "create", 
        '{"challenger":"' 
        + str(alice) +'", "host":"' + str(bob) + '"}', bob)

    cprint("""
See the response of the node to the `create` action, 
use `print(action_create)`:
    """, 'magenta')

    print(action_create)

    cprint("""
See the result of the action:
    """, 'magenta')

    time.sleep(2)

    t = contract_test.table("games", bob)

    print(t.json)

    assert(t.json["rows"][0]["board"][0] == 0)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 0)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)

        
    action_move = contract_test.push_action(
        "move", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' 
        + str(bob) + '", "by":"' 
        + str(bob) + '", "mvt":{"row":0, "column":0} }', bob)

    action_move = contract_test.push_action(
        "move", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' 
        + str(bob) + '", "by":"' 
        + str(alice) + '", "mvt":{"row":1, "column":1} }', alice)


    t = contract_test.table("games", bob)

    assert(t.json["rows"][0]["board"][0] == 1)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 2)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)


    action_restart = contract_test.push_action(
        "restart", 
        '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' + str(bob) + '"}',
        bob)

    t = contract_test.table("games", bob)

    assert(t.json["rows"][0]["board"][0] == 0)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 0)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)


    action_close = contract_test.push_action(
        "close", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' + str(bob) + '"}', bob)

    cprint(
        "OK OK OK OK OK OK OK OK 0K 0K 0K 0K 0K 0K 0K OK OK OK OK OK OK OK",
        'green'
    )

if __name__ == "__main__":
   test()