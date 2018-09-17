import unittest, sys
from pyteos.eosf import *

verbosity = [Verbosity.INFO, Verbosity.OUT]

CONTRACT_WORKSPACE = sys.path[0] + "/../"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Execute simple actions, debug buffer and authority mismatch detection.
        ''')
        reset()
        create_wallet()
        create_master_account("master")

        COMMENT('''
        Build and deploy the contract:
        ''')
        create_account("host", master)
        contract = Contract(host, CONTRACT_WORKSPACE)
        contract.build(force=False)
        contract.deploy()

        COMMENT('''
        Create tests accounts:
        ''')
        create_account("alice", master)
        create_account("carol", master)

    def test_01(self):
        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(Error):
            host.push_action("hi", {"user":carol})

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
