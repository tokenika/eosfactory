# python3 ./tests/unittest3.py

import setup
import eosf
import node
import unittest
from termcolor import cprint

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
        testnet = node.reset()
        assert(not testnet.error)

        wallet = eosf.Wallet()
        assert(not wallet.error)

        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)
        assert(not account_master.error)

        global account_deploy
        account_deploy = eosf.account(account_master)
        wallet.import_key(account_deploy)
        assert(not account_deploy.error)

        global account_alice
        account_alice = eosf.account(account_master)
        wallet.import_key(account_alice)
        assert(not account_alice.error)

        global account_carol
        account_carol = eosf.account(account_master)
        wallet.import_key(account_carol)
        assert(not account_carol.error)

        contract_eosio_bios = eosf.Contract(
            account_master, "eosio.bios").deploy()
        assert(not contract_eosio_bios.error)


    def setUp(self):
        pass


    def test_01(self):
        global contract
        cprint("""
Create a reference to the new contract
        """, 'magenta')
        contract = eosf.ContractBuilderFromTemplate(account_deploy,
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
Confirm `account_deploy` contains code
        """, 'magenta')
        self.assertFalse(account_deploy.code().error)


    def test_02(self):

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(account_alice) + '"}', account_alice)
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(account_alice) + '"}', account_alice)
        self.assertFalse(action.error)

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(account_carol) + '"}', account_carol)
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(account_carol) + '"}', account_carol)
        self.assertFalse(action.error)

        cprint("""
Action contract.push_action("hi", '{"user":"' + str(account_carol) + '"}', account_alice)
WARNING: This action should fail due to authority mismatch!
        """, 'magenta')
        action = contract.push_action(
            "hi", '{"user":"' + str(account_carol) + '"}', account_alice)
        self.assertTrue(action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        contract.delete()
        node.stop()


if __name__ == "__main__":
    unittest.main()