# Latest commit b6e5b55  on Dec 14, 2018

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
import eosfactory.core.eosjs.walletmanager as wm
import eosfactory.core.interface as interface


def config_rpc():
    code = utils.heredoc('''
const { Api, JsonRpc, RpcError } = require('eosjs');
const fetch = require('node-fetch');
const rpc = new JsonRpc('%(endpoint)s', { fetch });
    ''')
    setup.set_local_nodeos_address_if_none()
    return code


def config_api():
    code = utils.heredoc('''
const { Api, JsonRpc, RpcError } = require('eosjs');
const { JsSignatureProvider } = require('eosjs/dist/eosjs-jssig');
const fetch = require('node-fetch');
const rpc = new JsonRpc('%(endpoint)s', { fetch });
const { TextEncoder, TextDecoder } = require('util');
const signatureProvider = new JsSignatureProvider(%(keys)s);
const api = new Api({ 
    rpc, signatureProvider, 
    textDecoder: new TextDecoder, textEncoder: new TextEncoder });
    ''')

    return code % {
        "keys": json.dumps(wm.private_keys(is_verbose=False), indent=4),
        "endpoint": "%(endpoint)s"
        }


def permission_str(permission, account, default=None):
    permissions = []
    if permission is None and default is None:
        permissions.append(
                            {"actor": account, 
                            "permission": interface.Permission.ACTIVE})
    else:
        p = interface.permission_arg(permission)
        for perm in p:
            perm = perm.split("@")
            if len(perm) == 1:
                perm.append(interface.Permission.ACTIVE)
                permissions.append(
                                {"actor": perm[0], "permission": perm[1]})
    if not default is None:
        permissions.append(default)

    return str(permissions)


class Command():
    '''A prototype for ``eosjs`` command classes.
    '''
    def __init__(self, header, js, is_verbose=1):
        self.out_msg = None
        self.err_msg = None
        self.json = None
        self.is_verbose = is_verbose

        setup.set_local_nodeos_address_if_none()
        header = header % {'endpoint': utils.relay(
                            "http://" + config.RELY_URL, setup.nodeos_address(), 
                            setup.is_print_request, setup.is_print_response)
        }
        cl = ["node", "-e"]
        js = header + "\n" + utils.heredoc(js)

        cl.append(js)

        if setup.is_save_command_lines:
            setup.add_to__command_line_file("\n" + js + "\n") 
        if setup.is_print_command_lines:
            print("\n" + js + "\n")

        while True:
            process = subprocess.run(
                                        cl,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE) 
            self.out_msg = process.stdout.decode("ISO-8859-1")
            self.out_msg_details = process.stderr.decode("ISO-8859-1")
            self.err_msg = None
            error_key_words = \
                            ["ERROR", "Error", "error", "Failed", "FetchError"]
            for word in error_key_words:
                if word in self.out_msg_details:
                    self.err_msg = self.out_msg_details
                    error_msg = self.err_msg.split("\n")[0]
                    pattern = re.compile(r".+FetchError:")
                    if re.findall(pattern, error_msg):
                        self.err_msg = error_msg.replace(
                                        re.findall(pattern, error_msg)[0], "")
                    
                    self.out_msg_details = None
                    break

            if not self.err_msg:
                break
            if self.err_msg and not "Transaction took too long" in self.err_msg:
                break

        errors.validate(self)

        try:
            self.json = json.loads(self.out_msg)
        except:
            pass

        try:
            self.json = json.loads(self.out_msg_details)
        except:
            pass
                  
    def printself(self):
        if self.is_verbose:
            logger.OUT(self.__str__())

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)

    def __repr__(self):
        return ""


