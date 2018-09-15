import unittest
from eosf import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
_ = Logger()

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        _.SCENARIO('''
        Create a contract from template, then build and deploy it.
        Also, execute simple actions, debug buffer and authority mismatch detection.
        ''')
        reset()
        create_wallet()
        create_master_account("master")

        _.COMMENT('''
        Create test accounts:
        ''')
        create_account("alice", master)
        create_account("carol", master)


    def setUp(self):
        pass


    def test_01(self):
        _.COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("host", master)
        contract = Contract(host, project_from_template(
            CONTRACT_WORKSPACE, template="01_hello_world", remove_existing=True))
        contract.build()
        contract.deploy()

        _.COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
        self.assertTrue("alice" in host.debug_buffer)

        _.COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
        self.assertTrue("carol" in host.debug_buffer)

        _.COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        set_is_testing_errors(True)
        action = host.push_action(
            "hi", {"user":carol}, permission=(alice, Permission.ACTIVE))
        set_is_testing_errors(False)
        self.assertTrue(host.action.error)

        contract.delete()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
