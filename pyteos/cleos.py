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

setup_setup = setup.Setup()

_dont_keosd = []
def dont_keosd(status=True):
    """ Do not use `keosd` Wallet Manager.

    Instead, use `nodeos`. See https://github.com/EOSIO/eos/wiki/CLI-Wallet
    for explanations.

    If wallets are not managed by `keosd`, they can be reset with the
    `teos.node_reset()` function, what is desired when testing smart contracts
    locally.
    """
    global _dont_keosd
    if status:
        WalletStop(is_verbose=False, suppress_error_msg=True)
        config = teos.GetConfig(
            "", is_verbose=False)
        _dont_keosd = ["--wallet-url", "http://" \
            + config.json["EOSIO_DAEMON_ADDRESS"]]
    else:
        _dont_keosd = []

class _Cleos:
    """ A prototype for the `cleos` command classes. 
    """
    global setup_setup

    error = False
    _out = ""
    _err = ""
    isVerbose = True

    def __init__(
                self, args, first, second, 
                is_verbose=True, suppress_error_msg=False, 
                ok_substring="OK"):

        cl = [setup_setup.cleos_exe]
        global _dont_keosd
        cl.extend(_dont_keosd)

        if setup.is_print_request():
            cl.append("--print-request")
        if setup.is_print_response():
            cl.append("--print-response")

        cl.extend([first, second])
        cl.extend(args)
        self.args = args

        if setup.is_debug_mode():
            print("command line sent to cleos:")
            print(" ".join(cl))
            print("")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=str(pathlib.Path(setup_setup.cleos_exe).parent)) 

        self._out = process.stdout.decode("utf-8")
        self._err = process.stderr.decode("utf-8")
        self.is_verbose = setup.is_verbose() and is_verbose

        if setup.is_print_response() or setup.is_print_response():
            print(self._err)
            print("")

        self.error = ok_substring not in str(self._out)
        if self._err and self.error \
                and not setup.is_suppress_error_msg() and not suppress_error_msg:
            print("ERROR:")
            print(self._err)
            print("")              

        if self.is_verbose:
            print(self._out)
            print("")

    def __str__(self):
        return self._out
    
    def __repr__(self):
        return repr(self._out)      

    
class GetAccount(_Cleos):
    """ Retrieve an account from the blockchain.
    Usage: GetAccount(name, is_verbose=True)

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.

    - **attributes**::

        name: The name of the account.
        error: Whether any error ocurred.
        json: The json representation of the account, if `error` is not set.    
    """
    def __init__(self, account, is_verbose=True, suppress_error_msg=False):
        try:
            account_name = account.name
        except:
            account_name = account

        _Cleos.__init__(
            self, [account_name], 
            "get", "account", is_verbose, suppress_error_msg)

        if not self.error:
            self.name = self.json["account_name"]


class GetAccounts(_Cleos):
    """ Retrieve accounts associated with a public key.
    Usage: GetAccounts(public_key, is_verbose=True)
    """
    def __init__(self, key, is_verbose=True):
        try:
            key_public = key.key_public
        except:
            key_public = key

        _Cleos.__init__(
            self, [key_public], "get", "accounts", is_verbose)


class WalletCreate(_Cleos):
    """ Create a new wallet locally.
    Usage: WalletCreate(name="default", is_verbose=True)

    - **parameters**::

        name: The name of the new wallet, defaults to `default`.
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred. /////////////////////////////////////// TO_DO: add json   
    """
    def __init__(self, name="default", is_verbose=True):
        _Cleos.__init__(
            self, ["--name", name], "wallet", "create", is_verbose)
        msg = self._out
        if not self.error:
            self.name = name
            self.json = json.loads("{}")
            self.json["name"] = name
            self.json["password"] = msg[msg.find("\"")+1:msg.rfind("\"")]
            self.password = self.json["password"]


class WalletStop(_Cleos):
    """Stop keosd (doesn't work with nodeos).
    Usage: WalletStop(is_verbose=True, suppress_error_msg=False)
    """
    def __init__(self, is_verbose=True, suppress_error_msg=False):
        _Cleos.__init__(
            self, [], 
            "wallet", "stop", is_verbose, suppress_error_msg)


