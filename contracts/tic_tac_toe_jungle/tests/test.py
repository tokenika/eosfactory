import setup
import eosf
from termcolor import cprint

setup.set_verbose(True)
setup.use_keosd(True)
setup.set_nodeos_URL("dev.cryptolions.io:38888")

def test():
    global account_master
    global account_deploy
    global account_alice
    global account_carol

    wallet_name = "default"
    wallet_pass = "PW5KhZKX2jhmtJWKvUuSChuLE59BHAbFWgGhcsctoDw1Jy437APV3"
    
    wallet = eosf.Wallet(wallet_name, wallet_pass)
    cprint("""
Creating wallet: default
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5KhZKX2jhmtJWKvUuSChuLE59BHAbFWgGhcsctoDw1Jy437APV3"
    """, 'magenta')

    wallet.index()
    wallet.keys()

    restored = wallet.restore_accounts(globals())

    if (not "account_deploy" in restored):
        account_deploy = eosf.account(
            account_master,
            stake_net="1000 EOS",
            stake_cpu="1000 EOS",
            buy_ram_kbytes="1200",
            transfer=True)
        if (not account_deploy.error):
            wallet.import_key(account_deploy)

    if (not "account_alice" in restored):
        account_alice = eosf.account(
            account_master,
            stake_net="100 EOS",
            stake_cpu="100 EOS",
            buy_ram_kbytes="80",
            transfer=True)
        if (not account_alice.error):
            wallet.import_key(account_alice)

    if (not "account_carol" in restored):
        account_carol = eosf.account(
            account_master,
            stake_net="1000 EOS",
            stake_cpu="1000 EOS",
            buy_ram_kbytes="1200",
            transfer=True)
        if (not account_carol.error):
            wallet.import_key(account_carol)
    
    contract = eosf.Contract(
        account_deploy, "tic_tac_toe_jungle")
    
    cprint("""
Deploy the contract
    """, 'magenta')
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

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')



if __name__ == "__main__":
    test()
