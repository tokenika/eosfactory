import unittest
import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT])

CONTRACT_WORKSPACE = sys.path[0] + "/../"


class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Execute simple actions.
        ''')
        reset()

        cls.master = create_master_account("master")

        COMMENT('''
        Build and deploy the contract:
        ''')
        cls.host = create_account("host", cls.master)
        contract = Contract(cls.host, CONTRACT_WORKSPACE)
        contract.build(force=False)
        contract.deploy()

        COMMENT('''
        Create test accounts:
        ''')
        cls.alice = create_account("alice", cls.master)
        cls.carol = create_account("carol", cls.master)
        cls.bob = create_account("bob", cls.master)

    def setUp(self):
        pass

    def test_01(self):
        COMMENT('''
        Test an action for Alice:
        ''')
        self.host.push_action(
            "hi", {"user": self.alice}, permission=(self.alice, Permission.ACTIVE))

        COMMENT('''
        Test an action for Carol:
        ''')
        self.host.push_action(
            "hi", {"user": self.carol}, permission=(self.carol, Permission.ACTIVE))

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            self.host.push_action(
                "hi", {"user": self.carol}, permission=(self.bob, Permission.ACTIVE))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
