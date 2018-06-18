# python3 ./tests/test1.py

import setup
import cleos
import teos
import json

import unittest

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_03(self):
        wallet_stop = cleos.WalletStop()
        self.assertTrue(not wallet_stop.error, "WalletStop")

        print("---------------------------------------\n")

    def test_04(self):
        cleos.dont_keosd()

    def test_05(self):
        node_reset = teos.node_reset()
        self.assertTrue(node_reset, "node_reset")

    def test_10(self):
        global wallet_default
        wallet_default = cleos.WalletCreate()
        self.assertTrue(not wallet_default.error, "WalletCreate")
        print(json.dumps(wallet_default.json, indent=4))
        print(wallet_default.name)
        print(wallet_default.password)

        print("---------------------------------------\n")

    def test_15(self):
        wallet_list = cleos.WalletList()
        self.assertTrue(not wallet_list.error, "WalletList")
        print(json.dumps(wallet_list.json, indent=4))

        print("---------------------------------------\n")

    def test_20(self):
        global key_owner
        key_owner = cleos.CreateKey("owner")
        self.assertTrue(not key_owner.error, "CreateKey")
        print(json.dumps(key_owner.json, indent=4))
        print(key_owner.name)
        print(key_owner.key_private)
        print(key_owner.key_public)

        print("---------------------------------------\n")

    def test_25(self):
        global key_owner
        wallet_import = cleos.WalletImport(key_owner)
        self.assertTrue(not wallet_import.error, "WalletImport")
        print(json.dumps(wallet_import.json, indent=4))
        print(wallet_import.key_private)

        print("---------------------------------------\n")
        
    def test_30(self):
        wallet_list = cleos.WalletList()
        self.assertTrue(not wallet_list.error, "WalletList")
        print(json.dumps(wallet_list.json, indent=4))

        print("---------------------------------------\n")

    def test_35(self):
        wallet_keys = cleos.WalletKeys()
        self.assertTrue(not wallet_keys.error, "WalletKeys")
        print(json.dumps(wallet_keys.json, indent=4))

        print("---------------------------------------\n")

    def test_38(self):
        global wallet_default
        wallet_open = cleos.WalletOpen(wallet_default)
        self.assertTrue(not wallet_open.error, "WalletOpen")

        print("---------------------------------------\n")        

    def test_40(self):
        global wallet_default
        wallet_lock = cleos.WalletLock(wallet_default)
        self.assertTrue(not wallet_lock.error, "WalletLock")

        print("---------------------------------------\n")

    def test_45(self):
        global wallet_default
        wallet_unlock = cleos.WalletUnlock(wallet_default)
        self.assertTrue(not wallet_unlock.error, "WalletUnlock")

        print("---------------------------------------\n")

    def test_50(self):
        get_info = cleos.GetInfo()
        self.assertTrue(not get_info.error, "GetInfo")
        print(json.dumps(get_info.json, indent=4))
        print(get_info.head_block)
        print(get_info.head_block_time)
        print(get_info.last_irreversible_block_num)

        print("---------------------------------------\n")

    def test_53(self):
        get_block = cleos.GetBlock(3)
        self.assertTrue(not get_block.error, "GetBlock")
        print(json.dumps(get_block.json, indent=4))
        print(get_block.block_num)
        print(get_block.ref_block_prefix)
        print(get_block.timestamp)

        print("---------------------------------------\n")

    def test_56(self):
        global account_eosio
        account_eosio = cleos.AccountEosio()
        self.assertTrue(not account_eosio.error, "AccountEosio")
        print(json.dumps(account_eosio.json, indent=4))
        print(account_eosio.name)
        print(account_eosio.key_private)
        print(account_eosio.key_public)

        print("---------------------------------------\n")

    def test_60(self):
        global account_eosio
        global key_owner
        account_bob = cleos.CreateAccount(
            account_eosio, "bob", key_owner, key_owner)
        self.assertTrue(not account_bob.error, "CreateAccount")
        print(json.dumps(account_bob.json, indent=4))
        print(account_bob.name)

        global account_alice
        account_alice = cleos.CreateAccount(
            account_eosio, "alice", key_owner, key_owner, is_verbose=False)
        self.assertTrue(not account_alice.error, "CreateAccount Alice")
        print(account_alice.name)

        global account_carol
        account_carol = cleos.CreateAccount(
            account_eosio, "carol", key_owner, key_owner, is_verbose=False)
        self.assertTrue(not account_carol.error, "CreateAccount Carol")
        print(account_carol.name)

        print("---------------------------------------\n")

    def test_63(self):
        global account_eosio
        contract_eosio_bios = cleos.SetContract( account_eosio, "eosio.bios")
        self.assertTrue(not contract_eosio_bios.error, "SetContract bios")
        print(contract_eosio_bios.contract_path_absolute)

        print("---------------------------------------\n")
    
    def test_66(self):
        global account_eosio
        global key_owner
        global account_ttt
        account_ttt = cleos.CreateAccount(
            account_eosio, "ttt", key_owner, key_owner)
        self.assertTrue(not account_ttt.error, "CreateAccount ttt")
        global contract_ttt
        contract_ttt = cleos.SetContract(account_ttt, "eosio.token")
        self.assertTrue(not contract_ttt.error, "SetContract eosio.token")

        print("---------------------------------------\n")

    def test_69(self):
        global account_ttt
        get_code = cleos.GetCode(account_ttt)
        self.assertTrue(not get_code.error, "GetCode account_ttt")
        print(json.dumps(get_code.json, indent=4))
        print(get_code.code_hash)
        print("---------------------------------------\n")

    
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()