import unittest
from  eosfactory import *
import testnet_data

Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT]
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"

start_stake_net = "0.2 EOS" 
start_stake_cpu = "0.2 EOS"
game_stake_net = "0.1 EOS" 
game_stake_cpu = "0.1 EOS"
testnet = testnet_data.LocalTestnet(reset=reset) # cryptolion kylin 

class Test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        _.SCENARIO('''
There is the ``grandpa`` account that sponsors the ``tic_tac_toe_machine`` 
account equipped with an instance of the ``tic_tac_toe`` smart contract. There 
are two players ``alice`` and ``carol`` that play games. Test that the moves of 
the games are correctly stored in the blockchain database.
        ''')
        verify_testnet()

        if reset:
            remove_testnet_files()

        create_wallet(file=True)
        testnet.create_master_account("grandpa")
        create_account("alice", grandpa, start_stake_net, start_stake_cpu)  
        create_account("carol", grandpa, start_stake_net, start_stake_cpu)
        create_account(
            "tic_tac_toe_machine", grandpa, start_stake_net, start_stake_cpu)

        grandpa.delegate_bw(carol, game_stake_net, game_stake_cpu)

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
        if setup.is_local_address:
            stop()

import argparse

parser = argparse.ArgumentParser(description='''
Unittest for the ``tic-tac-toe`` smart contract.
''')

parser.add_argument("-r", "--restore", default=False)
parser.add_argument("-n", "--stake_net", default=0.1, help="in EOS")
parser.add_argument("-p", "--stake_cpu", default=0.1, help="in EOS")
parser.add_argument("-c", "--cryptolion", action="store_true")
parser.add_argument("-k", "--kylin", action="store_true")
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
            testnet = testnet_data.LocalTestnet(reset=args.restore)

game_stake_net = "{} EOS".format(args.stake_net)
game_stake_cpu = "{} EOS".format(args.stake_cpu)
configure_testnet(testnet.url, "tic_tac_toe")

unittest.main()
