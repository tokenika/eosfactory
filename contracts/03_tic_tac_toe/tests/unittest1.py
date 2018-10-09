import unittest, argparse, sys, time
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

INITIAL_RAM_KBYTES = 8
INITIAL_STAKE_NET = 3
INITIAL_STAKE_CPU = 3

class Test(unittest.TestCase):

    def stats():
        print_stats(
            [master, host, alice, carol],
            [
                "core_liquid_balance",
                "ram_usage",
                "ram_quota",
                "total_resources.ram_bytes",
                "self_delegated_bandwidth.net_weight",
                "self_delegated_bandwidth.cpu_weight",
                "total_resources.net_weight",
                "total_resources.cpu_weight",
                "net_limit.available",
                "net_limit.max",
                "net_limit.used",
                "cpu_limit.available",
                "cpu_limit.max",
                "cpu_limit.used"
            ]
        )


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        There is the ``master`` account that sponsors the ``host``
        account equipped with an instance of the ``tic_tac_toe`` smart contract. There
        are two players ``alice`` and ``carol``. We are testing that the moves of
        the game are correctly stored in the blockchain database.
        ''')

        testnet.verify_production()
        
        create_master_account("master", testnet)
        create_account("host", master,
            buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        create_account("alice", master,
            buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        create_account("carol", master,
            buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)

        if not testnet.is_local():
            cls.stats()

        contract = Contract(host, CONTRACT_WORKSPACE)
        contract.build(force=False)

        try:
            contract.deploy(payer=master)
        except errors.ContractRunningError:
            pass


    def setUp(self):
        pass


    def test_01(self):
        COMMENT('''
        Attempting to create a new game.
        This might fail if the previous game has not been closes properly:
        ''')
        try:
            host.push_action(
                "create",
                {
                    "challenger": alice,
                    "host": carol
                },
                permission=(carol, Permission.ACTIVE))
        except Error as e:
            if "game already exists" in e.message:
                COMMENT('''
                We need to close the previous game before creating a new one:
                ''')
                host.push_action(
                    "close",
                    {
                        "challenger": alice,
                        "host": carol
                    },
                    permission=(carol, Permission.ACTIVE))

                time.sleep(3)

                COMMENT('''
                Second attempt to create a new game:
                ''')
                host.push_action(
                    "create",
                    {
                        "challenger": alice, 
                        "host": carol
                    },
                    permission=(carol, Permission.ACTIVE))
            else:
                COMMENT('''
                The error is different than expected.
                ''')
                raise Error(str(e))

        t = host.table("games", carol)
        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        COMMENT('''
        First move is by carol:
        ''')
        host.push_action(
            "move",
            {
                "challenger": alice,
                "host": carol,
                "by": carol,
                "row":0, "column":0
            },
            permission=(carol, Permission.ACTIVE))

        COMMENT('''
        Second move is by alice:
        ''')
        host.push_action(
            "move",
            {
                "challenger": alice,
                "host": carol,
                "by": alice,
                "row":1, "column":1
            },
            permission=(alice, Permission.ACTIVE))

        t = host.table("games", carol)
        self.assertEqual(t.json["rows"][0]["board"][0], 1)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 2)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        COMMENT('''
        Restarting the game:
        ''')
        host.push_action(
            "restart",
            {
                "challenger": alice,
                "host": carol,
                "by": carol
            }, 
            permission=(carol, Permission.ACTIVE))

        t = host.table("games", carol)
        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)
        
        COMMENT('''
        Closing the game:
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            host.push_action(
                "close",
                {
                    "challenger": alice,
                    "host": carol
                },
                permission=(alice, Permission.ACTIVE))

        COMMENT('''
        Closing the game:
        ''')
        host.push_action(
            "close",
            {
                "challenger": alice,
                "host": carol
            },
            permission=(carol, Permission.ACTIVE))


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        if testnet.is_local():
            stop()
        else:
            cls.stats()


testnet = None

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    This is a unit test for the ``tic-tac-toe`` smart contract.
    It works both on a local testnet and remote testnet.
    The default option is local testnet.
    ''')

    parser.add_argument(
        "alias", nargs="?",
        help="Testnet alias")

    parser.add_argument(
        "-t", "--testnet", nargs=4,
        help="<url> <name> <owner key> <active key>")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset testnet cache")

    args = parser.parse_args()

    testnet = get_testnet(args.alias, args.testnet, reset=args.reset)
    testnet.configure()

    if args.reset and not testnet.is_local():
        testnet.clear_cache()

    unittest.main(argv=[sys.argv[0]])
