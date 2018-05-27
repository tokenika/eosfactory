#!/usr/bin/python3

"""
Session initiation and storage for session elements.

.. module:: sess
    :platform: Unix, Windows
    :synopsis: Session initiation and storage for session elements.

.. moduleauthor:: Tokenika

"""

import pyteos

def setup():
    """
    Initialise a test session.

    - **global variables**::

        eosio: The primary EOSIO account predefined in the genesis file.

        alice, bob, carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.

        wallet: The wallet holding keys.

        On error, return False.
    """

    global eosio
    eosio = pyteos.AccountEosio()
    if eosio.error:
        print("AccountEosio error.")
        return False

    global wallet
    wallet = pyteos.Wallet()
    if wallet.error:
        print("Wallet error.")
        return False

    contract_eosio_bios = pyteos.SetContract(
        eosio, "eosio.bios", permission=eosio )
    if contract_eosio_bios.error:
        print("eosio.bios set contract error.")
        return False

    global key_owner
    key_owner = pyteos.CreateKey("key_owner" )
    if key_owner.error:
        print("key_owner error.")
        return False
    
    global key_active
    key_active = pyteos.CreateKey("key_active", )
    if key_active.error:
        print("key_active error.")
        return False

    ok = wallet.import_key(key_owner) and wallet.import_key(key_active)
    if not ok:
        print("wallet.import_key error.")
        return False

    global alice
    alice = pyteos.Account(
        eosio, "alice", key_owner, key_active)    
    if alice.error:
        print("alice account error.")
        return False

    global bob
    bob = pyteos.Account(
        eosio, "bob", key_owner, key_active)
    if bob.error:
        print("bob account error.")
        return False            
            
    global carol
    carol = pyteos.Account(
        eosio, "carol", key_owner, key_active)
    if carol.error:
        print("carol account error.")
        return False

    if pyteos.is_verbose():
        print("#  Available test accounts: " 
            + eosio.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name + "\n")
    return True
