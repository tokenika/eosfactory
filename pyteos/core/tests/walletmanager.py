import unittest
from eosf import *
from core.walletmanager import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE])
wallet_name = "test_wallet"
second_wallet = "second_wallet"

class Test(unittest.TestCase):

    def test(self):
        COMMENT('''
        
        ''')
        delete(wallet_name)
        delete(second_wallet)
        COMMENT('''Create wallet:''')
        wallet = Create(wallet_name)
        COMMENT('''Create another wallet:''')
        Create(second_wallet)
        # COMMENT('''List wallets. All wallets are open:''')
        # list()
        COMMENT('''Lock all wallets:''')
        lock_all()
        COMMENT('''List wallets. All wallets are closed:''')
        list()
        COMMENT('''Open one wallet:''')
        open_wallet(wallet_name)
        COMMENT('''List wallets. One wallet is opened:''')
        list()
        COMMENT('''Get private keys: they are ciphered:''')
        private_keys(wallet_name)

        


if __name__ == "__main__":
    unittest.main()
