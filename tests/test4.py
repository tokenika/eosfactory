# python3 ./tests/test4.py

import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    c = Contract("tic.tac.toe")

    c.wast()
    c.deploy()

    print("Test OK")
    node.stop()

if __name__ == "__main__":
    run()
    