import subprocess
import json
import pathlib
import re
import random
import pprint

import core.utils as utils
import core.errors as errors
import core.config
import shell.setup as setup
import core.logger as logger
from shell.interface import *


# TO DO resolve this code reuse issue.
def set_local_nodeos_address_if_none():
    if not setup.nodeos_address():
        setup.set_nodeos_address(
            "http://" + pyteos.core.config.getHttpServerAddress())
        setup.is_local_address = True

    return setup.is_local_address


class _Eosjs():
    '''A prototype for ``cleos`` command classes.
    '''

    def __init__(self, js, is_verbose=1):
        self.out_msg = None
        self.err_msg = None
        self.json = None
        self.is_verbose = is_verbose
        cl = ["node", "-e"]
        js = utils.heredoc(js)
        # js = re.sub("\s+", " ", js.strip()) 
        cl.append(js)
        self.js = js

        set_local_nodeos_address_if_none()
        # cl.extend(["--url", setup.nodeos_address()])

        if setup.is_print_command_line:
            print("javascript:")
            print("___________")
            print("")
            print(js)
            print("")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE) 
        import pdb; pdb.set_trace()
        self.err_msg = process.stderr.decode("utf-8")
        if self.err_msg:
            raise errors.Error(self.err_msg)

        out = process.stdout.decode("utf-8")
        if "FetchError:" in out:
            out = out[out.find("{") + 2 :out.find("}")]
            self.err_msg = out
            raise errors.Error(self.err_msg)
        else:
            out = out[out.find("{"):]
            self.out_msg = out
        try:
            out = out.replace("'", '"')
            out = out.replace(': ', '": ')
            search = re.compile(r'\s(?=[a-z])')
            out = re.sub(search, ' "', out)
            out = out.replace('"null', 'null')
            out = out.replace('"false', 'false')
            out = out.replace('"true', 'true')
            out = out.replace('Object', '"Object"')
            self.json = json.loads(out)
        except Exception as e:
            print("ERROR:")
            print(out)
            raise e

        self.printself()
                  
    def printself(self):
        if self.is_verbose:
            logger.OUT(self.__str__())

    def __str__(self):
        if not self.json:
            return str(self.out_msg)
        return json.dumps(self.json, sort_keys=True, indent=4)

    def __repr__(self):
        return ""


class GetInfo(_Eosjs):
    '''Get current blockchain information.

    - **parameters**::

        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, is_verbose=1):

        _Eosjs.__init__(
            self, 
            '''
    const Eos = require('eosjs'); 
    Eos().getInfo(
        (error, result) => {console.log(error, result);}
    );
            ''', 
            is_verbose)

        self.head_block = self.json["head_block_num"]
        self.head_block_time = self.json["head_block_time"]
        self.last_irreversible_block_num \
            = self.json["last_irreversible_block_num"]


def get_last_block():
    info = GetInfo(is_verbose=0)
    return GetBlock(info.head_block)


def get_block_trx_data(block_num):
    block = GetBlock(block_num, is_verbose=0)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))
    else:
        for trx in trxs:
            logger.OUT(trx["trx"]["transaction"]["actions"][0]["data"])


def get_block_trx_count(block_num):
    block = GetBlock(block_num, is_verbose=0)
    trxs = block.json["transactions"]
    if not len(trxs):
        logger.OUT("No transactions in block {}.".format(block_num))    
    return len(trxs)


class GetBlock(_Eosjs):
    '''Retrieve a full block from the blockchain.

    - **parameters**::
    
        block_number: The number of the block to retrieve.
        block_id: The ID of the block to retrieve, if set, defaults to "".
        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.
            
    - **attributes**::

        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.    
    '''
    def __init__(self, block_number, block_id=None, is_verbose=1):
        block =  block_id if block_id else str(block_number)
        _Eosjs.__init__(
            self,
'''
    const Eos = require('eosjs'); 
    Eos().getBlock(
        {}, 
        (error, result) => {console.log(error, result);}
    );
            '''.format(block),
            is_verbose)

        self.block_num = self.json["block_num"]
        self.ref_block_prefix = self.json["ref_block_prefix"]
        self.timestamp = self.json["timestamp"]

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)


class GetAccount(Account, _Eosjs):
    '''Retrieve an account from the blockchain.

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        name: The name of the account.
        json: The json representation of the object.
        is_verbose: If set, print output.

    - **output json**::
    '''
    def __init__(self, account, is_info=True, is_verbose=True):
        Account.__init__(self, account_arg(account))
        _Eosjs.__init__(
            self, 
            '''
    const Eos = require('eosjs'); 
    Eos().getAccount(
        '{}', 
        (error, result) => {console.log(error, result);}
    );
            '''.format(self.name),
            is_verbose)

        self.owner_key = None
        self.active_key = None

        if self.json["permissions"][1]["required_auth"]:
            pass
            # self.owner_key = self.json["permissions"][1] \
            #     ["required_auth"]["keys"][0]["key"]
            # self.active_key = self.json["permissions"][0] \
            #     ["required_auth"]["keys"][0]["key"]                     


class GetAccounts(_Eosjs):
    '''Retrieve accounts associated with a public key.

    - **parameters**::

        key: A key object or a key string 

    - **attributes**::

        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, key, is_verbose=True):
        _Eosjs.__init__(
            self,
            '''
    const Eos = require('eosjs'); 
    Eos().getKeyAccounts('{}', 
        (error, result) => {console.log(error, result);}
        );            
            '''.format(key_arg(key, is_owner_key=True, is_private_key=False)),
            is_verbose)

        # self.names = self.json['account_names']

    def printself(self):
        if self.is_verbose:
            logger.OUT(pprint.pformat(self.json["account_names"]))


