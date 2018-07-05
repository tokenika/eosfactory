# python3 ./tests/test1.py

import sys
import json
import time
import setup
import eosf
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

cprint("""
Use `setup.use_keosd(False)` instruction, then the wallets are not
managed by the EOSIO keosd and, hence, can be safely manipulated.

If `setup.set_verbose(True)`, print the response messages of the
issued commands.
""", 'magenta')

setup.set_verbose(True)
setup.set_json(False)

account_test_name = "yeyuoae5rtcg"
# tic.tac.tog tic.tac.toe 
contract_dir = sys.path[0] + "/../"

def test():

    cprint("""eosf.reset():""", 'magenta')
    reset = eosf.reset() 

    cprint("""eosf.Wallet():""", 'magenta')
    wallet = eosf.Wallet()

    cprint("""eosf.AccountManager():""", 'magenta')
    account_master = eosf.AccountMaster()
    wallet.import_key(account_master)

    cprint("""
Contract(account_master, "eosio.bios").deploy():""", 
            'magenta')
    contract_eosio_bios = eosf.Contract(
                            account_master, "eosio.bios").deploy()

    cprint("""
Contract(eosf.account(name=account_test_name):""", 
            'magenta')
    account_test = eosf.account(name=account_test_name)
         
    ok = wallet.import_key(account_test)    
    cprint(
            "The contract account is put into the wallet: {}" \
                .format(ok), 
            'magenta')

    cprint("""Contract(account_test, contract_dir)""", 'magenta')
    contract_test = eosf.Contract(account_test, contract_dir)


    cprint("""contract_test.deploy()""", 'magenta')    
    deployed = contract_test.deploy()

                
    cprint("""account_test.code()""", 'magenta')
    code = account_test.code()
    print("code hash: {}".format(code.code_hash))

##############################################################################
#
##############################################################################

    cprint("""
Create accounts `alice`and `bob`, 
use `alice = eosf.account()` and `wallet.import_key(alice)`:
    """, 'magenta')

    alice = eosf.account()
    wallet.import_key(alice)

    bob = eosf.account()
    wallet.import_key(bob)        

    cprint("""
Inspect the account, use `bob.account()`:
    """, 'magenta')
    
    print(bob.info())

    cprint("""
contract_test.push_action("create", ...):
    """, 'magenta')

    action_create = contract_test.push_action(
        "create", 
        '{"challenger":"' 
        + str(alice) +'", "host":"' + str(bob) + '"}', bob, console=True)

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

    cprint("""
contract_test.push_action("move", ..., bob):
    """, 'magenta')    

    action_move = contract_test.push_action(
        "move", 
        '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' 
            + str(bob) + '", "mvt":{"row":0, "column":0} }', bob, 
        console=True)

    cprint("""
contract_test.push_action("move", ..., alice):
    """, 'magenta')    

    action_move = contract_test.push_action(
        "move", 
        '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' 
            + str(alice) + '", "mvt":{"row":1, "column":1} }', alice, 
        console=True)


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
            + str(bob) + '", "by":"' + str(bob) + '"}', bob, 
        console=True)

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
            + str(alice) + '", "host":"' + str(bob) + '"}', bob, 
        console=True)

    eosf.stop()

if __name__ == "__main__":
   test()