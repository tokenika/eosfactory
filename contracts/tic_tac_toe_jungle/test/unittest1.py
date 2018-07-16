import setup
import eosf
import unittest
import sys
from termcolor import cprint

wallet_name = "" # Enter wallet name
wallet_pass = "" # Enter wallet password

"""
This flag needs to be set to `True` only for the initial run
or after the contract is changed and re-built
"""
deployment = True

setup.set_verbose(True)
setup.use_keosd(True)
setup.set_nodeos_address("88.99.97.30:38888") # CryptoLions endpoint

class Test1(unittest.TestCase):

    global account_master
    global account_alice
    global account_carol

    wallet = eosf.Wallet(wallet_name, wallet_pass)
    assert(not wallet.error)
    
    restored = wallet.restore_accounts(globals())

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


    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        global contract

        contract = eosf.Contract(
            account_master, sys.path[0] + "/../build")

        if deployment:
            assert(not contract.deploy().error)


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
        self.assertFalse(action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
