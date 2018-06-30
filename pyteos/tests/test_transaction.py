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
#setup.set_debug_mode()


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
    
    contract_et = eosf.Contract(account_et, "eosio.token")

    cprint("""
test contract_et.code():
    """, 'magenta')

    print("code hash: ".format(contract_et.code()))

    cprint("""
test contract_et.deploy():
    """, 'magenta')

    contract = contract_et.deploy()
    contract.get_transaction()

    cprint("""
test contract_et.get_code():
    """, 'magenta')

    print("code hash: ".format(contract_et.code()))

    cprint("""
test contract_et.push_action("create"):
    """, 'magenta')
    
    action = contract_et.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_eosio) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    time.sleep(1)

    cprint("""
See a resume of the transaction:
    """, 'magenta')

    action.get_transaction()


    cprint("""
Stop the EOSIO node, use `teos.node.stop()`:
    """, 'magenta')

    teos.node_stop()


if __name__ == "__main__":
    test()