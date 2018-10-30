import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_iqhgcqllgnpkirjwwkms"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        Also, initialize the token and run a couple of transfers between different accounts.
        ''')
        reset()
        create_master_account("master")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("alice", master)
        create_account("bob", master)
        create_account("carol", master)


    def setUp(self):
        pass


    def test_01(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("host", master)
        contract = Contract(host, project_from_template(
            CONTRACT_WORKSPACE, template="02_eosio_token", remove_existing=True))
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
        self.assertTrue("250000" in DEBUG())

        host.push_action(
            "transfer",
            {
                "from": carol, "to": bob, 
                "quantity": "11.0000 EOS", "memo": ""
            },
            permission=(carol, Permission.ACTIVE))
        self.assertTrue("110000" in DEBUG())

        host.push_action(
            "transfer",
            {
                "from": carol, "to": bob, 
                "quantity": "2.0000 EOS", "memo": ""
            },
            permission=(carol, Permission.ACTIVE))
        self.assertTrue("20000" in DEBUG())

        host.push_action(
            "transfer",
            {
                "from": bob, "to": alice, \
                "quantity": "2.0000 EOS", "memo":""
            },
            permission=(bob, Permission.ACTIVE))
        self.assertTrue("20000" in DEBUG())

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

        contract.delete()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
