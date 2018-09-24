

import unittest
from eosf import *
import eosf_testnet
save_code()

Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT]
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"

start_stake_net = 0.2
start_stake_cpu = 0.2
game_stake_net = 0.1
game_stake_cpu = 0.1

reset = False
testnet = eosf_testnet.LocalTestnet(reset=reset) # cryptolion kylin  
set_nodeos_address(testnet.url, "tic_tac_toe")

class Test(unittest.TestCase):

    def stat():
        eosf_account.stat(
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
        
        verify_testnet()
        
        if reset:
            remove_testnet_files()
        
        create_wallet(file=True)
        
        create_master_account("grandpa", testnet)        
        create_account("alice", grandpa, start_stake_net, start_stake_cpu)  
        create_account("carol", grandpa, start_stake_net, start_stake_cpu) 
        create_account(
            "tic_tac_toe_machine", grandpa, start_stake_net, start_stake_cpu)

        # grandpa.buy_ram(20, tic_tac_toe_machine)
        # grandpa.buy_ram(20, alice)
        # grandpa.buy_ram(20, carol)
        
        grandpa.delegate_bw(carol, game_stake_net, game_stake_cpu)
        grandpa.delegate_bw(alice, game_stake_net, game_stake_cpu)
        Test.stat()

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
        Test.stat()
        if setup.is_local_address:
            stop()

unittest.main()


