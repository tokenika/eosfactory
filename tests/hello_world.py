#!/usr/bin/env python3
"""An example of functional test.

Note that the declarations
    `
    MASTER = Account()
    HOST = Account()
    ALICE = Account()
    BOB = Account()
    CAROL = Account()
    `
are abundant: they are in place to satisfy the linter, whu complains about 
dynamically created objects.
"""
import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

# Actors of the test:
MASTER = Account()
HOST = Account()
ALICE = Account()
CAROL = Account()
BOB = Account()

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SCENARIO("""
        Create a contract from template, then build and deploy it.
        """)
        reset()
        create_master_account("MASTER")

        COMMENT("""
        Create test accounts:
        """)
        create_account("ALICE", MASTER)
        create_account("CAROL", MASTER)
        create_account("BOB", MASTER)

    def test_functional(self):
        COMMENT("""
        Create, build and deploy the contract:
        """)
        create_account("HOST", MASTER)
        smart = Contract(HOST, project_from_template(
            CONTRACT_WORKSPACE, template="hello_world", 
            remove_existing=True))
        smart.build()
        smart.deploy()

        COMMENT("""
        Test an action for ALICE, including the debug buffer:
        """)
        HOST.push_action(
            "hi", {"user":ALICE}, 
            permission=(ALICE, Permission.ACTIVE),
            force_unique=True)
        self.assertTrue("ALICE" in DEBUG())

        COMMENT("""
        Test an action for CAROL, including the debug buffer:
        """)
        HOST.push_action(
            "hi", {"user":CAROL}, permission=(CAROL, Permission.ACTIVE))
        self.assertTrue("CAROL" in DEBUG())

        COMMENT("""
        WARNING: This action should fail due to authority mismatch!
        """)
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "hi", {"user":CAROL}, permission=(BOB, Permission.ACTIVE))
 
    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
