# python3 ./tests/unittest1.py

import setup
import teos
import cleos
import sess
import eosf
import json
import time
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

cprint("""
Use `cleos.dont_keosd()` instruction, then the wallets used for test are not
managed by the EOSIO keosd and, hence, can be safely manipulated.

If `setup.set_verbose(True)`, print the response messages of the
issued commands.
""", 'magenta')

cleos.dont_keosd()
setup.set_verbose(True)


def test():

    cprint("""
Start a local test EOSIO node, use `teos.node_reset()`:
    """, 'magenta')

    ok = teos.node_reset()
        
    cprint("""
Create a local wallet, use `wallet = eosf.Wallet()`:
    """, 'magenta')

    wallet = eosf.Wallet()

    cprint("""
Implement the `eosio` master account as a `cleos.AccountEosio` object,
use `account_eosio = cleos.AccountEosio()` 
and `wallet.import_key(account_eosio)`:
    """, 'magenta')

    account_eosio = cleos.AccountEosio()
    wallet.import_key(account_eosio)

    cprint("""
Deploy the `eosio.bios` contract, 
use `cleos.SetContract(account_eosio, "eosio.bios")`:
        """, 'magenta')

    contract_eosio_bios = cleos.SetContract(account_eosio, "eosio.bios")

    cprint("""
Create accounts `alice`, `bob` and `carol`:
    """, 'magenta')
    
    alice = eosf.Account()
    wallet.import_key(alice)

    bob = eosf.Account()
    wallet.import_key(bob)        

    carol = eosf.Account()
    wallet.import_key(carol) 

    cprint("""
Inspect the account, use `bob.account()`:
    """, 'magenta')

    print(bob.account())       

    account_at = eosf.Account()
    wallet.import_key(account_at)
    
    contract_at = eosf.Contract(account_at, "eosio.token")

    cprint("""
test contract_at.code():
    """, 'magenta')

    print("code hash: ".format(contract_at.code()))

    cprint("""
test contract_at.deploy():
    """, 'magenta')

    ok = contract_at.deploy()

    cprint("""
test contract_at.get_code():
    """, 'magenta')

    print("code hash: ".format(contract_at.code()))

    cprint("""
test contract_at.push_action("create"):
    """, 'magenta')
    
    action = contract_at.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_eosio) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    cprint("""
test contract_at.push_action("issue"):
    """, 'magenta')

    action = contract_at.push_action(
        "issue", 
        '{"to":"' + str(alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            account_eosio)

    cprint("""
test contract_at.push_action("transfer", alice):
        """, 'magenta')
        
    action = contract_at.push_action(
        "transfer", 
        '{"from":"' 
            + str(alice)
            + '", "to":"' + str(carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        alice)

    time.sleep(1)

    cprint("""
test contract_at.push_action("transfer", carol):
    """, 'magenta')
        
    action = contract_at.push_action(
        "transfer", 
        '{"from":"' 
            + str(carol)
            + '", "to":"' + str(bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        carol)

    cprint("""
test contract_at.push_action("transfer" bob):
    """, 'magenta')
        
    action = contract_at.push_action(
        "transfer", 
        '{"from":"' 
            + str(bob)
            + '", "to":"' 
            + str(alice)
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        bob)

    cprint("""
Get database table, use `contract_at.get_table("accounts", alice)`:
    """, 'magenta')

    t1 = contract_at.get_table("accounts", alice)
    
    cprint("""
Get database table, use `contract_at.get_table("accounts", bob)`:
    """, 'magenta')

    t2 = contract_at.get_table("accounts", bob)
    
    cprint("""
Get database table, use `contract_at.get_table("accounts", carol)`:
    """, 'magenta')
    
    t3 = contract_at.get_table("accounts", carol)

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

    teos.node_stop()


if __name__ == "__main__":
    test()