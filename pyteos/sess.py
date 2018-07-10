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

        account_master: The primary EOSIO account predefined in the genesis file.

        account_alice, account_bob, account_carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.

        wallet: The wallet holding keys.

        On error, return False.
    """

    global wallet
    global account_master
    global account_alice
    global account_bob
    global account_carol

    wallet = eosf.Wallet()

    account_master = eosf.AccountMaster()
    wallet.import_key(account_master)
    
    account_alice = eosf.account(account_master, "alice")
    wallet.import_key(account_alice)
    
    account_bob = eosf.account(account_master, "bob")
    wallet.import_key(account_bob)
    
    account_carol = eosf.account(account_master, "carol")
    wallet.import_key(account_carol)

    eosf.Contract(account_master, "eosio.bios").deploy()

    if setup.is_verbose():
        print("#  Available test accounts: " 
            + account_master.name + ", "  
            + account_alice.name + ", " + account_carol.name + ", " + account_bob.name + "\n")
