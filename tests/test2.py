# python3 ./tests/test2.py

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

    account_master = eosf.AccountMaster()
    assert(not account_master.error)
    wallet.import_key(account_master)

    account_alice = eosf.account(account_master)
    assert(not account_alice.error)
    wallet.import_key(account_alice)

    account_carol = eosf.account(account_master)
    assert(not account_carol.error)
    wallet.import_key(account_carol)

    account_deploy = eosf.account(account_master, name="tic.tac.toe")
    assert(not account_deploy.error)
    wallet.import_key(account_deploy)

    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios").deploy()
    assert(not contract_eosio_bios.error)

    contract = eosf.Contract(account_deploy, "tic_tac_toe")
    assert(not contract.error)

    deployment = contract.deploy()
    assert(not deployment.error)

    cprint("""
Action contract.push_action("create")
    """, 'magenta')
    action = contract.push_action(
        "create", 
        '{"challenger":"' 
        + str(account_alice) +'", "host":"' 
        + str(account_carol) + '"}', account_carol)
    print(action)
    assert(not action.error)
    
    t = contract.table("games", account_carol)
    assert(not t.error)

    assert(t.json["rows"][0]["board"][0] == 0)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 0)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)

    cprint("""
Action contract.push_action("move")
    """, 'magenta')
    action = contract.push_action(
        "move", 
        '{"challenger":"' 
        + str(account_alice) + '", "host":"' 
        + str(account_carol) + '", "by":"' 
        + str(account_carol) + '", "mvt":{"row":0, "column":0} }', account_carol)
    print(action)
    assert(not action.error)

    cprint("""
Action contract.push_action("move")
    """, 'magenta')
    action = contract.push_action(
        "move", 
        '{"challenger":"' 
        + str(account_alice) + '", "host":"' 
        + str(account_carol) + '", "by":"' 
        + str(account_alice) + '", "mvt":{"row":1, "column":1} }', account_alice)
    print(action)
    assert(not action.error)

    t = contract.table("games", account_carol)
    assert(not t.error)

    assert(t.json["rows"][0]["board"][0] == 1)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 2)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)

    cprint("""
Action contract.push_action("restart")
    """, 'magenta')
    action = contract.push_action(
            "restart", 
            '{"challenger":"' 
            + str(account_alice) + '", "host":"' 
            + str(account_carol) + '", "by":"' + str(account_carol) + '"}', account_carol)
    print(action)
    assert(not action.error)

    t = contract.table("games", account_carol)
    assert(not t.error)

    assert(t.json["rows"][0]["board"][0] == 0)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 0)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)

    cprint("""
Action contract.push_action("close")
    """, 'magenta')
    action = contract.push_action(
            "close", 
            '{"challenger":"' 
            + str(account_alice) + '", "host":"' + str(account_carol) + '"}', account_carol)
    print(action)
    assert(not action.error)

    node.stop()

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')
    

if __name__ == "__main__":
   test()