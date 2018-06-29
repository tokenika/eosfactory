# python3 ./tests/test1.py

import setup
import cleos
import teos
import eosf
import unittest
from termcolor import colored, cprint
import time

setup.set_json(False)        
setup.set_verbose(True)
cleos.dont_keosd()

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        global account_eosio
        account_eosio = cleos.AccountEosio()
        node_reset = teos.node_run()


    def setUp(self):
        pass


    def test_05(self):
        global wallet
        wallet = eosf.Wallet()
        wallet.restore_accounts()


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        teos.node_stop()

if __name__ == "__main__":
    unittest.main()