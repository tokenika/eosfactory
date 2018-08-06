import sys
import unittest
import setup
import eosf

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, \
    eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
_ = eosf.Logger()

ACCOUNT_MASTER = None
ACCOUNT_TTT = None

class Test1(unittest.TestCase):

    def test_tic_tac_toe(self):
        _.SCENARIO("""
        Given a ``Wallet`` class object in the global namespace; an account 
        master object named ``account_master`` in the global namespace;
        given an account object named ``account_tic_tac_toe`` account that keeps 
        the ``tic_tac_toe`` contract 
        -- create two player accounts: ``account_alice`` and ``account_carol``.
        
        Run games.
        """)
        
        account_master = globals()[ACCOUNT_MASTER]
        account_tic_tac_toe = globals()[ACCOUNT_TTT]

        account_create("account_alice", account_master)
        account_create("account_carol", account_master)

        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()

        ######################################################################  


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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) == 5:
            print(
                "Usage: python3 unittest_tic_tac_toe.1.py " \
                + "<wallet name> <password> <account master> <account ttt>")
        else:
            exit()

    if len(sys.argv) == 1:
        eosf.use_keosd(False)
        eosf.kill_keosd()
        eosf.reset([eosf.Verbosity.TRACE])

        wallet = Wallet()
        ACCOUNT_MASTER = "account_master"
        account_master_create(ACCOUNT_MASTER)

        ACCOUNT_TTT = "account_tic_tac_toe"
        account_create(ACCOUNT_TTT, account_master)

        contract_tic_tac_toe = Contract(
            globals()[ACCOUNT_TTT], "tic_tac_toe_jungle")
        contract_tic_tac_toe.build_abi()
        contract_tic_tac_toe.deploy()
    else:
        eosf.stop([eosf.Verbosity.TRACE])
        eosf.use_keosd(True)
        WALLET_NAME = sys.argv[1]
        PASSWORD = sys.argv[2]
        ACCOUNT_MASTER = sys.argv[3]
        ACCOUNT_TTT = sys.argv[4]
        eosf.use_keosd(True)
        wallet = Wallet(WALLET_NAME, PASSWORD)

    unittest.main()