class WalletList(_Cleos):
    """ List opened wallets, * marks unlocked.
    Usage: WalletList(is_verbose=True)

    - **parameters**::

        is_verbose: If `False`, do not print unless on error, 
            default is `True`.    
    """
    def __init__(self, is_verbose=True):
        _Cleos.__init__(self, [], "wallet", "list", is_verbose)


class WalletImport(_Cleos):
    """ Import private key into wallet.
    Usage: WalletImport(key, wallet="default", is_verbose=True)

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        key: A key object or a private key in WIF format to import.
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.
    """
    def __init__(self, key, wallet="default", is_verbose=True):
        try:
            key_private = key.key_private
        except:
            key_private = key 

        try:
            wallet_name = wallet.name
        except:
            wallet_name = wallet

        _Cleos.__init__(
            self, [key_private, "--name", wallet_name], 
            "wallet", "import", is_verbose)
        if not self.error:       
            self.key_private = key_private


class WalletKeys(_Cleos):
    """ List of public keys from all unlocked wallets.
    Usage: WalletKeys(is_verbose=True)

    - **parameters**::

        is_verbose: If `False`, do not print unless on error, 
            default is `True`.
    """
    def __init__(self, is_verbose=True):
        _Cleos.__init__(self, [], "wallet", "keys", is_verbose)         


class WalletOpen(_Cleos):
    """ Open an existing wallet.
    Usage: WalletOpen(wallet="default", is_verbose=True)

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.    
    """
    def __init__(self, wallet="default", is_verbose=True):      
        try:
            wallet_name = wallet.name
        except:
            wallet_name = wallet
        
        _Cleos.__init__(
            self, ["--name", wallet_name], "wallet", "open", is_verbose)


class WalletLock(_Cleos):
    """ Lock wallet.
    Usage: WalletLock(wallet="default", is_verbose=True)

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.     
    """
    def __init__(self, wallet="default", is_verbose=True):
        try:
            name = wallet.name
        except:
            name = wallet
        
        _Cleos.__init__(
            self, ["--name", wallet_name], "wallet", "lock", is_verbose)


class WalletUnlock(_Cleos):
    """ Unlock wallet.
    Usage: WalletUnlock(
        wallet="default", password="", timeout=0, is_verbose=True)

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, 
            like `CreateAccount`, or a string.
        password: If the wallet argument is not a wallet object, the password 
            returned by wallet create, else anything, defaults to "".
        timeout: The timeout for unlocked wallet in seconds, defoults to 
            unlimited.
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.
    """
    def __init__(
            self, wallet="default", password="", timeout=0, is_verbose=True):
        try:
            wallet_name = wallet.name
            password = wallet.password
        except:
            wallet_name = wallet

        _Cleos.__init__(
            self, 
            ["--name", wallet_name, "--password", password, \
                "--unlock-timeout", timeout], 
            "wallet", "unlock", is_verbose)


class GetInfo(_Cleos):
    """ Get current blockchain information.
    Usage: GetInfo(is_verbose=True, suppress_error_msg=False)

    - **parameters**::

        is_verbose: If `False`, do not print unless on error, 
            default is `True`.
        suppress_error_msg: If `True`, do not print on error.
    """
    def __init__(self, is_verbose=True, suppress_error_msg=False):
        _Cleos.__init__(
            self, [], "get", "info", is_verbose, suppress_error_msg,
            "head_block_num")

        if not self.error:
            try:
                self.json = json.loads(str(self._out))
                self.head_block = self.json["head_block_num"]
                self.head_block_time = self.json["head_block_time"]
                self.last_irreversible_block_num \
                    = self.json["last_irreversible_block_num"]
            except:
                pass


class GetBlock(_Cleos):
    """ Retrieve a full block from the blockchain.
    Usage: GetBlock(block_number, block_id="", is_verbose=True)

    - **parameters**::
    
        block_number: The number of the block to retrieve.
        block_id: The ID of the block to retrieve, if set, defaults to "".
        is_verbose: If `False`, do not print unless on error, 
            default is `True`.    
    """
    def __init__(self, block_number, block_id="", is_verbose=True):
        args = []
        if(block_id == ""):
            args = [block_number]
        else:
            args = [block_id]
        
        _Cleos.__init__(self, args, "get", "block", is_verbose)
        if not self.error:   
            self.block_num = self.json["block_num"]
            self.ref_block_prefix = self.json["ref_block_prefix"]
            self.timestamp = self.json["timestamp"]


