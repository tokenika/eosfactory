import sys
import node
import sess
from eosf import *

def run(contract_dir):
    print('test node.reset():')
    assert node.reset()

    print('test sess.init():')
    assert sess.init()

    print('test Contract():')
    c = Contract(contract_dir)
    assert c.is_created()

    print('test c.deploy():')
    assert c.deploy()

    print('test c.get_code():')
    assert c.get_code()

    print('test c.push_action("hi", sess.alice):')
    assert c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('test c.push_action("hi", sess.carol):')
    assert c.push_action("hi", '{"user":"carol"}', sess.carol)

    print('test c.push_action("hi", sess.alice):')
    assert not c.push_action("hi", '{"user":"carol"}', sess.alice)
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run(str(sys.argv[1]))