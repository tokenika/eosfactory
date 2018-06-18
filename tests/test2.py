
import pyteos as p
import node
import sess
import eosf

CONTRACT_NAME = "tic.tac.toe"
eosf.set_verbose(True)

def run():
    print('test node.reset():')
    assert node.reset()
    
    print('test sess.init():')
    assert sess.init()

    account_ttt = p.CreateAccount(
        "eosio", CONTRACT_NAME,
        sess.key_owner, sess.key_active)

    contract_ttt = p.SetContract(
        account_ttt, CONTRACT_NAME)

    # ./cleos push action tic.tac.toe create
    p.PushAction(account_ttt, '{"challenger":"alice", "host":"bob"}')

    print('test Contract():')
    c = Contract(CONTRACT_NAME)
    assert c.is_created()

    print('test c.deploy():')
    assert c.deploy()

    print('test c.push_action("create", sess.bob):')
    assert c.push_action("create", '{"challenger":"alice", "host":"bob"}', sess.bob)
    c.get_console()

    print('test c.get_table("games", sess.bob):')
    t = c.get_table("games", sess.bob)
    
    assert t.json["rows"][0]["board"][0] == '0'
    assert t.json["rows"][0]["board"][1] == '0'
    assert t.json["rows"][0]["board"][2] == '0'
    assert t.json["rows"][0]["board"][3] == '0'
    assert t.json["rows"][0]["board"][4] == '0'
    assert t.json["rows"][0]["board"][5] == '0'
    assert t.json["rows"][0]["board"][6] == '0'
    assert t.json["rows"][0]["board"][7] == '0'
    assert t.json["rows"][0]["board"][8] == '0'

    print('test c.push_action("move", sess.bob):')
    assert c.push_action("move", '{"challenger":"alice", "host":"bob", "by":"bob", "mvt":{"row":0, "column":0} }', sess.bob)
    c.get_console()


    print('test c.push_action("move", sess.alice):')
    assert c.push_action("move", '{"challenger":"alice", "host":"bob", "by":"alice", "mvt":{"row":1, "column":1} }', sess.alice)
    c.get_console()

    print('test c.get_table("games", sess.bob):')
    t = c.get_table("games", sess.bob)

    assert t.json["rows"][0]["board"][0] == '1'
    assert t.json["rows"][0]["board"][1] == '0'
    assert t.json["rows"][0]["board"][2] == '0'
    assert t.json["rows"][0]["board"][3] == '0'
    assert t.json["rows"][0]["board"][4] == '2'
    assert t.json["rows"][0]["board"][5] == '0'
    assert t.json["rows"][0]["board"][6] == '0'
    assert t.json["rows"][0]["board"][7] == '0'
    assert t.json["rows"][0]["board"][8] == '0'

    print('test c.push_action("restart", sess.bob):')
    assert c.push_action("restart", '{"challenger":"alice", "host":"bob", "by":"bob"}', sess.bob)
    c.get_console()

    print('test c.get_table("games", sess.bob):')
    t = c.get_table("games", sess.bob)
    
    assert t.json["rows"][0]["board"][0] == '0'
    assert t.json["rows"][0]["board"][1] == '0'
    assert t.json["rows"][0]["board"][2] == '0'
    assert t.json["rows"][0]["board"][3] == '0'
    assert t.json["rows"][0]["board"][4] == '0'
    assert t.json["rows"][0]["board"][5] == '0'
    assert t.json["rows"][0]["board"][6] == '0'
    assert t.json["rows"][0]["board"][7] == '0'
    assert t.json["rows"][0]["board"][8] == '0'

    print('test c.push_action("close", sess.bob):')
    assert c.push_action("close", '{"challenger":"alice", "host":"bob"}', sess.bob)
    c.get_console()    

    print('test node.stop():')
    node.stop()

    print("Test OK")


if __name__ == "__main__":
    run()