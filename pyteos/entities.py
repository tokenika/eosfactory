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
        """ Adds the `wallet_list` attribute that lists opened wallets, 
            * marks unlocked.
                
        - **wallet_list attributes**::

            error: Whether any error ocurred.
            json: The json representation of the object.
            is_verbose: Verbosity at the constraction time.
        """ 
        self.wallet_list = cleos.WalletList()
        return not self.wallet_list.error
    
    def open(self):
        """ Opens the wallet and adds the `wallet_open` attribute.
        
        - **wallet_open attributes**::

            error: Whether any error ocurred.
            json: The json representation of the object.
            is_verbose: Verbosity at the constraction time.     
        """
        self.wallet_open = cleos.WalletOpen(self.name)
        return not self.wallet_open.error

    def lock(self):
        """ Locks the wallet and adds the `wallet_lock` attribute.

        - **wallet_lock attributes**::

            error: Whether any error ocurred.
            json: The json representation of the object.
            is_verbose: Verbosity at the constraction time.    
        """
        self.wallet_lock = cleos.WalletLock(self.name)
        return not self.wallet_lock.error        

    def unlock(self):
        """ Unlocks the wallet and adds the `wallet_unlock` attribute.

        - **wallet_unlock attributes**::

            error: Whether any error ocurred.
            json: The json representation of the object.
            is_verbose: Verbosity at the constraction time.    
        """        
        self.wallet_unlock = cleos.WalletUnlock(
            self.name, self.json["password"])
        return not self.wallet_unlock.error

    def import_key(self, key_pair):
        """ Imports a private key into wallet and adds the `wallet_import` 
        attribute.

        - **parameters**::

            key: A private key in WIF format to import. May be an object 
                having the  May be an object having the attribute `key_private` 
                or a string.

        - **wallet_import attributes**::

            error: Whether any error ocurred.
            json: The json representation of the object.
            is_verbose: Verbosity at the constraction time. 
        """
        self.wallet_import = cleos.WalletImport(
            key_pair, self.name, is_verbose=False)
        return not self.wallet_import.error        

    def keys(self):
        """ Lists public keys from all unlocked wallets, and adds 
        the `wallet_keys`.

        - **wallet_keys attributes**::

            error: Whether any error ocurred.
            json: The json representation of the object.
            is_verbose: Verbosity at the constraction time.     
        """
        self.wallet_keys = cleos.WalletKeys()
        return not self.wallet_keys.error

    def __str__(self):
        retval = json.dumps(self.json, indent=4) + "\n"
        self.keys()
        retval = retval + json.dumps(self.wallet_keys.json, indent=4) + "\n"
        self.list()
        retval = retval + json.dumps(self.wallet_list.json, indent=4) + "\n"
        return retval


class Account(cleos.CreateAccount):

    def code(self, code="", abi="", wasm=False):
        self.code = cleos.GetCode(self.name, code, abi, is_verbose=False)
        return self.code

    def set_contract(
            self, account, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=False):

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

    def __str__(self):
        return str(cleos.GetAccount(self.name, is_verbose=True))   


class Contract(cleos.SetContract):

    def __init__(
            self, account, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True):
            
        self.name = pathlib.Path(contract_dir).parts[-1]
        try:
            self.account_name = account.name
        except:
            self.account_name = account
        
        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.permission = permission
        self.expiration_sec = expiration_sec
        self.skip_signature = skip_signature
        self.dont_broadcast =dont_broadcast
        self.forceUnique = forceUnique
        self.max_cpu_usage = max_cpu_usage
        self.max_net_usage = max_net_usage
        self.is_verbose = is_verbose
        self.is_mutable = True     
        self.console = ""

        import teos
        config = teos.GetConfig(contract_dir, is_verbose=False)
        try:       
            self.contract_path_absolute = config.json["contract-dir"]
        except:
            pass
        

    def __str__(self):
        return self._out

    def deploy(self):
        """ Deploy the contract.
        On error, return False.
        """
        super().__init__(
            self.account_name, self.contract_dir,
            self.wast_file, self.abi_file,
            self.permission, self.expiration_sec,
            self.skip_signature, self.dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.is_verbose)
        return not self.error

    def is_created(self):
        return not self.error

    def wast(self):
        if self.is_mutable:            
            wast = WAST(str(self.contract_path_absolute), self.account_name)
        else:
            if setup.is_verbose():
                print("ERROR!")
                print("Cannot modify system contracts.")
        return not wast.error
        

    def abi(self):
        if self.is_mutable:
            abi = ABI(str(self.contract_path_absolute), self.account_name)
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
            permission="",
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0, is_verbose=False
        ):

        if not permission:
            permission=self.account_name
        else:
            try: # permission is an account:
                permission=permission.name
            except: # permission is the name of an account:
                permission=permission
    
        push_action = PushAction(
            self.account_name, action, data,
            permission, 
            expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage
            )
            
        if push_action.error:
            return False

        if not push_action.error:
            self.action_json = push_action.json
            try:
                self.console = \
                    self.action_json["processed"]["action_traces"][0] \
                    ["console"]
                print(self.console + "\n")
            except:
                pass

        if (dont_broadcast or is_verbose) and not push_action.error:
            pprint.pprint(self.action_json)

        return True


    def get_console(self):
        return self.console


    def show_action(self, action, data, permission=""):
        """ Implements the `push action` command without broadcasting. 

        """
        return self.push_action(action, data, permission, dont_broadcast=1)
    

    def get_table(self, table, scope=""):
        """ Return a contract's table object.
        """
        if not scope:
            scope=self.account_name
        else:
            try: # scope is an account:
                scope=scope.name
            except: # scope is the name of an account:
                scope=scope                
        return GetTable(self.name, table, scope)


    def get_code(self):
        """ Print a contract's code.
        On error, return False.
        """
        code = GetCode(self.account_name)
        return not code.error


    def contract_path(self):
        """ Return contract directory path.
        """
        return str(self.contract_path_absolute)
