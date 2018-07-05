import setup
import cleos
import eosf
from termcolor import cprint

setup.set_verbose(True)
setup.use_keosd(True)
setup.set_nodeos_URL("dev.cryptolions.io:38888")  

def test():

    cleos.WalletStop()

    wallet_name = "default"
    wallet_pass = "PW5JhJKaibFbv1cg8sPQiCtiGLh5WP4FFWFeRqXANetKeA8XKn31N"
    global account_master

    wallet = eosf.Wallet(wallet_name, wallet_pass)
    cprint("""
Creating wallet: default
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5JhJKaibFbv1cg8sPQiCtiGLh5WP4FFWFeRqXANetKeA8XKn31N"
    """, 'magenta')

    wallet.index()
    wallet.keys()

    restored = wallet.restore_accounts(globals())
    print()
    print(account_master.info())

    global account_alice

    if "account_alice" in restored:
        print(account_alice.info())
    else:

        cprint("""
./programs/cleos/cleos -u http://"dev.cryptolions.io:38888 system newaccount 
nbhyi5exmjcl ljzirxm1wy1n 
EOS6wAChSUxgHpUaG8bdCSKVFEMbmT85qnja1bh7zaWiYDp4sLW98 
EOS6wAChSUxgHpUaG8bdCSKVFEMbmT85qnja1bh7zaWiYDp4sLW98 
--buy-ram-kbytes 8 --stake-net '100 EOS' --stake-cpu '100 EOS' --transfer
        """, 'magenta')

        account_alice = eosf.account(
            account_master,
            stake_net="100 EOS",
            stake_cpu="100 EOS",
            buy_ram_kbytes="8",
            transfer=True)
        if(not account_alice.error):
            wallet.import_key(account_alice)


    account_test = eosf.account(
                account_master,
                stake_net="10 EOS",
                stake_cpu="10 EOS",
                buy_ram_kbytes="8",
                transfer=True)

    print(account_test.info())
    cprint("""
name: yeyuoae5rtcg
permissions:
    owner     1:    1 EOS8jeCrY4EjJtvcveuy1aK2aFv7rqhGAGvGLJ2Sodazmv2yyi2hm
    active     1:    1 EOS5PD28JPyHALuRPPJnm1oR83KxLFKvKkVXx9VrsLjLieHSLq35j
    """, 'magenta')

    wallet.open()
    wallet.unlock()
    wallet.import_key(account_test)


if __name__ == "__main__":
    test()
