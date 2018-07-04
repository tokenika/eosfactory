# python3 ./tests/unittest1.py

import unittest
import json
import time
from termcolor import colored, cprint #sudo python3 -m pip install termcolor
import setup
import eosf

setup.set_verbose(False)
setup.use_keosd(False)

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
        global wallet
        global account_master
        global alice
        global bob
        global carol

        cprint("""
Start a local test EOSIO node, use `eosf.reset()`:
        """, 'magenta')

        reset = eosf.reset()
        self.assertTrue(not reset.error)
        
        cprint("""
Create a local wallet, use `wallet = eosf.Wallet()`:
        """, 'magenta')

        wallet = eosf.Wallet()
        self.assertTrue(not wallet.error)

        cprint("""
Implement the `eosio` master account as a `eosf.AccountMaster` object,
use `account_master = eosf.AccountMaster()` 
and `wallet.import_key(account_master)`:
        """, 'magenta')

        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)

        cprint("""
Deploy the `eosio.bios` contract, 
use `eosf.Contract(account_master, "eosio.bios").deploy()`:
        """, 'magenta')

        contract_eosio_bios = eosf.Contract(
                account_master, "eosio.bios").deploy()
        self.assertTrue(not contract_eosio_bios.error)

        cprint("""
Create accounts `alice`, `bob` and `carol`:
        """, 'magenta')
        
        alice = eosf.account()
        self.assertTrue(not alice.error)
        wallet.import_key(alice)

        bob = eosf.account()
        self.assertTrue(not bob.error)
        wallet.import_key(bob)        

        carol = eosf.account()
        self.assertTrue(not carol.error)
        wallet.import_key(carol) 

        cprint("""
Inspect the account, use `bob.info()`:
        """, 'magenta')     

        print(bob.info())   


    def test_05(self):
        global wallet
        global alice
        global bob
        global carol
        global account_master
        global contract_test

        account_test = eosf.account()
        wallet.import_key(account_test)
        

        contract_test = eosf.Contract(account_test, "eosio.token")
        self.assertTrue(not contract_test.error)

        cprint("""
test contract_test.code():
        """, 'magenta')
        self.assertTrue(not contract_test.code().error)

        cprint("""
test contract_test.deploy():
        """, 'magenta')
        self.assertTrue(contract_test.deploy())

        cprint("""
test contract_test.code():
        """, 'magenta')
        self.assertTrue(not contract_test.code().error)

        time.sleep(1)

        cprint("""
test contract_test.push_action("create"):
        """, 'magenta')
        self.assertTrue(not contract_test.push_action(
            "create", 
            '{"issuer":"' 
                + str(account_master) 
                + '", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}').error)

        cprint("""
test contract_test.push_action("issue"):
        """, 'magenta')
        self.assertTrue(not contract_test.push_action(
            "issue", 
            '{"to":"' + str(alice)
                + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
                account_master).error)

        cprint("""
test contract_test.push_action("transfer", alice):
        """, 'magenta')
        self.assertTrue(not contract_test.push_action(
            "transfer", 
            '{"from":"' 
                + str(alice)
                + '", "to":"' + str(carol)
                + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
            alice).error)

        time.sleep(1)

        cprint("""
test contract_test.push_action("transfer", carol):
        """, 'magenta')
        self.assertTrue(not contract_test.push_action(
            "transfer", 
            '{"from":"' 
                + str(carol)
                + '", "to":"' + str(bob)
                + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
            carol).error)

        cprint("""
test contract_test.push_action("transfer" bob):
        """, 'magenta')
        self.assertTrue(not contract_test.push_action(
            "transfer", 
            '{"from":"' 
                + str(bob)
                + '", "to":"' 
                + str(alice)
                + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
            bob).error)

        cprint("""
Get database table, use `contract_test.table("accounts", alice)`:
        """, 'magenta')

        t1 = contract_test.table("accounts", alice)
        
        cprint("""
Get database table, use `contract_test.table("accounts", bob)`:
        """, 'magenta')

        t2 = contract_test.table("accounts", bob)
        
        cprint("""
Get database table, use `contract_test.table("accounts", carol)`:
        """, 'magenta')
        
        t3 = contract_test.table("accounts", carol)

        cprint("""
self.assertTrue(t1.json["rows"][0]["balance"] == "77.0000 EOS":
        """, 'magenta')

        self.assertTrue(t1.json["rows"][0]["balance"] == '77.0000 EOS')
        
        cprint("""
self.assertTrue(t2.json["rows"][0]["balance"] == "11.0000 EOS":
        """, 'magenta')

        self.assertTrue(t2.json["rows"][0]["balance"] == '11.0000 EOS')
        
        cprint("""
self.assertTrue(t3.json["rows"][0]["balance"] == "12.0000 EOS":
        """, 'magenta')

        self.assertTrue(t3.json["rows"][0]["balance"] == '12.0000 EOS')

        cprint("""
test node.stop():
        """, 'magenta')
        eosf.stop()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        eosf.stop()


if __name__ == "__main__":
    unittest.main()