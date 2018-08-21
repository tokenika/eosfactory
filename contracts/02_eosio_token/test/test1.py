# python3 ./tests/unittest1.py

import sys
import setup
import eosf
import time
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

setup.set_verbose(False)
setup.set_json(False)


contract_dir = sys.path[0] + "/../"


def test():
    ok = eosf.reset(is_verbose=False)    
    cprint(
        "Started the local test EOSIO node: {}".format(ok), 
        'magenta')

    wallet = eosf.Wallet()
    cprint(
        "The wallet is OK: {}".format(not wallet.error), 
        'magenta')

    account_master = eosf.AccountMaster(is_verbose=False)
    ok = wallet.import_key(account_master)
    cprint(
        "The account_master is in the wallet: {}" \
            .format(ok), 
        'magenta')

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios", is_verbose=False).deploy()
    cprint(
        "The contract_eosio_bios is deployed: {}" \
            .format(not contract_eosio_bios.error), 
         'magenta')   

    account_test = eosf.account()
    cprint(
        "The name of the contract account is: {}" \
            .format(account_test.name), 
         'magenta')
         
    ok = wallet.import_key(account_test)    
    cprint(
        "The contract account is put into the wallet: {}" \
            .format(ok), 
        'magenta')

    contract_test = eosf.Contract(account_test, contract_dir)
    cprint(
        "The contract is created: {}".format(not contract_test.error), 
        'magenta')

    deployed = contract_test.deploy(is_verbose=0)
    cprint(
        "The contract is deployed: {}".format(not deployed.error), 
        'magenta')
                
    cprint("""
Confirm that the account `account_test` contains the contract code:
    """, 'magenta')

    code = contract_test.code()
    print("code hash: {}".format(code.code_hash))

##############################################################################
#
##############################################################################

    cprint("""
Create accounts `alice`, `bob` and `carol`and put them into the wallet:
    """, 'magenta')
    
    alice = eosf.account()
    wallet.import_key(alice)

    bob = eosf.account()
    wallet.import_key(bob)        

    carol = eosf.account()
    wallet.import_key(carol) 

    cprint("""
contract_test.push_action("create", ...):
    """, 'magenta')
    
    action = contract_test.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_master) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}',
        console=True)
        

    cprint("""
contract_test.push_action("issue"):
    """, 'magenta')

    action = contract_test.push_action(
        "issue", 
        '{"to":"' + str(alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            account_master, console=True)

    cprint("""
contract_test.push_action("transfer", alice):
        """, 'magenta')
        
    action = contract_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(alice)
            + '", "to":"' + str(carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        alice, console=True)

    time.sleep(1)

    cprint("""
contract_test.push_action("transfer", carol):
    """, 'magenta')
        
    action = contract_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(carol)
            + '", "to":"' + str(bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        carol, console=True)

    cprint("""
contract_test.push_action("transfer" bob):
    """, 'magenta')
        
    action = contract_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(bob)
            + '", "to":"' 
            + str(alice)
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        bob, console=True)

    cprint("""
contract_test.table("accounts", alice):
    """, 'magenta')

    t1 = contract_test.table("accounts", alice)
    
    cprint("""
contract_test.table("accounts", bob):
    """, 'magenta')

    t2 = contract_test.table("accounts", bob)
    
    cprint("""
contract_test.table("accounts", carol):
    """, 'magenta')
    
    t3 = contract_test.table("accounts", carol)


    cprint(""" eosf.stop(): """, 'magenta')
    eosf.stop()

if __name__ == "__main__":
    test()
