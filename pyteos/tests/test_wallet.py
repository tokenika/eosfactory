# python3 ./tests/test1.py

import setup
import cleos
import teos
import eosf
import unittest
from termcolor import colored, cprint
import time

setup.set_verbose(True)
is_registered_to_testnode = True

def test():
    cleos.dont_keosd(False)
    setup.set_nodeos_URL("54.38.137.99:8888")
    #setup.set_debug_mode()    
    cleos.WalletStop()

    # wallet_name = "tokenika3"
    # wallet_pass = "PW5JJ3ZJW3G1ezbfb8K8JQq3m4DCiaZB4knU3f88BHpbtsviogui3"
    wallet_name = "default"
    wallet_pass = "PW5K7Vz63bEEjTTVvRQMTqB3JVvJ7sGUYoN1fwDqA246JayKuiwnh"

    wallet = eosf.Wallet(wallet_name, wallet_pass)
    cprint("""
Creating wallet: default
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5K7Vz63bEEjTTVvRQMTqB3JVvJ7sGUYoN1fwDqA246JayKuiwnh"
    """, 'magenta')

    wallet.list()
    wallet.keys()


    if not is_registered_to_testnode:
##############################################################################        
# Register to a testnode:
##############################################################################

        account_master = cleos.AccountMaster()
        cprint("""
Register the following data with a testnode and
save them to restore in the future this account object.
Accout Name: afvrbndbxh4a
Owner Public Key: EOS8SJnPZGg1FJMsEz6qUquJJgC1jpc1SpK6TkobVEs6WS92rBsPk
Active Public Key: EOS7vV5VknErRjmUfNUNS9ANeGRe7k9UvW3XF26isNN6PCmUrKoF7


Owner Private Key: 5Ka46WCASq9BoCZy6SPW5YughLSD4BMmkLtYYRkWpZpH3nK9tRW
Active Private Key: EOS7vV5VknErRjmUfNUNS9ANeGRe7k9UvW3XF26isNN6PCmUrKoF7
        """, 'magenta')

        cprint("""
              
        """, 'magenta')

        wallet.import_key(account_master)

##############################################################################
# Registered to a testnode
##############################################################################
    #setup.set_debug_mode()
    cleos.GetAccount("afvrbndbxh4a")

    #wallet.restore_accounts(globals())

    

    #cleos.WalletStop()    
    return    
    cleos.WalletUnlock(wallet_name, wallet_pass)





    wallet = eosf.Wallet(wallet_name, is_verbose=1)
    # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    # print(wallet.error)
    # print(wallet.err_msg)
    # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")

    wallet = eosf.Wallet(wallet_name, tokenika_pass)
    # wallet.list()
    # wallet.keys()
    # wallet.open()
    # wallet.unlock()
    # wallet.import_key("5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp")
    # 
    
    cleos.GetAccount("upe1ahhgb3xq")


    wallet.restore_accounts(globals())

    print(play11111111.account())

if __name__ == "__main__":
    test()