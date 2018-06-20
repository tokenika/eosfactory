# python3 ./tests/test1.py

import json
import setup
import cleos
import teos
import eosf
import unittest
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        setup.set_verbose(False)
        #cleos.dont_keosd()


    def setUp(self):
        pass

    def test_05(self):
        node_reset = teos.node_reset()
        self.assertTrue(node_reset, "node_reset")

    def test_08(self):
        global wallet_default
        wallet_default = eosf.Wallet()
        wallet_second = eosf.Wallet("second")
        self.assertTrue(not wallet_default.error)
        global key_owner
        key_owner = cleos.CreateKey("owner")
        self.assertTrue(wallet_default.import_key(key_owner), "import_key")
        print(wallet_default)
        self.assertTrue(wallet_default.open())
        self.assertTrue(wallet_default.lock())
        print(wallet_default)
        self.assertTrue(wallet_default.unlock())

    def test_10(self):
        global key_owner        
        global account_eosio
        global account_alice
        global account_bill
        global account_carol

        account_eosio = cleos.AccountEosio() 
        contract_eosio_bios = cleos.SetContract( account_eosio, "eosio.bios")
        self.assertTrue(not contract_eosio_bios.error)

        account_alice = eosf.Account( 
            account_eosio, "alice", key_owner)
        self.assertTrue(not account_alice.error)

        account_bill = eosf.Account( 
            account_eosio, "bill", key_owner)
        self.assertTrue(not account_bill.error)

        account_carol = eosf.Account( 
            account_eosio, "carol", key_owner)
        self.assertTrue(not account_carol.error)

    def test_11(self):
        global wallet_default

        account = cleos.AccountLight()
        self.assertTrue(not account.error)
        wallet_default.import_key(account.active_key)

        contract = eosf.Contract(account, "tic_tac_toe")
        is_deployed = contract.deploy()
        info = cleos.GetInfo(is_verbose=-1)

        print(contract.contract.contract_path_absolute)
        print(contract.contract.error)
        if contract.contract.error:
            print(contract.contract.err_msg)
        print(is_deployed)

        print(colored("""
Create a new contract template directory:
        """, 'green'))
        contract_dir = "test"
        template = teos.Template(contract_dir, remove_existing=True)
        print("template path is {}".format(template.contract_path_absolute))

        print(colored("""
Again, create a new account, and add a contract to it:
        """, 'green'))
        account = cleos.AccountLight()
        self.assertTrue(not account.error)
        wallet_default.import_key(account.owner_key)
        wallet_default.import_key(account.active_key)
        contract = eosf.Contract(account, contract_dir)
        
        print(colored("""
However, the contract cannot be deployed because it is not built yet. An attempt
results in an error message:
        """, 'green'))
        is_deployed = contract.deploy()
        self.assertFalse(is_deployed)
        if contract.contract.error:
            print(contract.contract.err_msg)

        print(colored("""
Use the `build` method of the `eosf.Contract` object:
        """, 'green'))
        if not is_deployed:
            contract.build()

        is_deployed = contract.deploy()
        print("contract is deployed now: {}".format(is_deployed))
        
        self.assertTrue(template.delete())


    def test_12(self):
        global wallet_default
        global account_eosio
        global account_alice

        account = cleos.AccountLight()
        self.assertTrue(not account.error)
        wallet_default.import_key(account.active_key)

        contract = eosf.Contract(account, "eosio.token")
        is_deployed = contract.deploy()
        self.assertTrue(is_deployed)

        info = cleos.GetInfo(is_verbose=-1)

        print(colored("""
contract.push_action('create'
        """, 'green'))        
        action_create = contract.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}')
        self.assertTrue(not action_create.error)
        # print(action_create.console)
        # print(action_create.data)

        print(colored("""
contract.push_action('issue'
        """, 'green'))
        action_issue = contract.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"100.0000 EOS to alice"}', permission=account_eosio)
        self.assertTrue(not action_issue.error)

        print(colored("""
contract.push_action('transfer'
        """, 'green'))
        action_transfer = contract.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
            "memo":"100.0000 EOS to carol"}', permission=account_alice)
        self.assertTrue(not action_transfer.error)

        info = cleos.GetInfo(is_verbose=-1)

        print(colored("""
contract.get_table(account_alice.name, "accounts")
        """, 'green'))
        table = contract.get_table("accounts", account_alice )
        self.assertTrue(not table.error)
        print(json.dumps(table.json, indent=4))


    def test_13(self):
        global account_eosio
        global key_owner

        account_tokenika = eosf.Account( 
            account_eosio, "tokenika", key_owner)
        self.assertTrue(not account_tokenika.error)
        print(account_tokenika)

        code = account_tokenika.code()
        self.assertTrue(not code.error)
        print(code.code_hash)

        contract_tokenika = account_tokenika.set_contract("tic_tac_toe")
        self.assertTrue(not contract_tokenika.error, "contract_tokenika")
        code = account_tokenika.code()
        self.assertTrue(not code.error)
        print(code.code_hash)

    def test_15(self):
        global account_eosio
        global account_alice
        global key_owner

        account_ttt = eosf.Account(account_eosio, "ttt", key_owner)
        self.assertTrue(not account_ttt.error)
        contract_ttt = account_ttt.set_contract("eosio.token")
        self.assertTrue(not contract_ttt.error)

        print(colored("""
account_ttt.push_action('create'
        """, 'green')) 
        action_create = account_ttt.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}')
        self.assertTrue(not action_create.error)
        print(action_create.console)
        print(action_create.data)
        
        print(colored("""
account_ttt.push_action('issue'
        """, 'green')) 
        action_issue = account_ttt.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"100.0000 EOS to alice"}', permission=account_eosio)
        self.assertTrue(not action_issue.error)

        print(colored("""
account_ttt.push_action('transfer'
        """, 'green')) 
        action_transfer = account_ttt.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
            "memo":"100.0000 EOS to carol"}', permission=account_alice)
        self.assertTrue(not action_transfer.error)

        info = cleos.GetInfo(is_verbose=-1)
        table = account_ttt.get_table( "accounts", account_alice)
        self.assertTrue(not table.error)
        print(json.dumps(table.json, indent=4))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()