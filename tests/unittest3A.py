# python3 ./tests/unittest3.py

import setup
import teos
import cleos
import eosf
import unittest
import json
from termcolor import cprint

setup.set_verbose(True)
setup.set_json(False)
cleos.use_keosd(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        global testnet
        global wallet
        global contract_eosio_bios
        global alice
        global bob
        global carol

        testnet = teos.node_reset()

        wallet = eosf.Wallet()

        eosio = cleos.AccountEosio()
        wallet.import_key(eosio)

        contract_eosio_bios = cleos.SetContract(eosio, "eosio.bios")

        alice = eosf.account()
        wallet.import_key(alice)

        bob = eosf.account()
        wallet.import_key(bob)

        carol = eosf.account()
        wallet.import_key(carol)


    def setUp(self):
        self.assertTrue(testnet)
        self.assertTrue(not wallet.error)
        self.assertTrue(not contract_eosio_bios.error)
        self.assertTrue(not alice.error)
        self.assertTrue(not bob.error)
        self.assertTrue(not carol.error)


    def test_01(self):
        global template
        global contract

        contract_dir = "_e4b2ffc804529ce9c6fae258197648cc2"

        cprint("""
Create a new contract workplace
        """, 'magenta')
        template = teos.Template(contract_dir, remove_existing=True)

        cprint("""
Create an account associated with the contract
        """, 'magenta')
        account = eosf.account()
        self.assertTrue(not account.error)

        cprint("""
Add the account to the wallet
        """, 'magenta')
        wallet.import_key(account)

        cprint("""
Create a reference to the new contract
        """, 'magenta')
        contract = eosf.Contract(account, contract_dir)

        cprint("""
Build the contract
        """, 'magenta')
        self.assertTrue(contract.build())

        cprint("""
Deploy the contract
        """, 'magenta')
        self.assertTrue(not contract.deploy().error)
    
        cprint("""
Confirm the account contains code
        """, 'magenta')
        self.assertTrue(not account.code().error)


    def test_02(self):

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(alice) + '"}', alice)
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(alice) + '"}', alice)
        self.assertTrue(not action.error)

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(carol) + '"}', carol)
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(carol) + '"}', carol)
        self.assertTrue(not action.error)

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(carol) + '"}', alice)
WARNING: This action should fail due to authority mismatch!
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(carol) + '"}', alice)
        self.assertTrue(action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        template.delete()
        teos.node_stop()


if __name__ == "__main__":
    unittest.main()