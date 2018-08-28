'''
# Tic-tac-toe contract on a remote testnet

This file can be executed as a python script: 'python3 remote_tic_tac_toe.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

Test with a local node are perfectly reproducible and forgivable. It is not so
with remote test nodes because such tests have to -- otherwise they are 
useless -- mimic real cases when blockchain changes are to be paid.

With remote node tests, we assume two restrictions:

* Accounts have to be reused between test sessions.
* Contract deployment occurs only if contract changes.

### Imports and set-up definitions

```md
'''
import unittest
from  eosfactory import *
import testnet_data

Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT]
_ = Logger()
CONTRACT_DIR = "03_tic_tac_toe"
stake_net = "0.2 EOS" 
stake_cpu = "0.2 EOS"
testnode = testnet_data.cryptolion #  LocalTestnet() kylin
configure_testnet(testnode.url, "tic_tac_toe")
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
            The testnode does not answer.
            Is Internet connected?
            Is the testnode operative?
            '''.format(testnode.url))
        '''
```
### Test files

The Factory produces three files for each testnet used:

* wallet file (may be more than wallet files),
* wallet password mapping file,
* account mapping file.

The files are marked with a prefix that is set as the second argument in the statement `configure_testnet(...)` above.

These files should be edited rather, than being deleted. However if the testnode is set to be `testnet_data.LocalTestnet()`, and the local testnet is reset, the contents of them is useles, then remove them:
 
```md
        '''
        #remove_files()
        '''
```

### Exactly one 'Wallet' object in the namespace

It has to be exactly one 'Wallet' object in the namespace. 
```md
        '''
        create_wallet(file=True)
        '''
```
The parameter `file=True` causes that the password of the created walled is persisted between sessions.

### Accounts are reused between test sessions

When the singleton 'Wallet' object is opened or created, it reads the EOSFactory account mapping file (kept in the wallet directory) and attempts to create account objects for all the physical accounts listed there. Therefore, an account object is created only if it does not have its entry in the map. 

### Newly created accounts get RAM according to their needs

If a new account is created, the system precisely determines its need for the RAM, economizing the expenses. 

```md
        '''
        if not "account_master" in globals():
            testnode.create_master_account("account_master")

        if not "croupier" in globals():
            create_account(
                "croupier", account_master, stake_net, stake_cpu)
        else:
            _.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format("croupier"))

        if not "alice" in globals():
            create_account(
                "alice", account_master, stake_net, stake_cpu)  
        else:
            _.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format("alice"))

        if not "carol" in globals():
            create_account(
                "carol", account_master, stake_net, stake_cpu)
        else:
            _.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format("carol"))        
        
        contract = Contract(croupier, CONTRACT_DIR)
        if not contract.is_built():
            contract.build()
        contract.deploy(payer=account_master)                   
        '''
```

## Case

Given the ``Wallet`` class object in the global namespace and account  master 
object named ``account_master`` in the global namespace, given the account 
object named ``croupier`` that keeps the ``tic_tac_toe`` contract and two player accounts: ``alice`` and ``carol`` -- run games.

Gambling involves making the croupier to push acctions at the expense of the player that permits the action. The Factory feeds the paying accounts automatically if it is the first one in the permission list.
```md
        '''
    def test_tic_tac_toe(self):
        set_is_testing_errors()       
        croupier.push_action(
            "create", 
            {
                "challenger": alice, 
                "host": carol
            },
            carol, payer=account_master)
        set_is_testing_errors(False)
        import pdb; pdb.set_trace()
        if "game already exists" in croupier.action.err_msg:
            croupier.push_action(
                "close", 
                {
                    "challenger": alice,  
                    "host": carol 
                }, 
                carol, payer=account_master)
            set_is_testing_errors()
            
            croupier.push_action(
                "create", 
                {
                    "challenger": alice, 
                    "host": carol
                },
                carol, payer=account_master)
        
        t = croupier.table("games", carol)

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
            carol, payer=account_master)

        croupier.push_action(
            "move", 
            {
                "challenger": alice,  
                "host": carol,  
                "by": alice, 
                "row":1, "column":1 
            }, 
            alice, payer=account_master)

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
            carol, payer=account_master)

        t = croupier.table("games", carol)

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
            carol, payer=account_master)

    @classmethod
    def tearDownClass(cls):
        if is_local_address:
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

