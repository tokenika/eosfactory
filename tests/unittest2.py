# python3 ./tests/unittest2.py

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


    def test_11(self):
        global wallet
        global contract_test

        cprint("""
Create an account to be equipped with a smart contract, namely:
"tic_tac_toe" from the EOSIO repository, 
use `account_test = eosf.account()`:
        """, 'magenta')

        account_test = eosf.account(name="tic.tac.toe")
        self.assertTrue(not account_test.error)

        cprint("""
Put the account into the wallet, use `wallet.import_key(account_test)`:
        """, 'magenta')
        
        wallet.import_key(account_test)

        cprint("""
Create a smart contract object:
        """, 'magenta')

        contract_test = eosf.Contract(account_test, "tic_tac_toe")

        cprint("""
Deploy the contract:
        """, 'magenta')
        deployed = contract_test.deploy()
        self.assertTrue(not deployed.error)
                
        cprint("""
See the response of the node, use `print(contract.contract_test)`:
        """, 'magenta')

        print(contract_test.contract)

        cprint("""
See the response of the node, use `print(contract.contract_test)`:
        """, 'magenta')

        cprint("""
Confirm that the account `account_test` contains a contract code:
        """, 'magenta')

        code = account_test.code()
        print("code hash: {}".format(code.code_hash))

        time.sleep(1)


    def test_15(self):
        global alice
        global bob

        cprint("""
Create accounts `alice`and `bob`, 
use `alice = eosf.account()` and `wallet.import_key(alice)`:
        """, 'magenta')

        alice = eosf.account()
        self.assertTrue(not alice.error)
        wallet.import_key(alice)

        bob = eosf.account()
        self.assertTrue(not bob.error)
        wallet.import_key(bob)        

        cprint("""
Inspect the account, use `bob.account()`:
        """, 'magenta')
        
        print(bob.info())


    def test_20(self):
        global contract_test
        global alice
        global bob

        cprint("""
Push actions to the contract. Begin with the `create` action:
        """, 'magenta')
        action_create = contract_test.push_action(
            "create", 
            '{"challenger":"' 
            + str(alice) +'", "host":"' 
            + str(bob) + '"}', bob)

        cprint("""
See the response of the node to the `create` action, 
use `print(action_create)`:
        """, 'magenta')

        print(action_create)
        self.assertTrue(not action_create.error)

        cprint("""
See the result of the action:
        """, 'magenta')

        time.sleep(2)

        t = contract_test.table("games", bob)
        self.assertTrue(not t.error)

        time.sleep(2)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)


    def test_25(self):
        global contract_test
        global alice
        global bob
        
        action_move = contract_test.push_action(
            "move", 
            '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' 
            + str(bob) + '", "mvt":{"row":0, "column":0} }', bob)

        self.assertTrue(not action_move.error)

        action_move = contract_test.push_action(
            "move", 
            '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' 
            + str(alice) + '", "mvt":{"row":1, "column":1} }', alice)

        self.assertTrue(not action_move.error)

        t = contract_test.table("games", bob)
        self.assertTrue(not t.error)


        self.assertEqual(t.json["rows"][0]["board"][0], 1)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 2)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)


    def test_30(self):

        action_restart = contract_test.push_action(
                "restart", 
                '{"challenger":"' 
                + str(alice) + '", "host":"' 
                + str(bob) + '", "by":"' + str(bob) + '"}',
                bob)

        self.assertTrue(not action_restart.error)

        t = contract_test.table("games", bob)
        self.assertFalse(t.error, "table")

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)


    def test_35(self):

        action_close = contract_test.push_action(
                "close", 
                '{"challenger":"' 
                + str(alice) + '", "host":"' + str(bob) + '"}', bob)

        self.assertTrue(not action_close.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        eosf.stop()


if __name__ == "__main__":
    unittest.main()