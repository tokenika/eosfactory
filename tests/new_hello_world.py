'''An example of functional test.

This example shows a case of the simplest test, featuring a single test 
function. Its code demonstrates how the contract objects can be created by 
assignments `foo = new_account(foo_owner)`, for example. Compare this sythax 
with the standard EOSFactory one in the test `tests/hello_world.py`.

See the test example `tests/new_tic_tac_toe.py` for a more complex case.

AS all the action happens in the single function `test_functionality`, the 
contract objects `master, host, alice, ...` can be local. 

However, in the same time, the account objects are referenced in the global 
namespace of the module, what is a provision to avoid having to account objects 
of the same creation name, pointing to different physical eosio accounts. 
'''

import unittest
from amaxfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        ''')
        reset()

    def test_functional(self):
        master = new_master_account()
        COMMENT('''
        Create test accounts:
        ''')
        alice = new_account(master)
        carol = new_account(master)
        bob = new_account(master)

        COMMENT('''
        Create, build and deploy the contract:
        ''')
        host = new_account(master)
        smart = Contract(host, project_from_template(
            CONTRACT_WORKSPACE, template="hello_world", 
            remove_existing=True))
        smart.build()
        smart.deploy()

        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
        self.assertTrue("alice" in DEBUG())

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
        self.assertTrue("carol" in DEBUG())

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            host.push_action(
                "hi", {"user":carol}, permission=(bob, Permission.ACTIVE))
 

        COMMENT('''
        Create, build and deploy the contract: amax.token
        ''')
        # host = new_account(master)
        amax_toeken = Contract(host, 
            wasm_file='/root/contracts/amax.contracts/src_system/build/contracts/amax.token/amax.token.wasm',
            abi_file="/root/contracts/amax.contracts/src_system/build/contracts/amax.token/amax.token.abi")
        amax_toeken.deploy()

        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(amax_toeken, Permission.ACTIVE))
            
    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
