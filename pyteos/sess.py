#!/usr/bin/python3

""" 
This is a collection of EOSFactory session elements
"""

import pyteos

def init():
    """
    Initialise a test session.

    - **global variables**

        eosio: Primary EOSIO account predefined in the genesis file

        wallet: The wallet holding keys
        
        alice, bob, carol: Prefabricated demo accounts
    """
    global eosio
    eosio = pyteos.AccountEosio()

    global wallet
    wallet = pyteos.Wallet()

    contract_eosio_bios = pyteos.SetContract(
        eosio, "eosio.bios", permission=eosio)
    key_owner = pyteos.CreateKey("key_owner")
    key_active = pyteos.CreateKey("key_active")

    wallet.import_key(key_owner)
    wallet.import_key(key_active)

    global alice
    alice = pyteos.Account(
        eosio, "alice", key_owner, key_active)    
        
    global bob
    bob = pyteos.Account(
        eosio, "bob", key_owner, key_active)
            
    global carol
    carol = pyteos.Account(
        eosio, "carol", key_owner, key_active)

