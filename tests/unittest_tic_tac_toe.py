import os
import sys
import unittest
import setup
import eosf

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

class Test1(unittest.TestCase):

    def setUp(self):
        eosf.kill_keosd()

        global ACCOUNT_MASTER
        global ACCOUNT_TTT

        eosf.set_throw_error(True)
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
        contract_tic_tac_toe.deploy()
        code_hash = account_tic_tac_toe.code(json=True)["code_hash"]

        if IS_USE_KEOSD:
            eosf.stop([eosf.Verbosity.TRACE])
            eosf_account.restart()
            eosf.use_keosd(True)
            
            setup.set_nodeos_address(cryptolions)
            eosf.info()

            try:
                wallet_file = eosf.wallet_dir() + WALLET_NAME + ".wallet"
                os.remove(wallet_file)
                print("The deleted wallet file:\n{}\n".format(wallet_file))
            except Exception as e:
                print("Cannot delete the wallet file:\n{}\n".format(str(e))) 

            wallet = Wallet(
                WALLET_NAME, 
                verbosity=[eosf.Verbosity.TRACE, eosf.Verbosity.OUT]) 
            ACCOUNT_MASTER = ACCOUNT_TTT

            account_master_create(
                ACCOUNT_MASTER, ACCOUNT_NAME, OWNER_KEY, ACTIVE_KEY,
                verbosity=[eosf.Verbosity.TRACE, eosf.Verbosity.OUT])

            global account_master
            account_master = globals()[ACCOUNT_MASTER]
            global account_tic_tac_toe
            account_tic_tac_toe = globals()[ACCOUNT_TTT] 

            contract_tic_tac_toe = Contract(
                account_tic_tac_toe, "tic_tac_toe_jungle")        
            if not account_tic_tac_toe.code(json=True) == code_hash:
                contract_tic_tac_toe.deploy()

        account_create("account_alice", account_master)
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