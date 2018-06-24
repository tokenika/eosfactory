#!/usr/bin/python3

import setup
import teos
import cleos
import eosf
import unittest

class TestSessionInit(unittest.TestCase):

    setup.set_verbose(False)
    cleos.dont_keosd()    

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
        ok = teos.node_reset()
        self.assertTrue(ok)
        
        print("""
Create a local wallet (not with EOSIO `keosd` application:
        """)
        global wallet
        wallet = eosf.Wallet()
        self.assertTrue(not wallet.error)

        print("""
Implement the `eosio` master account as a `cleos.AccountEosio` object:
        """)
        global account_eosio
        account_eosio = cleos.AccountEosio()
        wallet.import_key(account_eosio)

        print("""
Create accounts `alice`, `bob` and `carol`:
        """)
        global alice
        alice = eosf.Account()
        self.assertTrue(not alice.error)
        alice.account
        wallet.import_key(alice)

        global bob
        bob = eosf.Account()
        self.assertTrue(not bob.error)
        wallet.import_key(bob)        

        global carol
        carol = eosf.Account()
        self.assertTrue(not carol.error)
        wallet.import_key(carol)        


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
