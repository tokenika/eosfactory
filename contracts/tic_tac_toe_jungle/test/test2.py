import setup
import eosf
from termcolor import cprint

wallet_name = "default"
wallet_pass = "PW5KftuwFePUSaqrq2d8ZcEtJZYQCsWPE5gyo6DMBEcSUeb646coy"
deployment = False

setup.set_verbose(True)
setup.use_keosd(True)
setup.set_nodeos_URL("88.99.97.30:38888")

def test():
    global account_master
    global account_alice2
    global account_carol2

    wallet = eosf.Wallet(wallet_name, wallet_pass)
    restored = wallet.restore_accounts(globals())

    assert("account_master" in restored)

    if (not "account_alice2" in restored):
        account_alice2 = eosf.account(
            account_master,
            stake_net="100 EOS",
            stake_cpu="100 EOS",
            buy_ram_kbytes="80",
            transfer=True)
        assert(not account_alice2.error)
        wallet.import_key(account_alice2)

    if (not "account_carol2" in restored):
        account_carol2 = eosf.account(
            account_master,
            stake_net="1000 EOS",
            stake_cpu="1000 EOS",
            buy_ram_kbytes="1200",
            transfer=True)
        assert(not account_carol2.error)
        wallet.import_key(account_carol2)

    contract = eosf.Contract(
        account_master, "tic_tac_toe_jungle")

    if deployment:
        assert(not contract.deploy().error)

    cprint("""
Action contract.push_action("create")
    """, 'magenta')
    action = contract.push_action(
        "create", 
        '{"challenger":"' 
        + str(account_alice2) +'", "host":"' 
        + str(account_carol2) + '"}', account_carol2)
    print(action)
    assert(not action.error)
    
    t = contract.table("games", account_carol2)
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
        + str(account_alice2) + '", "host":"' 
        + str(account_carol2) + '", "by":"' 
        + str(account_carol2) + '", "mvt":{"row":0, "column":0} }', account_carol2)
    print(action)
    assert(not action.error)

    cprint("""
Action contract.push_action("move")
    """, 'magenta')
    action = contract.push_action(
        "move", 
        '{"challenger":"' 
        + str(account_alice2) + '", "host":"' 
        + str(account_carol2) + '", "by":"' 
        + str(account_alice2) + '", "mvt":{"row":1, "column":1} }', account_alice2)
    print(action)
    assert(not action.error)

    t = contract.table("games", account_carol2)
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
            + str(account_alice2) + '", "host":"' 
            + str(account_carol2) + '", "by":"' + str(account_carol2) + '"}', account_carol2)
    print(action)
    assert(not action.error)

    t = contract.table("games", account_carol2)
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
            + str(account_alice2) + '", "host":"' + str(account_carol2) + '"}', account_carol2)
    print(action)
    assert(not action.error)

    cprint("OK OK OK OK OK OK OK OK 0K 0K 0K 0K", 'green')



if __name__ == "__main__":
    test()
