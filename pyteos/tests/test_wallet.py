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
    setup.set_nodeos_URL("dev.cryptolions.io:38888")
    #setup.set_debug_mode()    
    cleos.WalletStop()

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
Accout Name: nfldugwdvcb5
Owner Public Key: EOS5qxcKNeALwjHryCrbbhaHDy9CS1Fj5JQ7HikArb7VVNhpJoRys
Active Public Key: EOS85aw98yY3XZR4hcjjijprog2zAGdDMZFhsbVrAESzXFRRzbsNZ


Owner Private Key: 5JeGvwGC1FNyNdY8vjLmJqXajWf48aw1cpYJVaHboEXES81NgyH
Active Private Key: EOS85aw98yY3XZR4hcjjijprog2zAGdDMZFhsbVrAESzXFRRzbsNZ
        """, 'magenta')

        cprint("""
              
        """, 'magenta')

        wallet.import_key(account_master)

    else:
##############################################################################
# Registered to a testnode
##############################################################################
        #setup.set_debug_mode()
        #wallet.import_key(account_master)
        key_owner = cleos.CreateKey(
            "owner",
            "EOS5qxcKNeALwjHryCrbbhaHDy9CS1Fj5JQ7HikArb7VVNhpJoRys",
            "5JeGvwGC1FNyNdY8vjLmJqXajWf48aw1cpYJVaHboEXES81NgyH")

        key_active = cleos.CreateKey(
            "active",
            "EOS5qxcKNeALwjHryCrbbhaHDy9CS1Fj5JQ7HikArb7VVNhpJoRys",
            "5JeGvwGC1FNyNdY8vjLmJqXajWf48aw1cpYJVaHboEXES81NgyH")
            
        account_master = cleos.AccountMaster(
            "nfldugwdvcb5",
            "EOS5qxcKNeALwjHryCrbbhaHDy9CS1Fj5JQ7HikArb7VVNhpJoRys",
            "EOS85aw98yY3XZR4hcjjijprog2zAGdDMZFhsbVrAESzXFRRzbsNZ"
        )

        print(account_master.account())

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



#     cprint("""
# Restoration of the accounts is important when working with remote EOSIO nodes.
# Switch a remote node `54.38.137.99:8888`:
#     """, 'magenta')

#     cleos.dont_keosd(False)
#     setup.set_nodeos_URL("54.38.137.99:8888")
#     cleos.WalletStop()
#     setup.set_debug_mode()

#     wallet_name = "tokenika"
#     wallet = eosf.Wallet(wallet_name)

#     cprint("""
# Restoration of the accounts is important when working with remote EOSIO nodes.
# Switch a remote node `54.38.137.99:8888`:
#     """, 'magenta')
    # tokenika_pass = "PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ"
    # return
    # account_master = cleos.AccountMaster()
#     cprint("""
# We have got the following message:

# SAVE THE FOLLOWING DATA to use in the future to restore thisaccount object.
# Accout Name: upe1ahhgb3xq
# Owner Public Key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
# Active Public Key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP

# >>> print(account_master.owner_key)
# Private key: 5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp
# Public key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP

# >>> print(account_master.active_key)
# Private key: 5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp
# Public key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
#     """, 'magenta')



#     wallet = eosf.Wallet("tokenika", tokenika_pass)
#     # wallet.list()
#     # wallet.keys()
#     # wallet.open()
#     # wallet.unlock()
#     # wallet.import_key("5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp")
#     # 
#     return    
#     cleos.GetAccount("upe1ahhgb3xq")


#     wallet.restore_accounts(globals())

#     cprint("""
# Chose one item from the list of restored account objects. 
# If it is `play11111111`, then:
#     """, 'magenta')

#     print(play11111111.account())