import os
import sys
import unittest
import setup
import eosf
import eosf_account

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract
from user_data import *

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, \
    eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
_ = eosf.Logger()

IS_USE_KEOSD = False

ACCOUNT_MASTER = "account_master"
ACCOUNT_TTT = "account_tic_tac_toe"
_ = eosf.Logger()

class Test(unittest.TestCase):

    def setUp(self):
        eosf.kill_keosd()

        global ACCOUNT_MASTER
        global ACCOUNT_TTT

        eosf.set_throw_error(True)

        if IS_USE_KEOSD:
            eosf.stop([eosf.Verbosity.TRACE])
            eosf.use_keosd(True)
            
            setup.set_nodeos_address(remote_testnet)
            eosf.info()

            try:
                wallet_file = eosf.wallet_dir() + WALLET_NAME + ".wallet"
                os.remove(wallet_file)
                _.TRACE("The deleted wallet file:\n{}\n".format(wallet_file))
            except Exception as e:
                _.ERROR("Cannot delete the wallet file:\n{}\n".format(str(e))) 

            wallet = Wallet(
                WALLET_NAME, 
                verbosity=[eosf.Verbosity.TRACE]) 
            ACCOUNT_MASTER = ACCOUNT_TTT

            if not ACCOUNT_MASTER in globals():
                account_master_create(
                    ACCOUNT_MASTER, ACCOUNT_NAME, OWNER_KEY, ACTIVE_KEY,
                    verbosity=[eosf.Verbosity.TRACE, eosf.Verbosity.OUT])

        else:
            eosf.use_keosd(False)
            eosf.reset([eosf.Verbosity.TRACE])

            wallet = Wallet()
            account_master_create(ACCOUNT_MASTER)
            account_create(ACCOUNT_TTT, globals()[ACCOUNT_MASTER])

        global account_master
        account_master = globals()[ACCOUNT_MASTER]
        global account_tic_tac_toe
        account_tic_tac_toe = globals()[ACCOUNT_TTT] 

        contract_tic_tac_toe = Contract(
            account_tic_tac_toe, "tic_tac_toe_jungle")        
        contract_tic_tac_toe.build()
        if not account_tic_tac_toe.is_code():            
            contract_tic_tac_toe.deploy()

        if not "account_alice" in globals():
            account_create("account_alice", account_master)
        if not "account_carol" in globals():
            account_create("account_carol", account_master)

        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()

    def test_tic_tac_toe(self):
        _.SCENARIO("""
        Given a ``Wallet`` class object in the global namespace; an account 
        master object named ``account_master`` in the global namespace;
        given an account object named ``account_tic_tac_toe`` account that keeps 
        the ``tic_tac_toe`` contract; and given two player accounts: 
        ``account_alice`` and ``account_carol`` -- run games.
        """)

        account_tic_tac_toe.push_action(
            "create", 
            '''{
                "challenger": "account_alice",
                "host":"account_carol"
            }''',
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
            {
                "challenger": account_alice,                 
                "host": account_carol,
                "by": account_carol, 
                "row": 0, "column": 0 
            }, 
            account_carol)

        account_tic_tac_toe.push_action(
            "move", 
            {
                "challenger": account_alice, 
                "host": account_carol,
                "by": account_alice, 
                "row": 1, "column": 1 
            }, 
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
                {
                    "challenger": account_alice, 
                    "host": account_carol,
                    "by": account_carol
                }, 
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
                {
                    "challenger": account_alice,
                    "host": account_carol
                }, 
                account_carol)

    def tearDown(self):
        eosf.stop()

if __name__ == "__main__":
    """Test the ``tic_tac_toe`` contract either locally or remotely.
    """
    IS_USE_KEOSD = False
    if len(sys.argv) > 1:
        case = sys.argv.pop()
        if case.upper() == "REMOTE":
            IS_USE_KEOSD = True
        else:
            if not case.upper() == "LOCAL":
                print(
                    "Usage: python3 {} <remote | local>".format(sys.argv[0]))
                exit()

    unittest.main()