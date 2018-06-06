import node
import sess
from eosf import *

CONTRACT_NAME = "@CONTRACT_NAME@/build"
set_verbose(True)

def run():
    print('test node.reset():')
    assert node.reset()

    print('test sess.init():')
    assert sess.init()

    print('test Contract():')
    c = Contract(CONTRACT_NAME)
    assert c.is_created()

    print('test c.get_code():')
    assert c.get_code()

    print('test c.deploy():')
    assert c.deploy()

    print('test c.get_code():')
    assert c.get_code()

    print('test c.push_action("create"):')
    assert c.push_action(
        "create", 
        '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    print('test c.push_action("issue"):')
    assert c.push_action(
        "issue", 
        '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', \
            sess.eosio)

    print('test c.push_action("transfer", sess.alice):')
    assert c.push_action(
        "transfer", 
        '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
            "memo":"memo"}', sess.alice)

    print('test c.push_action("transfer", sess.carol):')
    assert c.push_action(
        "transfer", 
        '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", \
            "memo":"memo"}', sess.carol)

    print('test c.push_action("transfer" sess.bob):')
    assert c.push_action(
        "transfer", 
        '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", \
            "memo":"memo"}', sess.bob)

    print('test c.get_table("accounts", sess.alice):')
    t1 = c.get_table("accounts", sess.alice)
    
    print('test c.get_table("accounts", sess.bob):')
    t2 = c.get_table("accounts", sess.bob)
    
    print('test c.get_table("accounts", sess.carol):')
    t3 = c.get_table("accounts", sess.carol)

    print('assert t1.json["rows"][0]["balance"] == "77.0000 EOS":')
    assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
    
    print('assert t2.json["rows"][0]["balance"] == "11.0000 EOS":')
    assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
    
    print('assert t3.json["rows"][0]["balance"] == "12.0000 EOS":')
    assert t3.json["rows"][0]["balance"] == '12.0000 EOS'

    print('test node.stop():')
    node.stop()

    print("Test OK")


if __name__ == "__main__":
    run()