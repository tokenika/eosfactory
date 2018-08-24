import unittest, sys
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        reset([Verbosity.INFO])

        create_wallet()
        create_master_account("account_master")
        create_account("croupier", account_master)
        create_account("alice", account_master)
        create_account("carol", account_master)
        contract = Contract(
            croupier, sys.path[0] + "/../")

        if not contract.is_built():
            contract.build()
        contract.deploy()        

        _.SCENARIO("""
Having created the ``croupier`` account that keeps the ``tic_tac_toe`` contract 
from the EOSIO distribution, and two players: ``alice`` and ``carol``, Run 
games.
        """)

    def test_tic_tac_toe(self):

        croupier.push_action(
            "create", 
            {
                "challenger": alice,
                "host": carol
            },
            carol)

        t = croupier.table("games", carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        croupier.push_action(
            "move", 
            {
                "challenger": alice,
                "host": carol,
                "by": carol, 
                "row": 0, "column": 0 
            }, 
            carol)

        croupier.push_action(
            "move", 
            {
                "challenger": alice, 
                "host": carol,
                "by": alice, 
                "row": 1, "column": 1 
            }, 
            alice)

        t = croupier.table("games", carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 1)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 2)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        croupier.push_action(
            "restart", 
            {
                "challenger": alice, 
                "host": carol,
                "by": carol
            }, 
            carol)

        t = croupier.table("games", carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        croupier.push_action(
            "close",
            {
                "challenger": alice,
                "host": carol
            }, 
            carol)

    @classmethod
    def tearDownClass(cls):
        stop()

if __name__ == "__main__":
    unittest.main()