import sys
import setup
import eosf
import node
import unittest
from termcolor import cprint

setup.set_verbose(True)
setup.use_keosd(False)
setup.set_json(False)

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

        global account_alice
        account_alice = eosf.account(account_master)
        wallet.import_key(account_alice)
        assert(not account_alice.error)

        global account_carol
        account_carol = eosf.account(account_master)
        wallet.import_key(account_carol)
        assert(not account_carol.error)

        account_deploy = eosf.account(account_master)
        wallet.import_key(account_deploy)
        assert(not account_deploy.error)

        contract_eosio_bios = eosf.Contract(
            account_master, "eosio.bios").deploy()
        assert(not contract_eosio_bios.error)

        global contract
        contract = eosf.Contract(account_deploy, sys.path[0] + "/../")
        assert(not contract.error)

        deployment = contract.deploy()
        assert(not deployment.error)


    def setUp(self):
        pass


    def test_01(self):

        cprint(
            """contract.push_action("hi", '{"user":"' + str(account_alice) + '"}', account_alice)""", 'magenta')
        self.assertFalse(contract.push_action(
            "hi", '{"user":"' + str(account_alice) + '"}', account_alice).error)

        cprint(
            """contract.push_action("hi", '{"user":"' + str(account_carol) + '"}', account_carol)""", 'magenta')
        self.assertFalse(contract.push_action(
            "hi", '{"user":"' + str(account_carol) + '"}', account_carol).error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()
