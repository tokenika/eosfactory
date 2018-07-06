import setup
import eosf
import unittest
from termcolor import cprint
import time
import sys

wallet_name = "default"
wallet_pass = "PW5HuwzUusrEBuEVE3oTf1ZrJHEbdAEhfqyMBk8TcwbfEN456Pkum"
deployment = True

setup.set_verbose(True)
# setup.use_keosd(True)
# setup.set_nodeos_URL("88.99.97.30:38888")

global account_master
global account_alice
global account_carol
global account_test
global globals_
globals_ = globals()

contract_dir = sys.path[0] + "/../build"

class Test1(unittest.TestCase):
    
    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        global contract

        if setup.is_use_keosd():
            wallet = eosf.Wallet(wallet_name, wallet_pass)
            restored = wallet.restore_accounts(globals_)
            account_test = account_master
        else:
            testnet = eosf.reset()
            wallet = eosf.Wallet()
            account_master = eosf.AccountMaster()
            wallet.import_key(account_master)

            account_alice = eosf.account()
            wallet.import_key(account_alice)
            account_carol = eosf.account()
            wallet.import_key(account_carol)

            account_test = eosf.account(name="r2onomqunelj")
            wallet.import_key(account_test)            

            wallet = None
            account_alice = None
            account_carol = None

            wallet = eosf.Wallet()
            restored = wallet.restore_accounts(globals_)
            restored["account_master"] = account_master

         
        assert("account_master" in restored)

        if (not "account_alice" in restored):
            account_alice = eosf.account(
                account_master,
                stake_net="100 EOS",
                stake_cpu="100 EOS",
                buy_ram_kbytes="80",
                transfer=True)
            assert(not account_alice.error)
            wallet.import_key(account_alice)

        if (not "account_carol" in restored):
            account_carol = eosf.account(
                account_master,
                stake_net="1000 EOS",
                stake_cpu="1000 EOS",
                buy_ram_kbytes="1200",
                transfer=True)
            assert(not account_carol.error)
            wallet.import_key(account_carol)

        print(contract_dir)
        contract = eosf.Contract(account_test, contract_dir, is_verbose=1)
        
        if deployment:
            deploy = contract.deploy()
            assert(not deploy.error)

        time.sleep(1)

    def setUp(self):
        pass 


    def test_01(self):
        print(account_alice.info())

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
        pass


if __name__ == "__main__":
    unittest.main()
