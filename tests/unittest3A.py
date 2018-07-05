# python3 ./tests/unittest3.py

import unittest
import json
from termcolor import cprint
import setup
import eosf
import node

setup.set_verbose(True)
setup.set_json(False)
setup.use_keosd(False)

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
        global carol

        testnet = node.reset()
        wallet = eosf.Wallet()

        eosio = eosf.AccountMaster()
        wallet.import_key(eosio)

        alice = eosf.account()
        wallet.import_key(alice)

        carol = eosf.account()
        wallet.import_key(carol)

        contract_eosio_bios = eosf.Contract(
                eosio, "eosio.bios").deploy()


    def setUp(self):
        self.assertFalse(testnet.error)
        self.assertFalse(wallet.error)
        self.assertFalse(contract_eosio_bios.error)
        self.assertFalse(alice.error)
        self.assertFalse(carol.error)


    def test_01(self):
        global contract

        cprint("""
Create an account associated with the contract
        """, 'magenta')
        account = eosf.account()
        self.assertFalse(account.error)

        cprint("""
Add the account to the wallet
        """, 'magenta')
        wallet.import_key(account)

        cprint("""
Create a reference to the new contract
        """, 'magenta')
        contract = eosf.ContractFromTemplate(account,
            "_e4b2ffc804529ce9c6fae258197648cc2",
            remove_existing=True)

        cprint("""
Build the contract abi
        """, 'magenta')
        self.assertFalse(contract.build_abi().error)
        
        cprint("""
Build the contract wast
        """, 'magenta')
        self.assertFalse(contract.build_wast().error)

        cprint("""
Deploy the contract
        """, 'magenta')
        self.assertFalse(contract.deploy().error)
    
        cprint("""
Confirm the account contains code
        """, 'magenta')
        self.assertFalse(account.code().error)


    def test_02(self):

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(alice) + '"}', alice)
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(alice) + '"}', alice)
        self.assertFalse(action.error)

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(carol) + '"}', carol)
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(carol) + '"}', carol)
        self.assertFalse(action.error)

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
        contract.delete()
        node.stop()


if __name__ == "__main__":
    unittest.main()