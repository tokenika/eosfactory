import json
import time
from termcolor import colored, cprint
import setup
import eosf

cprint("""
Use `eosf.use_keosd(False)` instruction, then the wallets are not
managed by the EOSIO keosd and, hence, can be safely manipulated.

If `setup.set_verbose(True)`, print the response messages of the
issued commands.
""", 'magenta')

eosf.use_keosd(False)
setup.set_verbose(True)
#setup.set_command_line_mode()


def test():

    cprint("""
Start a local test EOSIO node, use `eosf.reset([eosf.Verbosity.TRACE])`:
    """, 'magenta')

    reset = eosf.reset([eosf.Verbosity.TRACE])
        
    cprint("""
Create a local wallet, use `wallet = eosf.Wallet()`:
    """, 'magenta')

    wallet = eosf.Wallet(is_verbose=2)

    account_master = eosf.AccountMaster()

    cprint("wallet.import_key(account_master):", 'magenta')
    wallet.import_key(account_master)

    account_bill = eosf.account()
    cprint("wallet.import_key(account_bill):", 'magenta')
    wallet.import_key(account_bill)

    cprint("wallet.import_key(alice):", 'magenta')
    account_alice = eosf.account()
    wallet.import_key(account_alice)

    return


if __name__ == "__main__":
    test()