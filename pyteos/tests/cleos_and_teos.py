# python3 ./tests/test1.py

import setup
import cleos
import teos

def run():

    teos.node_reset()
    cleos.WalletCreate()

if __name__ == "__main__":
    run()