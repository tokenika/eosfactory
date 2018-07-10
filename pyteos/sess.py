#!/usr/bin/python3

"""
Session initiation and storage for session elements.

.. module:: sess
    :platform: Unix, Windows
    :synopsis: Session initiation and storage for session elements.

.. moduleauthor:: Tokenika

"""

import setup
import eosf


def init():
    """
    Initialise a test session.

    - **global variables**::

        eosio: The primary EOSIO account predefined in the genesis file.

        alice, bob, carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.

        wallet: The wallet holding keys.

        On error, return False.
    """

    global wallet
    global eosio
    global alice
    global bob
    global carol

    wallet = eosf.Wallet()

    eosio = eosf.AccountMaster()
    wallet.import_key(eosio)
    
    alice = eosf.account(eosio, "alice")
    wallet.import_key(alice)
    
    bob = eosf.account(eosio, "bob")
    wallet.import_key(bob)
    
    carol = eosf.account(eosio, "carol")
    wallet.import_key(carol)

    eosf.Contract(eosio, "eosio.bios").deploy()

    if setup.is_verbose():
        print("#  Available test accounts: " 
            + eosio.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name + "\n")