class GetAccount(interface.Account, Command):
    '''Retrieve an account from the blockchain.

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        name: The name of the account.
        json: The json representation of the object.
    '''
    def __init__(self, account, is_info=True, is_verbose=True):
        interface.Account.__init__(self, interface.account_arg(account))
        Command.__init__(self, config_rpc(),
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


class GetTransaction(Command):
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
        Command.__init__(self, 
            '''
        (async (is, block_num_hint) => {
            result = await rpc.history_get_transaction(is, block_num_hint)
            console.log(JSON.stringify(result))

        })("%s", %d)
            '''.format(transaction_id, block_num_hint), is_verbose)


class WalletCreate(wm.Wallet):
    '''Create a new wallet locally.

    If the *password* argument is set, try to open a wallet. Otherwise, create
    a new wallet.

    Args:
        name (str): The name of the wallet. If not set, defaults to the value `.setup.wallet_default_name`
        password (str): The password to the wallet, if the wallet exists. 
        is_verbose (bool): If *False* do not print. Default is *True*.

    Attributes:
        name (str): The name of the wallet.
        password (str): The password returned by the *wallet create* 
            EOSIO cleos command.
        is_created (bool): True, if the wallet created.
    '''
    def __init__(self, name=None, password="", is_verbose=True):
        wm.Wallet.__init__(self, name, password, is_verbose)


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


class GetCode(Command):
    '''Retrieve the code and ABI for an account.

    - **parameters**::

        account: The name of an account whose code should be retrieved. 
            May be an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(self, account, is_verbose=True):

        Command.__init__(self, config_rpc(),
            '''
        async function get_code(account_name) {
            result = await rpc.get_code(account_name)
            console.log(JSON.stringify(result))
        }

        get_code("%s")
            ''' % (interface.account_arg(account)), is_verbose)

        self.code_hash = self.json["code_hash"]
        self.printself()

    def __str__(self):
        return "code hash: {}".format(self.code_hash)


class GetTable(Command):
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
        self.name = interface.account_arg(account)

        if not scope:
            scope=self.name
        try:
            scope_name = scope.name
        except:
            scope_name = scope

        Command.__init__(self, config_rpc(), 
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
                "key": interface.key_arg(key, is_owner_key=False, is_private_key=False),
                "lower": lower,
                "upper": upper
            }, is_verbose)


class CreateKey(interface.Key, Command):
    '''Create a new keypair and print the public and private keys.

    - **parameters**::

        key_name: Key name.

    - **attributes**::

        json: The json representation of the object.
    '''
    def __init__(
            self, key_public=None, key_private=None, 
            r1=False, is_verbose=True):
        interface.Key.__init__(self, key_public, key_private)

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

            Command.__init__(self, "",
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


class CreateAccount(interface.Account, Command):
    '''Create an account, buy ram, stake for bandwidth for the account.

    Args:
        creator (str or .interface.Account): The account creating 
            the new account.
        name: (str) The name of the new account.
        owner_key (str): If set, the owner public key for the new account, 
            otherwise random.
        active_key (str): If set, the active public key for the new account, 
            otherwise random.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.
    '''
    def __init__(
            self, creator, name, owner_key, 
            active_key=None,
            permission=None,
            expiration_sec=None, 
            skip_sign=0, 
            dont_broadcast=0,
            force_unique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True
            ):

        if not name: 
            name = account_name()
        interface.Account.__init__(self, name)

        self.owner_key = None # private keys
        self.active_key = None
        
        if not active_key:
            active_key = owner_key        

        owner_key_public = interface.key_arg(
            owner_key, is_owner_key=True, is_private_key=False)
        active_key_public = interface.key_arg(
            active_key, is_owner_key=False, is_private_key=False)

        # args = []
        # if force_unique:
        #     args.append("--force-unique")
        # if max_cpu_usage:
        #     args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        # if  max_net_usage:
        #     args.extend(["--max-net-usage", str(max_net_usage)])
        # if  ref_block:
        #     args.extend(["--ref-block", ref_block])

        Command.__init__(self, config_api(),
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
                                creator: '%(creator)s',
                                name: '%(name)s',
                                owner: {
                                    threshold: 1,
                                    keys: [
                                        {
                                            key: '%(owner_key_public)s',
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
                                            key: '%(active_key_public)s',
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
                }
            );

            console.log(JSON.stringify(result))
        })();
            ''' % {
                "creator": creator, 
                "name": name, 
                "owner_key_public": owner_key_public, 
                "active_key_public": active_key_public,
            }, is_verbose)

    def __str__(self):
        return self.name


def account_name():
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name


class PushAction(Command):
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
        force_unique: Force the transaction to be unique. this will consume extra 
            bandwidth and remove any protections against accidentally issuing the 
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
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            is_verbose=True,
            json=False
        ):
        self.account_name = interface.account_arg(account)

        args = [self.account_name, action, data]
        if json:
            args.append("--json")
        if not permission is None:
            p = permission_arg(permission)
            for perm in p:
                args.extend(["--permission", perm])

        args.extend(["--expiration", str(expiration_sec)])
        if skip_sign:
            args.append("--skip-sign")
        if dont_broadcast:
            args.append("--dont-broadcast")
        if force_unique:
            args.append("--force-unique")
        if max_cpu_usage:
            args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        if  max_net_usage:
            args.extend(["--max-net-usage", str(max_net_usage)])
        if  not ref_block is None:
            args.extend(["--ref-block", ref_block])
                        
        self.console = None
        self.data = None
        Command.__init__(self, args, "push", "action", is_verbose)

        self.console = self.json["processed"]["action_traces"][0]["console"]
        self.data = self.json["processed"]["action_traces"][0]["act"]["data"]

        self.printself()

    def get_transaction(self):
        return GetTransaction(self.transaction)