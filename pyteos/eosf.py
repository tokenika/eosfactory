#!/usr/bin/python3

"""
Python front-end for `EOSIO cleos`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for `EOSIO cleos`.

.. moduleauthor:: Tokenika

"""

import sys
import os
import json
import inspect
import types
import node
import shutil
import pprint
import enum
from termcolor import colored, cprint
from textwrap import dedent

import setup
import teos
import cleos
import cleos_system


def reload():
    import importlib
    importlib.reload(eosf)


class Verbosity(enum.Enum):
    CLEOS = 1
    TRACE = 2
    EOSF = 3
    ERROR = 4
    OUT = 5

_verbosity = []    
def set_verbosity(value=_verbosity):
    global _verbosity
    _verbosity = value

_is_throw_error = False
def set_throw_error(status=False):
    global _is_throw_error
    _is_throw_error = status


def wallet_dir():
    if setup.is_use_keosd():
        wallet_dir_ = os.path.expandvars(teos.get_keosd_wallet_dir())
    else:
        wallet_dir_ = teos.get_node_wallet_dir()
    return wallet_dir_


def account_map():
    wallet_dir_ = wallet_dir()
    try: # whether the setup map file exists:
        with open(wallet_dir_ + setup.account_map, "r") as input:
            account_map = json.load(input)
    except:
        account_map = {}
    return account_map


class _Eosf():

    eosf_color = 'blue'
    trace_color = 'magenta'
    error_color = 'red'
    verbosity = []

    def verify_is_verbose(self, verbosity=None, is_verbose=0):
        if verbosity is None:
            global _verbosity
            verbosity = _verbosity

        self.verbosity = verbosity
        if len(Verbosity) > 0 and not Verbosity.CLEOS in verbosity:
            return 0
        else:
            return is_verbose

    def EOSF(self, msg):
        if msg and Verbosity.EOSF in self.verbosity:
            cprint(
                dedent(msg).strip(),
                self.eosf_color)

    def TRACE(self, msg):
        if msg and Verbosity.TRACE in self.verbosity:
            cprint(
                dedent(msg).strip(),
                self.trace_color)

    def EOSF_TRACE(self, msg):
        if msg and Verbosity.EOSF in self.verbosity:
            self.EOSF(msg)
        else:
            self.TRACE(msg)

    def ERROR(self, msg):
        msg = colored(
            "ERROR\n{}".format(dedent(msg).strip()), 
            self.error_color)
        global _is_throw_error
        if _is_throw_error:
            raise Exception(msg)
        else:
            print(msg)


    def OUT(self, msg):
        if msg and Verbosity.TRACE in self.verbosity:
            print(dedent(msg).strip())


