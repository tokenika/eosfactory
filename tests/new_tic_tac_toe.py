'''Example of a functional test with non-global refference to account objects. 

We believe that EOSFactory tests are clearer if their account objects exist in 
the global namespace of the test module, if they can be referred to without 
namespace qualificators. 

There are practitioners of Python who preffer to restrain from using global 
variables. EOSFactory has tools that can satisfy them. This example presents 
these tools. 

For explanation see http://eosfactory.io/build/html/comments/account.html,
there the section 'Account objects reside in the global namespace'.

With the standard EOSFactory, account objects are created with `create` factory 
functions, for example
    `create_account("foo", owner_account)`
where `"foo"` is the given name of the account object to be created, and `owner_account` represent the account owner. This factory function create account objects, and place them in the global namespace of the module.

Now, another way is available: account objects can be assigned from `new` 
factory functions, for example
    `foo = new_account(owner_account)`
where `foo` is to be the new account object variable (global or local), and `owner_account` is the accout owner. This factory function creates an account object with its object name set to the name of the left side of the assignment ("foo").

The current script can be compared with `tests/tic_tac_toe.py` which is 
functionally identical, yet written with the standard EOSFactory style.
'''
import unittest, argparse, sys, time
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])

CONTRACT_WORKSPACE = "tic_tac_toe"

# Costs of the test:
INITIAL_RAM_KBYTES = 8
INITIAL_STAKE_NET = 3
INITIAL_STAKE_CPU = 3

