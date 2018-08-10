#!/usr/bin/python3

"""
Python front-end for `EOSIO cleos`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for `EOSIO cleos`.

.. moduleauthor:: Tokenika

"""

import random
import os
import time
import subprocess
import json as json_module
import pathlib
import setup
import teos
from textwrap import dedent

setup_setup = setup.Setup()
_wallet_address_arg = None

def restart():
    setup.restart()
    global setup_setup
    setup_setup = setup.Setup()
    global _wallet_address_arg
    _wallet_address_arg = None

def set_local_nodeos_address():
    config = teos.GetConfig(is_verbose=0)       
    setup.set_nodeos_address(config.json["EOSIO_DAEMON_ADDRESS"])
    setup.set_is_local_address(True)

def wallet_url():
    global _wallet_address_arg
    return _wallet_address_arg

def node_is_running():
    result = teos.NodeIsRunning(is_verbose=0)
    return not result.daemon_pid == ""
    
def is_notrunningnotkeosd_error(cleos_object=None):

    is_error = not setup.is_use_keosd() and not node_is_running()
    err_msg = heredoc("""
Cannot use the local node Wallet Manager if the node is not running.
            """)
    if cleos_object is None:
        if is_error:
            return err_msg
        else:
            return ""
    else:
        if is_error:
            cleos_object.set_error(err_msg)
            return True
        else:
            return False

def set_wallet_url_arg(cleos_object, url=None, check_error=True):
    """Implements the `use_keosd` flag in the `setup` module.
    """
    global _wallet_address_arg
    if not _wallet_address_arg is None:
        return

    if check_error and is_notrunningnotkeosd_error(cleos_object):
        _wallet_address_arg = None
        return        

    if not url is None:
        if not url:
            _wallet_address_arg = []
        else:
            _wallet_address_arg = ["--wallet-url", "http://" + url]
        return

    if _wallet_address_arg is None:
        _wallet_address_arg = []

def heredoc(msg):
    msg = dedent(msg).strip()
    msg.replace("<br>", "\n")
    return msg

class Named:
    """Having the ``name`` attribute.
    """    
    pass

class _Cleos:
    """A prototype for the `cleos` command classes.
    """
    global setup_setup

    def copy_to(self, to_object):
        to_object.error = self.error
        to_object.is_verbose = self.is_verbose
        to_object.json = self.json
        to_object.err_msg = self.err_msg
        to_object.out_msg = self.out_msg

    def set_is_verbose(self, is_verbose):
        if setup.is_verbose() and is_verbose > 0:
            self.is_verbose = 1
        else:
            if is_verbose < 0:
                self.is_verbose = -1
            else:
                self.is_verbose = 0

    def set_error(self, err_msg):
        if not self.error:
            self.error = True
            self.err_msg = err_msg

    def __init__(self, args, first, second, is_verbose=1):
        if setup.nodeos_address_arg() is None:
            set_local_nodeos_address()
        
        set_wallet_url_arg(self) # this may set self.error ON

        global _wallet_address_arg
        if not self.error:
            cl = [setup_setup.cleos_exe, setup.nodeos_address_arg(), \
                _wallet_address_arg]

            if setup.is_print_request():
                cl.append("--print-request")
            if setup.is_print_response():
                cl.append("--print-response")

            cl.extend([first, second])
            cl.extend(args)
            self.args = args

            if setup.is_print_command_line():
                print("command line sent to cleos:")
                print(" ".join(cl))
                print("")

            process = subprocess.run(
                cl,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(pathlib.Path(setup_setup.cleos_exe).parent)) 

            self.out_msg = process.stdout.decode("utf-8")
            self.err_msg = process.stderr.decode("utf-8")

        self.set_is_verbose(is_verbose)
        self.json = {}

        if setup.is_print_response() or setup.is_print_response():
            print(self.err_msg)
            print("")

        error_key_words = ["Error", "error", "Failed"]
        for word in error_key_words:
            if word in self.err_msg:
                self.error = True
                break

        if self.error:
            self.json["ERROR"] = self.err_msg
            if is_verbose > 0:
                self.print_error()

    def printself(self):
        if self.is_verbose > 0:
            print(self.__str__())

    def print_error(self):
        if self.is_verbose > -1:
            print("ERROR:")
            print(self.err_msg)
            print()

    def __str__(self):
        out = self.out_msg + "\n"
        out = out + self.err_msg
        return out

    def __repr__(self):
        return ""

    def account_to_string(self, account):
        logger = eosf.Logger()
        if isinstance(account, str):
            return account
        if isinstance(account, Account):
            return account.name

        self.set_error(heredoc("""
                creator_to_string(account):
                    wrong argument type.
            """))

    def permission_to_string(self, permission):
        if isinstance(permission, str):
            return permission
        if isinstance(permission, Account):
            return permission.name
        if isinstance(permission, tuple):
            retval = None
            if isinstance(permission[0], str):
                retval = permission[0]
            if isinstance(permission[0], Account):
                retval = permission[0].name
            if retval is None:
                self.set_error("""
                permission_to_string(permission):
                    not isinstance(permission[0], Account)
                    and
                    not isinstance(permission[0], str)
                """)
                return None

            if isinstance(permission[1], str):
                if permission[1][0] = "@":
                    retval = retval + permission[1]
                else:
                    retval = retval + "@" + permission[1]
                return retval
            else:
                self.set_error("""
                permission_to_string(permission):
                    not isinstance(permission[1], str)
                """)  
                return None          

        self.set_error("""
                permission_to_string(permission):
                    wrong argument type.
            """)

