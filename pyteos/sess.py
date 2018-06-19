#!/usr/bin/python3

"""
Session initiation and storage for session elements.

.. module:: sess
    :platform: Unix, Windows
    :synopsis: Session initiation and storage for session elements.

.. moduleauthor:: Tokenika

"""

import setup
import teos
import cleos
import entities


def init():
    """
    Initialise a test session.

    - **global variables**::

        account_eosio: The primary EOSIO account predefined in the genesis file.

        alice, bob, carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.

        wallet: The wallet holding keys.

        On error, return False.
    """

    global account_eosio
    account_eosio = cleos.AccountEosio()

    global wallet
    wallet = entities.Wallet()
    if wallet.error:
        print("Wallet error.")
        return False

    contract_eosio_bios = cleos.SetContract(account_eosio, "eosio.bios")
    if contract_eosio_bios.error:
        print("eosio.bios set contract error.")
        return False

    global key_owner
    key_owner = cleos.CreateKey("key_owner" )
    if key_owner.error:
        print("key_owner error.")
        return False
    
    global key_active
    key_active = cleos.CreateKey("key_active", )
    if key_active.error:
        print("key_active error.")
        return False

    ok = wallet.import_key(key_owner) and wallet.import_key(key_active)
    if not ok:
        print("wallet.import_key error.")
        return False

    global alice
    alice = cleos.PrivateAccount(key_owner, key_active)    
    if alice.error:
        print("alice account error.")
        return False

    global bob
    bob = cleos.PrivateAccount(key_owner, key_active)
    if bob.error:
        print("bob account error.")
        return False            
            
    global carol
    carol = cleos.PrivateAccount(key_owner, key_active)
    if carol.error:
        print("carol account error.")
        return False

    if setup.is_verbose():
        print("#  Available test accounts: " 
            + account_eosio.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name + "\n")
    return True
