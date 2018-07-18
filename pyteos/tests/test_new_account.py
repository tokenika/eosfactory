import unittest
from termcolor import cprint
import setup
import eosf


#eosf.set_verbosity([eosf.Verbosity.TRACE])
eosf.set_throw_error(False)
eosf.use_keosd(False)
#setup.set_command_line_mode()

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """
        if not result.failures:
            super().run(result)
        print("-------------------------------------------\n")

    @classmethod
    def setUpClass(cls):

        eosf.use_keosd(False)
        #setup.set_nodeos_address("88.99.97.30:38888")
        #wallet = eosf.Wallet("jungle_wallet2")
        account_master = eosf.AccountMaster()
        print(account_master.info())


        # eosf.reset()
        # global wallet
        # wallet = eosf.Wallet("xfsadqqada")
        # #wallet1 = eosf.Wallet()
        # account_master = eosf.AccountMaster()
        # wallet.import_key(account_master)
        # # print(account_master.info())
        # eosf.account_object("account_test")
        # # print(account_test.info())

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


