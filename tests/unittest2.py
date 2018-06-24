# python3 ./tests/unittest2.py

import unittest
import json
import time
import setup
import teos
import cleos
import eosf
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

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
        global wallet
        global account_eosio

        cprint("""
Start a local test EOSIO node, use `teos.node_reset()`:
        """, 'magenta')

        ok = teos.node_reset()
        self.assertTrue(ok)
        
        cprint("""
Create a local wallet, use `wallet = eosf.Wallet()`:
        """, 'magenta')

        wallet = eosf.Wallet()
        self.assertTrue(not wallet.error)

        cprint("""
Implement the `eosio` master account as a `cleos.AccountEosio` object,
use `account_eosio = cleos.AccountEosio()` 
and `wallet.import_key(account_eosio)`:
        """, 'magenta')

        account_eosio = cleos.AccountEosio()
        wallet.import_key(account_eosio)

        cprint("""
Deploy the `eosio.bios` contract, 
use `cleos.SetContract(account_eosio, "eosio.bios")`:
        """, 'magenta')

        contract_eosio_bios = cleos.SetContract(account_eosio, "eosio.bios")
        self.assertTrue(not contract_eosio_bios.error)


    def test_11(self):
        global wallet
        global contract_ttt

        cprint("""
Create an account to be equipped with a smart contract, namely:
"tic_tac_toe" from the EOSIO repository, 
use `account_ttt = eosf.Account()`:
        """, 'magenta')

        account_ttt = eosf.Account()
        self.assertTrue(not account_ttt.error)

        cprint("""
Put the account into the wallet, use `wallet.import_key(account_ttt)`:
        """, 'magenta')
        
        wallet.import_key(account_ttt)

        cprint("""
Create a smart contract object:
        """, 'magenta')

        contract_ttt = eosf.Contract(account_ttt, "tic_tac_toe")

        cprint("""
Deploy the contract:
        """, 'magenta')
        is_deployed = contract_ttt.deploy()
        self.assertTrue(is_deployed)
                
        cprint("""
See the response of the node, use `print(contract.contract_ttt)`:
        """, 'magenta')

        print(contract.contract_ttt)

        cprint("""
See the response of the node, use `print(contract.contract_ttt)`:
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
use `alice = eosf.Account()` and `wallet.import_key(alice)`:
        """, 'magenta')

        alice = eosf.Account()
        self.assertTrue(not alice.error)
        wallet.import_key(alice)

        bob = eosf.Account()
        self.assertTrue(not bob.error)
        wallet.import_key(bob)        

        cprint("""
Inspect the account, use `bob.account()`:
        """, 'magenta')
        
        print(bob.account())


    def test_20(self):
        global contract_ttt
        global alice
        global bob

        cprint("""
Push actions to the contract. Begin with the `create` action:
        """, 'magenta')
        action_create = contract_ttt.push_action(
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

        t = contract_ttt.get_table("games", bob)
        self.assertTrue(not t.error)

        print(t.json)

        # self.assertEqual(t.json["rows"][0]["board"][0], "0")
        # self.assertEqual(t.json["rows"][0]["board"][1], "0")
        # self.assertEqual(t.json["rows"][0]["board"][2], "0")
        # self.assertEqual(t.json["rows"][0]["board"][3], "0")
        # self.assertEqual(t.json["rows"][0]["board"][4], "0")
        # self.assertEqual(t.json["rows"][0]["board"][5], "0")
        # self.assertEqual(t.json["rows"][0]["board"][6], "0")
        # self.assertEqual(t.json["rows"][0]["board"][7], "0")
        # self.assertEqual(t.json["rows"][0]["board"][8], "0")


    def test_25(self):
        global contract_ttt
        global alice
        global bob
        
        action_move = contract_ttt.push_action(
            "move", 
            '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' 
            + str(bob) + '", "mvt":{"row":0, "column":0} }', bob)

        self.assertTrue(not action_move.error)

        action_move = contract_ttt.push_action(
            "move", 
            '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' 
            + str(alice) + '", "mvt":{"row":1, "column":1} }', alice)

        self.assertTrue(not action_move.error)

        t = contract_ttt.get_table("games", bob)
        self.assertTrue(not t.error)

        print("NNNNNNNNNNNNNNNNNNNNNNNNNNN")
        print(t.json)
        print("NNNNNNNNNNNNNNNNNNNNNNNNNNN")

#         self.assertEqual(t.json["rows"][0]["board"][0], "1")
#         self.assertEqual(t.json["rows"][0]["board"][1], "0")
#         self.assertEqual(t.json["rows"][0]["board"][2], "0")
#         self.assertEqual(t.json["rows"][0]["board"][3], "0")
#         self.assertEqual(t.json["rows"][0]["board"][4], "2")
#         self.assertEqual(t.json["rows"][0]["board"][5], "0")
#         self.assertEqual(t.json["rows"][0]["board"][6], "0")
#         self.assertEqual(t.json["rows"][0]["board"][7], "0")
#         self.assertEqual(t.json["rows"][0]["board"][8], "0")


#     def test_03(self):
#         self.assertTrue(
#             self.contract_ttt.push_action(
#             "restart", 
#             '{"challenger":"alice", "host":"bob", "by":"bob"}',
#             sess.bob), 
#             "push_action restart")

#         t = self.contract_ttt.get_table("games", sess.bob)
#         self.assertFalse(t.error, "get_table")

#         self.assertEqual(t.json["rows"][0]["board"][0], "0")
#         self.assertEqual(t.json["rows"][0]["board"][1], "0")
#         self.assertEqual(t.json["rows"][0]["board"][2], "0")
#         self.assertEqual(t.json["rows"][0]["board"][3], "0")
#         self.assertEqual(t.json["rows"][0]["board"][4], "0")
#         self.assertEqual(t.json["rows"][0]["board"][5], "0")
#         self.assertEqual(t.json["rows"][0]["board"][6], "0")
#         self.assertEqual(t.json["rows"][0]["board"][7], "0")
#         self.assertEqual(t.json["rows"][0]["board"][8], "0")


#     def test_04(self):
#         self.assertTrue(
#             self.contract_ttt.push_action(
#             "close", 
#             '{"challenger":"alice", "host":"bob"}',
#             sess.bob), 
#             "push_action close")


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        teos.node_stop()


if __name__ == "__main__":
    unittest.main()