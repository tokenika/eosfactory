import json
import time
import unittest
import setup
import cleos
import teos
import eosf


class Test(unittest.TestCase):

    def run(self, result=None):
        ''' Stop after first error '''      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        setup.is_verbose = True
        setup.is_json = False

    def setUp(self):
        pass
                

    def test_05(self):
        node_reset = eosf.reset([logger.Verbosity.INFO])
        self.assertTrue(node_reset)

    def test_10(self):
        global wallet_default
        wallet_default = cleos.WalletCreate()
        self.assertTrue(not wallet_default.error)
        print(json.dumps(wallet_default.json, indent=4))
        print(wallet_default.name)
        print(wallet_default.password)

    def test_15(self):
        wallet_list = cleos.WalletList()
        self.assertTrue(not wallet_list.error)
        print(json.dumps(wallet_list.json, indent=4))

    def test_20(self):
        global key_owner
        key_owner = cleos.CreateKey("owner")
        self.assertTrue(not key_owner.error)
        print(json.dumps(key_owner.json, indent=4))
        print(key_owner.name)
        print(key_owner.key_private)
        print(key_owner.key_public)

    def test_25(self):
        global key_owner
        wallet_import = cleos.WalletImport(key_owner)
        self.assertTrue(not wallet_import.error)
        print(json.dumps(wallet_import.json, indent=4))
        print(wallet_import.key_private)
        
    def test_30(self):
        wallet_list = cleos.WalletList()
        self.assertTrue(not wallet_list.error)
        print(json.dumps(wallet_list.json, indent=4))

    def test_35(self):
        wallet_keys = cleos.WalletKeys()
        self.assertTrue(not wallet_keys.error)
        print(json.dumps(wallet_keys.json, indent=4))

    def test_38(self):
        global wallet_default
        wallet_open = cleos.WalletOpen(wallet_default)
        self.assertTrue(not wallet_open.error, "WalletOpen")

    def test_40(self):
        global wallet_default
        wallet_lock = cleos.WalletLock(wallet_default)
        self.assertTrue(not wallet_lock.error, "WalletLock")

    def test_45(self):
        global wallet_default
        wallet_unlock = cleos.WalletUnlock(wallet_default)
        self.assertTrue(not wallet_unlock.error, "WalletUnlock")

    def test_50(self):
        get_info = cleos.GetInfo()
        self.assertTrue(not get_info.error, "GetInfo")
        print(json.dumps(get_info.json, indent=4))
        print(get_info.head_block)
        print(get_info.head_block_time)
        print(get_info.last_irreversible_block_num)

    def test_53(self):
        get_block = cleos.GetBlock(3)
        self.assertTrue(not get_block.error, "GetBlock")
        print(json.dumps(get_block.json, indent=4))
        print(get_block.block_num)
        print(get_block.ref_block_prefix)
        print(get_block.timestamp)

    def test_56(self):
        global account_master
        account_master = eosf.AccountMaster()
        wallet_import = cleos.WalletImport(account_master)
        print(json.dumps(account_master.json, indent=4))
        print(account_master.name)
        print(account_master.key_private)
        print(account_master.key_public)

    def test_60(self):
        global account_master
        global key_owner
        account_bob = cleos.CreateAccount(
            account_master, "bob", key_owner, key_owner)
        self.assertTrue(not account_bob.error, "CreateAccount")
        print(json.dumps(account_bob.json, indent=4))
        print(account_bob.name)

        global account_alice
        account_alice = cleos.CreateAccount(
            account_master, "alice", key_owner, key_owner, is_verbose=0)
        self.assertTrue(not account_alice.error, "CreateAccount Alice")
        print(account_alice.name)

        global account_carol
        account_carol = cleos.CreateAccount(
            account_master, "carol", key_owner, key_owner, is_verbose=0)
        self.assertTrue(not account_carol.error, "CreateAccount Carol")
        print(account_carol.name)

        time.sleep(1)

    def test_63(self):
        global account_master
        contract_eosio_bios = eosf.Contract(account_master, "eosio.bios").deploy()
        self.assertTrue(not contract_eosio_bios.error, "eosf.Contract(")
        print(contract_eosio_bios.contract_path_absolute)
    
    def test_66(self):
        global account_master
        global key_owner
        global account_test
        account_test = cleos.CreateAccount(
            account_master, "ttt", key_owner, key_owner)
        self.assertTrue(not account_test.error, "CreateAccount ttt")
        global contract_test
        contract_test = eosf.Contract(account_test, "eosio.token").deploy()
        self.assertTrue(not contract_test.error, "Contract(account_test")

    def test_69(self):
        global account_test
        get_code = cleos.GetCode(account_test)
        self.assertTrue(not get_code.error, "GetCode account_test")
        print(json.dumps(get_code.json, indent=4))
        print(get_code.code_hash)

    def test_72(self):
        global account_test
        get_info = cleos.GetInfo(is_verbose=-1)
        push_create = cleos.PushAction(
            account_test, "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}',
            permission=account_test)
        self.assertTrue(not push_create.error, "PushAction create")
        try:
            print(push_create.console)
            print(push_create.data) 
        except:
            pass         

        global account_master
        push_issue = cleos.PushAction(
            account_test, "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"100.0000 EOS to alice"}',
            permission=account_master)
        self.assertTrue(not push_issue.error, "PushAction issue")
        print(push_issue.console)
        print(push_issue.data)

        global account_alice
        push_transfer = cleos.PushAction(
            account_test, "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
            "memo":"100.0000 EOS to carol"}',
            permission=account_alice)
        self.assertTrue(not push_transfer.error, "PushAction issue")
        print(push_transfer.console)
        print(push_transfer.data)

    def test_74(self):
        global account_test
        global account_alice
        get_info = cleos.GetInfo(is_verbose=-1)
        table = cleos.GetTable(account_test, "accounts", account_alice)
        self.assertTrue(not table.error, "GetTable")
        print(json.dumps(table.json, indent=4))

    def test_77(self):
        global key_owner
        get_accounts = cleos.GetAccounts(key_owner)
        self.assertTrue(not get_accounts.error, "GetAcounts")
        print(json.dumps(get_accounts.json, indent=4))

    def test_80(self):
        global account_alice
        get_account = cleos.GetAccount(account_alice)
        self.assertTrue(not get_account.error, "GetAcount")
        print(json.dumps(get_account.json, indent=4))
    
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()