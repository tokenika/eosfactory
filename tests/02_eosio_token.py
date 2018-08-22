import unittest
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
set_throw_error(False)
_ = Logger()

CONTRACT_NAME = "02_eosio_token"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        reset([Verbosity.INFO])
        set_throw_error(True)
        set_is_testing_errors(False)

        wallet = Wallet()
        account_master_create("account_master")

        _.SCENARIO('''
        First we create a series of accounts and delpoy the ``eosio.token`` contract
        to one of them. Then we initialize the token, and run a couple of transfers
        between those accounts.
        ''')

        _.COMMENT('''
        Create a contract's hosting account, then build & deploy the contract:
        ''')
        account_create("account_host", account_master)
        contract = Contract(account_host, CONTRACT_NAME)
        # contract.build()
        contract.deploy()

        _.COMMENT('''
        Create accounts "alice", "bob" and "carol":
        ''')
        account_create("account_alice", account_master)
        account_create("account_bob", account_master)
        account_create("account_carol", account_master)


    def setUp(self):
        pass


    def test_01(self):

        _.COMMENT('''
        Initialize the contract and send some tokens to one of the accounts:
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

        # self.assertTrue(
        #     '"maximum_supply": "1000000000.0000 EOS"' \
        #         in account_host.eosf_buffer)

        account_host.push_action(
            "issue",
            {
                "to": account_alice, "quantity": "100.0000 EOS", "memo": ""
            },
            account_master)

        _.COMMENT('''
        Execute a series of transfers between the accounts:
        ''')

        account_host.push_action(
            "transfer",
            {
                "from": account_alice, "to": account_carol,
                "quantity": "25.0000 EOS", "memo":""
            },
            account_alice)

        account_host.push_action(
            "transfer",
            {
                "from": account_carol, "to": account_bob, 
                "quantity": "11.0000 EOS", "memo": ""
            },
            account_carol)

        account_host.push_action(
            "transfer",
            {
                "from": account_carol, "to": account_bob, 
                "quantity": "2.0000 EOS", "memo": ""
            },
            account_carol)

        account_host.push_action(
            "transfer",
            {
                "from": account_bob, "to": account_alice, \
                "quantity": "2.0000 EOS", "memo":""
            },
            account_bob)

        _.COMMENT('''
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


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
