# python3 ./tests/test3.py

import setup
import eosf
import node
import json
from termcolor import cprint

setup.use_keosd(False)
setup.set_verbose(True)
#setup.set_debug_mode()

def test():
    testnet = node.reset()
    assert(not testnet.error)

    wallet = eosf.Wallet()
    assert(not wallet.error)

    eosio = eosf.AccountMaster()
    assert(not eosio.error)
    wallet.import_key(eosio)

    alice = eosf.account()
    assert(not alice.error)
    wallet.import_key(alice)

    carol = eosf.account()
    assert(not carol.error)
    wallet.import_key(carol)

    contract_eosio_bios = eosf.Contract(
        eosio, "eosio.bios").deploy()
    assert(not contract_eosio_bios.error)

    cprint("""
Create an account associated with the contract
    """, 'magenta')
    account = eosf.account()
    assert(not account.error)

    cprint("""
Add the account to the wallet
    """, 'magenta')
    wallet.import_key(account)

    cprint("""
Create a reference to the new contract
    """, 'magenta')
    contract = eosf.ContractFromTemplate(account,
        "_e4b2ffc804529ce9c6fae258197648cc2",
        remove_existing=True)

    cprint("""
Build the contract abi
    """, 'magenta')
    assert(not contract.build_abi().error)
    
    cprint("""
Build the contract wast
    """, 'magenta')
    assert(not contract.build_wast().error)

    cprint("""
Deploy the contract
    """, 'magenta')
    assert(not contract.deploy().error)

    cprint("""
Confirm the account contains code
    """, 'magenta')
    assert(not account.code().error)

    cprint("""
Action contract.push_action("hi", '{"user":"' + str(alice) + '"}', alice)
    """, 'magenta')
    action = contract.push_action(
        "hi", '{"user":"' + str(alice) + '"}', alice)
    assert(not action.error)

    cprint("""
Action contract.push_action("hi", '{"user":"' + str(carol) + '"}', carol)
    """, 'magenta')
    action = contract.push_action(
        "hi", '{"user":"' + str(carol) + '"}', carol)
    assert(not action.error)

    cprint("""
Action contract.push_action("hi", '{"user":"' + str(carol) + '"}', alice)
WARNING: This action should fail due to authority mismatch!
    """, 'magenta')
    action = contract.push_action(
        "hi", '{"user":"' + str(carol) + '"}', alice)
    assert(action.error)

    node.stop()

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')


if __name__ == "__main__":
    test()