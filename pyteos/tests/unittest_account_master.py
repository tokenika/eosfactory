import unittest
import setup
import eosf
import cleos
import time

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT])
#eosf.set_verbosity_plus([eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
#setup.set_command_line_mode()

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
        eosf.restart()
        eosf.set_is_testing_errors(False)

    def test_too_many_wallets(self):
        l.COMMENT("""
        Check the condition that
        precisely one ``Wallet`` object is defined when calling the 
            ``account_master_create(...)`` function.
        """)
        eosf.set_throw_error(True)
        eosf.use_keosd(False)
        eosf.reset(is_verbose=0)
        wallet = Wallet()
        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()
        ######################################################################

        wallet1 = Wallet("second")
        l.COMMENT("""
        Added second wallet, named "second". Calling the ``account_master_create(...)`` 
        function should result in an error message:
        """)        
        eosf.set_is_testing_errors()
        logger = account_master_create("account_master")
        self.assertTrue("Too many `Wallet` objects." in logger.err_msg)

    def test_there_is_no_wallet(self):
        l.COMMENT("""
        Check the condition that
        precisely one ``Wallet`` object is defined when calling the 
            ``account_master_create(...)`` function.
        """)
        eosf.set_throw_error(True)
        eosf.use_keosd(False)
        eosf.reset(is_verbose=0)
        eosf.set_throw_error(False)
        ######################################################################

        l.COMMENT("""
        There is not any ``Wallet`` object. Calling the ``account_master_create(...)`` 
        function should result in an error message:
        """)
        eosf.set_is_testing_errors()
        logger = account_master_create("account_master")        
        self.assertTrue("Cannot find any `Wallet` object." in logger.err_msg)

    def test_is_not_running_not_keosd_set(self):
        l.COMMENT("""
        Check the condition that
        ``eosf.use_keosd(True)`` or the local testnet is running.
        """)
        eosf.set_throw_error(True)

        eosf.use_keosd(False)
        eosf.stop(is_verbose=0)
    
        eosf.set_throw_error(False)
        ######################################################################

        eosf.set_is_testing_errors()
        logger = account_master_create("account_master") 
        self.assertTrue(
            "Cannot use the local node Wallet Manager if the node is not running." \
                in logger.err_msg)

    def test_testnet_create_account(self):
        l.COMMENT("""
        If the local testnet is running, ``account_master_create(<test object name>)``
        puts the created account object into the global namespace, and puts the
        account into the wallet.

        With the local testnet, the name of the master account is ``eosio``.
        """)
        eosf.set_throw_error(True)

        eosf.use_keosd(False)
        eosf.reset(is_verbose=0)
        wallet = Wallet()

        eosf.set_throw_error(False)
        ######################################################################
        
        l.COMMENT("""
        With the local testnet, the name of the master account is ``eosio``:
        """)        
        account_master_create("account_master")
        self.assertTrue(account_master.name == "eosio")
        l.COMMENT("""
        Wallet keys:
        """)         
        wallet.keys()
        keys1 = wallet.wallet_keys.json

        l.COMMENT("""
        With the local testnet, the wallet passwords are stored in a file.
        Let us restart the testnet and restore the wallet:
        """)

        eosf.stop(is_verbose=0)
        eosf.run(is_verbose=0)
        wallet = Wallet()
        l.COMMENT("""
        Wallet keys:
        """)           
        wallet.keys()
        keys2 = wallet.wallet_keys.json

        l.COMMENT("""
        Assert that key lists are equal.
        """)
        self.assertTrue(keys1 == keys2)


    def test_testnet_create_account(self):
        if not_imputed:
            return
        l.COMMENT("""
        If the ``name`` argument is set, check the testnet for presence of the 
        account. If present, create the corresponding object and see whether it
        is in the wallets. If so, put the account object into the global namespace 
        of the caller. and **return**.
        """)
        eosf.set_throw_error(True)
        eosf.use_keosd(True)
        setup.set_nodeos_address(cryptolions)
        wallet = Wallet(
            "default",
            "PW5J5KW7erKzqJmn9gMrvzev4pLxR3Vt9BRkx94BqdfHkw4z4bNTd"
            )

        eosf.set_throw_error(False)
        ######################################################################
        
        account_master_create("account_master", "nbhyi5exmjcl")



        # wallet.keys()
        # info = account_master.info()
        # print(info)

        # l.COMMENT("""
        # Assert that the info is well-formed.
        # """)
        # self.assertTrue(
        #     "total staked delegated to account from others" in info)

        


    # def test_restore_testnet_account(self):
    #     setup.set_nodeos_address(cryptolions)
    #     eosf.use_keosd(True)
    #     wallet = Wallet(
    #         "default", 
    #         "PW5JhJKaibFbv1cg8sPQiCtiGLh5WP4FFWFeRqXANetKeA8XKn31N")
    #     ######################################################################

    #     account_master_create("account_master", "nbhyi5exmjcl")
    #     # print(account_master.info())



    # def test_usage(self):
    #     eosf.use_keosd(False)
    #     eosf.reset(is_verbose=0)
    #     wallet = Wallet()
    #     account_master_create("account_master")
    #     ######################################################################

    #     account_create("account_alice", account_master)
    #     print(account_alice.info())

    #     account_create("account_carrol")
    #     print("The name attribute of the 'account_carrol' account object is '{}'" \
    #         .format(account_carrol))
    #     print("{}".format(account_carrol.code()))

    #     account_create("account_alice")
    #     self.assertTrue(account_alice.error)

    #     account_create("account_test")
    #     contract_test = eosf.Contract(account_test, "eosio.token")
    #     deploy = contract_test.deploy()
    #     account_test.code()

    #     time.sleep(1)

    #     action = account_test.push_action(
    #         "create", 
    #         '{"issuer":"' 
    #             + str(account_master) 
    #             + '", "maximum_supply":"1000000000.0000 EOS", \
    #             "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    #     action = contract_test.push_action(
    #     "issue", 
    #     '{"to":"' + str(account_alice)
    #         + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
    #         account_master)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
