import os
import unittest
from termcolor import cprint
import setup
import cleos
import node
import eosf
import time


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT]) #, eosf.Verbosity.DEBUG])
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

    def test_05(self):
        setup.use_keosd(False)
        eosf.reset(is_verbose=0)
        wallet = eosf.Wallet()
        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)

        eosf.account_factory("account_alice")
        print(account_alice.info())

        eosf.account_factory("account_alice")
        

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
