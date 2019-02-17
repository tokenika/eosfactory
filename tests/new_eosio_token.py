import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

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
        Also, initialize the token and run a couple of transfers between different accounts.
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
        global BOB
        BOB = new_account(MASTER)
        global CAROL
        CAROL = new_account(MASTER)        
        
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        global HOST
        HOST = new_account(MASTER)
        contract = Contract(HOST, project_from_template(
            CONTRACT_WORKSPACE, template="eosio_token", remove_existing=True))
        contract.build()
        contract.deploy()

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

        table_alice = HOST.table("accounts", ALICE)
        table_bob = HOST.table("accounts", BOB)
        table_carol = HOST.table("accounts", CAROL)

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
