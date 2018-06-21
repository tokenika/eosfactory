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
    account_eosio = cleos.AccountEosio()

    global wallet
    wallet = eosf.Wallet()
    if wallet.error:
        print("Wallet error.")

    contract_eosio_bios = cleos.SetContract(account_eosio, "eosio.bios")
    if contract_eosio_bios.error:
        print("eosio.bios set contract error.")

    global alice
    alice = cleos.AccountLT()
    if alice.error:
        print("alice account error.")
        return False

    ok = wallet.import_key(alice)
    if not ok:
        print("wallet.import_key error.")
        return False

    global bob
    bob = cleos.AccountLT()
    if bob.error:
        print("bob account error.")
        return False
    ok = wallet.import_key(bob)

    global carol
    carol = cleos.AccountLT()
    if carol.error:
        print("carol account error.")
        return False
    ok = wallet.import_key(carol)

    if setup.is_verbose():
        print("#  Available test accounts: " 
            + account_eosio.name + ", "  
            + alice.name + ", " + carol.name + ", " + bob.name + "\n")
    return True
