import unittest, sys
from eosf import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
_ = Logger()

CONTRACT_WORKSPACE = sys.path[0] + "/../"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        _.SCENARIO('''
        Execute simple actions, debug buffer and authority mismatch detection.
        ''')
        reset()
        create_wallet()
        create_master_account("master")

        _.COMMENT('''
        Build and deploy the contract:
        ''')
        create_account("host", master)
        contract = Contract(host, CONTRACT_WORKSPACE)
        contract.build(force=False)
        contract.deploy()

        _.COMMENT('''
        Create test accounts:
        ''')
        create_account("alice", master)
        create_account("carol", master)


    def setUp(self):
        pass


    def test_01(self):
        _.COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, , permission=(alice, Permission.ACTIVE))

        _.COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))

        _.COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        set_is_testing_errors(True)
        action = host.push_action(
            "hi", {"user":carol}, permission=(alice, Permission.ACTIVE))
        set_is_testing_errors(False)
        self.assertTrue(host.action.error)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
