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

        alice, bob, carol: Prefabricated demo accounts.

        key_owner, key_active: Cryptographic keys.

        wallet: The wallet holding keys.

        On error, return False.
    """

    global account_master
    global wallet
    global alice
    global bob
    global carol

    wallet = eosf.Wallet()

    account_master = eosf.AccountMaster()
    wallet.import_key(account_master)
    
    contract_eosio_bios = eosf.Contract(
        account_master, "eosio.bios").deploy()
    alice = eosf.account()
    wallet.import_key(alice)
    bob = eosf.account()
    wallet.import_key(bob)
    carol = eosf.account()
    wallet.import_key(carol)

    if setup.is_verbose():
        print("#  Available test accounts: " 
            + account_master.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name + "\n")