class GetCode(_Cleos):
    """ Retrieve the code and ABI for an account.
    Usage: GetCode(
        account, code="", abi="", wasm=False, is_verbose=True)

    - **parameters**::

        account: The name of an account whose code should be retrieved. 
            May be an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.
        code: The name of the file to save the contract .wast/wasm to.
        abi: The name of the file to save the contract .abi to.
        wasm: Save contract as wasm.
    """
    def __init__(
            self, account, code="", abi="", 
            wasm=False, is_verbose=True
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
            self.code_hash = self.json["code_hash"]
            self.code = self.json["code"] 
            if "abi" in self.json:          
                self.abi = self.json["abi"]
            else:
                self.abi = ""


class GetTable(_Cleos):
    """ Retrieve the contents of a database table
    Usage: GetTable(
        contract, scope, table, 
        binary=False, limit=0, key="", lower="", upper="",
        is_verbose=True)

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
        
    """  
    def __init__(
        self, contract, scope, table,
        limit=10, key="", lower="", upper="",
        is_verbose=True
        ):

        try:
            contract_name = contract.name
        except:
            contract_name = contract

        args = [contract_name]

        try:
            scope_name = scope.name
        except:
            scope_name = scope

        args.append(scope_name)
        args.append(table)

        if binary:
            args.append("--binary")

        if limit:
            args.extend(["--limit", limit])

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


class CreateKey(_Cleos):
    """ Create a new keypair and print the public and private keys.
    Usage: CreateKey(key_name, r1=False, is_verbose=True)

    - **parameters**::

        key_name: Key name.
        r1: Generate a key using the R1 curve (iPhone), instead of the 
            K1 curve (Bitcoin)
    """
    def __init__(self, keyPairName, is_verbose=True):
        args = [key_name]
        if r1:
            args.append("--r1")

        _Cleos.__init__(self, args, "create", "key", is_verbose)
        if not self.error:  
            self.key_private = self.json["privateKey"]
            self.key_public = self.json["publicKey"]
            self.name = keyPairName       


class CreateAccount(_Cleos):
    """ Create an account, buy ram, stake for bandwidth for the account.
    Usage: CreateAccount(
        creator, name, owner_key, active_key,
        permission="",         
        expiration=30, 
        skip_sign=False, dont_broadcast=False, force_unique=False,
        max_cpu_usage_ms=0, max_net_usage=0,
        ref_block="",
        is_verbose=True)

    - **parameters**::

        creator: The name, of the account creating the new account. May be an 
            object having the  May be an object having the attribute `name`, 
            like `CreateAccount`, or a string.
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
    """
    def __init__(
            self, creator, name, owner_key, active_key,
            permission = "",
            expiration_sec=30, 
            skip_signature=0, 
            dont_broadcast=0,
            forceUnique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block="",
            is_verbose=True
            ):
        try:
            creator_name = creator.name
        except:
            creator_name = creator

        try:
            owner_key_public = owner_key.key_public
        except:
            owner_key_public = owner_key

        try:
            active_key_public = active_key.key_public
        except:
            active_key_public = active_key

        args = [creator_name, name, owner_key_public, active_key_public]

        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission

            args.expend(["--permission", permission_name])

        if skip_signature:
            args.append("--skip-sign")

        if dont_broadcast:
            args.append("--dont-broadcast")

        if forceUnique:
            args.append("--force-unique")

        if max_cpu_usage:
            args.expend(["--max-cpu-usage-ms", max_cpu_usage])

        if  max_net_usage:
            args.expend(["--max-net-usage", max_net_usage])

        if  ref_block:
            args.expend(["--ref-block", ref_block])
               
        _Cleos.__init__(self, args, "create", "account", is_verbose)
        if not self.error:
            self.name = name


class SetContract(_Cleos):
    """ Create or update the contract on an account.
    Usage: SetContract(
            account, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=True)

    - **parameters**:: 
    
        account: The account to publish a contract for. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string.
        contract_dir: The path containing the .wast and .abi. 
        wast_file: The file containing the contract WAST or WASM relative to 
            `contract_dir`.
        abi_file: The ABI for the contract relative to `contract_dir`.

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
    """
    def __init__(
            self, account, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=True
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
        config = teos.GetConfig(contract_dir, is_verbose=False)
        try:       
            self.contract_path_absolute = config.json["contract-dir"]
        except:
            return ##############################################TO_DO
            
        args = [account_name, self.contract_path_absolute]

        if wast_file:
            args.append(wast_file)
        else:
            args.append(account_name + ".wast")
        
        if abi_file:
            args.append(abi_file)
        else:
            args.append(account_name + ".abi")

        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission

            args.expend(["--permission", permission_name])

        if skip_signature:
            args.append("--skip-sign")

        if dont_broadcast:
            args.append("--dont-broadcast")

        if forceUnique:
            args.append("--force-unique")

        if max_cpu_usage:
            args.expend(["--max-cpu-usage-ms", max_cpu_usage])

        if  max_net_usage:
            args.expend(["--max-net-usage", max_net_usage])

        if  ref_block:
            args.expend(["--ref-block", ref_block])        
       
        _Cleos.__init__(self, args, "set", "contract", is_verbose)


class PushAction(_Cleos):
    """ Push a transaction with a single action
    Usage: PushAction(
        account, action, data,
        permission="", expiration_sec=30, 
        skip_signature=0, dont_broadcast=0, forceUnique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block="",
        is_verbose=True)

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
    """
    def __init__(
            self, account, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=True        
        ):
        try:
            account_name = account.name
        except:
            account_name = account

        args = [account_name, action, data]

        if permission:
            try:
                permission_name = permission.name
            except:
                permission_name = permission

            args.expend(["--permission", permission_name])

        if skip_signature:
            args.append("--skip-sign")

        if dont_broadcast:
            args.append("--dont-broadcast")

        if forceUnique:
            args.append("--force-unique")

        if max_cpu_usage:
            args.expend(["--max-cpu-usage-ms", max_cpu_usage])

        if  max_net_usage:
            args.expend(["--max-net-usage", max_net_usage])

        if  ref_block:
            args.expend(["--ref-block", ref_block])
                        
        _Cleos.__init__(self, args, "push", "action", is_verbose)
        if not self.error:
            self.name = account_name


class Wallet(WalletCreate):

    def __init__(self, name="default", is_verbose=True):
        super().__init__(name, is_verbose)
        self.json["keys"] = []

    def list(self):
        x = WalletList()
        return not x.error

    def open(self):
        x = WalletOpen(self.name)
        return not x.error

    def lock(self):
        x = WalletLock(self.name)
        return not x.error        

    def unlock(self):
        x = WalletUnlock(self.name, self.json["password"])
        return not x.error

    def import_key(self, key_pair):
        wallet_import = WalletImport(
            key_pair, self.name, is_verbose=False)
        if not wallet_import.error:
            self.json["keys"].append([key_pair.name, key_pair.key_private])
        return not wallet_import.error        

    def keys(self):
        x = WalletKeys()
        return not x.error

    def open(self):
        x = WalletOpen(self.name)
        return not x.error

    def __str__(self):
        return pprint.pformat(self.json)


class Account(CreateAccount):

    def code(self, wast_file="", abi_file=""):
        return GetAccount(self.name, is_verbose=False).code(wast_file, abi_file)

    def set_contract(
            self, contract_dir, wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0):
        return GetAccount(self.name, is_verbose=False).set_contract(
            contract_dir, wast_file, abi_file, 
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage)

    def __str__(self):
        return str(GetAccount(self.name, is_verbose=False)) 
    
    def __repr__(self):
        return repr(GetAccount(self.name, is_verbose=False))


class AccountEosio(Account):

    def __init__(self, is_verbose=True): 
        self.json = json.loads("{}")
        self.json["privateKey"] = \
            "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.json["publicKey"] = \
            "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
        self.key_private = self.json["privateKey"]
        self.key_public = self.json["publicKey"]
        self.name = "eosio"
        self._out = "#       transaction id: eosio"   


class Contract(SetContract):

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
