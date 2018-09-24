"""
# Unittesting the [School Lottery](https://github.com/cipherzzz/school_lottery)

This file can be executed as a python script: 
'python3 README_EOSFactory_test.md'.

Note, the script relies on its file's position relative to the 'src` directory, 
where is the code of the School Lottery. 

Here we explain methods of the Tokenika EOSFactory, applicable to the 
development and testing of EOS smart contracts. As the working example, we 
use the <a href="https://github.com/cipherzzz/school_lottery">School Lottery</a>, developed by CipherZ who kindly <a href="https://medium.com/coinmonks/your-first-eos-dapp-using-eosfactory-aa0394df95d9">reviewed</a> the EOSFactory 
in version 1.1.

Now we are close to the publication of the version 2.0 that is already <a href="https://github.com/tokenika/eosfactory">available</a> 
(branch 'dev') in its development form.

<a href="https://rawgit.com/tokenika/eosfactory/dev/docs/build/html/index.html">Here</a> you can find lot of information on this new EOSFactory.

In the current article, we explain a unittest.

## Setup

```md
"""
import sys
import unittest
import setup
import eosf
import time

from eosf import Verbosity
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract
"""
```
### Test conditions

Verbosity options:

* `Verbosity.TRACE` -- only headdings are printed, while with
* `Verbosity.EOSF` -- prints details;
* `Verbosity.OUT` -- prints the output from the blockchain;
* `Verbosity.DEBUG` -- prints debug info and console output from the 
    blockchain.

KEOSD options:

* False -- use the NODEOS Wallet Manager;
* True -- use the KEOSD Wallet Manager.

```md
"""
eosf.Logger.verbosity = [Verbosity.EOSF, Verbosity.OUT, Verbosity.DEBUG]
_ = eosf.Logger()
eosf.use_keosd(False)

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print("""

NEXT TEST ====================================================================
""")

    @classmethod
    def setUpClass(cls):
        """
```
### Starting test setup

Setup statements:

* `restart()` -- reset all the settings to the start conditions;
* `set_is_testing_errors(...)` -- if True, error messages are less alarming;
* `set_throw_error(...)` if True, exceptions are thrown rather than error 
    messages are printed. For setting a test up, chose throwing.

```md
        """
        eosf.restart()
        eosf.set_throw_error(True)
        eosf.set_is_testing_errors(False)
        """
```
### Starting the local node wallet and actor accounts

* `reset(...)` -- clean start the local node from its genesis conditions;
    other possibility is run(...), that is start the node being stopped 
    before;
* `wallet = Wallet()` -- start a singleton object that wraps a physical 
    wallet;
* `account_create(<account object name>, <account creating object>)` --
    create the object named <account object name> that wraps a physical 
    account of a random name; account objects are preserved between 
    sessions, if the local node is not reset; account objects are 
    automatically placed in the wallet.
* `account_master_create(<account object name>)` -- creates the object named 
    <account object name> having the power of the account creator.

```md
        """
        eosf.reset([eosf.Verbosity.TRACE]) 
        wallet = Wallet()
        account_master_create("account_master")

        account_create("account_admin", account_master)
        account_create("account_parent", account_master)
        account_create("account_lottery", account_master)

        contract = Contract(account_lottery, sys.path[0])
        contract.build()
        deploy = contract.deploy()
        time.sleep(1)
        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()

    def testGrade(self):
        """
```
## Test case

### Automatic translation

The EOSIO accounts are indexed by their names, therefore the names have to be 
unique in the blockchain, and to have the specific format. Then it is not 
possible to grasp any intuitive association between the account name and its 
role specified in the Ricardian Contract. 

For example, if there is in the Contract a notion of an account keeping a
‘school fund 2018’, we can try the name `school.fund1`. It is not only far to
a satisfactory name, but it can be taken already.

A natural solution to the problem is to have aliasses to the physical names.
Perhaps, the structure of the native EOSIO account should have a field and
method for this, it is not so now, therefore the EOSFactory uses its own 
system of the named account objects.

For example, the data for a contract action can be stated as in the script code
below. The names involved there are translated to the physical names before 
being sent to the blockchain, and decoded beck when they return in an answer 
from the blockchain.

```md
        """
        account_lottery.push_action(
            "addschool",
            # {
            #     "account": account_admin,
            #     "name": "Eastover"
            # },
            [account_admin, "Eastover"],
            account_admin)

        _.SCENARIO("""
        Having a school, add Grade as Admin.
        Expectation: Succeed and Data exists.
        """)

        account_lottery.push_action(
            "addgrade",
            {
                "account": account_admin,
                "schoolfk": "0",
                "grade_num": "1",
                "openings": "25"
            },
            account_admin)

        t = account_lottery.table("grade", account_lottery)
        self.assertEqual(t.json["rows"][0]["grade_num"], 1)
        self.assertEqual(t.json["rows"][0]["openings"], 25)

        _.SCENARIO("""
        Remove Grade as Parent.
        Expectation: Fail since only owner can remove.
        """)

        account_lottery.push_action(
            "remgrade", 
            {
                "account": account_parent,
                "key": "0"
            },
            account_parent)
        self.assertTrue(account_lottery.action.error)

        _.COMMENT("""
        Also, the 'grade' table should not be altered:
        """)

        t = account_lottery.table("grade", account_lottery)
        self.assertEqual(t.json["rows"][0]["grade_num"], 1)
        self.assertEqual(t.json["rows"][0]["openings"], 25)        

        _.SCENARIO("""
        Add same Grade.
        Expectation: Fail since grade must be unique.
        """)

        account_lottery.push_action(
            "addgrade", 
            # {
            #     "account": account_admin,
            #     "schoolfk": "0",
            #     "grade_num": "1",
            #     "openings": "35"                
            # }, 
            [account_admin, "0", "1", "35"],
            account_admin)
        self.assertTrue(account_lottery.action.error)

        _.COMMENT("""
        Also, the 'grade' table should not be altered:
        """)

        t = account_lottery.table("grade", account_lottery)
        self.assertEqual(t.json["rows"][0]["grade_num"], 1)
        self.assertEqual(t.json["rows"][0]["openings"], 25)
     
        _.SCENARIO("""
        Remove Grade as Admin.
        Expectation: Succeed and record removed.
        """)

        account_lottery.push_action(
            "remgrade", 
            {
                "account": account_admin,
                "key": "0"
            }, 
            account_admin)

        self.assertFalse(account_lottery.action.error)

        t = account_lottery.table("grade", account_lottery)
        self.assertEqual(t.json["rows"], [])

    @classmethod
    def tearDownClass(cls):
        eosf.stop()

unittest.main()
"""
```
## Unittest screen dumps

### Setup phase

The setup is verbose. You can see a detailed record of what happens.

<img src="resources/images/test_setup.png" width="720px"/>

### Test phase

<img src="resources/images/test_run.png" width="720px"/>
"""