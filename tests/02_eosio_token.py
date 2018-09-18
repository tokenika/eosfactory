import unittest
from eosf import *

verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]

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
        create_wallet()
        create_master_account("account_master")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("account_alice", account_master)
        create_account("account_bob", account_master)
        create_account("account_carol", account_master)


    def setUp(self):
        pass


    def test_01(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("account_host", account_master)
        contract = Contract(account_host, project_from_template(
            CONTRACT_WORKSPACE, template="02_eosio_token", remove_existing=True))
        contract.build()
        contract.deploy()

        COMMENT('''
        Initialize the token and send some tokens to one of the accounts:
        ''')

        account_host.push_action(
            "create",
            {
                "issuer": account_master,
                "maximum_supply": "1000000000.0000 EOS",
                "can_freeze": "0",
                "can_recall": "0",
                "can_whitelist": "0"
            }, [account_master, account_host])

        account_host.push_action(
            "issue",
            {
                "to": account_alice, "quantity": "100.0000 EOS", "memo": ""
            },
            account_master)

        COMMENT('''
        Execute a series of transfers between the accounts:
        ''')

        account_host.push_action(
            "transfer",
            {
                "from": account_alice, "to": account_carol,
                "quantity": "25.0000 EOS", "memo":""
            },
            account_alice)
        self.assertTrue("250000" in DEBUG())

        account_host.push_action(
            "transfer",
            {
                "from": account_carol, "to": account_bob, 
                "quantity": "11.0000 EOS", "memo": ""
            },
            account_carol)
        self.assertTrue("110000" in DEBUG())

        account_host.push_action(
            "transfer",
            {
                "from": account_carol, "to": account_bob, 
                "quantity": "2.0000 EOS", "memo": ""
            },
            account_carol)
        self.assertTrue("20000" in DEBUG())

        account_host.push_action(
            "transfer",
            {
                "from": account_bob, "to": account_alice, \
                "quantity": "2.0000 EOS", "memo":""
            },
            account_bob)
        self.assertTrue("20000" in DEBUG())

        COMMENT('''
        Verify the outcome:
        ''')

        table_alice = account_host.table("accounts", account_alice)
        table_bob = account_host.table("accounts", account_bob)
        table_carol = account_host.table("accounts", account_carol)

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
