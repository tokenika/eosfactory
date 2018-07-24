import unittest
import setup
import eosf
import time
import eosf_account

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create


eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT])
# eosf.set_verbosity_plus([eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)
#setup.set_command_line_mode()

cryptolions = "88.99.97.30:38888"
not_imputed = False
_ = eosf.Logger()

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
        eosf.set_throw_error(True)


    # def test_too_many_wallets(self):
    #     _.COMMENT("""
    #     Check the condition that
    #     precisely one ``Wallet`` object is defined when calling the 
    #         ``account_master_create(...)`` function.
    #     """)        
    #     eosf.use_keosd(False)
    #     eosf.reset([eosf.Verbosity.TRACE])
    #     wallet = Wallet()
    #     eosf.set_throw_error(False)
    #     eosf.set_is_testing_errors()
    #     ######################################################################
    #     _.COMMENT("""
    #     Added second wallet, named "second". Calling the ``account_master_create(...)`` 
    #     function should result in an error message:
    #     """)   
    #     wallet1 = Wallet("second")
    #     self.assertTrue("It can be only one" in wallet1.logger.err_msg)

    # def test_global_namespace1(self):
    #     _.COMMENT("""
    #     Check the condition that
    #     precisely one ``Wallet`` object is defined when calling the 
    #         ``account_master_create(...)`` function.
    #     """)
    #     eosf.use_keosd(False)
    #     eosf.reset([eosf.Verbosity.TRACE])
    #     eosf.set_throw_error(False)
    #     eosf.set_is_testing_errors()
    #     ######################################################################

    #     logger = account_master_create("account_master")
    #     self.assertTrue("Cannot find any `Wallet` object." in logger.err_msg)

    def test_account_name_conflict(self):
        if not_imputed:
            return

        eosf.use_keosd(False)
        eosf.reset([eosf.Verbosity.TRACE]) 
        wallet = Wallet()
        account_master_create("account_master")
        account_master.info()
        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()
        ######################################################################

        _.COMMENT("""
        As the ``account_master`` object is in the namespace, create two account
        objects: 
        ``account_alice`` and ``account_carrol``.
        Then try to create another account object called ``account_alice``. Although
        this object is going to refer to a new blockchain account, it cannot accept
        the given name: error is issued.

        You are prompted to change the blocking name. Change it to 
        ``account_alice_b``.
        """)
        account_create("account_alice", account_master)
        account_create("account_carrol", account_master)
        account_create("account_alice", account_master)
        wallet.keys()

        # print(account_alice.info())

        
        # print("The name attribute of the 'account_carrol' account object is '{}'" \
        #     .format(account_carrol))
        # print("{}".format(account_carrol.code()))

        # account_create("account_alice")
        # self.assertTrue(account_alice.error)

        # account_create("account_test")
        # contract_test = eosf.Contract(account_test, "eosio.token")
        # deploy = contract_test.deploy()
        # account_test.code()

        # time.sleep(1)

        # action = account_test.push_action(
        #     "create", 
        #     '{"issuer":"' 
        #         + str(account_master) 
        #         + '", "maximum_supply":"1000000000.0000 EOS", \
        #         "can_freeze":0, "can_recall":0, "can_whitelist":0}')

        # action = contract_test.push_action(
        # "issue", 
        # '{"to":"' + str(account_alice)
        #     + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
        #     account_master)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
