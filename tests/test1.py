# python3 ./tests/test1.py

import setup
import teos
import cleos
import sess
import entities

CONTRACT_NAME = "eosio.token"
setup.set_verbose(0)
cleos.dont_keosd()


def run():
    print('test node.reset():')
    assert teos.node_reset()

    print('test sess.init():')
    assert sess.init()

    print('test Contract():')
    contract = entities.Contract(
        cleos.AccountLight(sess.key_owner, sess.key_active), CONTRACT_NAME)
    assert not contract.error

    print('test contract.code():')
    assert not contract.code().error

    print('test contract.deploy():')
    assert contract.deploy()

    print('test contract.get_code():')
    assert not contract.code().error

    print('test contract.push_action("create"):')
    assert not contract.push_action(
        "create", 
        '{"issuer":"' 
            + sess.account_eosio.name 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}').error

    print('test contract.push_action("issue"):')
    assert not contract.push_action(
        "issue", 
        '{"to":"' + sess.alice.name 
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            sess.account_eosio).error

    print('test contract.push_action("transfer", sess.alice):')
    assert not contract.push_action(
        "transfer", 
        '{"from":"' 
            + sess.alice.name 
            + '", "to":"' + sess.carol.name 
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        sess.alice).error

    print('test contract.push_action("transfer", sess.carol):')
    assert not contract.push_action(
        "transfer", 
        '{"from":"' 
            + sess.carol.name 
            + '", "to":"' + sess.bob.name 
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        sess.carol).error

    print('test contract.push_action("transfer" sess.bob):')
    assert not contract.push_action(
        "transfer", 
        '{"from":"' 
            + sess.bob.name 
            + '", "to":"' 
            + sess.alice.name 
            + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
        sess.bob).error

    print('test contract.get_table("accounts", sess.alice):')
    t1 = contract.get_table("accounts", sess.alice)
    
    print('test contract.get_table("accounts", sess.bob):')
    t2 = contract.get_table("accounts", sess.bob)
    
    print('test contract.get_table("accounts", sess.carol):')
    t3 = contract.get_table("accounts", sess.carol)

    print('assert t1.json["rows"][0]["balance"] == "77.0000 EOS":')
    assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
    
    print('assert t2.json["rows"][0]["balance"] == "11.0000 EOS":')
    assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
    
    print('assert t3.json["rows"][0]["balance"] == "12.0000 EOS":')
    assert t3.json["rows"][0]["balance"] == '12.0000 EOS'

    print('test node.stop():')
    teos.node_stop()

    print("Test OK")


if __name__ == "__main__":
    run()