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
    c = Template("hello")
    
    print('test c.build():')
    c.build()

    print('test c.deploy():')
    c.deploy()

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('test c.push_action("hi", sess.carol):')
    c.push_action("hi", '{"user":"alice"}', sess.carol)

    print('test c.delete():')
    #c.delete()
    
    print('test node.stop():')
    node.stop()    
    print("Test OK")


if __name__ == "__main__":
    run()