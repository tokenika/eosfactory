'''
# Tic-tac-toe contract on a remote testnet

This file can be executed as a python script: 'python3 account_master.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

Test with a local node are perfectly reproducible and forgivable. It is not so
with remote test nodes because such tests have to -- otherwise they are 
useless -- mimic real uses when blockchain changes are to be paid.

With remote node tests, we assume the following restrictions.

* Accounts have to be reused between test sessions.
* Contract deployment occurs only if contract changes.
* Wallet passwords are not stored in a plain file.

### Imports and set-up definitions

```md
'''
from  eosfactory import *
verbosity = [Verbosity.INFO, Verbosity.OUT]
CONTRACT_DIR = "03_tic_tac_toe"

set_nodeos_address("88.99.97.30:38888")
WALLET_NAME = setup.wallet_default_name

ACCOUNT_MASTER = "account_master"
ACCOUNT_TTT = "account_tic_tac_toe"

import testnet_data
testnode = testnet_data.cryptolion
set_nodeos_address(testnode.url, "tic_tac_toe")
Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()
'''
```


```md
'''
class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
```
### Stop if the testnode is off

Be sure that the chosen testnode is operative:  
    
```md
        '''
        if not eosf.is_running():
            _.ERROR('''
            This test needs the testnode {} running, but it does not answer.
            '''.format(testnode.url))
        '''
```
### Remove results of a possible previous use of the current script.

Make sure that the chosen testnode is operative:    
```md
        '''
        remove_files()
        '''
```

#### Accounts are reused between test sessions

When the singleton 'Wallet' object is created, it reads the EOSFactory account 
mapping file (kept in the wallet directory) and attempts to create account 
objects, in the global namespace, wrapping all the physical accounts listed 
there. Therefore, an account object is to be created only if it does not exist.

We use the registration account as the contract holder. The factory function 
'account_master_create' creates the object, named for the 'ACCOUNT_MASTER' 
constant, in the global namespace. Other arguments of the factory are defined 
in the 'user_data.py' script.

The factory function puts the created account object into the wallet.

```md
        '''
        ACCOUNT_MASTER = ACCOUNT_TTT
        if not ACCOUNT_MASTER in globals():
            account_master_create(
                ACCOUNT_MASTER, ACCOUNT_NAME, OWNER_KEY, ACTIVE_KEY,
                verbosity=[Verbosity.INFO, Verbosity.OUT])
        else:
            _.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format(ACCOUNT_MASTER))
        
        
        global account_master
        account_master = globals()[ACCOUNT_MASTER]
        global account_tic_tac_toe
        account_tic_tac_toe = globals()[ACCOUNT_TTT]
        account_tic_tac_toe.info()

        contract_tic_tac_toe = Contract(
            account_tic_tac_toe, CONTRACT_DIR)        
        contract_tic_tac_toe.build()
        if not account_tic_tac_toe.is_code():            
            contract_tic_tac_toe.deploy()
        else:
            _.INFO('''
            * Contract cannot be deployed as the account already has a code.
                The current test is protected against overwriting the code.
            ''')
        '''
```
#### The 'insufficient ram` error

As the remote node takes quasi-money (but we test the real-money case), you can
expect a message like this one:

```md
ERROR:
Reading WAST/WASM from eosfactory/contracts/tic_tac_toe_jungle/build/tic_tac_toe.wast...
Assembling WASM...
Publishing contract...
Error 3080001: Account using more than allotted RAM usage
Error Details:
account dgxo1uyhoytn has insufficient ram; needs 138233 bytes has 64789 bytes
```
```md
        '''
        if not "account_alice" in globals():
            account_create("account_alice", account_master)
        else:
            _.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format("account_alice"))
        if not "account_carol" in globals():    
            account_create("account_carol", account_master)
        else:
            _.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format("account_carol"))


        set_is_testing_errors()            
        exit()
    def test_tic_tac_toe(self):
        '''
```
## Case

Given a ``Wallet`` class object in the global namespace; an account  master 
object named ``account_master`` in the global namespace; given an account 
object named ``account_tic_tac_toe`` account that keeps the ``tic_tac_toe`` 
contract; and given two player accounts: ``account_alice`` and ``account_carol`` 
-- run games.

```md
        '''
        account_tic_tac_toe.push_action(
            "create", 
            {
                "challenger": account_alice, 
                "host": account_carol
            },
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
            {
                "challenger": account_alice, 
                "host": account_carol, 
                "by": account_carol,  
                "row":0, "column":0 
            }, 
            account_carol)

        account_tic_tac_toe.push_action(
            "move", 
            {
                "challenger": account_alice,  
                "host": account_carol,  
                "by": account_alice, 
                "row":1, "column":1 
            }, 
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
                {
                    "challenger": account_alice, 
                    "host": account_carol, 
                    "by": account_carol
                }, 
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
                {
                    "challenger": account_alice,  
                    "host": account_carol 
                }, 
                account_carol)

    def tearDown(self):
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

