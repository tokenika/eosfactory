'''Example of a functional test.

This example shows a case of the simplest test, featuring a single test 
function. Its code demonstrates how the contract objects can be created by 
assignments `foo = new_account(foo_owner)`, for example. Compare this sythax 
with the standard EOSFactory one in the test `tests/eosio_token.py`.

See the test example `tests/new_tic_tac_toe.py` for a more complex case.

AS all the action happens in the single function `test_functionality`, the 
contract objects `master, host, alice, ...` can be local. 

However, in the same time, the account objects are referenced in the global 
namespace of the module, what is a provision to avoid having to account objects 
of the same creation name, pointing to different physical eosio accounts. 
'''

import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

class Test(unittest.TestCase):
    '''Unittest class definition.
    '''
    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        Also, initialize the token and run a couple of transfers between different accounts.
        ''')
        reset()

    def test_functionality(self):
        '''The only test function.

        The account objects `master, host, alice, ...` which are of the global namespace, do not have to be explicitly declared (and still keep the linter silent).
        '''
        master = new_master_account()

        COMMENT('''
        Create test accounts:
        ''')
        alice = new_account(master)
        bob = new_account(master)
        carol = new_account(master)        
        
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        host = new_account(master)
        contract = Contract(host, project_from_template(
            CONTRACT_WORKSPACE, template="eosio_token", remove_existing=True))
        contract.build()
        contract.deploy()

        COMMENT('''
        Initialize the token and send some tokens to one of the accounts:
        ''')

        host.push_action(
            "create",
            {
                "issuer": master,
                "maximum_supply": "1000000000.0000 EOS",
                "can_freeze": "0",
                "can_recall": "0",
                "can_whitelist": "0"
            },
            permission=[(master, Permission.ACTIVE), (host, Permission.ACTIVE)])

        host.push_action(
            "issue",
            {
                "to": alice, "quantity": "100.0000 EOS", "memo": ""
            },
            permission=(master, Permission.ACTIVE))

        COMMENT('''
        Execute a series of transfers between the accounts:
        ''')

        host.push_action(
            "transfer",
            {
                "from": alice, "to": carol,
                "quantity": "25.0000 EOS", "memo":""
            },
            permission=(alice, Permission.ACTIVE))

        host.push_action(
            "transfer",
            {
                "from": carol, "to": bob, 
                "quantity": "11.0000 EOS", "memo": ""
            },
            permission=(carol, Permission.ACTIVE))

        host.push_action(
            "transfer",
            {
                "from": carol, "to": bob, 
                "quantity": "2.0000 EOS", "memo": ""
            },
            permission=(carol, Permission.ACTIVE))

        host.push_action(
            "transfer",
            {
                "from": bob, "to": alice, \
                "quantity": "2.0000 EOS", "memo":""
            },
            permission=(bob, Permission.ACTIVE))

        COMMENT('''
        Verify the outcome:
        ''')

        table_alice = host.table("accounts", alice)
        table_bob = host.table("accounts", bob)
        table_carol = host.table("accounts", carol)

        self.assertEqual(
            table_alice.json["rows"][0]["balance"], '77.0000 EOS',
            '''assertEqual(table_alice.json["rows"][0]["balance"], '77.0000 EOS')''')
        self.assertEqual(
            table_bob.json["rows"][0]["balance"], '11.0000 EOS',
            '''assertEqual(table_bob.json["rows"][0]["balance"], '11.0000 EOS')''')
        self.assertEqual(
            table_carol.json["rows"][0]["balance"], '12.0000 EOS',
            '''assertEqual(table_carol.json["rows"][0]["balance"], '12.0000 EOS')''')

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