class Wallet(cleos.WalletCreate, _Eosf):
    """ Create a new wallet locally and operate it.
    Usage: WalletCreate(name="default", is_verbose=1)

    - **parameters**::

        name: The name of the new wallet, defaults to `default`.
        is_verbose: If `0`, do not print unless on error, 
            default is `1`.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the constraction time.  
    """
    def __init__(
                self, name="default", password="", is_verbose=1, 
                verbosity=None):

        is_verbose = self.verify_is_verbose(verbosity, is_verbose)

        self.EOSF_TRACE("######### Create a `Wallet` object.")

        if not setup.is_use_keosd(): # look for password:
            self.wallet_dir_ = teos.get_node_wallet_dir()
        else:
            self.wallet_dir_ = os.path.expandvars(teos.get_keosd_wallet_dir())

        if not setup.is_use_keosd(): # look for password:
            try:
                with open(self.wallet_dir_ + setup.password_map, "r") \
                        as input:    
                    password_map = json.load(input)
                    password = password_map[name]

                self.EOSF("""
                    Pasword is restored from the file:
                    {}
                    """.format(self.wallet_dir_ + setup.password_map))
            except:
                pass

        cleos.WalletCreate.__init__(self, name, password, is_verbose)

        if not self.error:
            if not setup.is_use_keosd(): 
                try:
                    with open(self.wallet_dir_ + setup.password_map, "r") \
                            as input:
                        password_map = json.load(input)
                except:
                    password_map = {}
                password_map[name] = self.password

                with open(self.wallet_dir_ + setup.password_map, "w+") \
                        as out:
                    json.dump(password_map, out)

                if not password: # new password
                    self.EOSF_TRACE("""
                        Created wallet `{}` with the local testnet. Wallet directory is
                        {}
                        Password is saved to file:
                        {}
                        """.format(
                                self.name, self.wallet_dir_,
                                self.wallet_dir_ + setup.password_map)
                    )

                else: # password taken from file
                    self.EOSF_TRACE("""
                        Opened wallet `{}`.
                        """.format(self.name))

            else: # KEOSD Wallet Manager
                if not password: # new password
                    self.EOSF_TRACE("""
                        Created wallet `{}` with the `keosd` Wallet Manager. Wallet directory is
                        {}
                        Save password to use in the future to unlock this wallet.
                        Without password imported keys will not be retrievable.
                        {}
                        """.format(self.name, self.wallet_dir_, self.password)
                    )

                else: # password introduced
                    self.EOSF_TRACE("""
                        Opened wallet {}
                        """.format(self.name))

        else: # self.error:
            print(self.err_msg)


    def index(self):
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
        # print("\ninspect.stack():\n")
        # pprint.pprint(inspect.stack())
        # print("\ninspect.stack()[1][0]:\n")
        # pprint.pprint(inspect.stack()[1][0])
        # print("\ninspect.stack()[1][0].f_locals:\n")
        # pprint.pprint(inspect.stack()[1][0].f_locals)
        # print("\ninspect.stack()[1][0].f_globals:\n")
        # pprint.pprint(inspect.stack()[1][0].f_globals)

        # print("\ninspect.stack()[2][0]:\n")
        # pprint.pprint(inspect.stack()[2][0])
        # print("\ninspect.stack()[2][0].f_locals:\n")
        # pprint.pprint(inspect.stack()[2][0].f_locals)
        # print("\ninspect.stack()[2][0].f_globals:\n")
        # pprint.pprint(inspect.stack()[2][0].f_globals)
            
        lcls = dir()
        try:
            lcls = inspect.stack()[1][0].f_locals
        except:
            pass
        try:
            lcls.update(inspect.stack()[2][0].f_locals) 
        except:
            pass

        account_name = None
        try: # whether account_or_key is an account:
            account_name = account_or_key.name
        except:
            pass
        if not account_name is None:
            for name in lcls:
                if id(account_or_key) == id(lcls[name]):
                    try: # whether the setup map file exists:
                        with open(self.wallet_dir_ + setup.account_map, "r") \
                            as input:
                            account_map = json.load(input)
                    except:
                        account_map = {}

                    if self.is_verbose > 0:
                        print("'{}' ({}) >>> '{}'".format(
                            name, account_name, self.wallet_dir_ + setup.account_map))

                    account_map[account_name] = name
                    with open(self.wallet_dir_ + setup.account_map, "w") as out:
                        out.write(json.dumps(account_map, sort_keys=True, indent=4))
                        

        imported_keys = []
        try: # whether account_or_key is an account:
            key = account_or_key.owner_key
            if key:
                imported_keys.append(
                    cleos.WalletImport(key, self.name, is_verbose=0))

            key = account_or_key.active_key
            if key:
                imported_keys.append(
                    cleos.WalletImport(key, self.name, is_verbose=0))
        except:
            imported_keys.append(cleos.WalletImport(
                account_or_key, self.name, is_verbose=0))

        return imported_keys


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
            if setup.is_use_keosd():
                wallet_dir_ = os.path.expandvars(teos.get_keosd_wallet_dir())
            else:
                wallet_dir_ = teos.get_node_wallet_dir()
            try:
                with open(wallet_dir_ + setup.account_map, "r") as input:    
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
        return restored


    def keys(self):
        """ Lists public keys from all unlocked wallets.
        Returns `cleos.WalletKeys` object.
        """
        return cleos.WalletKeys(is_verbose=self.is_verbose)


    def info(self):
        retval = json.dumps(self.json, indent=4) + "\n"
        retval = retval + json.dumps(self.keys().json, indent=4) + "\n"
        return retval + json.dumps(self.list().json, indent=4) + "\n"


