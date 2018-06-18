# python3 ./tests/test1.py

import json
import setup
import cleos
import teos
import entities

import unittest

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        setup.set_verbose(False)
        cleos.dont_keosd()

    def setUp(self):
        pass

    def test_05(self):
        node_reset = teos.node_reset()
        self.assertTrue(node_reset, "node_reset")

    def test_08(self):
        global wallet_default
        wallet_default = entities.Wallet()
        wallet_second = entities.Wallet("second")
        self.assertTrue(not wallet_default.error, "Wallet default")
        global key_owner
        key_owner = cleos.CreateKey("owner")
        self.assertTrue(wallet_default.import_key(key_owner), "import_key")
        print(wallet_default)
        self.assertTrue(wallet_default.open(), "open")
        self.assertTrue(wallet_default.lock(), "lock")
        print(wallet_default)
        self.assertTrue(wallet_default.unlock(), "unlock")

    def test_10(self):
        global key_owner        
        global account_eosio
        global account_alice
        global account_bill
        global account_carol

        account_eosio = cleos.AccountEosio() 
        contract_eosio_bios = cleos.SetContract( account_eosio, "eosio.bios")
        self.assertTrue(not contract_eosio_bios.error)

        account_alice = entities.Account( 
            account_eosio, "alice", key_owner)
        self.assertTrue(not account_alice.error)

        account_bill = entities.Account( 
            account_eosio, "bill", key_owner)
        self.assertTrue(not account_bill.error)

        account_carol = entities.Account( 
            account_eosio, "carol", key_owner)
        self.assertTrue(not account_carol.error)

    def test_12(self):
        global account_eosio
        global key_owner

        account_tokenika = entities.Account( 
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

        account_ttt = entities.Account(account_eosio, "ttt", key_owner)
        self.assertTrue(not account_ttt.error)
        contract_ttt = account_ttt.set_contract("eosio.token")
        self.assertTrue(not contract_ttt.error)

        action_create = account_ttt.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}')
        self.assertTrue(not action_create.error)
        print(action_create.console)
        print(action_create.data)

        action_issue = account_ttt.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"100.0000 EOS to alice"}', permission=account_eosio)
        self.assertTrue(not action_issue.error)

        action_transfer = account_ttt.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
            "memo":"100.0000 EOS to carol"}', permission=account_alice)
        self.assertTrue(not action_transfer.error)

        info = cleos.GetInfo(is_verbose=False, suppress_error_msg=True)
        table = account_ttt.get_table(account_alice, "accounts")
        self.assertTrue(not table.error)
        print(json.dumps(table.json, indent=4))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()