def get_transaction_id(cleos_object):
    transaction_id = ""
    msg_keyword = "executed transaction: "
    msg = cleos_object.err_msg
    json = {}
    if msg_keyword in msg:
        beg = msg.find(msg_keyword, 0) + len(msg_keyword)
        end = msg.find(" ", beg + 1)
        transaction_id = msg[beg : end]
    else:
        try:
            json = json_module.loads(cleos_object.out_msg)
            transaction_id = json["transaction_id"]
        except:
            pass
    return transaction_id

class GetAccount(_Cleos):
    """Retrieve an account from the blockchain.

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        name: The name of the account.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, account, is_verbose=1, json=False):
        try:
            self.name = account.name
        except:
            self.name = account

        args = [self.name]
        if setup.is_json() or json:
            args.append("--json")

        _Cleos.__init__(
            self, args, "get", "account", is_verbose)

        if not self.error:
            try:
                j = json_module.loads(self.out_msg)
                self.json = j
            except:
                pass

            self.printself()

    def __str__(self):
        out = "name: {}\n".format(self.name)
        out = out + str(_Cleos.__str__(self))
        return out

class GetAccounts(_Cleos):
    """Retrieve accounts associated with a public key.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, key, is_verbose=1):
        try:
            key_public = key.key_public
        except:
            key_public = key

        _Cleos.__init__(
            self, [key_public], "get", "accounts", is_verbose)

        if not self.error:
            self.json = json_module.loads(self.out_msg)
            self.names = self.json['account_names']
            self.printself()

class GetTransaction(_Cleos):
    """Retrieve a transaction from the blockchain.

    - **parameters**::

        transaction_id: ID of the transaction to retrieve.
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        transaction_id: ID of the transaction retrieved.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, transaction_id, is_verbose=1):
        
        self.transaction_id = transaction_id
        _Cleos.__init__(
            self, [transaction_id], "get", "transaction", is_verbose)

        if not self.error:
            self.json = json_module.loads(self.out_msg)

            self.printself()


class WalletCreate(_Cleos):
    """Create a new wallet locally.

    - **parameters**::

        name: The name of the new wallet, defaults to `default`.
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, name="default", password="", is_verbose=1):
        self.name = name
        self.password = None
        self.json["name"] = name
        self.set_is_verbose(is_verbose)

        if not password: # try to create a wallet
            _Cleos.__init__(
                self, ["--name", self.name], "wallet", "create", is_verbose)
            
            msg = self.out_msg
            if not self.error:
                self.password = msg[msg.find("\"")+1:msg.rfind("\"")]
                self.json["password"] = self.password
            else:
                return
        else: # try to open an existing wallet
            WalletOpen(name, is_verbose=-1)
            wallet_unlock = WalletUnlock(name, password, is_verbose=-1)
            self.err_msg = wallet_unlock.err_msg  

            if not wallet_unlock.error:
                self.name = name
                self.password = password
                self.json["password"] = self.password
                self.out_msg = "Restored wallet: {}".format(self.name)
            else:
                if "Nonexistent wallet" in self.err_msg:
                    _Cleos.__init__(
                        self, ["--name", self.name], "wallet", "create",
                        is_verbose)
                self.error = True

        if not self.error:
            self.printself()


