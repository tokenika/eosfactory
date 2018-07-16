import os
import unittest
from termcolor import cprint
import setup
import cleos
import node
import eosf
import time


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
#setup.set_command_line_mode()

cryptolions = "88.99.97.30:38888"

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

    def test_create_keosd_wallet(self):
        setup.use_keosd(True)
        cleos.WalletStop(is_verbose=0)
        wallet_name = "jungle_wallet"
        try:
            os.remove(eosf.wallet_dir() + wallet_name + ".wallet")
        except:
            pass

        setup.set_nodeos_address(cryptolions)
        wallet = eosf.Wallet(wallet_name)
        self.assertTrue(not wallet.error)


    def test_reopen_with_stored_password(self): 
        setup.use_keosd(False)
        eosf.reset(is_verbose=0)
        eosf.Wallet()
        eosf.stop(is_verbose=0)
        node.run(is_verbose=0)
        
        wallet = eosf.Wallet()
        self.assertTrue(wallet.error)


    def test_invalid_password(self): 
        setup.use_keosd(False)
        eosf.reset(is_verbose=0)
        wallet = eosf.Wallet()
        eosf.stop(is_verbose=0)
        eosf.run(is_verbose=0)        
        
        wallet = eosf.Wallet(
            "default", "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV")
        self.assertTrue(wallet.error)


    def test_is_not_running_not_keosd_set(self):
        setup.use_keosd(False)
        eosf.stop(is_verbose=0)
        
        wallet = eosf.Wallet()
        self.assertTrue(wallet.error)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()


