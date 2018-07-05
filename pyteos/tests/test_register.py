import setup
import eosf
from termcolor import cprint


setup.set_verbose(True)
setup.use_keosd(True)
setup.set_nodeos_URL("dev.cryptolions.io:38888")  


def test():
    global account_master

    wallet_name = "default"
    wallet_pass = "PW5KhZKX2jhmtJWKvUuSChuLE59BHAbFWgGhcsctoDw1Jy437APV3"
    
    wallet = eosf.Wallet(wallet_name, wallet_pass)
    cprint("""
Creating wallet: default
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5KhZKX2jhmtJWKvUuSChuLE59BHAbFWgGhcsctoDw1Jy437APV3"
    """, 'magenta')

    wallet.index()
    wallet.keys()

    restored = wallet.restore_accounts(globals())
    if (not "account_master" in restored):

        account_master = eosf.AccountMaster()
        cprint("""
Register the following data with a testnode, and
save them, to restore this account object in the future.
Accout Name: pb3ey3ikdi5j
Owner Public Key: EOS7SycZQs83yo5ziXdVvL7QeL1NguNeS39corGSbMVnxwEbweSYV
Active Public Key: EOS5uJB6cQ89nDzwPp3azDtcBRDLo6j4QcxEQ5DZRCBPPurCYywAk
Owner Private Key: 5HyPsQ3TJwma5mqideXtPwzLF8pUkioGy7r6xbDTtNysP9Rf4L4
Active Private Key: 5JZ6R6gz4e52atZwNGzS34KWRPkrjXfdcKGHTavKBiuKmHfe9Sv
        """, 'magenta')

        wallet.import_key(account_master)
    else:
        cprint("The 'account_master' is already in the wallet.", 'red')


if __name__ == "__main__":
    test()