class GetTransaction(_Eosjs):
    '''Retrieve a transaction from the blockchain.

    - **parameters**::

        transaction_id: ID of the transaction to retrieve.
        block_num_hint: A non-zero block number allows shorter transaction IDs 
            (8 hex, 4 bytes). Default is ``0``.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        transaction_id: ID of the transaction retrieved.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, transaction_id, block_num_hint=0, is_verbose=True):
        _Eosjs.__init__(
            self, 
            '''
    const Eos = require('eosjs'); 
    Eos().getKeyAccounts('{}', 
        (error, result) => {console.log(error, result);}
        );            
            '''.format(transaction_id, block_num_hint),
            
            is_verbose)


# class WalletCreate(Wallet, _Eosjs):
#     '''Create a new wallet locally.

#     - **parameters**::

#         name: The name of the new wallet, defaults to ``default``.
#         password: The password to the wallet, if the wallet exists. Default is None.
#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **attributes**::

#         name: The name of the wallet.
#         password: The password returned by wallet create.
#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, name="default", password="", is_verbose=True):
#         Wallet.__init__(self, name)
#         self.password = None
        
#         if not password: # try to create a wallet
#             _Eosjs.__init__(
#                 self, ["--name", self.name, "--to-console"], 
#                 "wallet", "create", is_verbose)
#             self.json["name"] = name
#             msg = self.out_msg

#             self.password = msg[msg.find("\"")+1:msg.rfind("\"")]
#             self.json["password"] = self.password
#             self.is_created = True

#         else: # try to open an existing wallet
#             WalletOpen(name, is_verbose=False)
#             wallet_unlock = WalletUnlock(name, password, is_verbose=False)
#             self.json = {} 
#             self.name = name
#             self.password = password
#             self.is_created = False
#             self.json["name"] = name
#             self.json["password"] = password
#             self.out_msg = "Restored wallet: {}".format(self.name)

#         self.printself(is_verbose)


# class WalletStop(_Eosjs):
#     '''Stop keosd (doesn't work with nodeos).
#     '''
#     def __init__(self, is_verbose=True):
#         _Eosjs.__init__(self, [], "wallet", "stop", is_verbose)

#         self.printself()


# class WalletList(_Eosjs):
#     '''List opened wallets, * marks unlocked.

#     - **parameters**::

#         is_verbose: If ``False`` do not print. Default is ``True``.
            
#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, is_verbose=True):
#         _Eosjs.__init__(
#             self, [], "wallet", "list", is_verbose)

#         self.json = json.loads("{" + self.out_msg.replace("Wallets", \
#             '"Wallets"', 1) + "}")
#         self.printself()


# class WalletImport(_Eosjs):
#     '''Import a private key into wallet.

#     - **parameters**::

