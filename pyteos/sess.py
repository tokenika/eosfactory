#!/usr/bin/python3

""" 
This is a collection of EOSFactory session elements
"""

import pyteos

def init():
    """
    Initialise a test session.

    - **global variables**

        eosio: Primary EOSIO account predefined in the genesis file.

        wallet: The wallet holding keys.
        
        alice, bob, carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.
    """
    global eosio
    eosio = pyteos.AccountEosio(is_verbose=False)

    global wallet
    wallet = pyteos.Wallet(is_verbose=False)

    contract_eosio_bios = pyteos.SetContract(
        eosio, "eosio.bios", permission=eosio, is_verbose=False)

    global key_owner
    key_owner = pyteos.CreateKey("key_owner", is_verbose=False)
    global key_active
    key_active = pyteos.CreateKey("key_active", is_verbose=False)

    wallet.import_key(key_owner)
    wallet.import_key(key_active)

    global alice
    alice = pyteos.Account(
        eosio, "alice", key_owner, key_active, is_verbose=False)    
        
    global bob
    bob = pyteos.Account(
        eosio, "bob", key_owner, key_active, is_verbose=False)
            
    global carol
    carol = pyteos.Account(
        eosio, "carol", key_owner, key_active, is_verbose=False)

