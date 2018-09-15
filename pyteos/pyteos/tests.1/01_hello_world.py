import unittest
from pyteos.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        Also, execute simple actions, debug buffer and authority mismatch detection.
        ''')
        reset()
        create_wallet()
        create_master_account("account_master")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("account_alice", account_master)
        create_account("account_carol", account_master)


    def setUp(self):
        pass


    def test_01(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("account_host", account_master)
        contract = Contract(account_host, project_from_template(
            CONTRACT_WORKSPACE, template="01_hello_world", remove_existing=True))
        contract.build()
        contract.deploy()

        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        account_host.push_action(
            "hi", {"user":account_alice}, account_alice)
        self.assertTrue("account_alice" in account_host.debug_buffer)

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        account_host.push_action(
            "hi", {"user":account_carol}, account_carol)
        self.assertTrue("account_carol" in account_host.debug_buffer)

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        set_is_testing_errors(True)
        action = account_host.push_action(
            "hi", {"user":account_carol})
        set_is_testing_errors(False)
        self.assertTrue(account_host.action.error)

        contract.delete()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
