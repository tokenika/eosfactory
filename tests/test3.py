# python3 ./tests/test3.py

import setup
import eosf
import node
from termcolor import cprint

setup.use_keosd(False)
setup.set_verbose(True)
#setup.set_command_line_mode()

CONTRACT_NAME = "_e4b2ffc804529ce9c6fae258197648cc2"

def test():
    testnet = node.reset()
    assert(not testnet.error)

    wallet = eosf.Wallet()
    assert(not wallet.error)

    account_master = eosf.AccountMaster()
    assert(not account_master.error)
    wallet.import_key(account_master)

    account_deploy = eosf.account(account_master)
    wallet.import_key(account_deploy)
    assert(not account_deploy.error)

    account_alice = eosf.account(account_master)
    assert(not account_alice.error)
    wallet.import_key(account_alice)

    account_carol = eosf.account(account_master)
    assert(not account_carol.error)
    wallet.import_key(account_carol)

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios").deploy()
    assert(not contract_eosio_bios.error)

    cprint("""
Create a reference to the new contract
    """, 'magenta')
    contract = eosf.ContractBuilderFromTemplate(CONTRACT_NAME,
        remove_existing=True)

    cprint("""
Build the contract abi
    """, 'magenta')
    assert(not contract.build_abi().error)

    cprint("""
Associate the contract with an account
    """, 'magenta')
    contract = eosf.Contract(account_deploy, CONTRACT_NAME)

    cprint("""
Build the contract wast
    """, 'magenta')
    assert(not contract.build_wast().error)

    cprint("""
Deploy the contract
    """, 'magenta')
    assert(not contract.deploy().error)

    cprint("""
Confirm `account_deploy` contains code
    """, 'magenta')
    assert(not account_deploy.code().error)

    cprint("""
Action contract.push_action("hi", '{"user":"' + str(account_alice) + '"}', account_alice)
    """, 'magenta')
    action = contract.push_action(
        "hi", '{"user":"' + str(account_alice) + '"}', account_alice)
    assert(not action.error)

    cprint("""
Action contract.push_action("hi", '{"user":"' + str(account_carol) + '"}', account_carol)
    """, 'magenta')
    action = contract.push_action(
        "hi", '{"user":"' + str(account_carol) + '"}', account_carol)
    assert(not action.error)

    cprint("""
Action contract.push_action("hi", '{"user":"' + str(account_carol) + '"}', account_alice)
WARNING: This action should fail due to authority mismatch!
    """, 'magenta')
    action = contract.push_action(
        "hi", '{"user":"' + str(account_carol) + '"}', account_alice)
    assert(action.error)

    contract.delete()
    node.stop()

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')


if __name__ == "__main__":
    test()