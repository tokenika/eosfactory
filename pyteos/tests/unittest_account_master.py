import unittest
import setup
import eosf
import cleos
import time
import eosf_account

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT])
# eosf.set_verbosity_plus([eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
# setup.set_command_line_mode()

cryptolions = "88.99.97.30:38888"
not_imputed = True
l = eosf.Logger()

class Test1(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print("""

NEXT TEST ====================================================================
""")

    @classmethod
    def setUpClass(cls):
        print()

    def setUp(self):
        eosf.set_is_testing_errors(False)
        eosf.set_throw_error(True)

    # def test_too_many_wallets(self):
    #     l.COMMENT("""
    #     Check the condition that
    #     precisely one ``Wallet`` object is defined when calling the 
    #         ``account_master_create(...)`` function.
    #     """)
    #     eosf.use_keosd(False)
    #     eosf.reset(is_verbose=0)
    #     wallet = Wallet()
    #     eosf.set_throw_error(False)
    #     eosf.set_is_testing_errors()
    #     ######################################################################

    #     wallet1 = Wallet("second")
    #     l.COMMENT("""
    #     Added second wallet, named "second". Calling the ``account_master_create(...)`` 
    #     function should result in an error message:
    #     """)        
    #     eosf.set_is_testing_errors()
    #     logger = account_master_create("account_master")
    #     self.assertTrue("Too many `Wallet` objects." in logger.err_msg)

    def test_there_is_no_wallet(self):
        l.COMMENT("""
        Check the condition that
        precisely one ``Wallet`` object is defined when calling the 
            ``account_master_create(...)`` function.
        """)
        eosf.use_keosd(False)
        eosf.reset(is_verbose=0)
        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()
        ######################################################################

        l.COMMENT("""
        There is not any ``Wallet`` object. Calling the ``account_master_create(...)`` 
        function should result in an error message:
        """)
        eosf.set_is_testing_errors()
        logger = account_master_create("account_master")        
        self.assertTrue("Cannot find any `Wallet` object." in logger.err_msg)

    # def test_is_not_running_not_keosd_set(self):
    #     l.COMMENT("""
    #     Check the condition that
    #     ``eosf.use_keosd(True)`` or the local testnet is running.
    #     """)

    #     eosf.use_keosd(False)
    #     eosf.stop(is_verbose=0)
    
    #     eosf.set_throw_error(False)
    #     ######################################################################

    #     eosf.set_is_testing_errors()
    #     logger = account_master_create("account_master") 
    #     self.assertTrue(
    #         "Cannot use the local node Wallet Manager if the node is not running." \
    #             in logger.err_msg)

    # def test_testnet_create_account(self):
    #     l.COMMENT("""
    #     If the local testnet is running, ``account_master_create(<test object name>)``
    #     puts the created account object into the global namespace, and puts the
    #     account into the wallet.

    #     With the local testnet, the name of the master account is ``eosio``.
    #     """)

    #     eosf.use_keosd(False)
    #     eosf.reset(is_verbose=0)
    #     wallet = Wallet()

    #     eosf.set_throw_error(False)
    #     ######################################################################
        
    #     l.COMMENT("""
    #     With the local testnet, the name of the master account is ``eosio``:
    #     """)        
    #     account_master_create("account_master")
    #     self.assertTrue(account_master.name == "eosio")
    #     l.COMMENT("""
    #     Wallet keys:
    #     """)         
    #     wallet.keys()
    #     keys1 = wallet.wallet_keys.json

    #     l.COMMENT("""
    #     With the local testnet, the wallet passwords are stored in a file.
    #     Let us restart the testnet and restore the wallet:
    #     """)

    #     eosf.stop(is_verbose=0)
    #     eosf.run(is_verbose=0)
    #     wallet = Wallet()
    #     l.COMMENT("""
    #     Wallet keys:
    #     """)           
    #     wallet.keys()
    #     keys2 = wallet.wallet_keys.json

    #     l.COMMENT("""
    #     Assert that key lists are equal.
    #     """)
    #     self.assertTrue(keys1 == keys2)


    # def test_testnet_create_account(self):
    #     if not_imputed:
    #         return
    
    #     l.COMMENT("""
    #     If the ``name`` argument is set, check the testnet for presence of the 
    #     account. If present, create the corresponding object and see whether it
    #     is in the wallets. If so, put the account object into the global namespace 
    #     of the caller.
    #     """)
    #     eosf.use_keosd(True)
    #     setup.set_nodeos_address(cryptolions)
    #     wallet = Wallet(
    #         "default",
    #         "PW5J5KW7erKzqJmn9gMrvzev4pLxR3Vt9BRkx94BqdfHkw4z4bNTd"
    #         )

    #     eosf.set_throw_error(False)
    #     ######################################################################
        
    #     account_master_create("account_master")

    # def test_is_do_not_exist_error(self):
    #     l.COMMENT("""
    #     The cleos ``get account`` command returns a not specific error responce when
    #     the given name is found. Probably, it may change, therefore is to be tested. 
    #     """)
    #     eosf.use_keosd(False)
    #     eosf.reset(is_verbose=0)
    #     eosf.set_throw_error(False)
    #     ######################################################################
    #     get_account = cleos.GetAccount("hwtsfwytrwty")
    #     l.EOSF("""
    #     The original error message is
    #     {}
    #             Next, it follows this message formatted:
    #     """.format(get_account.err_msg))
    #     self.assertTrue(eosf_account.is_do_not_exist_error(get_account, l))    

    def test_testnet_create_account(self):
        if not_imputed:
            return
            
        l.COMMENT("""
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
        """)
        eosf.use_keosd(True)
        setup.set_nodeos_address(cryptolions)
        wallet = Wallet(
            "default",
            "PW5J5KW7erKzqJmn9gMrvzev4pLxR3Vt9BRkx94BqdfHkw4z4bNTd"
            )

        wallet.remove_key("EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959")
        wallet.remove_key("EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv")
        wallet.keys()
        eosf.set_throw_error(False)
        ######################################################################
        
        account_master_create("account_master", "dgxo1uyhoytn",
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
