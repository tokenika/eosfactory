import unittest
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
set_throw_error(False)
_ = Logger()

CONTRACT_NAME = "_e4b2ffc804529ce9c6fae258197648cc2"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        reset([Verbosity.INFO])
        set_throw_error(True)
        set_is_testing_errors(False)

        wallet = Wallet()
        account_master_create("account_master")

        _.SCENARIO('''
        This is a test of creating a contract from a pre-defined template,
        then building and deploying it.
        Finnally, a couple of basic methods are tested.
        ''')

        _.COMMENT('''
        Create accounts "host", alice" and "carol":
        ''')
        account_create("account_host", account_master)
        account_create("account_alice", account_master)
        account_create("account_carol", account_master)


    def setUp(self):
        pass


    def test_01(self):

        contract_dir = contract_workspace_from_template(
                CONTRACT_NAME, remove_existing=True, visual_studio_code=False)

        contract = Contract(account_host, contract_dir)
        contract.build()
        contract.deploy()

        _.COMMENT('''
        Testing simple actions:
        ''')
        account_host.push_action(
            "hi", {"user":account_alice}, account_alice)

        account_host.push_action(
            "hi", {"user":account_carol}, account_carol)

        # _.COMMENT('''
        # WARNING: This action should fail due to authority mismatch!
        # ''')
        # set_throw_error(False)
        # set_is_testing_errors(True)
        # action = account_host.push_action(
        #     "hi", {"user":account_carol}, account_alice)
        # self.assertTrue(action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()