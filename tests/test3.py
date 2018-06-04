# python3 ./tests/test3.py

import node
import sess
from eosf import *

set_verbose(False)

def run():
    print('test node.reset():')
    assert node.reset()

    print('test sess.init():')
    assert sess.init()

    print('test ContractFromTemplate():')
    c = ContractFromTemplate("_e4b2ffc804529ce9c6fae258197648cc2", remove_existing = True)
    assert c.is_created()
    
    print('test c.build():')
    assert c.build()

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
    
    print('test c.delete():')
    c.delete()
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run()