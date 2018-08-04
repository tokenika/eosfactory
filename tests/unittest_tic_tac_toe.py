import unittest
import setup
import eosf

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT])
# eosf.set_verbosity_plus([eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
#setup.set_command_line_mode()

_ = eosf.Logger()

class Test1(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print("""

NEXT TEST ====================================================================
""")

    @classmethod
    def setUpClass(cls):
        print()

    def setUp(self):
        eosf.restart()
        eosf.set_is_testing_errors(False)
        eosf.set_throw_error(True)

    def test_tic_tac_toe(self):
        _.SCENARIO("""
        Use the local test net.
        Create the ``account_tic_tac_toe`` account that will keep the ``tic_tac_toe`` 
        contract. Note that the contract assumes that its account's name is 
        ``tic.tac.toe``. 
        Create two player accounts: ``account_alice`` and ``account_carol``.
        Deploy the Contract
        Run games.
        """)        
        eosf.use_keosd(False)
        eosf.reset([eosf.Verbosity.TRACE]) 
        wallet = Wallet()
        account_master_create("account_master")

        account_create(
            "account_tic_tac_toe", account_master, account_name="tic.tac.toe")
        account_create("account_alice", account_master)
        account_create("account_carol", account_master)

        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()

        ######################################################################  

        contract_tic_tac_toe = Contract(account_tic_tac_toe, "tic_tac_toe_jungle")
        #contract_tic_tac_toe.build()
        deploy = contract_tic_tac_toe.deploy()

        account_tic_tac_toe.push_action(
            "create", 
            '{"challenger":"' + str(account_alice) 
                +'", "host":"' + str(account_carol) + '"}',
            account_carol)

        t = account_tic_tac_toe.table("games", account_carol)
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

        account_tic_tac_toe.push_action(
            "move", 
            '{"challenger":"' + str(account_alice) 
                + '", "host":"' + str(account_carol) 
                + '", "by":"' + str(account_carol) 
                + '", "row":0, "column":0 }', 
            account_carol)

        account_tic_tac_toe.push_action(
            "move", 
            '{"challenger":"' + str(account_alice) 
                + '", "host":"' + str(account_carol) 
                + '", "by":"' + str(account_alice) 
                + '", "row":1, "column":1 }', 
            account_alice)

        t = account_tic_tac_toe.table("games", account_carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 1)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 2)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        account_tic_tac_toe.push_action(
                "restart", 
                '{"challenger":"' + str(account_alice) 
                    + '", "host":"' + str(account_carol) 
                    + '", "by":"' + str(account_carol) + '"}', 
                account_carol)

        t = account_tic_tac_toe.table("games", account_carol)
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

        account_tic_tac_toe.push_action(
                "close", 
                '{"challenger":"' + str(account_alice) 
                    + '", "host":"' + str(account_carol) + '"}', 
                account_carol)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        eosf.stop()

if __name__ == "__main__":
    unittest.main()