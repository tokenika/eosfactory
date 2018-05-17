# python3 ./tests/test2.py

import node
import sess
from eosf import *

def run():
    print('test node.reset():')
    node.reset()

    print('test node.info():')
    node.info()
    
    print('test sess.init():')
    sess.Init()

    print('test c = Contract("tic.tac.toe"):')
    c = Contract("tic.tac.toe")

    print('test c.deploy():')
    c.deploy()

    print('test c.push_action("create", sess.bob):')
    c.push_action("create", '{"challenger":"alice", "host":"bob"}', sess.bob)

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
    c.push_action("move", '{"challenger":"alice", "host":"bob", "by":"bob", "mvt":{"row":0, "column":0} }', sess.bob)

    print('test c.push_action("move", sess.alice):')
    c.push_action("move", '{"challenger":"alice", "host":"bob", "by":"alice", "mvt":{"row":1, "column":1} }', sess.alice)

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
    c.push_action("restart", '{"challenger":"alice", "host":"bob", "by":"bob"}', sess.bob)
    
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
    c.push_action("close", '{"challenger":"alice", "host":"bob"}', sess.bob)

    print('test node.stop():')
    node.stop()

    print("Test OK")


if __name__ == "__main__":
    run()