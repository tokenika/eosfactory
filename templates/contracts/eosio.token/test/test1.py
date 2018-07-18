import sys
import setup
import eosf
import node
from termcolor import cprint

eosf.use_keosd(False)
setup.set_verbose(False)
setup.set_json(False)

def test():

    testnet = node.reset()
    assert(not testnet.error)

    wallet = eosf.Wallet()
    assert(not wallet.error)

    account_master = eosf.AccountMaster()
    assert(not account_master.error)
    wallet.import_key(account_master)

    account_alice = eosf.account(account_master)
    assert(not account_alice.error)
    wallet.import_key(account_alice)

    account_bob = eosf.account(account_master)
    assert(not account_bob.error)
    wallet.import_key(account_bob)

    account_carol = eosf.account(account_master)
    assert(not account_carol.error)
    wallet.import_key(account_carol)

    account_deploy = eosf.account(account_master)
    assert(not account_deploy.error)
    wallet.import_key(account_deploy)

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios").deploy()
    assert(not contract_eosio_bios.error)

    contract = eosf.Contract(account_deploy, sys.path[0] + "/../")
    assert(not contract.error)

    deployment = contract.deploy()
    assert(not deployment.error)

    cprint("""
Action contract.push_action("create")
    """, 'magenta')
    assert(not contract.push_action(
        "create",
        '{"issuer":"'
            + str(account_master)
            + '", "maximum_supply":"1000000000.0000 EOS",\
            "can_freeze":0, "can_recall":0, "can_whitelist":0}', output=True).error)

    cprint("""
Action contract.push_action("issue")
    """, 'magenta')
    assert(not contract.push_action(
        "issue",
        '{"to":"' + str(account_alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}',
            account_master, output=True).error)

    cprint("""
Action contract.push_action("transfer", account_alice)
    """, 'magenta')
    assert(not contract.push_action(
        "transfer",
        '{"from":"' + str(account_alice)
            + '", "to":"' + str(account_carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        account_alice, output=True).error)

    cprint("""
Action contract.push_action("transfer", account_carol)
    """, 'magenta')
    assert(not contract.push_action(
        "transfer",
        '{"from":"' + str(account_carol)
            + '", "to":"' + str(account_bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        account_carol, output=True).error)

    cprint("""
Action contract.push_action("transfer" account_bob)
    """, 'magenta')
    assert(not contract.push_action(
        "transfer", 
        '{"from":"' + str(account_bob)
            + '", "to":"' + str(account_alice)
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        account_bob, output=True).error)

    cprint("""
Assign t1 = contract.table("accounts", account_alice)
    """, 'magenta')
    t1 = contract.table("accounts", account_alice)

    cprint("""
Assign t2 = contract.table("accounts", account_bob)
    """, 'magenta')
    t2 = contract.table("accounts", account_bob)
    
    cprint("""
Assign t3 = contract.table("accounts", account_carol)
    """, 'magenta')
    t3 = contract.table("accounts", account_carol)

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
