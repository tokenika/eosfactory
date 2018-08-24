import unittest
from  eosfactory import *

Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
_ = Logger()

CONTRACT_WORKSPACE = "03_tic_tac_toe"
ACCOUNT_MASTER = "account_master"
ACCOUNT_HOST = "account_host"

class Test(unittest.TestCase):

    def setUp(self):

        global ACCOUNT_MASTER
        global ACCOUNT_HOST

        set_throw_error(True)

        if IS_USE_KEOSD:
            stop([Verbosity.INFO])
            
            setup.set_nodeos_address(remote_testnet)
            info()

            try:
                wallet_file = wallet_dir() + WALLET_NAME + ".wallet"
                os.remove(wallet_file)
                _.INFO("The deleted wallet file:\n{}\n".format(wallet_file))
            except Exception as e:
                _.ERROR("Cannot delete the wallet file:\n{}\n".format(str(e)))

            create_wallet(
                WALLET_NAME,
                verbosity=[Verbosity.INFO])
            ACCOUNT_MASTER = ACCOUNT_HOST

            if not ACCOUNT_MASTER in globals():
                create_master_account(
                    ACCOUNT_MASTER, ACCOUNT_NAME, OWNER_KEY, ACTIVE_KEY,
                    verbosity=[Verbosity.INFO, Verbosity.OUT])

        else:
            reset([Verbosity.INFO])

            create_wallet()
            create_master_account(ACCOUNT_MASTER)
            create_account(ACCOUNT_HOST, globals()[ACCOUNT_MASTER])

        global account_master
        account_master = globals()[ACCOUNT_MASTER]
        global croupier
        croupier = globals()[ACCOUNT_HOST] 

        contract_tic_tac_toe = Contract(
            croupier, CONTRACT_WORKSPACE)

        if not contract.is_built():
            contract_tic_tac_toe.build()

        if not croupier.is_code():
            contract_tic_tac_toe.deploy()

        if not "alice" in globals():
            create_account("alice", account_master)
        if not "carol" in globals():
            create_account("carol", account_master)

        set_is_testing_errors()


    def test_tic_tac_toe(self):
        _.SCENARIO('''
        Run the ``tic-tac-toe`` game with the following prerequisites:
        * an instance of the Wallet class,
        * an instance of an AccountMaster class, named ``account_master``,
        * an instance of an Account class, named ``account_host``, which stores the contract,
        * and two player accounts named ``alice`` and ``carol``.
        ''')

        croupier.push_action(
            "create", 
            {
                "challenger": alice,
                "host": carol
            },
            carol)

        t = croupier.table("games", carol)
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

        croupier.push_action(
            "close",
            {
                "challenger": alice,
                "host": carol
            }, 
            carol)

    def tearDown(self):
        stop()

if __name__ == "__main__":
    '''Test the ``tic-tac-toe`` contract either locally or remotely.
    '''
    import sys
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