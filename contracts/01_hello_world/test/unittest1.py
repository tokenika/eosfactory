# python3 ./tests/unittest3.py

import sys
import unittest
import setup
import eosf
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

setup.set_verbose(True)
setup.set_json(False)

contract_dir = sys.path[0] + "/../"


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


    def test_04(self):
        global wallet
        global account_master

        cprint("""eosf.reset()""", 'magenta')
        reset = eosf.reset()
        self.assertTrue(reset)

        cprint("""eosf.Wallet()""", 'magenta')
        
        wallet = eosf.Wallet()
        self.assertTrue(not wallet.error)

        cprint("""account_master = eosf.AccountMaster()""", 'magenta')

        account_master = eosf.AccountMaster(is_verbose=False)
        wallet.import_key(account_master)

        cprint(
                "Contract( account_master, 'eosio.bios').deploy()", 
                'magenta')
        
        contract_eosio_bios = eosf.Contract( 
                account_master, "eosio.bios").deploy()
        self.assertTrue(not contract_eosio_bios.error)


    def test_10(self):
        global template
        global account_test
        global contract_test

        cprint("""account_test = eosf.account():""", 'magenta')


        account_test = eosf.account()
        self.assertTrue(not account_test.error)

        cprint("""wallet.import_key(account_test)""", 'magenta')

        wallet.import_key(account_test)

        cprint(
                """contract_test = eosf.Contract(
                                account_test, contract_dir):""", 
                'magenta')

        contract_test = eosf.Contract(account_test, contract_dir)

        cprint("""contract_test.deploy():""", 'magenta')

        self.assertTrue(not contract_test.deploy().error)
    
        cprint("""code = account_test.code()""", 'magenta')

        code = account_test.code()
        print("""code hash: {}""".format(code.code_hash))


    def test_15(self):

        cprint("""`alice`and `carol`""", 'magenta')

        global alice
        alice = eosf.account()
        self.assertTrue(not alice.error)
        wallet.import_key(alice)

        global carol
        carol = eosf.account()
        self.assertTrue(not carol.error)
        wallet.import_key(carol) 

        cprint("""alice.info():""", 'magenta')

        alice.info()


    def test_20(self):

        global contract_test
        global alice
        global carol

        cprint("""contract_test.push_action("hi", :""", 'magenta')

        action_hi = contract_test.push_action(
            "hi", '{"user":"' + str(alice) + '"}', alice)

        self.assertTrue(not action_hi.error)

        action_hi = contract_test.push_action(
            "hi", 
            '{"user":"' + str(carol) + '"}', carol)

        self.assertTrue(not action_hi.error)
        
        
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        eosf.stop()


if __name__ == "__main__":
    unittest.main()