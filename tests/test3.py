# python3 ./tests/test3.py

import pyteos
import node
import sess
from eosf import *

def run():
    print('test node.reset():')
    node.reset()

    print('test node.info():')
    node.info()

    print('test sess.setup():')
    sess.setup()

    print('test Contract():')
    c = ContractFromTemplate("_e4b2ffc804529ce9c6fae258197648cc2", remove_existing = True)
    
    print('test c.build():')
    c.build()

    print('test c.deploy():')
    c.deploy()

    print('test c.get_code():')
    c.get_code()

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('test c.push_action("hi", sess.carol):')
    c.push_action("hi", '{"user":"carol"}', sess.carol)
    
    print('test c.delete():')
    c.delete()
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run()