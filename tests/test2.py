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

    eosio = eosf.AccountMaster()
    assert(not eosio.error)
    wallet.import_key(eosio)

    alice = eosf.account()
    assert(not alice.error)
    wallet.import_key(alice)

    carol = eosf.account()
    assert(not carol.error)
    wallet.import_key(carol)

    account = eosf.account(name="tic.tac.toe")
    assert(not account.error)
    wallet.import_key(account)

    contract_eosio_bios = eosf.Contract(
        eosio, "eosio.bios").deploy()
    assert(not contract_eosio_bios.error)

    contract = eosf.Contract(account, "tic_tac_toe")
    assert(not contract.error)

    deployment = contract.deploy()
    assert(not deployment.error)

    cprint("""
Action contract.push_action("create")
    """, 'magenta')
    action = contract.push_action(
        "create", 
        '{"challenger":"' 
        + str(alice) +'", "host":"' 
        + str(carol) + '"}', carol)
    print(action)
    assert(not action.error)
    
    t = contract.table("games", carol)
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
        + str(alice) + '", "host":"' 
        + str(carol) + '", "by":"' 
        + str(carol) + '", "mvt":{"row":0, "column":0} }', carol)
    print(action)
    assert(not action.error)

    cprint("""
Action contract.push_action("move")
    """, 'magenta')
    action = contract.push_action(
        "move", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' 
        + str(carol) + '", "by":"' 
        + str(alice) + '", "mvt":{"row":1, "column":1} }', alice)
    print(action)
    assert(not action.error)

    t = contract.table("games", carol)
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
            + str(alice) + '", "host":"' 
            + str(carol) + '", "by":"' + str(carol) + '"}', carol)
    print(action)
    assert(not action.error)

    t = contract.table("games", carol)
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
            + str(alice) + '", "host":"' + str(carol) + '"}', carol)
    print(action)
    assert(not action.error)

    node.stop()

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')
    

if __name__ == "__main__":
   test()