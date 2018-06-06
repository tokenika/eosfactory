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
import os

def set_verbose(is_verbose):
    pyteos.set_verbose(is_verbose)

def set_suppress_error_msg(suppress_error_msg):
    pyteos.set_suppress_error_msg(suppress_error_msg)


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
    def wslMapWindowsLinux(self, path):
        if ":\\" in path:
            path = path.replace("\\", "/")
            drive = path[0]
            path = path.replace(drive + ":/", "/mnt/" + drive.lower() + "/")
        return path

    def __init__(
            self, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True):

        contract_dir = self.wslMapWindowsLinux(contract_dir)

        account_name = pathlib.Path(contract_dir).parts[-1]
        pattern = re.compile("^[a-z, ., 1-5]*$")
        if len(account_name) > 12 or not pattern.match(account_name):
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', \
                       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', \
                       'q', 'r', 's', 't', 'u', 'v', 'w', 'x', \
                       'y', 'z', '.', '1', '2', '3', '4', '5']
            account_name = ""
            for i in range(0, 11):
                account_name += letters[random.randint(0, 31)]
            while True:
                last_letter = letters[random.randint(0, 31)]
                if last_letter != '.':
                    account_name += last_letter
                    break

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
        p = self.contract_path()
        print("#  " + p)


    def is_created(self):
        return not self.error
        # try:
        #     self.json["transaction id"]
        #     return True
        # except:
        #     return False
        

    def is_deployed(self):
        if not self.get_code():
            return False
        t = self.account.code()
        return not (t.json["code_hash"] == "0000000000000000000000000000000000000000000000000000000000000000")
         

    def delete(self):
        shutil.rmtree(self.contract_path())
        print("#  Contract deleted.\n")


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


class ContractFromTemplate(Contract):
    def __init__(self, name, template="", remove_existing=False, is_verbose=True):
        t = pyteos.Template(name, template, remove_existing, is_verbose)
        super().__init__(t.contract_path())