class WalletStop(_Cleos):
    """Stop keosd (doesn't work with nodeos).
    """
    def __init__(self, is_verbose=1):
        _Cleos.__init__(self, [], "wallet", "stop", is_verbose)

        if not self.error:
            self.printself()


class WalletList(_Cleos):
    """List opened wallets, * marks unlocked.

    - **parameters**::

        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.
            
    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, is_verbose=1):
        _Cleos.__init__(
            self, [], "wallet", "list", is_verbose)

        if not self.error:
            self.json = json_module.loads("{" + self.out_msg.replace("Wallets", \
                '"Wallets"', 1) + "}")
            self.printself()


class WalletImport(_Cleos):
    """Import a private key into wallet.

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        key: A key object or a private key in WIF format to import.
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, key, wallet="default", is_verbose=1):

        self.set_is_verbose(is_verbose)

        try: # is the key a key object?
            key_private = key.key_private
        except: # key is a string:
            key_private = key 

        try: # is the wallet an Wallet object?
            wallet_name = wallet.name
        except: # wallet is a string
            wallet_name = wallet

        _Cleos.__init__(
            self, ["--private-key", key_private, "--name", wallet_name],
            "wallet", "import", is_verbose)

        if not self.error:
            self.json["key_private"] = key_private
            self.key_private = key_private
            self.printself()

class WalletRemove_key(_Cleos):
    """Remove key from wallet
    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        password: The password returned by wallet create.
        key: A key object or a private key in WIF format to import.
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        error: Whether any error ocurred.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, key, wallet, password, is_verbose=1):

        self.set_is_verbose(is_verbose)

        try: # is the key a key object?
            key_public = key.key_public
        except: # key is a string:
            key_public = key 

        try: # is the wallet an Wallet object?
            wallet_name = wallet.name
        except: # wallet is a string
            wallet_name = wallet

        _Cleos.__init__(
            self, [key_public, "--name", wallet_name, "--password", password], 
            "wallet", "remove_key", is_verbose)

        if not self.error:
            self.json["key_public"] = key_public
            self.key_public = key_public
            self.printself()


class WalletKeys(_Cleos):
    """List of public keys from all unlocked wallets.

    - **parameters**::

        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **parameters**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, is_verbose=1):
        _Cleos.__init__(
            self, [], "wallet", "keys", is_verbose)

        if not self.error:
            if self.out_msg == "[]\n":
                self.json[""] = []
            else:
                self.json[""] = self.out_msg.replace("\n", "") \
                    .replace("[  ", "").replace('"',"").replace("]", "") \
                    .split(",  ")
                    
            self.printself() 

    def __str__(self):
        out = "Keys in all opened wallets:\n"
        out = out + str(_Cleos.__str__(self))
        return out


class WalletOpen(_Cleos):
    """Open an existing wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, wallet="default", is_verbose=1):
        try:
            wallet_name = wallet.name
        except:
            wallet_name = wallet
        
        _Cleos.__init__(
            self, ["--name", wallet_name], "wallet", "open", is_verbose)

        if not self.error:
            self.printself()


class WalletLockAll(_Cleos):
    """Lock all unlocked wallets.
    """
    def __init__(self, wallet="default", is_verbose=1):
        _Cleos.__init__(
            self, [], "wallet", "lock_all", is_verbose)

        if not self.error:
            self.printself()


class WalletLock(_Cleos):
    """Lock wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **parameters**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, wallet="default", is_verbose=1):
        try:
            wallet_name = wallet.name
        except:
            wallet_name = wallet
        
        _Cleos.__init__(
            self, ["--name", wallet_name], "wallet", "lock", is_verbose)

        if not self.error:
            self.printself()


