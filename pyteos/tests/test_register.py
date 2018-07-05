import setup
import eosf
from termcolor import cprint


setup.set_verbose(True)
setup.use_keosd(True)
setup.set_nodeos_URL("88.99.97.30:38888")  


def test():
    """
Creating wallet: default
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5KftuwFePUSaqrq2d8ZcEtJZYQCsWPE5gyo6DMBEcSUeb646coy"
    """
    """
Use the following data to register a new account on a public testnet:
Accout Name: gpdwptppwhs3
Owner Public Key: EOS8Lg58cfq8sZswvj6jfMQfngsvHjiLuj6MpNna66PM1mUMPZiXd
Owner Private Key: 5KhXVUvYd5o3sGoZL8usGNBFauLsYTWtdmzHck1GTCVhNJhoAtJ
Active Public Key: EOS5z8pbMiugbJ5nSBxpQggqhwUFYmHwtxka9f5J8QKXBEn4xE3B6
Active Private Key: 5HuW65NGrGCQuRKz4SivsCA9JdENUcE91pFYB5TYNUkqm62VeRV
    """

    global account_master

    wallet_name = "default"
    wallet_pass = "PW5KftuwFePUSaqrq2d8ZcEtJZYQCsWPE5gyo6DMBEcSUeb646coy"
    
    wallet = eosf.Wallet(wallet_name, wallet_pass)

    wallet.index()
    wallet.keys()

    restored = wallet.restore_accounts(globals())

    if (not "account_master" in restored):
        account_master = eosf.AccountMaster()
        wallet.import_key(account_master)
    else:
        cprint("\nThe 'account_master' is already in the wallet.\n", 'green')


if __name__ == "__main__":
    test()
