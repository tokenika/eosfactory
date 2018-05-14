# python3 ./tests/test3.py

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

    print('test Template():')
    c = Template("hello-test3")

    print('test c.path():')
    c.path()
    
    print('test c.build():')
    c.build()

    print('test c.deploy():')
    c.deploy()

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('assert c.get_console() == "Hello, alice":')
    assert c.get_console() == "Hello, alice"

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"carol"}', sess.carol)
    
    print('assert c.get_console() == "Hello, carol":')
    assert c.get_console() == "Hello, carol"

    print('test c.delete():')
    c.delete()
    
    print('test node.stop():')
    node.stop()    
    print("Test OK")


if __name__ == "__main__":
    run()