# python3 ./tests/test1.py

import eosf
import sess
import cleos
import teos
import setup

CONTRACT_NAME = "eosio.token"
setup.set_verbose(0)
cleos.dont_keosd()
#setup.set_nodeos_URL("54.38.137.99:8090")


def run():
    print('test node.reset():')
    assert teos.node_reset()

    print('test sess.init():')
    assert sess.init()

    print('test Contract():')
    account = cleos.AccountLT()
    sess.wallet.import_key(account)
    contract = eosf.Contract(account, CONTRACT_NAME)
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
            + str(sess.account_eosio) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}').error

    print('test contract.push_action("issue"):')
    assert not contract.push_action(
        "issue", 
        '{"to":"' + str(sess.alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            sess.account_eosio).error

    print('test contract.push_action("transfer", sess.alice):')
    assert not contract.push_action(
        "transfer", 
        '{"from":"' 
            + str(sess.alice)
            + '", "to":"' + str(sess.carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        sess.alice).error

    print('test contract.push_action("transfer", sess.carol):')
    assert not contract.push_action(
        "transfer", 
        '{"from":"' 
            + str(sess.carol)
            + '", "to":"' + str(sess.bob)
            + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
        sess.carol).error

    print('test contract.push_action("transfer" sess.bob):')
    assert not contract.push_action(
        "transfer", 
        '{"from":"' 
            + str(sess.bob)
            + '", "to":"' 
            + str(sess.alice)
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