class Transaction():
    def __init__(self, msg):
        self.transaction_id = ""
        msg_keyword = "executed transaction: "
        if msg_keyword in msg:
            beg = msg.find(msg_keyword, 0)
            end = msg.find(" ", beg + 1)
            self.transaction_id = msg[beg : end]
        else:
            try:
                self.transaction_id = msg.json["transaction_id"]
            except:
                pass

    def get_transaction(self):
        pass


class ContractBuild():
    def __init__(
            self, contract_dir,
            wast_file="", abi_file="",
            is_mutable = True,  
            is_verbose=1):

        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.is_mutable = is_mutable
        self.is_verbose = is_verbose

    def build_wast(self):
        if self.is_mutable:
            wast = teos.WAST(
                self.contract_dir, "", 
                is_verbose=self.is_verbose)                
        else:
            if self.is_verbose > 0:
                print("ERROR!")
                print("Cannot modify system contracts.")
        return wast

    def build_abi(self):
        if self.is_mutable:
            abi = teos.ABI(
                self.contract_dir, "", 
                is_verbose=self.is_verbose)                
        else:
            if self.is_verbose > 0:
                print("ERROR!")
                print("Cannot modify system contracts.")
        return abi

    def build(self):
        return not self.build_abi().error and not self.build_wast().error


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
        self._console = None
        self.is_verbose = is_verbose
        self.error = self.account.error


    def deploy(self, permission="", is_verbose=1):
        self.contract = cleos.SetContract(
            self.account, self.contract_dir, 
            self.wast_file, self.abi_file, 
            permission, self.expiration_sec, 
            self.skip_signature, self.dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.ref_block,
            self.is_verbose > 0 and is_verbose > 0
        )
        if not self.contract.error:
            try:
                self.contract.json = json.loads(self.contract.err_msg)
                for action in self.contract.json["actions"]:
                    action["data"] = "contract code data, deleted for readability ..................."
            except:
                pass

            return self.contract


    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error


    def build_wast(self):
        return ContractBuild(
            self.contract_dir, "", "", 
            self.is_mutable, self.is_verbose).build_wast()


    def build_abi(self):
        return ContractBuild(
            self.contract_dir, "", "", 
            self.is_mutable, self.is_verbose).build_abi()

    
    def build(self):
        return ContractBuild(
            self.contract_dir, "", "", 
            self.is_mutable, self.is_verbose).build()


    def push_action(
            self, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0, 
            ref_block="",
            is_verbose=1,
            json=False,
            output=False
        ):
        if not permission:
            permission = self.account.name
        else:
            try: # permission is an account:
                permission = permission.name
            except: # permission is the name of an account:
                permission = permission

        if output:
            is_verbose = 0
            json = True
    
        self.action = cleos.PushAction(
            self.account.name, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            self.is_verbose > 0 and is_verbose > 0, json)

        if not self.action.error:
            try:
                self._console = self.action.console
                if self.is_verbose:
                    print(self._console + "\n") 
            except:
                pass

        return self.action


    def show_action(self, action, data, permission=""):
        """ Implements the `push action` command without broadcasting. 

        """
        return self.push_action(action, data, permission, dont_broadcast=1)
    

    def table(
            self, table_name, scope="",
            binary=False, 
            limit=10, key="", lower="", upper=""):
        """ Return a contract's table object.
        """
        self._table = cleos.GetTable(
                    self.account.name, table_name, scope,
                    binary=False, 
                    limit=10, key="", lower="", upper="", 
                    is_verbose=self.is_verbose)
            
        return self._table


    def code(self, code="", abi="", wasm=False):
        return cleos.GetCode(
            self.account.name, code, abi, wasm, is_verbose=self.is_verbose)


    def console(self):
        return self._console


    def path(self):
        """ Return contract directory path.
        """
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str(self.contract_dir)


    def delete(self):
        try:
            if self.contract:
                shutil.rmtree(str(self.contract.contract_path_absolute))
            else:
                shutil.rmtree(str(self.contract_dir))
            return True
        except:
            return False


    def __str__(self):
        if self.is_deployed():
            return str(self.contract)
        else:
            return str(self.account)