class WalletUnlock(_Cleos):
    """Unlock wallet.

    - **parameters**::

        wallet: The name of the wallet. May be an object 
            having the  May be an object having the attribute `name`, 
            like `CreateAccount`, or a string.
        password: If the wallet argument is not a wallet object, the password 
            returned by wallet create, else anything, defaults to "".
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::
    
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(
            self, wallet="default", password="", timeout=0, is_verbose=1):
        try:
            wallet_name = wallet.name
            password = wallet.password
        except:
            wallet_name = wallet

        _Cleos.__init__(
            self, 
            ["--name", wallet_name, "--password", password], 
            "wallet", "unlock", is_verbose)

        if not self.error:
            self.printself()


class GetInfo(_Cleos):
    """Get current blockchain information.

    - **parameters**::

        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(self, is_verbose=1):
        _Cleos.__init__(
            self, [], "get", "info", is_verbose)
        if not self.error:
            self.json = json_module.loads(str(self.out_msg))
            self.head_block = self.json["head_block_num"]
            self.head_block_time = self.json["head_block_time"]
            self.last_irreversible_block_num \
                = self.json["last_irreversible_block_num"]
            self.printself()


def get_last_block():
    info = GetInfo()
    return GetBlock(info.head_block)


def get_block_trx_data(block_num):
    block = GetBlock(block_num)
    trxs = block.json["transactions"]
    for trx in trxs:
        print(trx["trx"]["transaction"]["actions"][0]["data"])


def get_block_trx_cout(block_num):
    block = GetBlock(block_num)
    trxs = block.json["transactions"]
    return len(trxs)


class GetBlock(_Cleos):
    """Retrieve a full block from the blockchain.

    - **parameters**::
    
        block_number: The number of the block to retrieve.
        block_id: The ID of the block to retrieve, if set, defaults to "".
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.
            
    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.    
    """
    def __init__(self, block_number, block_id="", is_verbose=1):
        args = []
        if(block_id == ""):
            args = [str(block_number)]
        else:
            args = [block_id]
        
        _Cleos.__init__(
            self, args, "get", "block", is_verbose)

        if not self.error:
            self.json = json_module.loads(self.out_msg)
            self.block_num = self.json["block_num"]
            self.ref_block_prefix = self.json["ref_block_prefix"]
            self.timestamp = self.json["timestamp"]
            self.printself()


class GetCode(_Cleos):
    """Retrieve the code and ABI for an account.

    - **parameters**::

        account: The name of an account whose code should be retrieved. 
            May be an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.
        code: The name of the file to save the contract .wast/wasm to.
        abi: The name of the file to save the contract .abi to.
        wasm: Save contract as wasm.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.    
    """
    def __init__(
            self, account, code="", abi="", 
            wasm=False, is_verbose=1
        ):

        try:
            account_name = account.name
        except:
            account_name = account

        args = [account_name]
        if code:
            args.extend(["--code", code])
        if abi:
            args.extend(["--abi", abi])
        if wasm:
            args.extend(["--wasm"])

        _Cleos.__init__(self, args, "get", "code", is_verbose)

        if not self.error:
            msg = str(self.out_msg)
            self.json["code_hash"] = msg[msg.find(":") + 2 : len(msg) - 1]
            self.code_hash = self.json["code_hash"]
            self.printself()


