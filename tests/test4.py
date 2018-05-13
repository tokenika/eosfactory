# python3 ./tests/test4.py

import node
import sess
from eosf import *

def run():
    print('test node.reset():')
    node.reset()
    print('test node.info():')
    node.info()
    print('test sess.init():')
    sess.init()

    print('test Contract("eosio.token"):')
    c = Contract("eosio.token")
    print('test c.get_code():')
    c.get_code()
    print('test c.deploy():')
    c.deploy()
    print('test c.get_code():')
    c.get_code()

    print('test c.push_action("create"):')
    c.push_action("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}')
    
    print('test c.show_action("issue"):')
    c.show_action("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', sess.eosio)

    print('test c.show_action("issue"):')
    c.show_action("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', sess.eosio)
    
    print('test node.stop():')
    node.stop()
    print("Test OK")


if __name__ == "__main__":
    run()