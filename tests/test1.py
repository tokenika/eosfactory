# python3 ./tests/unittest1.py

import json
import time
from termcolor import colored, cprint #sudo python3 -m pip install termcolor
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
#setup.set_debug_mode()


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
Create accounts `alice`, `bob` and `carol`:
    """, 'magenta')
    
    alice = eosf.account()
    wallet.import_key(alice)

    bob = eosf.account()
    wallet.import_key(bob)

    carol = eosf.account()
    wallet.import_key(carol) 

    cprint("""
Inspect the account, use `bob.account()`:
    """, 'magenta')

    print(bob.info())

    account_test = eosf.account()
    wallet.import_key(account_test)
    
    contract_test = eosf.Contract(account_test, "eosio.token")

    cprint("""
test contract_test.code():
    """, 'magenta')

    print("code hash: ".format(contract_test.code()))

    cprint("""
test contract_test.deploy():
    """, 'magenta')

    deployed = contract_test.deploy()

    cprint("""
test contract_test.code():
    """, 'magenta')

    print("code hash: ".format(contract_test.code()))

    time.sleep(1)

    cprint("""
test contract_test.push_action("create"):
    """, 'magenta')
    
    action = contract_test.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_master) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    cprint("""
test contract_test.push_action("issue"):
    """, 'magenta')

    action = contract_test.push_action(
        "issue", 
        '{"to":"' + str(alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            account_master)

    cprint("""
test contract_test.push_action("transfer", alice):
        """, 'magenta')
        
    action = contract_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(alice)
            + '", "to":"' + str(carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        alice)

    time.sleep(1)

    cprint("""
test contract_test.push_action("transfer", carol):
    """, 'magenta')
        
    action = contract_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(carol)
            + '", "to":"' + str(bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        carol)

    cprint("""
test contract_test.push_action("transfer" bob):
    """, 'magenta')
        
    action = contract_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(bob)
            + '", "to":"' 
            + str(alice)
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        bob)

    cprint("""
Get database table, use `contract_test.table("accounts", alice)`:
    """, 'magenta')

    t1 = contract_test.table("accounts", alice)
    
    cprint("""
Get database table, use `contract_test.table("accounts", bob)`:
    """, 'magenta')

    t2 = contract_test.table("accounts", bob)
    
    cprint("""
Get database table, use `contract_test.table("accounts", carol)`:
    """, 'magenta')
    
    t3 = contract_test.table("accounts", carol)

    cprint("""
assert(t1.json["rows"][0]["balance"] == "77.0000 EOS":
    """, 'magenta')

    time.sleep(1)

    assert(t1.json["rows"][0]["balance"] == '77.0000 EOS')
    
    cprint("""
assert(t2.json["rows"][0]["balance"] == "11.0000 EOS":
    """, 'magenta')

    assert(t2.json["rows"][0]["balance"] == '11.0000 EOS')
    
    cprint("""
assert(t3.json["rows"][0]["balance"] == "12.0000 EOS":
    """, 'magenta')

    assert(t3.json["rows"][0]["balance"] == '12.0000 EOS')

    cprint("""
Stop the EOSIO node, use `eosf.stop()`:
    """, 'magenta')

    eosf.stop()

    cprint(
        "OK OK OK OK OK OK OK OK 0K 0K 0K 0K 0K 0K 0K OK OK OK OK OK OK OK",
        'green'
    )

if __name__ == "__main__":
    test()