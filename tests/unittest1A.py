# python3 ./tests/unittest1.py

import unittest
import json
from termcolor import cprint
import setup
import eosf


setup.set_verbose(False)
setup.set_json(False)
setup.use_keosd(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        global testnet
        global wallet
        global account_master
        global contract_eosio_bios
        global alice
        global bob
        global carol
        global contract
        global deployment

        testnet = eosf.reset()
        wallet = eosf.Wallet()

        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)

        alice = eosf.account()
        wallet.import_key(alice)

        bob = eosf.account()
        wallet.import_key(bob)

        carol = eosf.account()
        wallet.import_key(carol)

        account = eosf.account()
        wallet.import_key(account)

        contract_eosio_bios = eosf.Contract(
            account_master, "eosio.bios").deploy()

        contract = eosf.Contract(account, "eosio.token")
        deployment = contract.deploy()


    def setUp(self):
        self.assertTrue(not testnet.error)
        self.assertTrue(not wallet.error)
        self.assertTrue(not contract_eosio_bios.error)
        self.assertTrue(not alice.error)
        self.assertTrue(not bob.error)
        self.assertTrue(not carol.error)
        self.assertTrue(not contract.error)
        self.assertTrue(not deployment.error)


    def test_01(self):
        global account_master

        cprint("""
Action contract.push_action("create")
        """, 'magenta')
        self.assertTrue(not contract.push_action(
            "create",
            '{"issuer":"'
                + str(account_master)
                + '", "maximum_supply":"1000000000.0000 EOS",\
                "can_freeze":0, "can_recall":0, "can_whitelist":0}').error)

        cprint("""
Action contract.push_action("issue")
        """, 'magenta')
        self.assertTrue(not contract.push_action(
            "issue",
            '{"to":"' + str(alice)
                + '", "quantity":"100.0000 EOS", "memo":"memo"}',
                account_master).error)


    def test_02(self):

        cprint("""
Action contract.push_action("transfer", alice)
        """, 'magenta')
        self.assertTrue(not contract.push_action(
            "transfer",
            '{"from":"' + str(alice)
                + '", "to":"' + str(carol)
                + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
            alice).error)

        cprint("""
Action contract.push_action("transfer", carol)
        """, 'magenta')
        self.assertTrue(not contract.push_action(
            "transfer",
            '{"from":"' + str(carol)
                + '", "to":"' + str(bob)
                + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
            carol).error)

        cprint("""
Action contract.push_action("transfer" bob)
        """, 'magenta')
        self.assertTrue(not contract.push_action(
            "transfer", 
            '{"from":"' + str(bob)
                + '", "to":"' + str(alice)
                + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
            bob).error)


    def test_03(self):

        cprint("""
Assign t1 = contract.get_table("accounts", alice)
        """, 'magenta')
        t1 = contract.get_table("accounts", alice)

        cprint("""
Assign t2 = contract.get_table("accounts", bob)
        """, 'magenta')
        t2 = contract.get_table("accounts", bob)
        
        cprint("""
Assign t3 = contract.get_table("accounts", carol)
        """, 'magenta')
        t3 = contract.get_table("accounts", carol)

        cprint("""
Assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
        """, 'magenta')
        self.assertTrue(t1.json["rows"][0]["balance"] == '77.0000 EOS')

        cprint("""
Assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
        """, 'magenta')
        self.assertTrue(t2.json["rows"][0]["balance"] == '11.0000 EOS')

        cprint("""
Assert t3.json["rows"][0]["balance"] == '12.0000 EOS'
        """, 'magenta')
        self.assertTrue(t3.json["rows"][0]["balance"] == '12.0000 EOS')


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        eosf.stop()


if __name__ == "__main__":
    unittest.main()