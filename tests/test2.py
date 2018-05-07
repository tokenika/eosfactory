# python3 ./tests/test2.py

import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    c = Template("test2")
    c.build()
    c.deploy()

    c.show_action("hi", '{"user":"carol"}', sess.alice)
    
    print("Test OK")
    node.stop()

if __name__ == "__main__":
    run()
    