class ContractFromTemplate(Contract):
    def __init__(self, account, name, template="", remove_existing=False, visual_studio_code=False, is_verbose=True):
        t = teos.Template(name, template, remove_existing, visual_studio_code, is_verbose)
        super().__init__(account, t.contract_path_absolute)


class AccountEosio():

    json = {}
    error = False
    account_info = "The account is not opened yet!"

    def __init__(
            self, is_verbose=1):

        cleos.set_wallet_url(self) # this may set self.error ON
        if not self.error:
            self.name = "eosio"  
            self.json["name"] = self.name
            config = teos.GetConfig(is_verbose=0)

            self.json["privateKey"] = config.json["EOSIO_KEY_PRIVATE"]
            self.json["publicKey"] = config.json["EOSIO_KEY_PUBLIC"]
            self.key_private = self.json["privateKey"]
            self.key_public = self.json["publicKey"]
            self._out = "transaction id: eosio"

            account = cleos.GetAccount(self.name, is_verbose=-1)
            if not account.error:
                self.account_info = account._out
            else:
                if "main.cpp:2712" in account.err_msg:
                    self.account_info = "The account is not opened yet!"
                else:
                    self.account_info = account.err_msg
        else:
            print(self.err_msg)

    
    def info(self):
        return self.account_info
        

    def __str__(self):
        return self.name


class AccountMaster(AccountEosio):

    def set_account_info(self):
        account_ = cleos.GetAccount(self.name, is_verbose=-1)
        if not account_.error:
            self.account_info = str(account_)
            return True
        else:
            if "main.cpp:2712" in account_.err_msg:
                self.account_info = "The account is not opened yet!"
            else:
                self.account_info = account_.err_msg
            return False

    def __init__(
            self, name="", owner_key_public="", active_key_public="", 
            is_verbose=1):

        cleos.set_wallet_url(self)  # this may set self.error ON
        if not self.error:
            AccountEosio.__init__(self, is_verbose)
            if self.set_account_info():
                return
            
            # not local testnet:
            if not owner_key_public: # print data for registration
                self.new_account = True
                if not name: 
                    self.name = cleos.account_name()
                else:
                    self.name = name

                self.owner_key = cleos.CreateKey("owner", is_verbose=0)
                self.active_key = cleos.CreateKey("active", is_verbose=0)
                print(
                    "\nUse the following data to register a new account on a public testnet:\n" \
                    + "Accout Name: {}\n".format(self.name) \
                    + "Owner Public Key: {}\n".format(self.owner_key.key_public) \
                    + "Owner Private Key: {}\n".format(self.owner_key.key_private) \
                    + "Active Public Key: {}\n".format(self.active_key.key_public) \
                    + "Active Private Key: {}\n".format(self.active_key.key_private))
            else: # restore the master account
                self.name = name
                self.new_account = False
                self.owner_key = CreateKey("owner", owner_key_public, is_verbose=0)
                if not active_key_public:
                    self.active_key = owner_key
                else:
                    self.active_key = CreateKey(
                        "active", active_key_public, is_verbose=0)
        else:
            print(self.err_msg)

        self.set_account_info()
    

    def info(self):
        return self.account_info
        

    def __str__(self):
        return self.name