class Test(unittest.TestCase):
    '''Unittest class definition.
    '''
    @classmethod
    def stats(cls):
        '''Prints statistics of the accounts involved in the test.
        '''
        print_stats(
            [cls.master, cls.host, cls.alice, cls.carol],
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
        There is the ``master`` account that sponsors the ``host`` account equipped with an instance of the ``tic_tac_toe`` smart contract. There 
        are two players ``alice`` and ``carol``. We are testing that the moves of the game are correctly stored in the blockchain database.
        ''')

        testnet.verify_production()
        cls.master = new_master_account(testnet)
        cls.host = new_account(
            cls.master, buy_ram_kbytes=INITIAL_RAM_KBYTES, 
            stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        cls.alice = new_account(
            cls.master, buy_ram_kbytes=INITIAL_RAM_KBYTES, 
            stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)
        cls.carol = new_account(
            cls.master, buy_ram_kbytes=INITIAL_RAM_KBYTES, 
            stake_net=INITIAL_STAKE_NET, stake_cpu=INITIAL_STAKE_CPU)

        if not testnet.is_local():
            cls.stats()
            if (extra_ram > 0):
                cls.master.buy_ram(extra_ram, cls.host)
                cls.master.buy_ram(extra_ram, cls.alice)
                cls.master.buy_ram(extra_ram, cls.carol)
            if (extra_stake_net > 0 or extra_stake_cpu > 0):
                cls.master.delegate_bw(
                    extra_stake_net, extra_stake_cpu, cls.host)
                cls.master.delegate_bw(
                    extra_stake_net, extra_stake_cpu, cls.alice)
                cls.master.delegate_bw(
                    extra_stake_net, extra_stake_cpu, cls.carol)
            if (extra_ram > 0 or extra_stake_net > 0 or extra_stake_cpu > 0):
                cls.stats()

        smart = Contract(cls.host, CONTRACT_WORKSPACE)
        smart.build(force=False)

        try:
            smart.deploy(payer=cls.master)
        except errors.ContractRunningError:
            pass

    def test_functionality(self):
        '''Testing script.
        '''
        COMMENT('''
        Attempting to create a new game.
        This might fail if the previous game has not been closes properly:
        ''')
        try:
            Test.host.push_action(
                "create",
                {
                    "challenger": Test.alice,
                    "host": Test.carol
                },
                permission=(Test.carol, Permission.ACTIVE))
        except Error as e:
            if "game already exists" in e.message:
                COMMENT('''
                We need to close the previous game before creating a new one:
                ''')
                Test.host.push_action(
                    "close",
                    {
                        "challenger": Test.alice,
                        "host": Test.carol
                    },
                    permission=(Test.carol, Permission.ACTIVE))

                time.sleep(3)

                COMMENT('''
                Second attempt to create a new game:
                ''')
                Test.host.push_action(
                    "create",
                    {
                        "challenger": Test.alice, 
                        "host": Test.carol
                    },
                    permission=(Test.carol, Permission.ACTIVE))
            else:
                COMMENT('''
                The error is different than expected.
                ''')
                raise Error(str(e))

        table = Test.host.table("games", Test.carol)
        self.assertEqual(table.json["rows"][0]["board"][0], 0)
        self.assertEqual(table.json["rows"][0]["board"][1], 0)
        self.assertEqual(table.json["rows"][0]["board"][2], 0)
        self.assertEqual(table.json["rows"][0]["board"][3], 0)
        self.assertEqual(table.json["rows"][0]["board"][4], 0)
        self.assertEqual(table.json["rows"][0]["board"][5], 0)
        self.assertEqual(table.json["rows"][0]["board"][6], 0)
        self.assertEqual(table.json["rows"][0]["board"][7], 0)
        self.assertEqual(table.json["rows"][0]["board"][8], 0)

        COMMENT('''
        First move is by carol:
        ''')
        Test.host.push_action(
            "move",
            {
                "challenger": Test.alice,
                "host": Test.carol,
                "by": Test.carol,
                "row":0, "column":0
            },
            permission=(Test.carol, Permission.ACTIVE))

        COMMENT('''
        Second move is by alice:
        ''')
        Test.host.push_action(
            "move",
            {
                "challenger": Test.alice,
                "host": Test.carol,
                "by": Test.alice,
                "row":1, "column":1
            },
            permission=(Test.alice, Permission.ACTIVE))

        table = Test.host.table("games", Test.carol, show_payer=True)
        self.assertEqual(table.json["rows"][0]["data"]["board"][0], 1)
        self.assertEqual(table.json["rows"][0]["data"]["board"][1], 0)
        self.assertEqual(table.json["rows"][0]["data"]["board"][2], 0)
        self.assertEqual(table.json["rows"][0]["data"]["board"][3], 0)
        self.assertEqual(table.json["rows"][0]["data"]["board"][4], 2)
        self.assertEqual(table.json["rows"][0]["data"]["board"][5], 0)
        self.assertEqual(table.json["rows"][0]["data"]["board"][6], 0)
        self.assertEqual(table.json["rows"][0]["data"]["board"][7], 0)
        self.assertEqual(table.json["rows"][0]["data"]["board"][8], 0)

        COMMENT('''
        Restarting the game:
        ''')
        Test.host.push_action(
            "restart",
            {
                "challenger": Test.alice,
                "host": Test.carol,
                "by": Test.carol
            }, 
            permission=(Test.carol, Permission.ACTIVE))

        table = Test.host.table("games", Test.carol)
        self.assertEqual(table.json["rows"][0]["board"][0], 0)
        self.assertEqual(table.json["rows"][0]["board"][1], 0)
        self.assertEqual(table.json["rows"][0]["board"][2], 0)
        self.assertEqual(table.json["rows"][0]["board"][3], 0)
        self.assertEqual(table.json["rows"][0]["board"][4], 0)
        self.assertEqual(table.json["rows"][0]["board"][5], 0)
        self.assertEqual(table.json["rows"][0]["board"][6], 0)
        self.assertEqual(table.json["rows"][0]["board"][7], 0)
        self.assertEqual(table.json["rows"][0]["board"][8], 0)

        COMMENT('''
        Closing the game:
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            Test.host.push_action(
                "close",
                {
                    "challenger": Test.alice,
                    "host": Test.carol
                },
                permission=(Test.alice, Permission.ACTIVE))

        COMMENT('''
        Closing the game:
        ''')
        Test.host.push_action(
            "close",
            {
                "challenger": Test.alice,
                "host": Test.carol
            },
            permission=(Test.carol, Permission.ACTIVE))

    @classmethod
    def tearDownClass(cls):
        if testnet.is_local():
            stop()
        else:
            cls.stats()


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
        "-table", "--testnet", nargs=4,
        help="<url> <name> <owner key> <active key>")

    parser.add_argument(
        "-r", "--reset", action="store_true",
        help="Reset testnet cache")

    parser.add_argument(
        "--ram", default=0, help="extra RAM in kbytes")
    parser.add_argument(
        "--net", default=0, help="extra NET stake in EOS")
    parser.add_argument(
        "--cpu", default=0, help="extra CPU stake in EOS")

    args = parser.parse_args()
    testnet = get_testnet(args.alias, args.testnet, reset=args.reset)
    testnet.configure()

    if args.reset and not testnet.is_local():
        testnet.clear_cache()

    extra_ram = int(args.ram)
    extra_stake_net = int(args.net)
    extra_stake_cpu = int(args.cpu)

    unittest.main(argv=[sys.argv[0]])
