# python3 ./tests/test1.py

import setup
import cleos
import teos
import eosf
import unittest
from termcolor import colored, cprint #sudo python3 -m pip install termcolor
import time

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        setup.set_json(False)        
        setup.set_verbose(True)

    def setUp(self):
        pass


    def test_04(self):

        print(colored("""
Start the local node without the `keosd` Wallet Manager, as the 
`cleos.dont_keosd()` status is set. Also note that the setup status
`setup.set_json(False)` determines descriptive responce of the node,
and 'setup.set_verbose()` determines that this responce is visible.
With `setup.set_verbose(0)`, error messages are printed, only,
with `setup.set_verbose(0)`, nothing is printed.
        """, 'magenta'))

        cleos.dont_keosd()
        node_reset = teos.node_reset()
        self.assertTrue(node_reset)

    def test_05(self):
        setup.set_json(False)

        print(colored("""
Create an account without any wallet available. Should fail:
        """, 'magenta'))

        allice = cleos.AccountLight()
        self.assertTrue(allice.error, "No available wallet")

        print(colored("""
Make a wallet and reattempt the account creation:
        """, 'magenta'))

        global wallet
        wallet = eosf.Wallet()  
        self.assertTrue(not wallet.error)

        print(colored("""
Call for keys in the wallet:
        """, 'magenta'))

        self.assertTrue(not wallet.keys().error)

        print(colored("""
Create the account:
        """, 'magenta'))

        global alice        
        alice = cleos.AccountLight()
        self.assertTrue(not alice.error)

        print(colored("""
Import alice's active key to the wallet. `wallet.import_key(alice)`:
        """, 'magenta'))

        self.assertTrue(not wallet.import_key(alice).error)

        print(colored("""
Call for keys in the wallet:
        """, 'magenta'))

        self.assertTrue(not wallet.keys().error)

        print(colored("""
Introduce two other acconts, `bob` and `carol`:
        """, 'magenta'))

        global bob
        bob = cleos.AccountLight()
        wallet.import_key(bob)

        global carol
        carol = cleos.AccountLight()
        wallet.import_key(carol)        

    def test_15(self):
        global wallet

        print(colored("""
Now, create an account object that will keep a contract:
        """, 'magenta'))

        account_ttt = eosf.Account()
        self.assertTrue(not account_ttt.error)

        print(colored("""
Let the wallet know the account:
        """, 'magenta'))
        self.assertTrue(not wallet.import_key(account_ttt).error)

        print(colored("""
Deploy the contract:
        """, 'magenta'))

        contract_ttt = account_ttt.set_contract("eosio.token")
        self.assertTrue(not contract_ttt.error)

        time.sleep(1)
        
        global alice
        global bob
        global carol

        print(colored("""
account_ttt.push_action('create'
        """, 'magenta')) 

        action_create = account_ttt.push_action(
            "create", 
            '{"issuer":"' 
                + str(cleos.AccountEosio()) 
                + '", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}')

        self.assertTrue(not action_create.error)
        
        print(colored("""
account_ttt.push_action('issue'
        """, 'magenta')) 

        action_issue = account_ttt.push_action(
            "issue", 
            '{"to":"' + str(alice)
                + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
                permission=cleos.AccountEosio())
        

        print(colored("""
account_ttt.push_action('transfer'
        """, 'magenta')) 

        action_transfer = account_ttt.push_action(
            "transfer", 
            '{"from":"' 
                + str(alice)
                + '", "to":"' + str(carol)
                + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
            permission=alice)
        self.assertTrue(not action_transfer.error)

        print(colored("""
Inspect  database entries, for the `alice` account:
        """, 'magenta'))

        table = account_ttt.get_table( "accounts", alice)
        self.assertTrue(not table.error)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        teos.node_stop()

if __name__ == "__main__":
    unittest.main()