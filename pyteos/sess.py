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
import eosf


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
    global wallet
    global alice
    global bob
    global carol

    wallet = eosf.Wallet()

    account_eosio = cleos.AccountEosio()
    wallet.import_key(account_eosio)
    
    contract_eosio_bios = cleos.SetContract(account_eosio, "eosio.bios")
    alice = eosf.Account()
    wallet.import_key(alice)
    bob = eosf.Account()
    wallet.import_key(bob)
    carol = eosf.Account()
    wallet.import_key(carol)

    if setup.is_verbose():
        print("#  Available test accounts: " 
            + account_eosio.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name + "\n")
