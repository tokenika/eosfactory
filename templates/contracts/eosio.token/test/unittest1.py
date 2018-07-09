import sys
import setup
import eosf
import node
import unittest
from termcolor import cprint

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
        testnet = node.reset()
        assert(not testnet.error)

        wallet = eosf.Wallet()
        assert(not wallet.error)

        global account_master
        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)
        assert(not account_master.error)

        global account_alice
        account_alice = eosf.account(account_master)
        wallet.import_key(account_alice)
        assert(not account_alice.error)

        global account_bob
        account_bob = eosf.account(account_master)
        wallet.import_key(account_bob)
        assert(not account_bob.error)

        global account_carol
        account_carol = eosf.account(account_master)
        wallet.import_key(account_carol)
        assert(not account_carol.error)

        account_deploy = eosf.account(account_master)
        wallet.import_key(account_deploy)
        assert(not account_deploy.error)

        contract_eosio_bios = eosf.Contract(
            account_master, "eosio.bios").deploy()
        assert(not contract_eosio_bios.error)

        global contract
        contract = eosf.Contract(account_deploy, "eosio.token")
        assert(not contract.error)

        deployment = contract.deploy()
        assert(not deployment.error)


    def setUp(self):
        pass


    def test_01(self):
        
        cprint("""
Action contract.push_action("create")
        """, 'magenta')
        self.assertFalse(contract.push_action(
            "create",
            '{"issuer":"'
                + str(account_master)
                + '", "maximum_supply":"1000000000.0000 EOS",\
                "can_freeze":0, "can_recall":0, "can_whitelist":0}').error)

        cprint("""
Action contract.push_action("issue")
        """, 'magenta')
        self.assertFalse(contract.push_action(
            "issue",
            '{"to":"' + str(account_alice)
                + '", "quantity":"100.0000 EOS", "memo":"memo"}',
                account_master).error)


    def test_02(self):

        cprint("""
Action contract.push_action("transfer", account_alice)
        """, 'magenta')
        self.assertFalse(contract.push_action(
            "transfer",
            '{"from":"' + str(account_alice)
                + '", "to":"' + str(account_carol)
                + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
            account_alice).error)

        cprint("""
Action contract.push_action("transfer", account_carol)
        """, 'magenta')
        self.assertFalse(contract.push_action(
            "transfer",
            '{"from":"' + str(account_carol)
                + '", "to":"' + str(account_bob)
                + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
            account_carol).error)

        cprint("""
Action contract.push_action("transfer", account_bob)
        """, 'magenta')
        self.assertFalse(contract.push_action(
            "transfer", 
            '{"from":"' + str(account_bob)
                + '", "to":"' + str(account_alice)
                + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
            account_bob).error)


    def test_03(self):

        cprint("""
Assign t1 = contract.table("accounts", account_alice)
        """, 'magenta')
        t1 = contract.table("accounts", account_alice)

        cprint("""
Assign t2 = contract.table("accounts", account_bob)
        """, 'magenta')
        t2 = contract.table("accounts", account_bob)
        
        cprint("""
Assign t3 = contract.table("accounts", account_carol)
        """, 'magenta')
        t3 = contract.table("accounts", account_carol)

        cprint("""
Assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
        """, 'magenta')
        self.assertEqual(t1.json["rows"][0]["balance"], '77.0000 EOS')

        cprint("""
Assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
        """, 'magenta')
        self.assertEqual(t2.json["rows"][0]["balance"], '11.0000 EOS')

        cprint("""
Assert t3.json["rows"][0]["balance"] == '12.0000 EOS'
        """, 'magenta')
        self.assertEqual(t3.json["rows"][0]["balance"], '12.0000 EOS')


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()
