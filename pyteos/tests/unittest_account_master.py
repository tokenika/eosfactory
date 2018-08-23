import unittest
import setup
import eosf
import cleos
import time
import eosf_account

from eosf_wallet import Wallet
from eosf_account import create_account, create_master_account


front_end.Logger.verbosity = [front_end.Verbosity.TRACE, front_end.Verbosity.OUT]

remote_testnet = "http://88.99.97.30:38888"
not_imputed = True
_ = front_end.Logger()

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print('''

NEXT TEST ====================================================================
''')

    @classmethod
    def setUpClass(cls):
        print()

    def setUp(self):
        front_end.set_is_testing_errors(False)
        front_end.set_throw_error(True)

    # def test_too_many_wallets(self):
    #     _.COMMENT('''
    #     Check the condition that
    #     precisely one ``Wallet`` object is defined when calling the 
    #         ``create_master_account(...)`` function.
    #     ''')
    #     eosf.reset([front_end.Verbosity.INFO])
    #     create_wallet()
    #     front_end.set_throw_error(False)
    #     front_end.set_is_testing_errors()
    #     ######################################################################

        # wallet1 = Wallet("second")
        # _.COMMENT('''
        # Added second wallet, named "second". Calling the ``create_master_account(...)`` 
        # function should result in an error message:
        # ''')        
        # wallet1 = Wallet("second")
        # self.assertTrue("It can be only one" in wallet1.front_end.err_msg)

    def test_there_is_no_wallet(self):
        _.COMMENT('''
        Check the condition that
        precisely one ``Wallet`` object is defined when calling the 
            ``create_master_account(...)`` function.
        ''')
        eosf.reset([front_end.Verbosity.INFO])
        front_end.set_is_testing_errors()
        ######################################################################

        _.COMMENT('''
        There is not any ``Wallet`` object. Calling the ``create_master_account(...)`` 
        function should result in an error message:
        ''')
        front_end.set_is_testing_errors()
        logger =create_master_account("account_master")        
        self.assertTrue("Cannot find any `Wallet` object." in front_end.err_msg)

    # def test_testnet_create_account(self):
    #     _.COMMENT('''
    #     If the local testnet is running, ``create_master_account(<test object name>)``
    #     puts the created account object into the global namespace, and puts the
    #     account into the wallet.

    #     With the local testnet, the name of the master account is ``eosio``.
    #     ''')

    #     eosf.reset([front_end.Verbosity.INFO])
    #     create_wallet()

    #     front_end.set_throw_error(False)
    #     ######################################################################
        
    #     _.COMMENT('''
    #     With the local testnet, the name of the master account is ``eosio``:
    #     ''')        
    #     create_master_account("account_master")
    #     self.assertTrue(account_master.name == "eosio")
    #     _.COMMENT('''
    #     Wallet keys:
    #     ''')         
    #     wallet.keys()
    #     keys1 = wallet.wallet_keys.json

    #     _.COMMENT('''
    #     With the local testnet, the wallet passwords are stored in a file.
    #     Let us restart the testnet and restore the wallet:
    #     ''')

    #     eosf.stop(is_verbose=0)
    #     eosf.run(is_verbose=0)
    #     create_wallet()
    #     _.COMMENT('''
    #     Wallet keys:
    #     ''')           
    #     wallet.keys()
    #     keys2 = wallet.wallet_keys.json

    #     _.COMMENT('''
    #     Assert that key lists are equal.
    #     ''')
    #     self.assertTrue(keys1 == keys2)


    # def test_testnet_create_account(self):
    #     if not_imputed:
    #         return
    
    #     _.COMMENT('''
    #     If the ``name`` argument is set, check the testnet for presence of the 
    #     account. If present, create the corresponding object and see whether it
    #     is in the wallets. If so, put the account object into the global namespace 
    #     of the caller.
    #     ''')
    #     setup.set_nodeos_address(remote_testnet)
    #     wallet = Wallet(
    #         None,
    #         "PW5J5KW7erKzqJmn9gMrvzev4pLxR3Vt9BRkx94BqdfHkw4z4bNTd"
    #         )

    #     front_end.set_throw_error(False)
    #     ######################################################################
        
    #     create_master_account("account_master")

    # def test_is_do_not_exist_error(self):
    #     _.COMMENT('''
    #     The cleos ``get account`` command returns a not specific error responce when
    #     the given name is found. Probably, it may change, therefore is to be tested. 
    #     ''')
    #     eosf.reset([front_end.Verbosity.INFO])
    #     front_end.set_throw_error(False)
    #     ######################################################################
    #     get_account = cleos.GetAccount("hwtsfwytrwty")
    #     _.TRACE('''
    #     The original error message is
    #     {}
    #             Next, it follows this message formatted:
    #     '''.format(get_account.err_msg))
    #     self.assertTrue(eosf_account.is_do_not_exist_error(get_account, _))    

    def test_testnet_create_account(self):
        if not_imputed:
            return
            
        _.COMMENT('''
        If the ``name`` argument is set, and, additionally, private keys are given,
        check the testnet for presence of the 
        account. If present, create the corresponding object and put it
        into the wallet. Next, put the account object into the global namespace 
        of the caller.

        Accout Name: dgxo1uyhoytn
        Owner Public Key: EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959
        Active Public Key: EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv

        Owner Private Key: 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY
        Active Private Key: 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA        
        ''')
        setup.set_nodeos_address(remote_testnet)
        wallet = Wallet(
            None,
            "PW5J5KW7erKzqJmn9gMrvzev4pLxR3Vt9BRkx94BqdfHkw4z4bNTd"
            )

        wallet.remove_key("EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959")
        wallet.remove_key("EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv")
        wallet.keys()
        front_end.set_throw_error(False)
        ######################################################################
        
        create_master_account("account_master", "dgxo1uyhoytn",
                "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
                "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
            )

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
