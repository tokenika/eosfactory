
import unittest
import argparse
import sys
from  eosfactory import *

class Test(unittest.TestCase):

    def stats():
        eosf_account.stats(
            [grandpa, alice, carol],
            [
                # "ram_usage", 
                # "ram_quota",
                "core_liquid_balance",
                "self_delegated_bandwidth.cpu_weight",
                "total_resources.cpu_weight",
                "cpu_limit.available", 
                "cpu_limit.max",
                "cpu_limit.used",
                "total_resources.ram_bytes"
            ]
            )

    @classmethod
    def setUpClass(cls):
        _.SCENARIO('''
There is the ``grandpa`` account that sponsors the ``tic_tac_toe_machine`` 
account equipped with an instance of the ``tic_tac_toe`` smart contract. There 
are two players ``alice`` and ``carol`` that play games. Test that the moves of 
the games are correctly stored in the blockchain database.
        ''')

        verify_testnet()
        
        create_wallet(file=True)

        create_master_account("grandpa", testnet)        
        create_account("alice", grandpa, start_stake_net, start_stake_cpu)  
        create_account("carol", grandpa, start_stake_net, start_stake_cpu) 
        create_account(
            "tic_tac_toe_machine", grandpa, start_stake_net, start_stake_cpu)

        # grandpa.buy_ram(20, tic_tac_toe_machine)
        # grandpa.buy_ram(20, alice)
        # grandpa.buy_ram(20, carol)

        grandpa.delegate_bw(
           game_stake_net, game_stake_cpu, tic_tac_toe_machine)
        grandpa.delegate_bw(game_stake_net, game_stake_cpu, alice)
        grandpa.delegate_bw(game_stake_net, game_stake_cpu, carol)
        
        Test.stats()

        contract = Contract(tic_tac_toe_machine, CONTRACT_DIR)
        if not contract.is_built():
            contract.build()
           
        contract.deploy(payer=grandpa)                   

    def test_tic_tac_toe(self):

        set_is_testing_errors()       
        tic_tac_toe_machine.push_action(
            "create", 
            {
                "challenger": alice, 
                "host": carol
            },
            carol, payer=grandpa)
        set_is_testing_errors(False)

        if "game already exists" in tic_tac_toe_machine.action.err_msg:
            tic_tac_toe_machine.push_action(
                "close", 
                {
                    "challenger": alice,  
                    "host": carol 
                }, 
                carol, payer=grandpa)
            
            tic_tac_toe_machine.push_action(
                "create", 
                {
                    "challenger": alice, 
                    "host": carol
                },
                carol, payer=grandpa)
        else: 
            tic_tac_toe_machine.action.ERROR()
        
        t = tic_tac_toe_machine.table("games", carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        tic_tac_toe_machine.push_action(
            "move", 
            {
                "challenger": alice, 
                "host": carol, 
                "by": carol,  
                "row":0, "column":0 
            }, 
            carol, payer=grandpa)

        tic_tac_toe_machine.push_action(
            "move", 
            {
                "challenger": alice,  
                "host": carol,  
                "by": alice, 
                "row":1, "column":1 
            }, 
            alice, payer=grandpa)

        t = tic_tac_toe_machine.table("games", carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 1)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 2)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        tic_tac_toe_machine.push_action(
            "restart", 
            {
                "challenger": alice, 
                "host": carol, 
                "by": carol
            }, 
            carol, payer=grandpa)

        t = tic_tac_toe_machine.table("games", carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)
        self.assertEqual(t.json["rows"][0]["board"][1], 0)
        self.assertEqual(t.json["rows"][0]["board"][2], 0)
        self.assertEqual(t.json["rows"][0]["board"][3], 0)
        self.assertEqual(t.json["rows"][0]["board"][4], 0)
        self.assertEqual(t.json["rows"][0]["board"][5], 0)
        self.assertEqual(t.json["rows"][0]["board"][6], 0)
        self.assertEqual(t.json["rows"][0]["board"][7], 0)
        self.assertEqual(t.json["rows"][0]["board"][8], 0)

        tic_tac_toe_machine.push_action(
            "close", 
            {
                "challenger": alice,  
                "host": carol 
            }, 
            carol, payer=grandpa)

    @classmethod
    def tearDownClass(cls):
        Test.stats()
        if setup.is_local_address:
            stop()


Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"

start_stake_net = "0.2 EOS" 
start_stake_cpu = "0.2 EOS"
game_stake_net = None
game_stake_cpu = None
testnet = None

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''
    Unittest for the ``tic-tac-toe`` smart contract.
    Default testnet is the local node.
    ''')

    parser.add_argument(
        "-r", "--reset", action="store_true", 
        help="Reset wallet files.")
    parser.add_argument("-n", "--stake_net", default=0.1, help="in EOS")
    parser.add_argument("-p", "--stake_cpu", default=0.1, help="in EOS")
    parser.add_argument(
        "-c", "--cryptolion", action="store_true", 
        help="Using the cryptolion testnet")
    parser.add_argument(
        "-k", "--kylin", action="store_true", help="Using the kylin testnet")
    parser.add_argument(
        "-t", "--testnet", nargs=4, help="<url> <name> <owner key> <active key>")
        
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

    game_stake_net = "{} EOS".format(args.stake_net)
    game_stake_cpu = "{} EOS".format(args.stake_cpu)
    configure_testnet(testnet.url, "tic_tac_toe")
    # testnet.configure("tic_tac_toe")

    sys.argv[1:] = []
    unittest.main()
