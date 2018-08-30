
import unittest
import argparse
import sys
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"

extra_ram = 20
initial_stake_net = "1.0 EOS"
initial_stake_cpu = "1.0 EOS"


class Test(unittest.TestCase):

    def stats():
        eosf_account.stats(
            [master, host, alice, carol],
            [
                "core_liquid_balance",
                "ram_usage",
                "ram_quota",
                "total_resources.ram_bytes",
                "self_delegated_bandwidth.cpu_weight",
                "total_resources.cpu_weight",
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

        testnet.create_master_account("master")
        create_account("alice", master, initial_stake_net, initial_stake_cpu)
        create_account("carol", master, initial_stake_net, initial_stake_cpu)
        create_account("host", master, initial_stake_net, initial_stake_cpu)

        # master.buy_ram(extra_ram, host)
        # master.buy_ram(extra_ram, alice)
        # master.buy_ram(extra_ram, carol)

        # master.delegate_bw(extra_stake_net, extra_stake_cpu, host)
        # master.delegate_bw(extra_stake_net, extra_stake_cpu, alice)
        # master.delegate_bw(extra_stake_net, extra_stake_cpu, carol)

        cls.stats()

        contract = Contract(host, CONTRACT_DIR)
        if not contract.is_built():
            contract.build()

        contract.deploy(payer=master)


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


extra_stake_net = None
extra_stake_cpu = None
testnet = None

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    Unit test for the ``tic-tac-toe`` smart contract.
    It works both on a local private testnet and remote public testnet.
    The default option is a local private testnet.
    ''')

    parser.add_argument("-net", "--stake_net", default=10.0, help="net stake in EOS")
    parser.add_argument("-cpu", "--stake_cpu", default=10.0, help="cpu stake in EOS")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset the local testnet")
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
                if args.reset:
                    remove_testnet_files()

    extra_stake_net = "{} EOS".format(args.stake_net)
    extra_stake_cpu = "{} EOS".format(args.stake_cpu)
    configure_testnet(testnet.url, "tic_tac_toe")

    sys.argv[1:] = []
    unittest.main()
