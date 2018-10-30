import subprocess
import json
import pathlib
import re
import random
import pprint
import os

import eosfactory.core.utils as utils
import eosfactory.core.errors as errors
import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.logger as logger
import eosfactory.core.teos as teos
import eosfactory.core.walletmanager as wm
from eosfactory.core.interface import *


# TO DO resolve this code reuse issue.
def set_local_nodeos_address_if_none():
    if not setup.nodeos_address():
        setup.set_nodeos_address(
            "http://" + config.http_server_address())
        setup.is_local_address = True

    return setup.is_local_address


def config_rpc():
    code = utils.heredoc('''
const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('%(endpoint)s', { fetch });
    ''')

    return code % {'endpoint': setup.nodeos_address()}


def config_api():
    code = utils.heredoc('''
const eosjs = require('eosjs')
const fetch = require('node-fetch')
const rpc = new eosjs.Rpc.JsonRpc('%(endpoint)s', { fetch })

const { TextDecoder, TextEncoder } = require('text-encoding');
const signatureProvider = new eosjs.SignatureProvider(%(keys)s);
const api = new eosjs.Api({ rpc, signatureProvider, 
    textDecoder: new TextDecoder, textEncoder: new TextEncoder });
    ''')

    return code % {
        'endpoint': setup.nodeos_address(),
        'keys': json.dumps(wm.private_keys(is_verbose=False), indent=4)
        }



###############################################################################
# TO DO ?
# authorization
# :[{actor: "gy4dkmjzhege", permission: "active"}]

#     scope: [
#      "exchange"
#    ]
###############################################################################

class _Eosjs():
    '''A prototype for ``cleos`` command classes.
    '''
    def __init__(self, header, js, is_verbose=1):
        self.out_msg = None
        self.err_msg = None
        self.json = None
        self.is_verbose = is_verbose
        cl = ["node", "-e"]
        js = header + "\n" + utils.heredoc(js)

        cl.append(js)

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

        self.err_msg = process.stderr.decode("utf-8")
        if self.err_msg:
            raise errors.Error(self.err_msg)

        self.out_msg = process.stdout.decode("utf-8")
        self.json = json.loads(self.out_msg)

        self.printself()
                  
    def printself(self):
        if self.is_verbose:
            logger.OUT(self.__str__())

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)

    def __repr__(self):
        return ""


