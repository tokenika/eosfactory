import sys
import setup
import eosf
import node
import unittest
from termcolor import cprint


setup.set_verbose(True)
setup.use_keosd(False)
setup.set_json(False)


contract_dir = sys.path[0] + "/../"


class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        global testnet
        global wallet
        global eosio
        global contract_eosio_bios
        global alice
        global carol
        global contract
        global deployment

        testnet = node.reset()
        wallet = eosf.Wallet()

        eosio = eosf.AccountMaster()
        wallet.import_key(eosio)

        alice = eosf.account()
        wallet.import_key(alice)

        carol = eosf.account()
        wallet.import_key(carol)

        account = eosf.account()
        wallet.import_key(account)

        contract_eosio_bios = eosf.Contract(
            eosio, "eosio.bios").deploy()

        contract = eosf.Contract(account, contract_dir)
        deployment = contract.deploy()


    def setUp(self):
        self.assertFalse(testnet.error)
        self.assertFalse(wallet.error)
        self.assertFalse(contract_eosio_bios.error)
        self.assertFalse(alice.error)
        self.assertFalse(carol.error)
        self.assertFalse(contract.error)
        self.assertFalse(deployment.error)


    def test_01(self):

        cprint(
            """contract.push_action("hi", '{"user":"' + str(alice) + '"}', alice)""", 'magenta')
        self.assertFalse(contract.push_action(
            "hi", '{"user":"' + str(alice) + '"}', alice).error)

        cprint(
            """contract.push_action("hi", '{"user":"' + str(carol) + '"}', carol)""", 'magenta')
        self.assertFalse(contract.push_action(
            "hi", '{"user":"' + str(carol) + '"}', carol).error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()
