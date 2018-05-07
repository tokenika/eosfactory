# python3 ./tests/test3.py

import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    
    
    print("Test OK")
    node.stop()

if __name__ == "__main__":
    run()
    