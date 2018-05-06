import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    c = Contract("currency")
    c.get_code()

    c.abi()
    c.wast()

    c.abi()

    #print("Test OK")
    node.stop()

if __name__ == "__main__":
    run()
    