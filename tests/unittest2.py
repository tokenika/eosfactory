# python3 ./tests/unittest2.py

import setup
import eosf
import node
import unittest
from termcolor import cprint

setup.set_verbose(False)
eosf.use_keosd(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        testnet = node.reset()
        assert(not testnet.error)

        wallet = eosf.Wallet()
        assert(not wallet.error)

        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)
        assert(not account_master.error)

        global account_alice
        account_alice = eosf.account(account_master)
        wallet.import_key(account_alice)
        assert(not account_alice.error)

        global account_carol
        account_carol = eosf.account(account_master)
        wallet.import_key(account_carol)
        assert(not account_carol.error)

        account_deploy = eosf.account(account_master, name="tic.tac.toe")
        wallet.import_key(account_deploy)
        assert(not account_deploy.error)

        contract_eosio_bios = eosf.Contract(
            account_master, "eosio.bios").deploy()
        assert(not contract_eosio_bios.error)

        global contract
        contract = eosf.Contract(account_deploy, "tic_tac_toe")
        assert(not contract.error)

        deployment = contract.deploy()
        assert(not deployment.error)


    def setUp(self):
        pass


    def test_01(self):

        cprint("""
Action contract.push_action("create")
        """, 'magenta')
        action = contract.push_action(
            "create", 
            '{"challenger":"' 
            + str(account_alice) +'", "host":"' 
            + str(account_carol) + '"}', account_carol)
        print(action)
        self.assertFalse(action.error)
        
        t = contract.table("games", account_carol)
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
            + str(account_alice) + '", "host":"' 
            + str(account_carol) + '", "by":"' 
            + str(account_carol) + '", "mvt":{"row":0, "column":0} }', account_carol)
        print(action)
        self.assertFalse(action.error)

        cprint("""
Action contract.push_action("move")
        """, 'magenta')
        action = contract.push_action(
            "move", 
            '{"challenger":"' 
            + str(account_alice) + '", "host":"' 
            + str(account_carol) + '", "by":"' 
            + str(account_alice) + '", "mvt":{"row":1, "column":1} }', account_alice)
        print(action)
        self.assertFalse(action.error)

        t = contract.table("games", account_carol)
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
                + str(account_alice) + '", "host":"' 
                + str(account_carol) + '", "by":"' + str(account_carol) + '"}', account_carol)
        print(action)
        self.assertFalse(action.error)

        t = contract.table("games", account_carol)
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
                + str(account_alice) + '", "host":"' + str(account_carol) + '"}', account_carol)
        print(action)
        self.assertFalse(action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()