# python3 ./tests/unittest1.py

import setup
import teos
import cleos
import sess
import eosf
import unittest
import json
import time

setup.set_verbose(False)
cleos.dont_keosd()

class Test1(unittest.TestCase):

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


    def test_05(self):
        global wallet
        global alice
        global bob
        global carol
        global account_eosio

        account = eosf.Account()
        wallet.import_key(account)
        
        print(alice)
        print(bob)
        print(carol)
        print(account)

        self.contract = eosf.Contract(account, "eosio.token")
        self.assertTrue(not self.contract.error)

        print("""
test contract.code():
        """)
        self.assertTrue(not self.contract.code().error)

        print("""
test contract.deploy():
        """)
        self.assertTrue(self.contract.deploy())

        print("""
test contract.get_code():
        """)
        self.assertTrue(not self.contract.code().error)

        print("""
test contract.push_action("create"):
        """)
        self.assertTrue(not self.contract.push_action(
            "create", 
            '{"issuer":"' 
                + str(account_eosio) 
                + '", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}').error)

        print("""
test contract.push_action("issue"):
        """)
        self.assertTrue(not self.contract.push_action(
            "issue", 
            '{"to":"' + str(alice)
                + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
                account_eosio).error)

        print("""
test contract.push_action("transfer", alice):
        """)
        self.assertTrue(not self.contract.push_action(
            "transfer", 
            '{"from":"' 
                + str(alice)
                + '", "to":"' + str(carol)
                + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
            alice).error)

        time.sleep(1)

        print("""
test contract.push_action("transfer", carol):
        """)
        self.assertTrue(not self.contract.push_action(
            "transfer", 
            '{"from":"' 
                + str(carol)
                + '", "to":"' + str(bob)
                + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
            carol).error)

        print("""
test contract.push_action("transfer" bob):
        """)
        self.assertTrue(not self.contract.push_action(
            "transfer", 
            '{"from":"' 
                + str(bob)
                + '", "to":"' 
                + str(alice)
                + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
            bob).error)

        print("""
test contract.get_table("accounts", alice):
        """) 
        t1 = self.contract.get_table("accounts", alice)
        
        print("""
test contract.get_table("accounts", bob):
        """)

        t2 = self.contract.get_table("accounts", bob)
        
        print("""
test contract.get_table("accounts", carol):
        """)
        t3 = self.contract.get_table("accounts", carol)

        print("""
self.assertTrue(t1.json["rows"][0]["balance"] == "77.0000 EOS":
        """)
        self.assertTrue(t1.json["rows"][0]["balance"] == '77.0000 EOS""")
        
        print("""
self.assertTrue(t2.json["rows"][0]["balance"] == "11.0000 EOS":
        """)
        self.assertTrue(t2.json["rows"][0]["balance"] == '11.0000 EOS""")
        
        print("""
self.assertTrue(t3.json["rows"][0]["balance"] == "12.0000 EOS":
        """)
        self.assertTrue(t3.json["rows"][0]["balance"] == '12.0000 EOS""")

        print("""
test node.stop():
        """)
        teos.node_stop()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        teos.node_stop()


if __name__ == "__main__":
    unittest.main()