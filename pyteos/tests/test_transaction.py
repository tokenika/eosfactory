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
Use `setup.use_keosd(False)` instruction, then the wallets used for test are not
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
Inspect the account, use `bob.info()`:
    """, 'magenta')

    print(bob.info())       

    account_et = eosf.account()
    wallet.import_key(account_et)
    
    contract_et = eosf.Contract(account_et, "eosio.token")

    cprint("""
Test contract_et.code():
    """, 'magenta')

    print("code hash: ".format(contract_et.code()))

    cprint("""
Test contract_et.deploy():
    """, 'magenta')

    contract = contract_et.deploy()
    contract.get_transaction()

    cprint("""
Test contract_et.code():
    """, 'magenta')

    print("code hash: ".format(contract_et.code()))

    cprint("""
Test contract_et.push_action("create"):
    """, 'magenta')
    
    action = contract_et.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_master) 
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

    eosf.stop()


if __name__ == "__main__":
    test()