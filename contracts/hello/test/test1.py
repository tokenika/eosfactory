# python3 ./tests/unittest3.py

import sys
import setup
import eosf
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

setup.set_verbose(False)
setup.set_json(False)
contract_dir = sys.path[0] + "/../"


def test():
    reset = eosf.reset(is_verbose=False)    
    cprint(
        "Started the local test node: {}".format(not reset.error), 
        'magenta')

    wallet = eosf.Wallet()
    cprint(
        "The wallet is OK: {}".format(not wallet.error), 
        'magenta')

    account_master = eosf.AccountMaster(is_verbose=False)
    ok = wallet.import_key(account_master)
    cprint(
        "The account_master is in the wallet: {}" \
            .format(not account_master.error), 
        'magenta')

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios", is_verbose=False).deploy()   
    cprint(
        "The contract_eosio_bios is deployed: {}" \
            .format(not contract_eosio_bios.error), 
         'magenta') 


    cprint("""account_test = eosf.account()""", 'magenta')
    account_test = eosf.account()

    cprint("""wallet.import_key(account_test)""", 'magenta')
    ok = wallet.import_key(account_test)    

    cprint("""eosf.Contract(account_test, contract_dir)""", 'magenta')
    contract_test = eosf.Contract(account_test, contract_dir, dont_broadcast=True)


    cprint("""contract_test.deploy(is_verbose=0)""", 'magenta')
    deployed = contract_test.deploy(is_verbose=1)
    import json
    print(json.dumps(deployed.json, indent=4))

    cprint("""contract_test.code()""", 'magenta')
    code = contract_test.code()
    print("code hash: {}".format(code.code_hash))

##############################################################################
#
##############################################################################

    cprint("""alice = eosf.account()""", 'magenta')
    alice = eosf.account()
    wallet.import_key(alice)

    carol = eosf.account()
    wallet.import_key(carol) 

    cprint("""print(alice.info())""", 'magenta')
    print(alice.info())

    cprint("""
`contract_test.push_action("hi", '{"user":"' + str(alice) + '"}', alice)`:
    """, 'magenta')

    action_hi = contract_test.push_action(
        "hi", '{"user":"' + str(alice) + '"}', alice, console=True)

    cprint("""
`contract_test.push_action("hi", '{"user":"' + str(carol) + '"}', carol)`:
    """, 'magenta')

    action_hi = contract_test.push_action(
        "hi", 
        '{"user":"' + str(carol) + '"}', carol, console=True)

    cprint("""
eosf.stop():
    """, 'magenta')

    eosf.stop()
        
if __name__ == "__main__":
    test()
