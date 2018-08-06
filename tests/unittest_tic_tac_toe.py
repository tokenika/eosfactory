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
cryptolions = "88.99.97.30:38888"

ACCOUNT_MASTER = "account_master"
ACCOUNT_TTT = None
WALLET_NAME = "VhZNXMGZ48Ti7u84nDnyq87rv"
IS_USE_KEOSD = False

ACCOUNT_NAME = "dgxo1uyhoytn"
OWNER_KEY = "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY"
ACTIVE_KEY = "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"

class Test1(unittest.TestCase):

    def setUp(self):
        if IS_USE_KEOSD:
            eosf.stop([eosf.Verbosity.TRACE])
            eosf.use_keosd(True)
            eosf.stop()

            setup.set_nodeos_address(cryptolions)
            eosf.info()

            ACCOUNT_TTT = ACCOUNT_MASTER
            eosf.use_keosd(True)
            eosf.kill_keosd()
            try:
                wallet_file = eosf.wallet_dir() + WALLET_NAME + ".wallet"
                os.remove(wallet_file)
                print("The deleted wallet file:\n{}\n".format(wallet_file))
            except Exception as e:
                print("Cannot delete the wallet file:\n{}\n".format(str(e))) 

            wallet = Wallet(WALLET_NAME)

            account_master_create(
                ACCOUNT_MASTER, ACCOUNT_NAME, OWNER_KEY, ACTIVE_KEY)
        else:
            eosf.use_keosd(False)
            eosf.kill_keosd()
            eosf.reset([eosf.Verbosity.TRACE])

            wallet = Wallet()
            ACCOUNT_MASTER = "account_master"
            account_master_create(ACCOUNT_MASTER)

            ACCOUNT_TTT = "account_tic_tac_toe"
            account_create(ACCOUNT_TTT, account_master)

        global account_master
        account_master = globals()[ACCOUNT_MASTER]
        global account_tic_tac_toe
        account_tic_tac_toe = globals()[ACCOUNT_TTT] 

        contract_tic_tac_toe = Contract(
            account_tic_tac_toe, "tic_tac_toe_jungle")
        contract_tic_tac_toe.build_abi()
        contract_tic_tac_toe.deploy()        
        eosf.set_throw_error(False)            

    def test_tic_tac_toe(self):
        _.SCENARIO("""
        Given a ``Wallet`` class object in the global namespace; an account 
        master object named ``account_master`` in the global namespace;
        given an account object named ``account_tic_tac_toe`` account that keeps 
        the ``tic_tac_toe`` contract 
        -- create two player accounts: ``account_alice`` and ``account_carol``.
        
        Run games.
        """)
        
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

    def tearDown(self):
        eosf.stop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if not isinstance(sys.argv[1], bool) :
            print(
                "Usage: python3 unittest_tic_tac_toe.1.py <is use keosd>")
            exit()            

    if len(sys.argv) == 1 or not sys.argv[1]:
        IS_USE_KEOSD = False
    else:
        IS_USE_KEOSD = True

    unittest.main()