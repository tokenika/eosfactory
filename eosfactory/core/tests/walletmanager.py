import unittest
import time

import eosfactory.core.setup as setup
import eosfactory.core.eosjs as eosjs
from eosfactory.eosf import *
from eosfactory.core.walletmanager import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])
wallet_name = "test_wallet"
second_wallet = "second_wallet"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        TRACE('''
==============================================================================
===============================================================================
        ''')

    def test_import_key(self):
        SCENARIO('''
        Given a wallet and a key pair, import keys to the wallet. 
        
        List private and public keys stored in the wallet and compare them with the
        imported key pair.
        ''')

        delete(wallet_name, is_verbose=False)
        wallet = Create(wallet_name, is_verbose=False)

        COMMENT('''Create key pair:''')
        owner_key = eosjs.CreateKey()

        COMMENT('''Import key:''')
        import_key(wallet, owner_key)

        COMMENT('''
        Get private keys. The first one is the wallet manager ID.
        ''')
        private_keys_ = private_keys(wallet)
        self.assertTrue(private_keys_[1] == owner_key.key_private)

        COMMENT('''
        Get public keys. The first one is the wallet manager ID.
        ''')
        keys_ = keys(wallet)
        self.assertTrue(keys_[1] == owner_key.key_public)


    def test_wrong_password(self):
        delete(wallet_name, is_verbose=False)
        wallet = Create(wallet_name)

        SCENARIO('''
        Given a wallet, lock it, and unlock with the password received at the craetion
        time.
        ''')

        COMMENT('''
        Get public keys. The first one is the wallet manager ID.
        ''')
        keys(wallet)
        lock_all()

        COMMENT('''
        As the wallet is locked, keys cannot be listed:
        ''')
        with self.assertRaises(Error) as cm:
            keys(wallet)
        print(cm.exception.message)

        COMMENT('''
        As the password is wrong, wallet cannot be unlocked:
        ''')
        with self.assertRaises(Error) as cm:      
            unlock(wallet, "TbVJIaTC76vUo8RQ_5EPQIsWkBIZbxlKSxhY7qXN0rQ=")
        print(cm.exception.message)

        COMMENT('''
        Now, use the right password to unlock and list keys:
        ''')
        unlock(wallet)
        keys(wallet)

    def test_wallet_reopen(self):
        delete(wallet_name, is_verbose=False)
        wallet = Create(wallet_name)

        COMMENT('''Create key pair:''')
        owner_key = eosjs.CreateKey()

        COMMENT('''Import key:''')
        import_key(wallet, owner_key)
        keys_ = keys(wallet)
        
        COMMENT('''
        Stop the wallet manager, erase existing wallet objects:
        ''')
        stop()

        COMMENT('''
        Restote the wallet object from its ciphered file, using the stored password. See 
        whether the imported keys are in place still:
        ''')
        wallet_restored = Create(wallet_name, wallet.password)
        self.assertTrue(keys_ == keys(wallet_restored))

    def test_timeover(self):
        delete(wallet_name, is_verbose=False)
        
        wallet = Create(wallet_name)

        COMMENT('''
        Shorten the 'timeover` setting of the wallet manager, wait a time to pass it, 
        and try listing keys:
        ''')
        setTimeout(5)
        unlock(wallet)
        setTimeout(300)
        time.sleep(8)
        with self.assertRaises(Error) as cm:
            keys(wallet_name)
        print(cm.exception.message)

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
