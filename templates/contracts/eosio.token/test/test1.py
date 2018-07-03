# python3 ./tests/unittest1.py

import setup
import teos
import cleos
import sess
import eosf
import json
import time
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

CONTRACT_NAME = "@CONTRACT_NAME@"

cprint("""
Use `setup.use_keosd(False)` instruction, then the wallets used for test are not
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
Implement the `eosio` master account as a `cleos.AccountMaster` object,
use `account_master = eosf.AccountMaster()` 
and `wallet.import_key(account_master)`:
    """, 'magenta')

    account_master = eosf.AccountMaster()
    wallet.import_key(account_master)

    cprint("""
Deploy the `eosio.bios` contract, 
use `cleos.SetContract(account_master, "eosio.bios")`:
        """, 'magenta')

    contract_eosio_bios = eosf.Contract(account_master, "eosio.bios").deploy()

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

    print(bob.account())       

    account_et = eosf.account()
    wallet.import_key(account_et)
    
    contract_et = eosf.Contract(account_et, CONTRACT_NAME)

    cprint("""
test contract_et.code():
    """, 'magenta')

    print("code hash: ".format(contract_et.code()))

    cprint("""
test contract_et.deploy():
    """, 'magenta')

    deployed = contract_et.deploy()

    cprint("""
test contract_et.code():
    """, 'magenta')

    print("code hash: ".format(contract_et.code()))

    cprint("""
test contract_et.push_action("create"):
    """, 'magenta')
    
    action = contract_et.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_master) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    cprint("""
test contract_et.push_action("issue"):
    """, 'magenta')

    action = contract_et.push_action(
        "issue", 
        '{"to":"' + str(alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            account_master)

    cprint("""
test contract_et.push_action("transfer", alice):
        """, 'magenta')
        
    action = contract_et.push_action(
        "transfer", 
        '{"from":"' 
            + str(alice)
            + '", "to":"' + str(carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        alice)

    time.sleep(1)

    cprint("""
test contract_et.push_action("transfer", carol):
    """, 'magenta')
        
    action = contract_et.push_action(
        "transfer", 
        '{"from":"' 
            + str(carol)
            + '", "to":"' + str(bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        carol)

    cprint("""
test contract_et.push_action("transfer" bob):
    """, 'magenta')
        
    action = contract_et.push_action(
        "transfer", 
        '{"from":"' 
            + str(bob)
            + '", "to":"' 
            + str(alice)
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        bob)

    cprint("""
Get database table, use `contract_et.get_table("accounts", alice)`:
    """, 'magenta')

    t1 = contract_et.get_table("accounts", alice)
    
    cprint("""
Get database table, use `contract_et.get_table("accounts", bob)`:
    """, 'magenta')

    t2 = contract_et.get_table("accounts", bob)
    
    cprint("""
Get database table, use `contract_et.get_table("accounts", carol)`:
    """, 'magenta')
    
    t3 = contract_et.get_table("accounts", carol)

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
Stop the EOSIO node, use `teos.node.stop()`:
    """, 'magenta')

    eosf.stop()


if __name__ == "__main__":
    test()