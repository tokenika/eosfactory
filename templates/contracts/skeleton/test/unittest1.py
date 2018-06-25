# python3 ./tests/unittest3.py

import unittest
import json
import setup
import teos
import cleos
import eosf
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

CONTRACT_NAME = "@CONTRACT_NAME@"

cprint("""
Use `cleos.dont_keosd()` instruction, then the wallets used for test are not
managed by the EOSIO keosd and, hence, can be safely manipulated.

If you use `setup.set_verbose(True)`, you can see the response messages of the
issued commands.
""", 'magenta')

cleos.dont_keosd()
setup.set_verbose(True)
setup.set_json(False)


class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)

    
    @classmethod
    def setUpClass(cls):
        pass
        
    def setUp(self):
        pass


    def test_04(self):
        global wallet
        global account_eosio

        cprint("""
Start a local test EOSIO node, use `teos.node_reset()`:
        """, 'magenta')
        ok = teos.node_reset()
        self.assertTrue(ok)

        cprint("""
Create a local wallet object of the class `eosf.Wallet`, 
use `wallet = eosf.Wallet()`:
        """, 'magenta')
        
        wallet = eosf.Wallet()
        self.assertTrue(not wallet.error)

        cprint("""
Implement the `eosio` master account as a `cleos.AccountEosio` object,
use `account_eosio = cleos.AccountEosio()` 
and `wallet.import_key(account_eosio)`:
        """, 'magenta')

        account_eosio = cleos.AccountEosio()
        wallet.import_key(account_eosio)

        cprint("""
Deploy the `eosio.bios` contract:
        """, 'magenta')
        
        contract_eosio_bios = cleos.SetContract( account_eosio, "eosio.bios")
        self.assertTrue(not contract_eosio_bios.error)


    def test_10(self):
        global template
        global account_test
        global contract_test

        contract_dir = CONTRACT_NAME

        cprint("""
Create a new contract workplace, rooted at `contract_dir = CONTRACT_NAME`, and 
populate if with elements of a template workspace,
use `teos.Template(contract_dir)`: 
        """, 'magenta')
        
        template = teos.Template(contract_dir, remove_existing=True)
        print("template path is {}".format(template.contract_path_absolute))

        cprint("""
Create an account for the contract of the workspace. The account is 
represented with an object of the class `eosf.Account`,
use `account_test = eosf.Account()`:
        """, 'magenta')


        account_test = eosf.Account()
        self.assertTrue(not account_test.error)

        cprint("""
Put the account `account_test` to the wallet, 
use `wallet.import_key(account_test)` ...
        """, 'magenta')

        wallet.import_key(account_test)

        cprint("""
... and define an object of the class `eosf.Contract` that represents the
the contract, use `contract_test = eosf.Contract(account_test, contract_dir)`:
        """, 'magenta')

        contract_test = eosf.Contract(account_test, contract_dir)

        cprint("""
Deploy the contract use `contract_test.deploy()`:
        """, 'magenta')

        self.assertTrue(contract_test.deploy())
    
        cprint("""
Confirm that the account `account_test` contains a contract code:
        """, 'magenta')

        code = account_test.code()
        print("code hash: {}".format(code.code_hash))


    def test_15(self):

        cprint("""
Create accounts `alice`and `carol` and put them into the wallet, 
use `alice = eosf.Account()` and `wallet.import_key(alice)`:
        """, 'magenta')

        global alice
        alice = eosf.Account()
        self.assertTrue(not alice.error)
        wallet.import_key(alice)

        global carol
        carol = eosf.Account()
        self.assertTrue(not carol.error)
        wallet.import_key(carol) 

        cprint("""
Inspect an account, use `alice.account()`:
        """, 'magenta')

        alice.account()


    def test_20(self):

        global contract_test
        global alice
        global carol

        cprint("""
Invoke an action of the contract, 
use `contract_test.push_action("hi", '{"user":"' + str(alice) + '"}', alice)`:
        """, 'magenta')

        action_hi = contract_test.push_action(
            "hi", '{"user":"' + str(alice) + '"}', alice)

        self.assertTrue(not action_hi.error)

        action_hi = contract_test.push_action(
            "hi", 
            '{"user":"' + str(carol) + '"}', carol)

        self.assertTrue(not action_hi.error)
        
        cprint("""
This should fail due to authority mismatch:
        """, 'magenta')

        action_hi = contract_test.push_action(
            "hi", 
            '{"user":"' + str(carol) + '"}', alice)
        
        self.assertTrue(action_hi.error)
        

    def test_80(self):
        global template
        self.assertTrue(template.delete())

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        teos.node_stop()


if __name__ == "__main__":
    unittest.main()