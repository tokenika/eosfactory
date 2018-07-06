import setup
import eosf
from termcolor import cprint

setup.set_verbose(True)

def test():
    global wallet
    wallet = eosf.Wallet()
    # wallet1 = eosf.Wallet("xxx")
    #print(type(wallet))
    eosf.account_object("account_test")
    # print(account_test)

if __name__ == "__main__":
    test()
