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
import cleos_system
import inspect
import types

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
    def __init__(self, name="default", password="", is_verbose=1):

        if not cleos.is_keosd(): # look for password:
            wallet_dir = os.path.expandvars(teos.get_node_wallet_dir())
            try:
                with open(wallet_dir + setup.password_map, "r") \
                        as input:    
                    password_map = json.load(input)
                    password = password_map[name]
            except:
                pass

        cleos.WalletCreate.__init__(self, name, password, is_verbose)

        if not self.error:
            if not cleos.is_keosd():
                wallet_dir = teos.get_node_wallet_dir()
                try:
                    with open(wallet_dir + setup.password_map, "r") \
                            as input:    
                        password_map = json.load(input)
                except:
                    password_map = {}
                password_map[name] = self.password

                with open(wallet_dir + setup.password_map, "w+") \
                        as out:    
                    password_map = json.dump(password_map, out)

    def list(self):
        """ Lists opened wallets, * marks unlocked.
        Returns `cleos.WalletList` object
        """ 
        return cleos.WalletList(is_verbose=self.is_verbose)
    
    def open(self):
        """ Opens the wallet.
        Returns `WalletOpen` object     
        """
        self.wallet_open = cleos.WalletOpen(
            self.name, is_verbose=self.is_verbose)
        return self.wallet_open

    def lock(self):
        """ Locks the wallet.
        Returns `cleos.WalletLock` object.   
        """
        self.wallet_lock = cleos.WalletLock(
            self.name, is_verbose=self.is_verbose)
        return self.wallet_lock    


    def unlock(self):
        """ Unlocks the wallet.
        Returns `WalletUnlock` object.
        """        
        self.wallet_unlock = cleos.WalletUnlock(
            self.name, self.json["password"], is_verbose=self.is_verbose)
        return self.wallet_unlock


    def import_key(self, account_or_key):
        """ Imports private keys of an account into wallet.
        Returns list of `cleos.WalletImport` objects
        """
        lcls = inspect.stack()[1][0].f_locals
        lcls.update(inspect.stack()[2][0].f_locals) 
        retval = []
        try:
            account_name = account_or_key.name
            for name in lcls:
                if id(account_or_key) == id(lcls[name]):
                    if cleos.is_keosd():
                        wallet_dir = \
                            os.path.expandvars(teos.get_keosd_wallet_dir())
                    else:
                        wallet_dir = teos.get_node_wallet_dir()
                    try:
                        with open(wallet_dir + setup.account_map, "r") \
                            as input:    
                            account_map = json.load(input)
                    except:
                        account_map = {}

                    account_map[account_name] = name
                    with open(wallet_dir + setup.account_map, "w") as out:
                        json.dump(account_map, out)

            key = account_or_key.owner_key
            if key:
                retval.append(
                    cleos.WalletImport(key, self.name, is_verbose=0))

            key = account_or_key.active_key
            if key:
                retval.append(
                    cleos.WalletImport(key, self.name, is_verbose=0))
        except:          
            retval.append(cleos.WalletImport(
                account_or_key, self.name, is_verbose=0))

        return retval


    def restore_accounts(self, namespace):
        account_names = set() # accounts in wallets
        keys = cleos.WalletKeys(is_verbose=0).json

        for key in keys[""]:
            accounts = cleos.GetAccounts(key, is_verbose=0)
            for acc in accounts.json["account_names"]:
                account_names.add(acc)

        if self.is_verbose:
            print("Restored accounts as global variables:")

        restored = dict()
        if len(account_names) > 0:
            if cleos.is_keosd():
                wallet_dir = os.path.expandvars(teos.get_keosd_wallet_dir())
            else:
                wallet_dir = teos.get_node_wallet_dir()
            try:
                with open(wallet_dir + setup.account_map, "r") as input:    
                    account_map = json.load(input)
            except:
                account_map = {}
            
            object_names = set()

            for name in account_names:
                try:
                    object_name = account_map[name]
                    if object_name in object_names:
                        object_name = object_name + "_" + name
                except:
                    object_name = name
                object_names.add(object_name)

                if object_name:
                    if self.is_verbose:
                        print("     {0} ({1})".format(object_name, name))
                    restored[object_name] = account(name, restore=True)
        else:
            if self.is_verbose:
                print("     empty list")
        
        namespace.update(restored)
        return ""

    def keys(self):
        """ Lists public keys from all unlocked wallets.
        Returns `cleos.WalletKeys` object.    
        """
        return cleos.WalletKeys(is_verbose=self.is_verbose)


    def info(self):
        retval = json.dumps(self.json, indent=4) + "\n"
        retval = retval + json.dumps(self.keys().json, indent=4) + "\n"
        return retval + json.dumps(self.list().json, indent=4) + "\n"
        


