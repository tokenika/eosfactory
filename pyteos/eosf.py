#!/usr/bin/python3

"""
Macros made of elements of the :mod:`pyteos` module, intended for experiments with EOSIO smart-contracts.

.. module:: eosf
    :platform: Unix, Windows
    :synopsis: Macros made of elements of the `pyteos` module, intended for experiments with EOSIO smart-contracts.

.. moduleauthor:: Tokenika

"""

import pathlib
import pyteos
import sess
import re
import random
import shutil

class Contract(pyteos.Contract):
    """
    Creates a contract, given a contract directory containing WAST and ABI.

    This class extends the `pyteos.Contract`: it goes without the `account`
    parameter, instead it uses an account created internally.

    - **parameters**::

        contract_dir: A contract directory, structures according to the 
            *contract template*, that means, including the `build` directory
            that contains WAST and ABI.
        wast_file: The file containing the contract WAST, relative 
            to the *contract directory*, defaults to empty string.
        abi_file: The file containing the contract ABI, relative 
            to the *contract directory*, defaults to empty string.
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

    - **attributes**::

        name: The name of contract`s account. It has the value of the last
        part of the contract directory path.
        key_owner: A key object.
        key_active: Another key object.
        account: The account that owns the contract.
    """
    def __init__(
            self, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True):

        account_name = pathlib.Path(contract_dir).parts[-1]
        pattern = re.compile("^[a-z, ., 1-5]*$")
        if len(account_name) > 12 or not pattern.match(account_name):
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                       'q', 'r', 's', 't', 'u', 'v', 'w', 'x', \
                       'y', 'z', '.', '1', '2', '3', '4', '5']
            account_name = ""
            for i in range(0, 12):
                account_name += letters[random.randint(0, 31)]

        self.name = account_name

        account = pyteos.GetAccount(
            self.name, is_verbose=False, suppress_error_msg=True)

        if not account.error:
            self.account = account
        else:
            key_owner = pyteos.CreateKey("key_owner")
            key_active = pyteos.CreateKey("key_active")
            sess.wallet.import_key(key_owner)
            sess.wallet.import_key(key_active)
            self.account = pyteos.Account(
                sess.eosio, self.name, key_owner, key_active)
                
        if not permission:
            permission = account

        super().__init__(
            self.account, contract_dir,
            wast_file, abi_file,
            permission, expiration_sec,
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            is_verbose) 


    def path(self):
        p = self.get_path()
        print("#  " + p)
         

    def delete(self):
        shutil.rmtree(self.get_path())
        print("#  Contract deleted.")


class Template(Contract):
    """
    Creates a new contract from a pre-defined template.
    """
    def __init__(
            self, name, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True):

        template = pyteos.Template(name)
        if not template.error:
            super().__init__(
                name, 
                wast_file=wast_file, abi_file=abi_file, 
                permission=permission, expiration_sec=expiration_sec, 
                skip_signature=skip_signature, dont_broadcast=skip_signature, 
                forceUnique=forceUnique,
                max_cpu_usage=max_cpu_usage, max_net_usage=max_net_usage,
                is_verbose=is_verbose            
            )



class Account(pyteos.Account):
    """
    Creates an account and imports its keys into the *wallet*.
    """
    def __init__(self, name, creator):
        
        key_owner = pyteos.CreateKey("key_owner")
        key_active = pyteos.CreateKey("key_active")

        sess.wallet.import_key(key_owner)
        sess.wallet.import_key(key_active)
        
        super().__init__(
            creator, name, key_owner, key_active)
