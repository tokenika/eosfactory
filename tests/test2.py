# python3 ./tests/test2.py

import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    c = Contract("tic.tac.toe")
    c.deploy()

    c.push_action("create", '{"challenger":"alice", "host":"bob"}', sess.bob)

    t=c.get_table("games", sess.bob)
    
    assert t.json["rows"][0]["board"][0] == '0'
    assert t.json["rows"][0]["board"][1] == '0'
    assert t.json["rows"][0]["board"][2] == '0'
    assert t.json["rows"][0]["board"][3] == '0'
    assert t.json["rows"][0]["board"][4] == '0'
    assert t.json["rows"][0]["board"][5] == '0'
    assert t.json["rows"][0]["board"][6] == '0'
    assert t.json["rows"][0]["board"][7] == '0'
    assert t.json["rows"][0]["board"][8] == '0'

    c.push_action("move", '{"challenger":"alice", "host":"bob", "by":"bob", "mvt":{"row":0, "column":0} }', sess.bob)
    c.push_action("move", '{"challenger":"alice", "host":"bob", "by":"alice", "mvt":{"row":1, "column":1} }', sess.alice)

    t=c.get_table("games", sess.bob)

    assert t.json["rows"][0]["board"][0] == '1'
    assert t.json["rows"][0]["board"][1] == '0'
    assert t.json["rows"][0]["board"][2] == '0'
    assert t.json["rows"][0]["board"][3] == '0'
    assert t.json["rows"][0]["board"][4] == '2'
    assert t.json["rows"][0]["board"][5] == '0'
    assert t.json["rows"][0]["board"][6] == '0'
    assert t.json["rows"][0]["board"][7] == '0'
    assert t.json["rows"][0]["board"][8] == '0'

    c.push_action("restart", '{"challenger":"alice", "host":"bob", "by":"bob"}', sess.bob)
    
    t=c.get_table("games", sess.bob)
    
    assert t.json["rows"][0]["board"][0] == '0'
    assert t.json["rows"][0]["board"][1] == '0'
    assert t.json["rows"][0]["board"][2] == '0'
    assert t.json["rows"][0]["board"][3] == '0'
    assert t.json["rows"][0]["board"][4] == '0'
    assert t.json["rows"][0]["board"][5] == '0'
    assert t.json["rows"][0]["board"][6] == '0'
    assert t.json["rows"][0]["board"][7] == '0'
    assert t.json["rows"][0]["board"][8] == '0'

    c.push_action("close", '{"challenger":"alice", "host":"bob"}', sess.bob)

    print("Test OK")
    node.stop()

if __name__ == "__main__":
    run()