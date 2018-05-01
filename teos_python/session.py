#!/usr/bin/python3

""" 
This is a collection of macros made of elements of the teos module, intent 
for experiments with EOSIO smart contracts. 
"""

import teos
import pathlib

def init():
    """
    Initialise a test session.

    - **global variables**

        account_eosio: Primary owned account.
        wallet: The wallet.
        allice, bob, carol: Prefabricated accounts.

    """
    global account_eosio
    account_eosio = teos.AccountEosio()

    global wallet
    wallet = teos.Wallet()

    contract_eosio_bios = teos.SetContract(
        account_eosio, "eosio.bios", permission=account_eosio)
    key_owner = teos.CreateKey("key_owner")
    key_active = teos.CreateKey("key_active")

    wallet.import_key(key_owner)
    wallet.import_key(key_active)

    global alice
    alice = teos.Account(
        account_eosio, "alice", key_owner, key_active)    
        
    global bob
    bob = teos.Account(
        account_eosio, "bob", key_owner, key_active)
            
    global carol
    carol = teos.Account(
        account_eosio, "carol", key_owner, key_active)

class Contract(teos.Contract):
    """
    Given a contract directory defining WAST and ABA, creates a contract.

    This class extends the teos.Contract: it goes without the `account`
    parameter, instead it uses an account created internally.

    - **parameters**
        contract_dir: A contract directory, structures according to the 
            `contract template', that means, including the `build' directory
            that contains WAST and ABI.
        wast_file: The file containing the contract WAST, relative 
            to contract-dir, defaults to "".
        abi_file: The file containing the contract ABI, relative 
            to contract-dir, defaults to "".
        permission: An account object or the name of an account that 
            authorizes the creation.
        expiration_sec: The time in seconds before a transaction expires, 
            defaults to 30s.
        skip_signature:  If unlocked wallet keys should be used to sign 
            transaction, defaults to 0.
        dont_broadcast: Whether to broadcast transaction to the network (or 
            print to stdout), defaults to 0.
        forceUnique: Whether to force the transaction to be unique, what will 
            consume extra bandwidth and remove any protections against 
            accidently issuing the same transaction multiple times, defaults 
            to 0.
        max_cpu_usage: An upper limit on the cpu usage budget, in 
            instructions-retired, for the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: An upper limit on the net usage budget, in bytes, for 
            the transaction (defaults to 0 which means no limit). 

    The extended constructor adds the following attributes:

    - **attributes**
        name: The name of contract`s account. It has the value of the last
            part of the contract directory path.
        key_owner: A key object.
        key_active: Another key object.
        account: The account that owns the contract.
    """
    def __init__(self, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True):
        contract_path = pathlib.Path(contract_dir)
        self.name = contract_path.parts[-1]
        self.key_owner = teos.CreateKey("key_owner")
        self.key_active = teos.CreateKey("key_active")

        global wallet
        wallet.import_key(self.key_owner)
        wallet.import_key(self.key_active)
        
        global account_eosio
        self.account = teos.Account(
            account_eosio, self.name, self.key_owner, self.key_active)
        super().__init__(self.account, contract_dir, 
            wast_file, abi_file, 
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            is_verbose)


