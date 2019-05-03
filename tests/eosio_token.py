'''An example of functional test.

Note that the declarations
    `
    MASTER = MasterAccount()
    HOST = Account()
    ALICE = Account()
    BOB = Account()
    CAROL = Account()
    `
are abundant: they are in place to satisfy the linter, whu complains about 
dynamically created objects. 
'''
import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
BOB = Account()
CAROL = Account()

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
        create_master_account("MASTER")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("ALICE", MASTER)
        create_account("BOB", MASTER)
        create_account("CAROL", MASTER)

    def test_functionality(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("HOST", MASTER)
        smart = Contract(HOST, project_from_template(
            CONTRACT_WORKSPACE, template="eosio_token", remove_existing=True))
        smart.build()
        smart.deploy()

        COMMENT('''
        Initialize the token and send some tokens to one of the accounts:
        ''')
        HOST.push_action(
            "create",
            {
                "issuer": MASTER,
                "maximum_supply": "1000000000.0000 EOS",
                "can_freeze": "0",
                "can_recall": "0",
                "can_whitelist": "0"
            },
            permission=[(MASTER, Permission.ACTIVE), (HOST, Permission.ACTIVE)])

        HOST.push_action(
            "issue",
            {
                "to": ALICE, "quantity": "100.0000 EOS", "memo": ""
            },
            permission=(MASTER, Permission.ACTIVE))

        COMMENT('''
        Execute a series of transfers between the accounts:
        ''')

        HOST.push_action(
            "transfer",
            {
                "from": ALICE, "to": CAROL,
                "quantity": "25.0000 EOS", "memo":""
            },
            permission=(ALICE, Permission.ACTIVE))

        HOST.push_action(
            "transfer",
            {
                "from": CAROL, "to": BOB, 
                "quantity": "11.0000 EOS", "memo": ""
            },
            permission=(CAROL, Permission.ACTIVE))

        HOST.push_action(
            "transfer",
            {
                "from": CAROL, "to": BOB, 
                "quantity": "2.0000 EOS", "memo": ""
            },
            permission=(CAROL, Permission.ACTIVE))

        HOST.push_action(
            "transfer",
            {
                "from": BOB, "to": ALICE, \
                "quantity": "2.0000 EOS", "memo":""
            },
            permission=(BOB, Permission.ACTIVE))

        COMMENT('''
        Verify the outcome:
        ''')
        xxx = __package__

        table_ALICE = HOST.table("accounts", ALICE)
        table_BOB = HOST.table("accounts", BOB)
        table_CAROL = HOST.table("accounts", CAROL)

        self.assertEqual(
            table_ALICE.json["rows"][0]["balance"], '77.0000 EOS',
            '''assertEqual(table_ALICE.json["rows"][0]["balance"], '77.0000 EOS')''')
        self.assertEqual(
            table_BOB.json["rows"][0]["balance"], '11.0000 EOS',
            '''assertEqual(table_BOB.json["rows"][0]["balance"], '11.0000 EOS')''')
        self.assertEqual(
            table_CAROL.json["rows"][0]["balance"], '12.0000 EOS',
            '''assertEqual(table_CAROL.json["rows"][0]["balance"], '12.0000 EOS')''')

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
