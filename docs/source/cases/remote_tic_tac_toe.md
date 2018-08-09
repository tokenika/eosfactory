"""
# Tic-tac-toe contract on a remote testnet

<pre>
This file can be executed as a python script: 'python3 account_master.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre>

## Set-up
```md
Test with a local node are perfectly reproducible and forgivable. It is not so
with remote test nodes because such tests have to -- otherwise they are 
useless -- mimic real uses when blockchain changes are to be paid.

With remote node tests, we assume the following restrictions.

    * Accounts have to be reused between test sessions.
    * Contract deployment occurs only if contract changes.
    * Wallet passwords are not stored in an open file.
```
### Imports and set-up definitions

```md
"""
import os
import unittest
import setup
import eosf
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

ACCOUNT_MASTER = "account_master"
ACCOUNT_TTT = "account_tic_tac_toe"
_ = eosf.Logger()
"""
```
#### Remote node registration data
```md
Experiments with remote nodes depend on definitions, set in relevant 
registration forms. These definitions are stored in the 'user_data.py' script:
```
```md
"""
from user_data import *
"""
```
#### Unittest test class definition begins here
```md
"""
class Test(unittest.TestCase):

    def setUp(self):

        global ACCOUNT_MASTER
        global ACCOUNT_TTT

        eosf.set_throw_error(True)

        eosf.stop([eosf.Verbosity.TRACE])
        eosf.use_keosd(True)
        
        setup.set_nodeos_address(cryptolions)
        eosf.info()
        
        """
```
#### Wallet passwords are not stored in an open file automatically
```md
For tests, we use volatile wallets of improbable names. At the beginning of
a test, its wallet is recreated with a new password.
```
```md
        """
        eosf.kill_keosd()      # Active KEOSD Wallet manager blocks wallet files
        try:
            wallet_file = eosf.wallet_dir() + WALLET_NAME + ".wallet"
            os.remove(wallet_file)
            _.TRACE("The deleted wallet file:\n{}\n".format(wallet_file))
        except Exception as e:
            _.ERROR("Cannot delete the wallet file:\n{}\n".format(str(e))) 

        wallet = Wallet(
            WALLET_NAME, 
            verbosity=[eosf.Verbosity.TRACE])
        """
```
#### Accounts are reused between test sessions
```md
When the singleton 'Wallet' object is created, it reads the EOSFactory account 
mapping file (kept in the wallet directory) and attempts to create account 
objects, in the global namespace, wrapping all the physical accounts listed 
there. Therefore, an account object is to be created only if it does not exist.

We use the registration account as the contract holder. The factory function 
'account_master_create' creates the object, named for the 'ACCOUNT_MASTER' 
constant, in the global namespace. Other arguments of the factory are defined 
in the 'user_data.py' script.

The factory function puts the created account object into the wallet.
```
```md
        """
        ACCOUNT_MASTER = ACCOUNT_TTT

        if not ACCOUNT_MASTER in globals():
            account_master_create(
                ACCOUNT_MASTER, ACCOUNT_NAME, OWNER_KEY, ACTIVE_KEY,
                verbosity=[eosf.Verbosity.TRACE, eosf.Verbosity.OUT])
        else:
            _.TRACE("""
            ######## {} account object restored from the blockchain.
            """.format(ACCOUNT_MASTER))

        global account_master
        account_master = globals()[ACCOUNT_MASTER]
        global account_tic_tac_toe
        account_tic_tac_toe = globals()[ACCOUNT_TTT]
        account_tic_tac_toe.info()

        contract_tic_tac_toe = Contract(
            account_tic_tac_toe, "tic_tac_toe_jungle")        
        contract_tic_tac_toe.build()
        if not account_tic_tac_toe.is_code():            
            contract_tic_tac_toe.deploy()
        else:
            _.TRACE("""
            * Contract cannot be deployed as the account already has a code.
                The current test is protected against overwriting the code.
            """)
        """
```
#### The 'insufficient ram` error
```md
As the remote node takes quasi-money (but we test the real-money case), you can
expect a message like this one:
```
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
        """
        if not "account_alice" in globals():
            account_create("account_alice", account_master)
        else:
            _.TRACE("""
            ######## {} account object restored from the blockchain.
            """.format("account_alice"))
        if not "account_carol" in globals():    
            account_create("account_carol", account_master)
        else:
            _.TRACE("""
            ######## {} account object restored from the blockchain.
            """.format("account_carol"))

        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()            
        exit()
    def test_tic_tac_toe(self):
        """
```
## Case
```md
Given a ``Wallet`` class object in the global namespace; an account  master 
object named ``account_master`` in the global namespace; given an account 
object named ``account_tic_tac_toe`` account that keeps the ``tic_tac_toe`` 
contract; and given two player accounts: ``account_alice`` and ``account_carol`` 
-- run games.
```
```md
        """
        account_tic_tac_toe.push_action(
            "create", 
            '{"challenger":"' + str(account_alice) 
                +'", "host":"' + str(account_carol) + '"}',
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
            '{"challenger":"' + str(account_alice) 
                + '", "host":"' + str(account_carol) 
                + '", "by":"' + str(account_carol) 
                + '", "row":0, "column":0 }', 
            account_carol)

        account_tic_tac_toe.push_action(
            "move", 
            '{"challenger":"' + str(account_alice) 
                + '", "host":"' + str(account_carol) 
                + '", "by":"' + str(account_alice) 
                + '", "row":1, "column":1 }', 
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
                '{"challenger":"' + str(account_alice) 
                    + '", "host":"' + str(account_carol) 
                    + '", "by":"' + str(account_carol) + '"}', 
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
                '{"challenger":"' + str(account_alice) 
                    + '", "host":"' + str(account_carol) + '"}', 
                account_carol)

    def tearDown(self):
        eosf.stop()
"""
```
#### Run the unittest
```md
"""
unittest.main()
"""
```
"""