class GetTable(_Cleos):
    """Retrieve the contents of a database table

    - **parameters**::

        contract: The name, of the contract that owns the table. May be 
            an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.
        scope: The scope within the contract in which the table is found,
            can be a `CreateAccount` or `Account` object, or a name.
        table: The name of the table as specified by the contract abi.
        binary: Return the value as BINARY rather than using abi to 
            interpret as JSON
        limit: The maximum number of rows to return.
        key: The name of the key to index by as defined by the abi, 
            defaults to primary key.
        lower: JSON representation of lower bound value of key, 
            defaults to first.
        upper: JSON representation of upper bound value value of key, 
            defaults to last.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(
        self, contract, table, scope,
        binary=False, 
        limit=10, key="", lower="", upper="",
        is_verbose=1
        ):

        try:
            contract_name = contract.name
        except:
            contract_name = contract

        args = [contract_name]

        if not scope:
            scope=self.name
        else:
            try:
                scope_name = scope.name
            except:
                scope_name = scope

        args.append(scope_name)
        args.append(table)

        if binary:
            args.append("--binary")
        if limit:
            args.extend(["--limit", str(limit)])
        if key:
            try:
                key_public = key.active_key_public
            except:
                key_public = key
            args.extend(["--key", key_public])
        if lower:
            args.extend(["--lower", lower])
        if upper:
            args.extend(["--upper", upper])

        _Cleos.__init__(self, args, "get", "table", is_verbose)

        if not self.error:
            try:
                self.json = json_module.loads(self.out_msg)
            except:
                pass

            self.printself()


class CreateKey(_Cleos):
    """Create a new keypair and print the public and private keys.

    - **parameters**::

        key_name: Key name.
        r1: Generate a key using the R1 curve (iPhone), instead of the 
            K1 curve (Bitcoin)

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.    
    """
    def __init__(
            self, key_name, key_public="", key_private="", r1=False, is_verbose=1):

        if key_public or key_private:
            self.json["publicKey"] = self.key_public = key_public           
            self.json["privateKey"] = self.key_private = key_private
            self.out_msg = "Private key: {0}\nPublic key: {1}\n" \
                .format(key_private,key_public)
        else:
            args = []
            if r1:
                args.append("--r1")

            _Cleos.__init__(
                self, args, "create", "key", is_verbose)
            
            if not self.error:
                self.json["name"] = key_name
                msg = str(self.out_msg)
                first_collon = msg.find(":")
                first_end = msg.find("\n")
                second_collon = msg.find(":", first_collon + 1)
                self.json["privateKey"] = msg[first_collon + 2 : first_end]
                self.json["publicKey"] = msg[second_collon + 2 : len(msg) - 1]
                self.printself()
                self.key_private = self.json["privateKey"]
                self.key_public = self.json["publicKey"]

        self.name = key_name



class RestoreAccount():

    def __init__(self, name, is_verbose=1):

        acc = GetAccount(name, is_verbose=0, json=True)
        acc.copy_to(self)

        if not self.error:
            self.name = self.json["account_name"]
            self.owner_key = ""
            self.active_key = ""
            self.is_verbose = setup.is_verbose() and is_verbose > 0

    def info(self):
        print(str(GetAccount(self.name, is_verbose=0)))

    def __str__(self):
        return self.name


class CreateAccount(_Cleos):
    """Create an account, buy ram, stake for bandwidth for the account.

    - **parameters**::

        creator: The name, of the account creating the new account. May be an 
            object having the attribute `name`, like `CreateAccount`, 
            or a string.
        name: The name of the new account.
        owner_key: The owner public key for the new account.
        active_key: The active public key for the new account.

        permission: An account and permission level to authorize, as in 
            'account@permission'. May be a `CreateAccount` or `Account` object
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        forceUnique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidently issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).

    - **attributes**::

        owner_key: Owner private key.
        active_key: Active private key.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.    
    """
    def __init__(
            self, creator, name, owner_key, 
            active_key="",
            permission="",
            expiration_sec=30, 
            skip_signature=0, 
            dont_broadcast=0,
            forceUnique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block="",
            is_verbose=1
            ):
        try:
            creator_name = creator.name
        except:
            creator_name = creator

        self.owner_key = None # private keys
        self.active_key = None
        
        try:
            owner_key_public = owner_key.key_public
            self.owner_key = owner_key.key_private
        except:
            owner_key_public = owner_key

        if not active_key:
            active_key = owner_key
        try:
            active_key_public = active_key.key_public
            self.active_key = active_key.key_private
        except:
            active_key_public = active_key
        self.name = name
        
        args = [creator_name, name, owner_key_public, active_key_public]
        if setup.is_json():
            args.append("--json")
        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission
            args.extend(["--permission", permission_name])
        args.extend(["--expiration", str(expiration_sec)])
        if skip_signature:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if forceUnique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", max_cpu_usage])
        if  max_net_usage:
            args.extend(["--max-net-usage", max_net_usage])
        if  ref_block:
            args.extend(["--ref-block", ref_block])

        _Cleos.__init__(
            self, args, "create", "account", is_verbose)
            
        if not self.error:
            self.transaction = get_transaction_id(self)
            self.json = GetAccount(name, is_verbose=0, json=True).json
            self.printself()

    def info(self):
        print(str(GetAccount(self.name, is_verbose=0)))

    def get_transaction(self):
        return GetTransaction(self.transaction)
            
    def __str__(self):
        return self.name


def account_name():
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name


class SetContract(_Cleos):
    """Create or update the contract on an account.

    - **parameters**:: 

        account: The account to publish a contract for. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string.
        contract_dir: The path containing the .wast and .abi. 
        wast_file: The file containing the contract WAST or WASM (absolute).
        abi_file: The ABI for the contract (absolute).

        permission: An account and permission level to authorize, as in 
            'account@permission'. May be a `CreateAccount` or `Account` object
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        forceUnique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidently issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.    
    """
    def __init__(
            self, account, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=1,
            json=False
            ):

        try:
            self.account_name = account.name
        except:
            self.account_name = account

        try:
            permission_name = permission.name
        except:
             permission_name = permission

        import teos
        config = teos.GetConfig(contract_dir, is_verbose=0)
        try:
            self.contract_path_absolute = config.json["contract-dir"]
            wast_file = config.json["contract-wast"]
            abi_file = config.json["contract-abi"]
        except:
            self.set_error("cannot find the contract directory.")
            return

        args = [self.account_name, self.contract_path_absolute]
        if setup.is_json() or json:
            args.append("--json")
        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission
            args.extend(["--permission", permission_name])
        args.extend(["--expiration", str(expiration_sec)])
        if skip_signature:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if forceUnique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", max_cpu_usage])
        if  max_net_usage:
            args.extend(["--max-net-usage", max_net_usage])
        if  ref_block:
            args.extend(["--ref-block", ref_block]) 
        if wast_file:
            args.append(wast_file)
        if abi_file:
            args.append(abi_file)

        _Cleos.__init__(
            self, args, "set", "contract", is_verbose)

        if not self.error:
            if setup.is_json() or json:
                self.json = json_module.loads(self.out_msg)
            self.transaction = get_transaction_id(self)
            self.printself()

    def get_transaction(self):
        return GetTransaction(self.transaction)


class PushAction(_Cleos):
    """Push a transaction with a single action

    - **parameters**::

        account: The account to publish a contract for.  May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string.
        action: A JSON string or filename defining the action to execute on 
            the contract.
        data: The arguments to the contract.

        permission: An account and permission level to authorize, as in 
            'account@permission'. May be a `CreateAccount` or `Account` object
        expiration: The time in seconds before a transaction expires, 
            defaults to 30s
        skip_sign: Specify if unlocked wallet keys should be used to sign 
            transaction.
        dont_broadcast: Don't broadcast transaction to the network (just print).
        forceUnique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidently issuing the 
            same transaction multiple times.
        max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
            the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: Upper limit on the net usage budget, in bytes, for the 
            transaction (defaults to 0 which means no limit).
        ref_block: The reference block num or block id used for TAPOS 
            (Transaction as Proof-of-Stake).

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the construction time.
    """
    def __init__(
            self, account, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=1,
            json=False
        ):
        try:
            self.account_name = account.name
        except:
            self.account_name = account

        args = [self.account_name, action, data]
        if setup.is_json() or json:
            args.append("--json")

        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission

            args.extend(["--permission", permission_name])
        args.extend(["--expiration", str(expiration_sec)])
        if skip_signature:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if forceUnique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", max_cpu_usage])
        if  max_net_usage:
            args.extend(["--max-net-usage", max_net_usage])
        if  ref_block:
            args.extend(["--ref-block", ref_block])
                        
        self.console = None
        self.data = None
        _Cleos.__init__(self, args, "push", "action", is_verbose)

        if not self.error:
            self.transaction = get_transaction_id(self)
            try:
                self.json = json_module.loads(self.out_msg)
                self.console = self.json["processed"]["action_traces"][0]["console"]
                self.data = self.json["processed"]["action_traces"][0]["act"]["data"]
            except:
                pass

            self.printself()

    def get_transaction(self):
        return GetTransaction(self.transaction)
