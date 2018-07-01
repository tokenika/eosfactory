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
cleos.use_keosd(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        global wallet 
        global account_eosio

        account_eosio = cleos.AccountEosio()
        node_reset = teos.node_reset()
        wallet = eosf.Wallet()
        wallet.import_key(account_eosio)


    def setUp(self):
        pass


    def test_05(self):
        global wallet 

        alice = eosf.account()
        self.assertTrue(not alice.error)
        
        owner_key = alice.owner_key
        self.assertTrue(not owner_key.error)
        print("owner keys:")
        print(owner_key)

        # active_key = alice.active_key
        # self.assertTrue(not active_key.error)
        # print("owner keys:")
        # print(active_key)

        # code = alice.code()
        # self.assertTrue(not code.error)

        # import_key = wallet.import_key(alice)
        # print("wallet.import_key[0]:")
        # print(import_key[0])

        # contract = alice.set_contract("eosio.token")
        # self.assertTrue(not contract.error)
        # print(contract)

    # def test_10(self):
    #     global wallet

    #     bob = eosf.account()
    #     import_key = wallet.import_key(bob)
    #     carol = eosf.account()
    #     import_key = wallet.import_key(carol)
        
    #     names = set()
    #     keys = wallet.keys()
    #     for key in keys.json[""]:
    #         accounts = cleos.GetAccounts(key, is_verbose=0)
    #         #print(accounts.json)
    #         for acc in accounts.json["account_names"]:
    #             names.add(acc)

    #     print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
    #     print(names)
    #     print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        teos.node_stop()

if __name__ == "__main__":
    unittest.main()