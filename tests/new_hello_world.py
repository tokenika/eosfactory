import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

# Actors of the test:
MASTER = None
HOST = None
ALICE = None
BOB = None
CAROL = None

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        ''')
        reset()

    def test_01(self):
        global MASTER
        MASTER = new_master_account()
        COMMENT('''
        Create test accounts:
        ''')
        global ALICE
        ALICE = new_account(MASTER)
        global CAROL
        CAROL = new_account(MASTER)
        global BOB
        BOB = new_account(MASTER)

        COMMENT('''
        Create, build and deploy the contract:
        ''')
        HOST = new_account(MASTER)
        contract = Contract(HOST, project_from_template(
            CONTRACT_WORKSPACE, template="hello_world", 
            remove_existing=True))
        contract.build()
        contract.deploy()

        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        HOST.push_action(
            "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))
        self.assertTrue("ALICE" in DEBUG())

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        HOST.push_action(
            "hi", {"user":CAROL}, permission=(CAROL, Permission.ACTIVE))
        self.assertTrue("CAROL" in DEBUG())

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "hi", {"user":CAROL}, permission=(BOB, Permission.ACTIVE))
 
    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
