# python3 ./tests/test1.py

import setup
import eosf
import node
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

    bob = eosf.account()
    assert(not bob.error)
    wallet.import_key(bob)

    carol = eosf.account()
    assert(not carol.error)
    wallet.import_key(carol)

    account = eosf.account()
    assert(not account.error)
    wallet.import_key(account)

    contract_eosio_bios = eosf.Contract(
        eosio, "eosio.bios").deploy()
    assert(not contract_eosio_bios.error)

    contract = eosf.Contract(account, "eosio.token")
    assert(not contract.error)

    deployment = contract.deploy()
    assert(not deployment.error)

    cprint("""
Action contract.push_action("create")
    """, 'magenta')
    assert(not contract.push_action(
        "create",
        '{"issuer":"'
            + str(eosio)
            + '", "maximum_supply":"1000000000.0000 EOS",\
            "can_freeze":0, "can_recall":0, "can_whitelist":0}').error)

    cprint("""
Action contract.push_action("issue")
    """, 'magenta')
    assert(not contract.push_action(
        "issue",
        '{"to":"' + str(alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}',
            eosio).error)

    cprint("""
Action contract.push_action("transfer", alice)
    """, 'magenta')
    assert(not contract.push_action(
        "transfer",
        '{"from":"' + str(alice)
            + '", "to":"' + str(carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        alice).error)

    cprint("""
Action contract.push_action("transfer", carol)
    """, 'magenta')
    assert(not contract.push_action(
        "transfer",
        '{"from":"' + str(carol)
            + '", "to":"' + str(bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        carol).error)

    cprint("""
Action contract.push_action("transfer" bob)
    """, 'magenta')
    assert(not contract.push_action(
        "transfer", 
        '{"from":"' + str(bob)
            + '", "to":"' + str(alice)
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        bob).error)

    cprint("""
Assign t1 = contract.table("accounts", alice)
    """, 'magenta')
    t1 = contract.table("accounts", alice)

    cprint("""
Assign t2 = contract.table("accounts", bob)
    """, 'magenta')
    t2 = contract.table("accounts", bob)
    
    cprint("""
Assign t3 = contract.table("accounts", carol)
    """, 'magenta')
    t3 = contract.table("accounts", carol)

    cprint("""
Assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
    """, 'magenta')
    assert(t1.json["rows"][0]["balance"] == '77.0000 EOS')

    cprint("""
Assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
    """, 'magenta')
    assert(t2.json["rows"][0]["balance"] == '11.0000 EOS')

    cprint("""
Assert t3.json["rows"][0]["balance"] == '12.0000 EOS'
    """, 'magenta')
    assert(t3.json["rows"][0]["balance"] == '12.0000 EOS')

    node.stop()

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')


if __name__ == "__main__":
    test()