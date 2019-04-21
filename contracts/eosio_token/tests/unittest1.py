import unittest, sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
BOB = Account()
CAROL = Account()

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Initialize the token and run a couple of transfers between different accounts.
        ''')
        reset()
        create_master_account("MASTER")

        COMMENT('''
        Build & deploy the contract:
        ''')
        create_account("HOST", MASTER)
        smart = Contract(HOST, CONTRACT_WORKSPACE)
        smart.build(force=False)
        smart.deploy()

        COMMENT('''
        Create test accounts:
        ''')
        create_account("ALICE", MASTER)
        create_account("BOB", MASTER)
        create_account("CAROL", MASTER)


    def setUp(self):
        pass


    def test_01(self):

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
            permission=[(MASTER, Permission.OWNER), (HOST, Permission.ACTIVE)])

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
                "from": BOB, "to": ALICE,
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


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
