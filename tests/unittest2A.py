# python3 ./tests/unittest2.py

import unittest
import json
from termcolor import cprint
import setup
import eosf
import node

setup.set_verbose(False)
setup.use_keosd(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        global testnet
        global wallet
        global eosio
        global contract_eosio_bios
        global alice
        global carol
        global contract
        global deployment

        testnet = node.reset()
        wallet = eosf.Wallet()

        eosio = eosf.AccountMaster()
        wallet.import_key(eosio)

        alice = eosf.account()
        wallet.import_key(alice)

        carol = eosf.account()
        wallet.import_key(carol)

        account = eosf.account(name="tic.tac.toe")
        wallet.import_key(account)

        contract_eosio_bios = eosf.Contract(
            eosio, "eosio.bios").deploy()

        contract = eosf.Contract(account, "tic_tac_toe")
        deployment = contract.deploy()


    def setUp(self):
        self.assertFalse(testnet.error)
        self.assertFalse(wallet.error)
        self.assertFalse(contract_eosio_bios.error)
        self.assertFalse(alice.error)
        self.assertFalse(carol.error)
        self.assertFalse(contract.error)
        self.assertFalse(deployment.error)


    def test_01(self):

        cprint("""
Action contract.push_action("create")
        """, 'magenta')
        action = contract.push_action(
            "create", 
            '{"challenger":"' 
            + str(alice) +'", "host":"' 
            + str(carol) + '"}', carol)
        print(action)
        self.assertFalse(action.error)
        
        t = contract.table("games", carol)
        self.assertFalse(t.error)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)


    def test_02(self):

        cprint("""
Action contract.push_action("move")
        """, 'magenta')
        action = contract.push_action(
            "move", 
            '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(carol) + '", "by":"' 
            + str(carol) + '", "mvt":{"row":0, "column":0} }', carol)
        print(action)
        self.assertFalse(action.error)

        cprint("""
Action contract.push_action("move")
        """, 'magenta')
        action = contract.push_action(
            "move", 
            '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(carol) + '", "by":"' 
            + str(alice) + '", "mvt":{"row":1, "column":1} }', alice)
        print(action)
        self.assertFalse(action.error)

        t = contract.table("games", carol)
        self.assertFalse(t.error)

        self.assertEqual(t.json["rows"][0]["board"][0], 1)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 2)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)


    def test_03(self):

        cprint("""
Action contract.push_action("restart")
        """, 'magenta')
        action = contract.push_action(
                "restart", 
                '{"challenger":"' 
                + str(alice) + '", "host":"' 
                + str(carol) + '", "by":"' + str(carol) + '"}', carol)
        print(action)
        self.assertFalse(action.error)

        t = contract.table("games", carol)
        self.assertFalse(t.error)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)


    def test_04(self):

        cprint("""
Action contract.push_action("close")
        """, 'magenta')
        action = contract.push_action(
                "close", 
                '{"challenger":"' 
                + str(alice) + '", "host":"' + str(carol) + '"}', carol)
        print(action)
        self.assertFalse(action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()