def account(
        creator="", 
        stake_net="", stake_cpu="",
        name="", 
        owner_key="", active_key="",
        permission = "",
        buy_ram_kbytes=0, buy_ram="",
        transfer=False,
        expiration_sec=30, 
        skip_signature=0, dont_broadcast=0, forceUnique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block="",
        is_verbose=1,
        restore=False):

    account_object = None
    if restore:
        if creator:
            name = creator
        account_object = cleos.RestoreAccount(name, is_verbose)
    else:

        if not name:
            name = cleos.account_name()

        if owner_key:
            if not active_key:
                active_key = owner_key
        else:
            owner_key = cleos.CreateKey("owner", is_verbose=-1)
            active_key = cleos.CreateKey("active", is_verbose=-1)

        if not creator:
            creator = cleos.AccountEosio()

        if stake_net:
            account_object = cleos_system.SystemNewaccount(
                    creator, name, owner_key, active_key,
                    stake_net, stake_cpu,
                    permission,
                    buy_ram_kbytes, buy_ram,
                    transfer,
                    expiration_sec, 
                    skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    is_verbose
                    )
        else:
            account_object = cleos.CreateAccount(
                    creator, name, 
                    owner_key, active_key,
                    permission,
                    expiration_sec, skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    is_verbose=is_verbose
                    )
                    
        account_object.owner_key = owner_key
        account_object.active_key = active_key

    def code(self, code="", abi="", wasm=False):      
        return cleos.GetCode(
            account_object, code, abi, 
            is_verbose=account_object.is_verbose)

    account_object.code = types.MethodType(code, account_object)

    def set_contract(
            self, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=""):

        account_object.set_contract = cleos.SetContract(
            account_object, contract_dir, 
            wast_file, abi_file, 
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=account_object.is_verbose
        )

        return account_object.set_contract

    account_object.set_contract = types.MethodType(
                                    set_contract , account_object)

    def push_action(
            self, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=""):
        if not permission:
            permission = account_object.name
        else:
            try: # permission is an account:
                permission=permission.name
            except: # permission is the name of an account:
                permission=permission

        account_object.action = cleos.PushAction(
            account_object, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=account_object.is_verbose)

        if not account_object.action.error:
            try:
                account_object.console = account_object.action.console
                if account_object.is_verbose > 0:
                    print(account_object.console + "\n") 
            except:
                pass

        return account_object.action

    account_object.push_action = types.MethodType(
                                    push_action , account_object)

    def get_table(
            self, table, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        account_object.table = cleos.GetTable(
                                account_object, table, scope,
                                binary, 
                                limit, key, lower, upper,
                                is_verbose=account_object.is_verbose)
        return account_object.table

    account_object.get_table = types.MethodType(
                                    get_table, account_object)

    def __str__(self):
        return account_object.name

    account_object.__str__ = types.MethodType(
                                        __str__, account_object)

    return account_object

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
            is_verbose=self.is_verbose
        )

        return self.is_deployed()


    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error


    def wast(self):
        if self.is_mutable:            
            wast = teos.WAST(
                self.contract_dir, self.account.name, 
                is_verbose=self.is_verbose)
        else:
            if self.is_verbose > 0:
                print("ERROR!")
                print("Cannot modify system contracts.")
        return not wast.error
        

    def abi(self):            
        if self.is_mutable:
            abi = teos.ABI(
                self.contract_dir, self.account.name, 
                is_verbose=self.is_verbose)
        else:
            if self.is_verbose > 0:
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
            ref_block=""
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
            is_verbose=self.is_verbose)

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
                    is_verbose=self.is_verbose)
            
        return self.table


    def code(self, code="", abi="", wasm=False):
        return cleos.GetCode(
            self.account.name, code, abi, is_verbose=self.is_verbose)


    def contract_path(self):
        """ Return contract directory path.
        """
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str("NOT DEFINED JET")

    def __str__(self):
        if self.is_deployed():
            return str(self.contract)
        else:
            return str(self.account)


