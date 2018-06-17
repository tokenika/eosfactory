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
        cleos.dont_keosd()

    def setUp(self):
        pass

    def test_05(self):
        node_reset = teos.node_reset()
        self.assertTrue(node_reset, "node_reset")

    def test_10(self):
        global wallet_create
        wallet_create = cleos.WalletCreate()
        self.assertTrue(not wallet_create.error, "WalletCreate")
        print(json.dumps(wallet_create.json, indent=4))
        print(wallet_create.name)
        print(wallet_create.password)
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

    def test_40(self):
        global wallet_create
        wallet_lock = cleos.WalletLock(wallet_create)
        self.assertTrue(not wallet_lock.error, "WalletLock")
        print("---------------------------------------\n")

    def test_45(self):
        global wallet_create
        wallet_unlock = cleos.WalletUnlock(wallet_create)
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

    
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()