#!/usr/bin/python3

import setup
import teos
import cleos
import eosf
import unittest

class TestSessionInit(unittest.TestCase):

    setup.set_verbose(False)
    setup.use_keosd(False)    

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        pass
        
    def setUp(self):
        pass


    def test_04(self):
        print("""
Start a local test EOSIO node:
        """)
        reset = eosf.reset()
        self.assertTrue(ok)
        
        print("""
Create a local wallet (not with EOSIO `keosd` application):
        """)
        global wallet
        wallet = eosf.Wallet()
        self.assertTrue(not wallet.error)

        print("""
Implement the `eosio` master account as a `cleos.AccountMaster` object:
        """)
        global account_master
        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)

        print("""
Create accounts `alice`, `bob` and `carol`:
        """)
        global alice
        alice = eosf.account()
        self.assertTrue(not alice.error)
        alice.account
        wallet.import_key(alice)

        global bob
        bob = eosf.account()
        self.assertTrue(not bob.error)
        wallet.import_key(bob)        

        global carol
        carol = eosf.account()
        self.assertTrue(not carol.error)
        wallet.import_key(carol)        


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