def account_object(
        account_object_name,
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
        restore=False,        
        is_verbose=1,
        verbosity=None):

    self = _Eosf()
    is_verbose = self.verify_is_verbose(verbosity, is_verbose)

    objects = None    
    context_locals = inspect.stack()[1][0].f_locals
    context_globals = inspect.stack()[1][0].f_globals
    objects = {**context_globals, **context_locals}

    wallet = None
    wallets = []
    for name in objects:
        if isinstance(objects[name], Wallet):
            wallets.append(name)
            wallet = objects[name]

    error = False

    if len(wallets) == 0:
        self.ERROR("""
            Cannot find any `Wallet` object.
            Add the definition of an `Wallet` object, for example:
            `wallet = eosf.Wallet()`
            """)
    if len(wallets) > 1:
        self.ERROR("""
            Too many `Wallet` objects.
            Can be precisely one wallet object in the scope, but there is many: 
            {}
            """.format(wallets))

    account_map_ = account_map()
    for name, acc_name in account_map_.items():
        if acc_name == account_object_name:
            self.ERROR( """
                The given account object name
                `{}`({})
                points to an existing account, mapped in a file in directory:
                `{}`
                Cannot overwrite it.
                """.format(acc_name, name, wallet_dir()))

    # create account object:

    return

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
            creator = AccountMaster()

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

    # append account methodes to the account_object:

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
                permission = permission.name
            except: # permission is the name of an account:
                permission = permission

        account_object.action = cleos.PushAction(
            account_object, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=account_object.is_verbose)

        if not account_object.action.error:
            try:
                account_object._console = account_object.action.console
                if account_object.is_verbose > 0:
                    print(account_object._console + "\n") 
            except:
                pass

        return account_object.action

    account_object.push_action = types.MethodType(
                                    push_action , account_object)

    def table(
            self, table_name, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        account_object._table = cleos.GetTable(
                                account_object, table_name, scope,
                                binary, 
                                limit, key, lower, upper,
                                is_verbose=account_object.is_verbose)
        return account_object._table

    account_object.table = types.MethodType(
                                    table, account_object)

    def __str__(self):
        return account_object.name

    account_object.__str__ = types.MethodType(
                                        __str__, account_object)

    # export the account object to the globals in the calling module:

    context_globals[account_object_name] = account_object

    # put the account object to the wallet:

    wallet.open()
    wallet.unlock()
    wallet.import_key(account_object)

    return account_object


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

    wallet = None
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
            creator = AccountMaster()

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
                permission = permission.name
            except: # permission is the name of an account:
                permission = permission

        account_object.action = cleos.PushAction(
            account_object, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=account_object.is_verbose)

        if not account_object.action.error:
            try:
                account_object._console = account_object.action.console
                if account_object.is_verbose > 0:
                    print(account_object._console + "\n") 
            except:
                pass

        return account_object.action

    account_object.push_action = types.MethodType(
                                    push_action , account_object)

    def table(
            self, table_name, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        account_object._table = cleos.GetTable(
                                account_object, table_name, scope,
                                binary, 
                                limit, key, lower, upper,
                                is_verbose=account_object.is_verbose)
        return account_object._table

    account_object.table = types.MethodType(
                                    table, account_object)

    def __str__(self):
        return account_object.name

    account_object.__str__ = types.MethodType(
                                        __str__, account_object)

    return account_object


def reset(is_verbose=1):
    return node.reset(is_verbose)


def run(is_verbose=1):
    return node.run(is_verbose)


def stop(is_verbose=1):
    return node.stop(is_verbose)


if __name__ == "__main__":
    template = ""
    if len(sys.argv) > 2:
        template = str(sys.argv[2])

    teos.Template(str(sys.argv[1]), template, visual_studio_code=True)