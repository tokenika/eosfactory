import unittest
import setup
import eosf
import time

from eosf_wallet import Wallet
from eosf_account import account_factory, AccountMaster


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, eosf.Verbosity.DEBUG])
eosf.set_throw_error(True)
#setup.set_command_line_mode()

class Test1(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print("""

NEXT TEST ====================================================================
""")


    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass


    def test_local_testnet(self):
        setup.use_keosd(False)
        eosf.reset(is_verbose=0)
        eosf.stop(is_verbose=0)
        eosf.run(is_verbose=0)

        account_master = AccountMaster()
        print(account_master.info())


    def test_remote_testnet_new_account(self):
        setup.use_keosd(True)
        setup.set_nodeos_URL("88.99.97.30:38888")

        account_master = AccountMaster()
        print()

    
    def test_remote_testnet_existing_account(self):
        setup.use_keosd(True)
        setup.set_nodeos_URL("88.99.97.30:38888")
        
        AccountMaster(
            "nbhyi5exmjcl",
            "account_master")
        print(account_master.owner_key)
        #print(account_master.info())


    def test_is_not_running_not_keosd_set(self):
        setup.use_keosd(False)
        eosf.stop(is_verbose=0)

        with self.assertRaises(Exception):
            AccountMaster()

  
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
        #eosf.stop()


if __name__ == "__main__":
    unittest.main()


