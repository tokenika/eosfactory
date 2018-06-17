# python3 ./tests/test1.py

import setup
import cleos
import teos

def run():

    print("test dont_keosd ------------------------")
    cleos.dont_keosd()
    print("----------------------------------------")
    
    print("test node_reset ------------------------")
    teos.node_reset()
    print("----------------------------------------")

    print("test WalletCreate ----------------------")
    cleos.WalletCreate()
    print("----------------------------------------")

    print("test WalletList ------------------------")
    wallet_list = cleos.WalletList()
    print(wallet_list.json)
    print("----------------------------------------")

    print("test CreateKey -------------------------")
    key_owner = cleos.CreateKey("owner")
    print(key_owner.json)
    print(key_owner.key_private)
    print(key_owner.key_public)
    print("----------------------------------------")

    print("test WalletImport ----------------------")
    wallet_import = cleos.WalletImport(key_owner)
    print(wallet_import.key_private)
    print("----------------------------------------")


if __name__ == "__main__":
    run()