import unittest
import setup
import logger
import eosf
import time

from logger import Verbosity
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract, contract_workspace_from_template


logger.Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
logger.set_throw_error(False)
_ = logger.Logger()


CONTRACT_NAME = "_e4b2ffc804529ce9c6fae258197648cc2"


class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        print()


    def setUp(self):
        eosf.restart()
        logger.set_is_testing_errors(False)
        logger.set_throw_error(True)


    def test_contract_template(self):
        eosf.reset([logger.Verbosity.INFO]) 
        wallet = Wallet()
        account_master_create("account_master")
        logger.set_throw_error(False)
        logger.set_is_testing_errors()

        _.SCENARIO('''
        Suppose, you are going to develop a smart contract. With the ``EOSFactory``, 
        you do it within a specialized work-space, with the ``Visual Studio Code``.

        The system provides means for creating a template work-space. This unittest 
        tests them.

        Create a work-space file system in the ``EOSIO_CONTRACT_WORKSPACE`` folder.
        In practice, you will work on the sources of the contract but now, take it as
        it is: the ``hello`` contract.
        ''')

        contract_dir = contract_workspace_from_template(
                CONTRACT_NAME, remove_existing=True, visual_studio_code=False)

        account_create("account_host", account_master)
        account_create("account_alice", account_master)
        account_create("account_carol", account_master)

        contract = Contract(account_host, contract_dir)
        contract.build()
        contract.deploy()

        account_host.push_action(
            "hi", {"user":account_alice}, account_alice)

        account_host.push_action(
            "hi", {"user":account_carol}, account_carol)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        eosf.stop()


if __name__ == "__main__":
    unittest.main()