#         wallet: A wallet object or the name of the wallet to import key into.
#         key: A key object or a private key in WIF format to import.
#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, key, wallet="default", is_verbose=True):
#         key_private = key_arg(key, is_owner_key=True, is_private_key=True)
#         _Eosjs.__init__(
#             self, 
#             ["--private-key", key_private, "--name", wallet_arg(wallet)],
#             "wallet", "import", is_verbose)

#         self.json["key_private"] = key_private
#         self.key_private = key_private
#         self.printself()

# class WalletRemove_key(_Eosjs):
#     '''Remove key from wallet
#     - **parameters**::

#         wallet: A wallet object or the name of the wallet to import key into.
#         password: The password returned by wallet create.
#         key: A key object or a private key in WIF format to import.
#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **attributes**::

#         error: Whether any error ocurred.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, key, wallet, password, is_verbose=True):
#         key_public = key_arg(key, is_owner_key=True, is_private_key=False)

#         _Eosjs.__init__(
#             self, 
#             [key_public, "--name", wallet_arg(wallet), 
#                 "--password", password], 
#             "wallet", "remove_key", is_verbose)

#         self.json["key_public"] = key_public
#         self.key_public = key_public
#         self.printself()


# class WalletKeys(_Eosjs):
#     '''List of public keys from all unlocked wallets.

#     - **parameters**::

#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **parameters**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, is_verbose=True):
#         _Eosjs.__init__(
#             self, [], "wallet", "keys", is_verbose)                
#         self.printself() 

#     def __str__(self):
#         out = "Keys in all opened wallets:\n"
#         out = out + str(_Eosjs.__str__(self))
#         return out


# class WalletOpen(_Eosjs):
#     '''Open an existing wallet.

#     - **parameters**::

#         wallet: The name of the wallet to import key into. May be an object 
#             having the  May be an object having the attribute `name`, like 
#             `CreateAccount`, or a string. 
#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, wallet="default", is_verbose=True):
#         _Eosjs.__init__(
#             self, ["--name", wallet_arg(wallet)], 
#             "wallet", "open", is_verbose)

#         self.printself()


# class WalletLockAll(_Eosjs):
#     '''Lock all unlocked wallets.
#     '''
#     def __init__(self, is_verbose=True):
#         _Eosjs.__init__(
#             self, [], "wallet", "lock_all", is_verbose)

#         self.printself()


# class WalletLock(_Eosjs):
#     '''Lock wallet.

#     - **parameters**::

#         wallet: The name of the wallet to import key into. May be an object 
#             having the  May be an object having the attribute `name`, like 
#             `CreateAccount`, or a string. 
#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **parameters**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(self, wallet="default", is_verbose=True):
#         _Eosjs.__init__(
#             self, ["--name", wallet_arg(wallet)], 
#             "wallet", "lock", is_verbose)

#         self.printself()


# class WalletUnlock(_Eosjs):
#     '''Unlock wallet.

#     - **parameters**::

#         wallet: The name of the wallet. May be an object 
#             having the  May be an object having the attribute `name`, 
#             like `CreateAccount`, or a string.
#         password: If the wallet argument is not a wallet object, the password 
#             returned by wallet create, else anything, defaults to "".
#         is_verbose: If ``False`` do not print. Default is ``True``.

#     - **attributes**::
    
#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(
#             self, wallet="default", password="", timeout=0, is_verbose=True):
 
#         if isinstance(wallet, Wallet):
#             password = wallet.password

#         _Eosjs.__init__(
#             self, 
#             ["--name", wallet_arg(wallet), "--password", password], 
#             "wallet", "unlock", is_verbose)

#         self.printself()


# class GetCode(_Eosjs):
#     '''Retrieve the code and ABI for an account.

#     - **parameters**::

#         account: The name of an account whose code should be retrieved. 
#             May be an object having the  May be an object having the attribute 
#             `name`, like `CreateAccount`, or a string.
#         code: The name of the file to save the contract .wast/wasm to.
#         abi: The name of the file to save the contract .abi to.
#         wasm: Save contract as wasm.

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.    
#     '''
#     def __init__(
#             self, account, code="", abi="", 
#             wasm=False, is_verbose=True):

#         account_name = account_arg(account)

