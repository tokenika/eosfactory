# python3 ./tests/test.py

import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    ############################
    # Your unit-test goes here #
    ############################
    
    node.stop()
    print("Test OK")


if __name__ == "__main__":
    run()