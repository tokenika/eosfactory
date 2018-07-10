import unittest
from termcolor import cprint
import setup
import cleos
import eosf


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, eosf.Verbosity.DEBUG])
eosf.set_throw_error(True)
#setup.set_command_line_mode()

class Test1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass


    def test_reopen_with_stored_password(self): 
        setup.use_keosd(False)
        eosf.reset(is_verbose=0)
        eosf.Wallet()
        eosf.stop()
        eosf.run()
        
        eosf.Wallet()


    def test_invalid_password(self): 
        setup.use_keosd(False)
        eosf.reset(is_verbose=0)
        eosf.Wallet()
        eosf.stop()
        eosf.run()        
        
        with self.assertRaises(Exception):
            eosf.Wallet(
            "default", "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV")


  
    def test_is_not_running_not_keosd_set(self):
        setup.use_keosd(False)
        eosf.stop(is_verbose=0)
        
        with self.assertRaises(Exception):
            eosf.Wallet()


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()


