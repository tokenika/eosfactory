import unittest, argparse, sys
from eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"
CACHE_ID = "tic-tac-toe"

INITIAL_RAM_KBYTES = 12
INITIAL_STAKE_NET = 10.0
INITIAL_STAKE_CPU = 10.0

class Test(unittest.TestCase):

    def stats():
        eosf_account.stats(
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
        _.SCENARIO('''
        There is the ``master`` account that sponsors the ``host``
        account equipped with an instance of the ``tic_tac_toe`` smart contract. There
        are two players ``alice`` and ``carol``. We are testing that the moves of
        the game are correctly stored in the blockchain database.
        ''')

        verify_testnet()
        
        create_wallet(file=True)
        create_master_account("master", testnet)
        create_account("host", master,
            buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        create_account("alice", master,
            buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        create_account("carol", master,
            buy_ram_kbytes=INITIAL_RAM_KBYTES, stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)


        if (extra_ram > 0):
            master.buy_ram(extra_ram, host)
            master.buy_ram(extra_ram, alice)
            master.buy_ram(extra_ram, carol)

        if (extra_stake_net > 0 or extra_stake_cpu > 0):
            master.delegate_bw(extra_stake_net, extra_stake_cpu, host)
            master.delegate_bw(extra_stake_net, extra_stake_cpu, alice)
            master.delegate_bw(extra_stake_net, extra_stake_cpu, carol)

        cls.stats()

        contract = Contract(host, CONTRACT_WORKSPACE)
        contract.build(force=False)
        contract.deploy(force=False, payer=master)


    def setUp(self):
        pass


    def test_01(self):
        _.COMMENT('''
        Attempting to create a new game.
        This might fail if the previous game has not been closes properly:
        ''')
        set_is_testing_errors(True)
        host.push_action(
            "create",
            {
                "challenger": alice,
                "host": carol
            },
            carol, payer=master)
        set_is_testing_errors(False)

        if host.action.err_msg:
            if "game already exists" in host.action.err_msg:
                _.COMMENT('''
                We need to close the previous game before creating a new one:
                ''')
                host.push_action(
                    "close",
                    {
                        "challenger": alice,
                        "host": carol
                    },
                    carol, payer=master)

                _.COMMENT('''
                Second attempt to create a new game:
                ''')
                host.push_action(
                    "create",
                    {
                        "challenger": alice, 
                        "host": carol
                    },
                    carol, payer=master)
            else:
                _.COMMENT('''
                The error is different than expected.
                ''')
                host.action.ERROR()
                return

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

        _.COMMENT('''
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
            carol, payer=master)

        _.COMMENT('''
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
            alice, payer=master)

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

        _.COMMENT('''
        Restarting the game:
        ''')
        host.push_action(
            "restart",
            {
                "challenger": alice,
                "host": carol,
                "by": carol
            }, 
            carol, payer=master)

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

        _.COMMENT('''
        Closing the game:
        ''')
        host.push_action(
            "close",
            {
                "challenger": alice,
                "host": carol
            },
            carol, payer=master)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        cls.stats()
        if setup.is_local_address:
            stop()


testnet = None
extra_ram = None
extra_stake_net = None
extra_stake_cpu = None

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    This is a unit test for the ``tic-tac-toe`` smart contract.
    It works both on a local testnet and remote testnet.
    The default option is local testnet.
    ''')

    parser.add_argument(
        "-ram", "--ram_kbytes", default=0, help="extra RAM in kbytes")
    parser.add_argument(
        "-net", "--stake_net", default=0, help="extra NET stake in EOS")
    parser.add_argument(
        "-cpu", "--stake_cpu", default=0, help="extra CPU stake in EOS")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset testnet cache")
    parser.add_argument(
        "-c", "--cryptolion", action="store_true",
        help="Using the cryptolion testnet")
    parser.add_argument(
        "-k", "--kylin", action="store_true",
        help="Using the kylin testnet")
    parser.add_argument(
        "-t", "--testnet", nargs=4,
        help="<url> <name> <owner key> <active key>")

    args = parser.parse_args()
    if args.testnet:
        testnet = testnet_data.Testnet(
            args.testnet[0], args.testnet[1], args.testnet[2], args.testnet[3]
        )
    else:
        if args.cryptolion:
            testnet = testnet_data.cryptolion
        else:
            if args.kylin:
                testnet = testnet_data.kylin
            else:
                testnet = testnet_data.LocalTestnet(reset=args.reset)

    testnet.configure(prefix=CACHE_ID)

    if args.reset and not setup.is_local_address:
        remove_testnet_cache()

    extra_ram = int(args.ram_kbytes)
    extra_stake_net = args.stake_net
    extra_stake_cpu = args.stake_cpu

    sys.argv[1:] = [] #needed to prevent passing `argv` to `unittest`.
    unittest.main()