class GetInfo(_Eosjs):
    '''Get current blockchain information.

    - **parameters**::

        is_verbose: If `0`, do not print unless on error; if `-1`, 
            do not print. Default is `1`.

    - **attributes**::

        json: The json representation of the object.
        is_verbose: If set, print output.
    '''
    def __init__(self, is_verbose=1):

        _Eosjs.__init__(self, config_rpc(), 
            '''
    (async () => {
        result = await rpc.get_info()
        console.log(JSON.stringify(result))    
    })()
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

        json: The json representation of the object.
    '''
    def __init__(self, block_number, block_id=None, is_verbose=1):
        if block_id:
            _Eosjs.__init__(self, config_rpc(),
                '''
        (async (block_num_or_id) => {
            result = await rpc.get_block(block_num_or_id)
            console.log(JSON.stringify(result))

        })("%s")
                ''' % (block_id), is_verbose)
        else:
            _Eosjs.__init__(self, config_rpc(),
                '''
        (async (block_num_or_id) => {
            result = await rpc.get_block(block_num_or_id)
            console.log(JSON.stringify(result))

        })(%d)
                ''' % (block_number), is_verbose)                        

        self.block_num = self.json["block_num"]
        self.ref_block_prefix = self.json["ref_block_prefix"]
        self.timestamp = self.json["timestamp"]


class GetAccount(Account, _Eosjs):
    '''Retrieve an account from the blockchain.

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        name: The name of the account.
        json: The json representation of the object.
    '''
    def __init__(self, account, is_info=True, is_verbose=True):
        Account.__init__(self, account_arg(account))
        _Eosjs.__init__(self, config_rpc(),
            '''
        (async (account_name) => {
            result = await rpc.get_account(account_name)
            console.log(JSON.stringify(result))
        })("%s")
            ''' % (self.name), is_verbose)

        self.owner_key = self.json['permissions'][0]['required_auth'] \
            ['keys'][0]['key']
        self.active_key = self.json['permissions'][1]['required_auth'] \
            ['keys'][0]['key']                 


class GetAccounts(_Eosjs):
    '''Retrieve accounts associated with a public key.

    - **parameters**::

        key: A key object or a key string 

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(self, key, is_verbose=True):
        _Eosjs.__init__(self, config_rpc(),
            '''
        (async (public_key) => {
            result = await rpc.history_get_key_accounts(public_key)
            console.log(JSON.stringify(result))

        })("%s")    
            ''' % (key_arg(key, is_owner_key=True, is_private_key=False)),
            is_verbose=is_verbose)


class GetTransaction(_Eosjs):
    '''Retrieve a transaction from the blockchain.

    - **parameters**::

        transaction_id: ID of the transaction to retrieve.
        block_num_hint: A non-zero block number allows shorter transaction IDs 
            (8 hex, 4 bytes). Default is ``0``.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        transaction_id: ID of the transaction retrieved.
        json: The json representation of the object.
    '''
    def __init__(self, transaction_id, block_num_hint=0, is_verbose=True):
        _Eosjs.__init__(self, 
            '''
        (async (is, block_num_hint) => {
            result = await rpc.history_get_transaction(is, block_num_hint)
            console.log(JSON.stringify(result))

        })("%s", %d)
            '''.format(transaction_id, block_num_hint), is_verbose)


class WalletCreate(wm.Create):
    '''Create a new wallet locally.

    - **parameters**::

        name: The name of the new wallet, defaults to ``default``.
        password: The password to the wallet, if the wallet exists. Default is None.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        json: The json representation of the object.
    '''
    def __init__(self, name="default", password="", is_verbose=True):
        wm.Create.__init__(self, name, password, is_verbose)


class WalletStop:
    '''Close all open wallets.
    '''
    def __init__(self, is_verbose=True):
        wm.stop()


class WalletList:
    '''List opened wallets, * marks unlocked.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.
    '''
    def __init__(self, is_verbose=True):
        wm.list()


class WalletImport:
    '''Import a private key into wallet.

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        key: A key object or a private key in WIF format to import.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(self, key, wallet="default", is_verbose=True):
        wm.import_key(wallet, key, is_verbose)


class WalletRemove_key:
    '''Remove key from wallet
    - **parameters**::

        password: The password returned by wallet create.
        key: A key object or a public key in WIF format to remove.
        is_verbose: If ``False`` do not print. Default is ``True``.
    '''
    def __init__(self, key, password, is_verbose=True):
        wm.remove_key(wallet, key, is_verbose)


class WalletKeys:
    '''List of public keys from all unlocked wallets.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.

    - **parameters**::

        json: The json representation of the object.
        is_verbose: If set, print output.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(self, is_verbose=True):
        self.json = wm.keys(None, is_verbose)

    def __str__(self):
        out = "Keys in all opened wallets:\n"
        out = out + str(self.json)
        return out


class WalletPrivateKeys:
    '''List of private keys from all unlocked wallets.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.

    - **parameters**::

        json: The json representation of the object.
        is_verbose: If set, print output.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(self, is_verbose=True):
        self.json = wm.private_keys(None, is_verbose)

    def __str__(self):
        out = "Private keys in all opened wallets:\n"
        out = out + str(self.json)
        return out


class WalletOpen:
    '''Open an existing wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If ``False`` do not print. Default is ``True``.
    '''
    def __init__(self, wallet="default", is_verbose=True):
        wm.open_wallet(wallet, is_verbose)


class WalletLockAll:
    '''Lock all unlocked wallets.
    '''
    def __init__(self, is_verbose=True):
        wm.lock_all(is_verbose)


class WalletLock:
    '''Lock wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If ``False`` do not print. Default is ``True``.
    '''
    def __init__(self, wallet="default", is_verbose=True):
        wm.lock(wallet, is_verbose)


class WalletUnlock():
    '''Unlock wallet.

    - **parameters**::

        wallet: The name of the wallet. May be an object 
            having the  May be an object having the attribute `name`, 
            like `CreateAccount`, or a string.
        password: If the wallet argument is not a wallet object, the password 
            returned by wallet create, else anything, defaults to "".
        is_verbose: If ``False`` do not print. Default is ``True``.
    '''
    def __init__(
            self, wallet="default", password="", is_verbose=True):
        wm.unlock(wallet, password, is_verbose)


class GetCode(_Eosjs):
    '''Retrieve the code and ABI for an account.

    - **parameters**::

        account: The name of an account whose code should be retrieved. 
            May be an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(self, account, is_verbose=True):

        _Eosjs.__init__(self, config_rpc(),
            '''
        async function get_code(account_name) {
            result = await rpc.get_code(account_name)
            console.log(JSON.stringify(result))
        }

        get_code("%s")
            ''' % (account_arg(account)), is_verbose)

        self.code_hash = self.json["code_hash"]
        self.printself()

    def __str__(self):
        return "code hash: {}".format(self.code_hash)


class GetTable(_Eosjs):
    '''Retrieve the contents of a database table

    - **parameters**::

        account: The name of the account that owns the table. May be 
            an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.
        scope: The scope within the account in which the table is found,
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

        json: The json representation of the object.
    '''
    def __init__(
            self, account, table, scope,
            binary=False, 
            limit=10, key="", lower="", upper="",
            is_verbose=True
            ):
        self.name = account_arg(account)

        if not scope:
            scope=self.name
        try:
            scope_name = scope.name
        except:
            scope_name = scope

        _Eosjs.__init__(self, config_rpc(), 
        '''
        async function get_table(
                code, scope, table, json=true, limit=10, table_key="", 
                lower_bound="", upper_bound="") {
            __namedParameters = {
                code: code,
                json: json,
                limit: limit,
                lower_bound: lower_bound,
                scope: scope,
                table: table,
                table_key: table_key,
                upper_bound: upper_bound
            }
            result = await rpc.get_table_rows__namedParameters()
                console.log(result)
        }

        get_block(
            "%(code)s", "%(scope)s", "%(table)s", %s(json)s,
            %(limit)d, "%(key)s", "%(lower)s", "%(upper)s"

        ''' % {
                "code": self.name,
                "scope": scope_name,
                "table": "table",
                "json": "false" if binary else "true",
                "limit": limit,
                "key": key_arg(key, is_owner_key=False, is_private_key=False),
                "lower": lower,
                "upper": upper
            }, is_verbose)


class CreateKey(Key, _Eosjs):
    '''Create a new keypair and print the public and private keys.

    - **parameters**::

        key_name: Key name.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(
            self, key_name=None, key_public=None, key_private=None, 
            r1=False, is_verbose=True):
        Key.__init__(self, key_name, key_public, key_private)

        if self.key_public or self.key_private:
            self.json = {}
            self.json["key_public"] = self.key_public           
            self.json["key_private"] = self.key_private
            self.out_msg = "Private key: {0}\nPublic key: {1}\n" \
                .format(self.key_private, self.key_public)
        else:
            args = ["--to-console"]
            if r1:
                args.append("--r1")

            _Eosjs.__init__(self, "",
                '''
        const ecc = require('eosjs-ecc');

        (async () => {
            private_key = await ecc.randomKey()
            public_key = ecc.privateToPublic(private_key)
            const result = {
                key_private: private_key,
                key_public: public_key
            }
            console.log(JSON.stringify(result))
        })()
                ''',
                is_verbose)
        self.json["name"] = key_name
        self.name = key_name

        self.key_private = self.json["key_private"]
        self.key_public = self.json["key_public"]


class RestoreAccount(GetAccount):

    def __init__(self, account, is_verbose=True):
        GetAccount.__init__(self, account, is_verbose=False, is_info=False)

        self.name = self.json["account_name"]
        self.owner_key = ""
        self.active_key = ""
        
    def info(self):
        print(str(GetAccount(self.name, is_verbose=False)))

    def __str__(self):
        return self.name


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
        json: The json representation of the object.  
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

        if not name: 
            name = account_name()
        Account.__init__(self, name)

        self.owner_key = None # private keys
        self.active_key = None
        
        if not active_key:
            active_key = owner_key        

        owner_key_public = key_arg(
            owner_key, is_owner_key=True, is_private_key=False)
        active_key_public = key_arg(
            active_key, is_owner_key=False, is_private_key=False)

        # args = []
        # if forceUnique:
        #     args.append("--force-unique")
        # if max_cpu_usage:
        #     args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        # if  max_net_usage:
        #     args.extend(["--max-net-usage", str(max_net_usage)])
        # if  ref_block:
        #     args.extend(["--ref-block", ref_block])

        authorization = []
        if permission:
            authorization = permission_arg(permission)
            
        _Eosjs.__init__(self, config_api(),
                '''
        (async () => {
            const result = await api.transact(
                {
                    actions: [
                        {
                            account: 'eosio',
                            name: 'newaccount',
                            authorization: [
                                {
                                    actor: 'eosio',
                                    permission: 'active',
                                }
                            ],
                            data: {
                                creator: '%s',
                                name: '%s',
                                owner: {
                                    threshold: 1,
                                    keys: [
                                        {
                                            key: '%s',
                                            weight: 1
                                        }
                                    ],
                                    accounts: [],
                                    waits: []
                                },
                                    active: {
                                    threshold: 1,
                                    keys: [
                                        {
                                            key: '%s',
                                            weight: 1
                                        }
                                    ],
                                    accounts: [],
                                    waits: []
                                }
                            }
                        }
                    ]
                },
                {
                    blocksBehind: 3,
                    expireSeconds: 30,
                });

        console.log(JSON.stringify(result))
        })()
            ''' % (
                creator, name, owner_key_public, active_key_public
                ), is_verbose)

    def __str__(self):
        return self.name


def account_name():
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name

def contract_is_built(contract_dir, wasm_file=None, abi_file=None):
    contract_path_absolute = config.contract_dir(contract_dir)
    if not contract_path_absolute:
        return []

    if not wasm_file:
        wasm_file = config.wasm_file(contract_dir)
        if not wasm_file:
            return []
    else:
        if not os.path.isfile(
                os.path.join(contract_path_absolute, wasm_file)):
            return []

    if not abi_file:
        abi_file = config.abi_file(contract_dir)
        if not abi_file:
            return []
    else:
        if not os.path.isfile(
                os.path.join(contract_path_absolute, abi_file)):
            return []

    return [contract_path_absolute, wasm_file, abi_file]

class SetContract(_Eosjs):
    '''Create or update the contract on an account.

    - **parameters**:: 

        account: The account to publish a contract for. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string.
        contract_dir: The path containing the .wast and .abi. 
        wasm_file: The file containing the contract WASM relative 
            to contract_dir.
        abi_file: The ABI for the contract relative to contract-dir.

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

        json: The json representation of the object.
    '''
    def __init__(
            self, account, contract_dir, 
            wasm_file=None, abi_file=None, 
            permission=None, expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            is_verbose=True,
            json=False
            ):

        files = contract_is_built(contract_dir, wasm_file, abi_file)
        if not files:
            raise errors.Error("""
            Cannot determine the contract directory. The clue is 
            {}.
            """.format(contract_dir))
            return

        self.contract_path_absolute = files[0]
        wasm_file = os.path.join(files[0], files[1])
        abi_file =  os.path.join(files[0], files[2])

        self.account_name = account_arg(account)

        # if forceUnique:
        #     args.append("--force-unique")
        # if max_cpu_usage:
        #     args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        # if  max_net_usage:
        #     args.extend(["--max-net-usage", str(max_net_usage)])
        # if  ref_block:
        #     args.extend(["--ref-block", ref_block])

        authorization = [self.account_name + "@active"]
        if permission:
            authorization.extend(permission_arg(permissions))

        _Eosjs.__init__(self, config_rpc(),
            '''
    const fs = require("fs");
    const abi = JSON.parse(fs.readFileSync("%s"));

    function api() {
        eos.setabi("%s", abi, options).then(print_result)
    }            ''' % (
                abi_file,               
                self.account_name
                ), is_verbose) 

        _Eosjs.__init__(self, config_rpc(),
            '''
    const fs = require("fs")
    const wasm = fs.readFileSync("%s")

    function api() {
        eos.setcode("%s", 0, 0, wasm).then(print_result)
    }
            ''' % (
                wasm_file,               
                self.account_name
                ), is_verbose)

        self.printself()

    def get_transaction(self):
        return GetTransaction(self.transaction)


class PushAction(_Eosjs):
    '''Push a transaction with a single action

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

        json: The json representation of the object.
    '''
    def __init__(
            self, account, action, data,
            permission=None, expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            is_verbose=True,
            json=False
        ):
        self.account_name = account_arg(account)

        args = [self.account_name, action, data]
        if json:
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
                        
        self.console = None
        self.data = None
        _Eosjs.__init__(self, args, "push", "action", is_verbose)

        self.console = self.json["processed"]["action_traces"][0]["console"]
        self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()

    def get_transaction(self):
        return GetTransaction(self.transaction)
