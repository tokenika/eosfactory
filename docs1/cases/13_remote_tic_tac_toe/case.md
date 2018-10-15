
'''
# Tic-tac-toe contract on a remote testnet

This file can be executed as a python script: 'python3 remote_tic_tac_toe.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

Test with a local node are perfectly reproducible and forgivable. It is not so
with remote test nodes because such tests have to -- otherwise they are 
useless as unrealistic -- mimic interaction with a live blockchain where changes are to be paid.

Therefore, remote node tests have to reuse accounts between sessions.

### Imports and set-up definitions

```md
'''
import unittest
from eosfactory.eosf import *
import eosf_testnet
save_code()

verbosity([Verbosity.TRACE, Verbosity.OUT])
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"

start_stake_net = 0.2
start_stake_cpu = 0.2
game_stake_net = 0.1
game_stake_cpu = 0.1

reset = False
testnet = eosf_testnet.LocalTestnet(reset=reset) # cryptolion kylin  
set_nodeos_address(testnet.url, "tic_tac_toe")
'''
```

```md
'''
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
        '''
```
### Stop if the testnet is off

Be sure that the chosen testnet is operative:  
    
```md
        '''
        verify_testnet()
        '''
```
### Test files

The Factory produces three files for each testnet used:

* wallet file (may be more than wallet files),
* wallet password mapping file,
* account mapping file.

The files are marked with a prefix that is set as the second argument in the statement `set_nodeos_address(...)` above.

These files should be edited rather, than being deleted. However if the testnet is set to be `eosf_testnet.LocalTestnet()`, and the local testnet is reset, the contents of them is useles, then remove them:
 
```md
        '''
        if reset:
            remove_testnet_files()
        '''
```

### Exactly one 'Wallet' object in the namespace

It has to be exactly one 'Wallet' object in the namespace. This is controlled automatically.
The password of the created walled is persisted between testnet (not live) sessions. 

### Accounts are reused between test sessions

When the singleton 'Wallet' object is opened or created, it reads the EOSFactory account mapping file (kept in the wallet directory) and attempts to create account objects for all the physical accounts listed there. Therefore, an account object is created only if it does not have its entry in the map. 

### Newly created accounts get RAM according to their needs

If a new account is created, the system precisely determines its need for the RAM, economizing the expenses paid by the creating account:

```md
        '''
        create_master_account("grandpa", testnet)        
        create_account("alice", grandpa, start_stake_net, start_stake_cpu)  
        create_account("carol", grandpa, start_stake_net, start_stake_cpu) 
        create_account(
            "tic_tac_toe_machine", grandpa, start_stake_net, start_stake_cpu)

        # grandpa.buy_ram(20, tic_tac_toe_machine)
        # grandpa.buy_ram(20, alice)
        # grandpa.buy_ram(20, carol)
        '''
```
Grandpa pays for the game:
```md
        '''
        grandpa.delegate_bw(carol, game_stake_net, game_stake_cpu)
        grandpa.delegate_bw(alice, game_stake_net, game_stake_cpu)
        Test.stat()

        contract = Contract(tic_tac_toe_machine, CONTRACT_DIR)
        if not contract.is_built():
            contract.build()
        '''
```
Deployment costs money, therefore the deploying method takes the `payer` argument:
```md
        '''            
        contract.deploy(payer=grandpa)                   
        '''
```

## Case

Given the ``Wallet`` class object in the global namespace and account  master 
object named ``grandpa`` there in the global namespace, given the account 
object named ``tic_tac_toe_machine`` that keeps the ``tic_tac_toe`` contract, and two player accounts: ``alice`` and ``carol`` -- run games.

Gaming involves making the tic_tac_toe_machine to push acctions at the expense of the player that permits the action. The Factory feeds the paying accounts automatically if it is the first one in the permission list.
```md
        '''
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
'''
```
#### Run the unittest

```md
'''
unittest.main()
'''
```
'''

