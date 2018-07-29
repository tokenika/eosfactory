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

"""
Accout Name: dgxo1uyhoytn
Owner Public Key: EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959
Active Public Key: EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv

Owner Private Key: 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY
Active Private Key: 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA 
"""

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
        eosf_account.account_master_test = eosf_account.GetAccount(
            "account_master_test",
            "dgxo1uyhoytn", 
            "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
            "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
        )
        eosf_account.account_master_test.ERROR()

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