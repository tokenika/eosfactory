import unittest
from termcolor import cprint
import setup
import eosf


eosf.set_verbosity([eosf.Verbosity.TRACE])
eosf.set_throw_error(True)
setup.use_keosd(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):
        #eosf.reset()
        global wallet
        wallet = eosf.Wallet()
        #wallet1 = eosf.Wallet()
        # account_master = eosf.AccountMaster()
        # wallet.import_key(account_master)
        # print(account_master.info())
        # eosf.account_object("account_test")
        # print(account_test)

    def setUp(self):
        pass

    def test_05(self):
        pass


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        eosf.stop()


if __name__ == "__main__":
    unittest.main()


