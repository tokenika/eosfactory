# python3 ./tests/test.py

import node
import sess
from eosf import *

def run():
    print("test node.reset():")
    node.reset()
    print("test sess.init():")
    sess.init()

    ############################
    # Your unit-test goes here #

    c = Template("hello")

    ############################
    
    print("test node.stop():")
    node.stop()    
    print("Test OK")


if __name__ == "__main__":
    run()