#         args = [account_name]
#         if code:
#             args.extend(["--code", code])
#         if abi:
#             args.extend(["--abi", abi])
#         if wasm:
#             args.extend(["--wasm"])

#         _Eosjs.__init__(self, args, "get", "code", is_verbose)

#         msg = str(self.out_msg)
#         self.json["code_hash"] = msg[msg.find(":") + 2 : len(msg) - 1]
#         self.code_hash = self.json["code_hash"]
#         self.printself()


# class GetTable(_Eosjs):
#     '''Retrieve the contents of a database table

#     - **parameters**::

#         account: The name of the account that owns the table. May be 
#             an object having the  May be an object having the attribute 
#             `name`, like `CreateAccount`, or a string.
#         scope: The scope within the account in which the table is found,
#             can be a `CreateAccount` or `Account` object, or a name.
#         table: The name of the table as specified by the contract abi.
#         binary: Return the value as BINARY rather than using abi to 
#             interpret as JSON
#         limit: The maximum number of rows to return.
#         key: The name of the key to index by as defined by the abi, 
#             defaults to primary key.
#         lower: JSON representation of lower bound value of key, 
#             defaults to first.
#         upper: JSON representation of upper bound value value of key, 
#             defaults to last.

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(
#             self, account, table, scope,
#             binary=False, 
#             limit=10, key="", lower="", upper="",
#             is_verbose=True
#             ):
#         args = [account_arg(account)]

#         if not scope:
#             scope=self.name
#         else:
#             try:
#                 scope_name = scope.name
#             except:
#                 scope_name = scope

#         args.append(scope_name)
#         args.append(table)

#         if binary:
#             args.append("--binary")
#         if limit:
#             args.extend(["--limit", str(limit)])
#         if key:
#             args.extend(
#                 ["--key", 
#                 key_arg(key, is_owner_key=False, is_private_key=False)])
#         if lower:
#             args.extend(["--lower", lower])
#         if upper:
#             args.extend(["--upper", upper])

#         _Eosjs.__init__(self, args, "get", "table", is_verbose)

#         self.printself()


# class CreateKey(Key, _Eosjs):
#     '''Create a new keypair and print the public and private keys.

#     - **parameters**::

#         key_name: Key name.
#         r1: Generate a key using the R1 curve (iPhone), instead of the 
#             K1 curve (Bitcoin)

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.    
#     '''
#     def __init__(
#             self, key_name, key_public="", key_private="", r1=False, is_verbose=True):
#         Key.__init__(self, key_name, key_public, key_private)

#         if self.key_public or self.key_private:
#             self.json = {}
#             self.json["publicKey"] = self.key_public           
#             self.json["privateKey"] = self.key_private
#             self.out_msg = "Private key: {0}\nPublic key: {1}\n" \
#                 .format(self.key_private, self.key_public)
#         else:
#             args = ["--to-console"]
#             if r1:
#                 args.append("--r1")

#             _Eosjs.__init__(
#                 self, args, "create", "key", is_verbose)
            
#             self.json["name"] = key_name
#             msg = str(self.out_msg)
#             first_collon = msg.find(":")
#             first_end = msg.find("\n")
#             second_collon = msg.find(":", first_collon + 1)
#             self.json["privateKey"] = msg[first_collon + 2 : first_end]
#             self.json["publicKey"] = msg[second_collon + 2 : len(msg) - 1]
#             self.printself()
#             self.key_private = self.json["privateKey"]
#             self.key_public = self.json["publicKey"]

#         self.name = key_name

# class RestoreAccount(GetAccount):

#     def __init__(self, account, is_verbose=True):
#         GetAccount.__init__(self, account, is_verbose=False, is_info=False)

#         self.name = self.json["account_name"]
#         self.owner_key = ""
#         self.active_key = ""
        
#     def info(self):
#         print(str(GetAccount(self.name, is_verbose=False)))

#     def __str__(self):
#         return self.name


class CreateAccount(Account, _Eosjs):
    '''Create an account, buy ram, stake for bandwidth for the account.

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
        is_verbose: If set, print output.    
    '''
    def __init__(
            self, creator, name, owner_key, 
            active_key=None,
            permission=None,
            expiration_sec=30, 
            skip_signature=0, 
            dont_broadcast=0,
            forceUnique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block=None,
            is_verbose=True
            ):

        if name is None: 
            name = account_name()
        Account.__init__(self, name)

        self.owner_key = None # private keys
        self.active_key = None
        
        if active_key is None:
            active_key = owner_key        

        owner_key_public = key_arg(
            owner_key, is_owner_key=True, is_private_key=False)
        active_key_public = key_arg(
            active_key, is_owner_key=False, is_private_key=False)

        args = [
                account_arg(creator), self.name, 
                owner_key_public, active_key_public
            ]

        args.append("--json")
        if not permission is None:
            p = permission_arg(permission)
            for perm in p:
                args.extend(["--permission", perm])

        args.extend(["--expiration", str(expiration_sec)])
        if skip_signature:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if forceUnique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if  max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if  not ref_block is None:
            args.extend(["--ref-block", ref_block])
        import pdb; pdb.set_trace()
        _Eosjs.__init__(
            self,
#             '''
# const Eos = require('eosjs');
# eosConfig = {keyProvider: 
#     ['5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3']}
# let eos = Eos(eosConfig)
# eos.transaction(tr => {
#     tr.newaccount({
#         creator: 'eosio',
#         name: '{0}',
#         owner: '{1}',
#         active: '{2}'
#     })});
#            '''
            '''
    Eos = require("eosjs");
    binaryen = require("binaryen");

    keyProvider = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
    pubkey = "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV";

    eos = Eos({ keyProvider, binaryen });

    eos.transaction(tr => {
        tr.newaccount({
            creator: "%s",
            name: "%s",
            owner: pubkey,
            active: pubkey
        });
    });
            ''' % (creator, name),
            is_verbose)
            
    #     self.json = GetAccount(self.name, is_verbose=False, is_info=False).json
    #     self.printself()

    # def info(self):
    #     print(str(GetAccount(self.name, is_verbose=False)))

    # def get_transaction(self):
    #     return GetTransaction(self.transaction)
            
    def __str__(self):
        return self.name


def account_name():
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name

# def contract_is_built(contract_dir, wasm_file=None, abi_file=None):

#     contract_path_absolute = config.getContractDir(contract_dir)
#     if not contract_path_absolute:
#         return []

#     if not wasm_file:
#         wasm_file = config.get_wasm_file(contract_dir)
#         if not wasm_file:
#             return []
#     else:
#         if not os.path.isfile(
#                 os.path.join(contract_path_absolute, wasm_file)):
#             return []

#     if not abi_file:
#         abi_file = config.get_abi_file(contract_dir)
#         if not abi_file:
#             return []
#     else:
#         if not os.path.isfile(
#                 os.path.join(contract_path_absolute, abi_file)):
#             return []

#     return [contract_path_absolute, wasm_file, abi_file]

# class SetContract(_Eosjs):
#     '''Create or update the contract on an account.

#     - **parameters**:: 

#         account: The account to publish a contract for. May be an object 
#             having the  May be an object having the attribute `name`, like 
#             `CreateAccount`, or a string.
#         contract_dir: The path containing the .wast and .abi. 
#         wasm_file: The file containing the contract WASM relative 
#             to contract_dir.
#         abi_file: The ABI for the contract relative to contract-dir.

#         permission: An account and permission level to authorize, as in 
#             'account@permission'. May be a `CreateAccount` or `Account` object
#         expiration: The time in seconds before a transaction expires, 
#             defaults to 30s
#         skip_sign: Specify if unlocked wallet keys should be used to sign 
#             transaction.
#         dont_broadcast: Don't broadcast transaction to the network (just print).
#         forceUnique: Force the transaction to be unique. this will consume extra 
#             bandwidth and remove any protections against accidently issuing the 
#             same transaction multiple times.
#         max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
#             the execution of the transaction 
#             (defaults to 0 which means no limit).
#         max_net_usage: Upper limit on the net usage budget, in bytes, for the 
#             transaction (defaults to 0 which means no limit).
#         ref_block: The reference block num or block id used for TAPOS 
#             (Transaction as Proof-of-Stake).

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.    
#     '''
#     def __init__(
#             self, account, contract_dir, 
#             wasm_file=None, abi_file=None, 
#             permission=None, expiration_sec=30, 
#             skip_signature=0, dont_broadcast=0, forceUnique=0,
#             max_cpu_usage=0, max_net_usage=0,
#             ref_block=None,
#             is_verbose=True,
#             json=False
#             ):

#         files = contract_is_built(contract_dir, wasm_file, abi_file)
#         if not files:
#             raise errors.Error("""
#             Cannot determine the contract directory. The clue is 
#             {}.
#             """.format(contract_dir))
#             return

#         self.contract_path_absolute = files[0]
#         wasm_file = files[1]
#         abi_file = files[2]            

#         self.account_name = account_arg(account)

#         args = [self.account_name, self.contract_path_absolute]

#         if json:
#             args.append("--json")
#         if not permission is None:
#             p = permission_arg(permission)
#             for perm in p:
#                 args.extend(["--permission", perm])

#         args.extend(["--expiration", str(expiration_sec)])
#         if skip_signature:
#             args.append("--skip-sign")
#         if dont_broadcast:
#             args.append("--dont-broadcast")
#         if forceUnique:
#             args.append("--force-unique")
#         if max_cpu_usage:
#             args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
#         if  max_net_usage:
#             args.extend(["--max-net-usage", str(max_net_usage)])
#         if  not ref_block is None:
#             args.extend(["--ref-block", ref_block]) 
#         if wasm_file:
#             args.append(wasm_file)
#         if abi_file:
#             args.append(abi_file)

#         _Eosjs.__init__(
#             self, args, "set", "contract", is_verbose)

#         self.printself()

#     def get_transaction(self):
#         return GetTransaction(self.transaction)


# class PushAction(_Eosjs):
#     '''Push a transaction with a single action

#     - **parameters**::

#         account: The account to publish a contract for.  May be an object 
#             having the  May be an object having the attribute `name`, like 
#             `CreateAccount`, or a string.
#         action: A JSON string or filename defining the action to execute on 
#             the contract.
#         data: The arguments to the contract.

#         permission: An account and permission level to authorize, as in 
#             'account@permission'. May be a `CreateAccount` or `Account` object
#         expiration: The time in seconds before a transaction expires, 
#             defaults to 30s
#         skip_sign: Specify if unlocked wallet keys should be used to sign 
#             transaction.
#         dont_broadcast: Don't broadcast transaction to the network (just print).
#         forceUnique: Force the transaction to be unique. this will consume extra 
#             bandwidth and remove any protections against accidently issuing the 
#             same transaction multiple times.
#         max_cpu_usage: Upper limit on the milliseconds of cpu usage budget, for 
#             the execution of the transaction 
#             (defaults to 0 which means no limit).
#         max_net_usage: Upper limit on the net usage budget, in bytes, for the 
#             transaction (defaults to 0 which means no limit).
#         ref_block: The reference block num or block id used for TAPOS 
#             (Transaction as Proof-of-Stake).

#     - **attributes**::

#         error: Whether any error ocurred.
#         json: The json representation of the object.
#         is_verbose: If set, print output.
#     '''
#     def __init__(
#             self, account, action, data,
#             permission=None, expiration_sec=30, 
#             skip_signature=0, dont_broadcast=0, forceUnique=0,
#             max_cpu_usage=0, max_net_usage=0,
#             ref_block=None,
#             is_verbose=True,
#             json=False
#         ):
#         self.account_name = account_arg(account)

#         args = [self.account_name, action, data]
#         if json:
#             args.append("--json")
#         if not permission is None:
#             p = permission_arg(permission)
#             for perm in p:
#                 args.extend(["--permission", perm])

#         args.extend(["--expiration", str(expiration_sec)])
#         if skip_signature:
#             args.append("--skip-sign")
#         if dont_broadcast:
#             args.append("--dont-broadcast")
#         if forceUnique:
#             args.append("--force-unique")
#         if max_cpu_usage:
#             args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
#         if  max_net_usage:
#             args.extend(["--max-net-usage", str(max_net_usage)])
#         if  not ref_block is None:
#             args.extend(["--ref-block", ref_block])
                        
#         self.console = None
#         self.data = None
#         _Eosjs.__init__(self, args, "push", "action", is_verbose)

#         self.console = self.json["processed"]["action_traces"][0]["console"]
#         self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

#         self.printself()

#     def get_transaction(self):
#         return GetTransaction(self.transaction)
