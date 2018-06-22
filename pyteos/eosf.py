#!/usr/bin/python3

"""
Python front-end for `EOSIO cleos`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for `EOSIO cleos`.

.. moduleauthor:: Tokenika

"""

import os
import subprocess
import json
import pprint
import re
import pathlib
import setup
import teos
import cleos

def reload():
    import importlib
    importlib.reload(eosf)

class Wallet(cleos.WalletCreate):
    """ Create a new wallet locally and operate it.
    Usage: WalletCreate(name="default", is_verbose=True)

    - **parameters**::

        name: The name of the new wallet, defaults to `default`.
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the constraction time.  
    """
    def list(self):
        """ Lists opened wallets, * marks unlocked.
        Returns `cleos.WalletList` object
        """ 
        return cleos.WalletList()
    
    def open(self):
        """ Opens the wallet.
        Returns `WalletOpen` object     
        """
        self.wallet_open = cleos.WalletOpen(self.name)
        return not self.wallet_open.error

    def lock(self):
        """ Locks the wallet.
        Returns `cleos.WalletLock` object.   
        """
        self.wallet_lock = cleos.WalletLock(self.name)
        return not self.wallet_lock.error        

    def unlock(self):
        """ Unlocks the wallet.
        Returns `WalletUnlock` object.
        """        
        self.wallet_unlock = cleos.WalletUnlock(
            self.name, self.json["password"])
        return not self.wallet_unlock.error

    def import_key(self, key_pair):
        """ Imports a private key into wallet.
        Returns `cleos.WalletImport` object
        """
        return cleos.WalletImport(
            key_pair, self.name, is_verbose=False)       

    def keys(self):
        """ Lists public keys from all unlocked wallets.
        Returns `cleos.WalletKeys` object.    
        """
        return cleos.WalletKeys()

    def __str__(self):
        retval = json.dumps(self.json, indent=4) + "\n"
        retval = retval + json.dumps(self.keys().json, indent=4) + "\n"
        retval = retval + json.dumps(self.list().json, indent=4) + "\n"
        return retval


class Account(cleos.AccountLT):

    def code(self, code="", abi="", wasm=False):
        get_code = cleos.GetCode(
            self.name, code, abi, is_verbose=False)
        if not get_code.error and self.is_verbose:
            print("code hash: {}".format(get_code.code_hash))
        return get_code

    def set_contract(
            self, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=""):

        self.set_contract = cleos.SetContract(
            self.name, contract_dir, 
            wast_file, abi_file, 
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=False
        )
        return self.set_contract

    def push_action(
            self, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=""):
        if not permission:
            permission = self.name
        else:
            try: # permission is an account:
                permission=permission.name
            except: # permission is the name of an account:
                permission=permission

        self.action = cleos.PushAction(
            self.name, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=0)

        if not self.action.error:
            try:
                self.console = self.action.console
                if self.is_verbose:
                    print(self.console + "\n") 
            except:
                pass

        return self.action

    def get_table(
            self, table, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        self.table = cleos.GetTable(
                                self.name, table, scope,
                                binary, 
                                limit, key, lower, upper,
                                is_verbose=0)
        return self.table

    def __str__(self):
        return self.name


class Contract():

    def __init__(
            self, account, contract_dir,
            wast_file="", abi_file="",  
            permission="",
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=1):

        self.account = account
        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.expiration_sec = expiration_sec
        self.skip_signature = skip_signature
        self.dont_broadcast = dont_broadcast
        self.forceUnique = forceUnique
        self.max_cpu_usage = max_cpu_usage
        self.max_net_usage = max_net_usage
        self.ref_block = ref_block
        self.is_mutable = True

        self.contract = None
        self.console = None
        self.is_verbose = is_verbose
        self.error = self.account.error

    def deploy(self, permission=""):
        self.contract = cleos.SetContract(
            self.account, self.contract_dir, 
            self.wast_file, self.abi_file, 
            permission, self.expiration_sec, 
            self.skip_signature, self.dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.ref_block,
            is_verbose=0
        )
        return self.is_deployed()

    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error

    def wast(self):
        if self.is_mutable:            
            wast = teos.WAST(self.contract_dir, self.account.name)
        else:
            if setup.is_verbose():
                print("ERROR!")
                print("Cannot modify system contracts.")
        return not wast.error
        

    def abi(self, build_dir=""):            
        if self.is_mutable:
            abi = teos.ABI(self.contract_dir, self.account.name)
        else:
            if setup.is_verbose():
                print("ERROR!")
                print("Cannot modify system contracts.")
        return not abi.error

    
    def build(self):
        ok = self.abi()
        ok = ok and self.wast()
        return ok


    def push_action(
            self, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0, 
            ref_block="",
            is_verbose=0
        ):

        if not permission:
            permission=self.account.name
        else:
            try: # permission is an account:
                permission=permission.name
            except: # permission is the name of an account:
                permission=permission
    
        self.action = cleos.PushAction(
            self.account.name, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=0)

        if not self.action.error:
            try:
                self.console = self.action.console
                if self.is_verbose:
                    print(self.console + "\n") 
            except:
                pass        

        return self.action


    def get_console(self):
        return self.console


    def show_action(self, action, data, permission=""):
        """ Implements the `push action` command without broadcasting. 

        """
        return self.push_action(action, data, permission, dont_broadcast=1)
    

    def get_table(
            self, table, scope="",
            binary=False, 
            limit=10, key="", lower="", upper=""):
        """ Return a contract's table object.
        """

        self.table = cleos.GetTable(
                    self.account.name, table, scope,
                    binary=False, 
                    limit=10, key="", lower="", upper="", 
                    is_verbose=0)
        return self.table


    def code(self, code="", abi="", wasm=False):
        get_code = cleos.GetCode(
            self.account.name, code, abi, is_verbose=0)
        if not get_code.error and self.is_verbose:
            print("code hash: {}".format(get_code.code_hash))
        return get_code


    def contract_path(self):
        """ Return contract directory path.
        """
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str("NOT DEFINED JET")


