#!/usr/bin/python3

"""
Session initiation and storage for session elements.

.. module:: sess
    :platform: Unix, Windows
    :synopsis: Session initiation and storage for session elements.

.. moduleauthor:: Tokenika

"""

import pyteos

def init():
    """
    Initialise a test session.

    - **global variables**::

        eosio: The primary EOSIO account predefined in the genesis file.

        alice, bob, carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.

        wallet: The wallet holding keys.
    """
    error = False

    global eosio
    eosio = pyteos.AccountEosio(is_verbose=False)
    error = error and eosio.error
    if error:
        return

    global wallet
    wallet = pyteos.Wallet(is_verbose=False)
    error = error and wallet.error
    if error:
        return

    contract_eosio_bios = pyteos.SetContract(
        eosio, "eosio.bios", permission=eosio, is_verbose=False)
    error = error and contract_eosio_bios.error
    if error:
        return

    global key_owner
    key_owner = pyteos.CreateKey("key_owner", is_verbose=False)
    error = error and key_owner.error
    if error:
        return
    
    global key_active
    key_active = pyteos.CreateKey("key_active", is_verbose=False)
    error = error and key_active.error
    if error:
        return

    result = wallet.import_key(key_owner)
    error = error and not result
    result =  wallet.import_key(key_active)
    error = error and result
    if error:
        return

    global alice
    alice = pyteos.Account(
        eosio, "alice", key_owner, key_active, is_verbose=False)    
    error = error and alice.error
    if error:
        return

    global bob
    bob = pyteos.Account(
        eosio, "bob", key_owner, key_active, is_verbose=False)
    error = error and bob.error
    if error:
        return            
            
    global carol
    carol = pyteos.Account(
        eosio, "carol", key_owner, key_active, is_verbose=False)
    error = error and carol.error
    if error:
        return

    if pyteos.is_verbose():
        print("#  Available test accounts: " 
            + eosio.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name)
