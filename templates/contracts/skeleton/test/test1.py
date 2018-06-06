import node
import sess
from eosf import *

CONTRACT_NAME = "@CONTRACT_NAME@/build"
set_verbose(False)

def run():
    print('test node.reset():')
    assert node.reset()

    print('test sess.init():')
    assert sess.init()

    print('test Contract():')
    c = Contract(CONTRACT_NAME)
    assert c.is_created()

    print('test c.deploy():')
    assert c.deploy()

    print('test c.get_code():')
    assert c.get_code()

    print('test c.push_action("hi", sess.alice):')
    assert c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('test c.push_action("hi", sess.carol):')
    assert c.push_action("hi", '{"user":"carol"}', sess.carol)

    set_suppress_error_msg(True)
    print('test c.push_action("hi", sess.alice):')
    assert not c.push_action("hi", '{"user":"carol"}', sess.alice)
    set_suppress_error_msg(False)
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run()