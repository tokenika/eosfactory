import sys
import node
import sess
from eosf import *

def run(contract_dir):
    print('test node.reset():')
    node.reset()

    print('test node.info():')
    node.info()

    print('test sess.setup():')
    sess.setup()

    print('test Contract():')
    c = Contract(contract_dir)

    print('test c.deploy():')
    c.deploy()

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('test c.push_action("hi", sess.carol):')
    c.push_action("hi", '{"user":"carol"}', sess.carol)
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run(str(sys.argv[1]))