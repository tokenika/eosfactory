import os
import unittest
import setup
import eosf
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, \
    eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)

cryptolions = "88.99.97.30:38888"
_ = eosf.Logger()

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
        eosf.set_is_testing_errors(False)
        eosf.set_throw_error(True)

    def test_create_keosd_wallet(self):
        _.SCENARIO("""
Test registering to a remote testnet.
Set-up: 
    * delete existing, if any, wallet named ``jungle_wallet`` using
        a general procedure as the EOSFactory does not have any;
    * set KEOSD as the Wallet Manager;
    * set the URL of a remote testnet;
    * stop the KEOSD Wallet Manager.
    * create a wallet named ``jungle_wallet``;
        Expected result is that a password message is printed.
        """)

        eosf.use_keosd(True)
        setup.set_nodeos_address(cryptolions)
        eosf.kill_keosd()

        wallet_name = "jungle_wallet"
        try:
            os.remove(eosf.wallet_dir() + wallet_name + ".wallet")
        except:
            pass

        wallet = Wallet(wallet_name)
        eosf_account.account_master_test = eosf_account.AccountMaster(
            "dgxo1uyhoytn", 
            "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
            "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
        )
        if(eosf_account.account_master_test.error):
            print("""
The test assumes that you kno an account on the testnet, that is, you know
* account name;
* account owner key private;
* account active key private.

The data that you have specified in the above definition of the 
``AccountMaster`` object are wrong.

Cannot continue.
            """)
            return

        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()        
        ######################################################################

        account_master_create("account_master")


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()        