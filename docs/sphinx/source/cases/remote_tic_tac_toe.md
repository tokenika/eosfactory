'''
# Tic-tac-toe contract on a remote testnet

This file can be executed as a python script: 'python3 remote_tic_tac_toe.md'.

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
import unittest
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"

import testnet_data
testnode = testnet_data.LocalTestnet()
set_nodeos_address(testnode.url, "tic_tac_toe")

#ACCOUNT_TTT = "croupier"
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
        if not node_is_operative():
            _.ERROR('''
            This test needs the testnode {} running, but it does not answer.
            '''.format(testnode.url))
        '''
```
### Remove results of a possible previous use of the current script

Make sure that the chosen testnode is operative:    
```md
        '''
        remove_files()
        '''
```

### Exactly one 'Wallet' object in the namespace

It has to be exactly one 'Wallet' object in the namespace. 
```md
        '''
        create_wallet()
        '''
```

#### Accounts are reused between test sessions

When the singleton 'Wallet' object is created, it reads the EOSFactory account 
mapping file (kept in the wallet directory) and attempts to create account 
objects, in the global namespace, wrapping all the physical accounts listed 
there. Therefore, an account object is to be created only if it does not exist.

```md
        '''
        if not "account_master" in globals():
            create_master_account(
                "account_master",
                testnode.account_name, 
                testnode.owner_key, 
                testnode.active_key)

        if not "croupier" in globals():
            create_account("croupier", account_master)
        else:
            _.INFO('''
            * The account {} restored from the wallet.
            '''.format("croupier"))

        if not "alice" in globals():
            create_account("alice", account_master)
        else:
            _.INFO('''
            * The account {} restored from the wallet.
            '''.format("alice"))

        if not "carol" in globals():
            create_account("carol", account_master)
        else:
            _.INFO('''
            * The account {} restored from the wallet.
            '''.format("carol"))
            
        if not croupier.is_code():
            contract = Contract(
                croupier, CONTRACT_DIR)

            if not contract.is_built():
                contract.build()
            contract.deploy()  
        else:
            _.INFO('''
            * The account {} has code.
            '''.format("croupier"))            

        exit()
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
    def test_tic_tac_toe(self):
        '''
```
## Case

Given a ``Wallet`` class object in the global namespace, an account  master 
object named ``account_master`` in the global namespace, given an account 
object named ``croupier`` account that keeps the ``tic_tac_toe`` 
contract, and two player accounts: ``alice`` and ``carol`` 
-- run games.

```md
        '''
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
                "row":0, "column":0 
            }, 
            carol)

        croupier.push_action(
            "move", 
            {
                "challenger": alice,  
                "host": carol,  
                "by": alice, 
                "row":1, "column":1 
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

    @classmethod
    def tearDownClass(cls):
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

