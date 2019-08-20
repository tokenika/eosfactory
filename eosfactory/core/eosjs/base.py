# Latest commit b6e5b55  on Dec 14, 2018

import subprocess
import json as json_module
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
import eosfactory.core.common as common
import eosfactory.core.to_string.get_account as get_account_str


def config_rpc():
    code = utils.heredoc("""
const { Api, JsonRpc, RpcError } = require('eosjs');
const fetch = require('node-fetch');
const rpc = new JsonRpc('%(endpoint)s', { fetch });
    """)
    setup.set_local_nodeos_address_if_none()
    return code

SIG_PROVIDER = \
    "const signatureProvider = new JsSignatureProvider([/*private keys*/]);"


def config_api():
    code = utils.heredoc("""
const { Api, JsonRpc, RpcError } = require('eosjs');
const { JsSignatureProvider } = require('eosjs/dist/eosjs-jssig');
const fetch = require('node-fetch');
const rpc = new JsonRpc('%(endpoint)s', { fetch });
const { TextEncoder, TextDecoder } = require('util');
%(signatureProvider)s
const api = new Api({ 
    rpc, 
    signatureProvider, 
    textDecoder: new TextDecoder, 
    textEncoder: new TextEncoder 
});
    """)

    return code % {
        "signatureProvider": SIG_PROVIDER,
        "endpoint": "%(endpoint)s"
        }


def permission_str(permission, account, default=None):
    permission_json = []
    if not permission and not default:
        permission_json.append(
                            {"actor": account, 
                            "permission": interface.Permission.ACTIVE.value})
    else:
        if not isinstance(permission, list):
            permission = interface.permission_arg(permission)

        for perm in permission:
            perm = perm.split("@")
            if len(perm) == 1:
                perm.append(interface.Permission.ACTIVE.value)
            permission_json.append({"actor": perm[0], "permission": perm[1]})
    if default:
        permission_json.append(default)

    return json_module.dumps(permission_json)


class Command():
    """A prototype for ``eosjs`` command classes.
    """
    def __init__(self, header, js, is_verbose=True):
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

        if setup.is_show_private_keys:
            js = js.replace(
                SIG_PROVIDER, 
                "const signatureProvider = new JsSignatureProvider(\n{}\n);".format(
                    json_module.dumps(wm.private_keys(is_verbose=False), indent=4))) 

        if setup.is_save_command_lines:
            setup.add_to__command_line_file("\n" + js + "\n") 
        if setup.is_print_command_lines:
            print("\n" + js + "\n")

        js = js.replace(
            SIG_PROVIDER, 
            "const signatureProvider = new JsSignatureProvider(\n{}\n);".format(
                json_module.dumps(wm.private_keys(is_verbose=False), indent=4)))        

        cl.append(js)

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
            self.json = json_module.loads(self.out_msg)
        except:
            pass

        try:
            self.json = json_module.loads(self.out_msg_details)
        except:
            pass
                  
    def printself(self, is_verbose=False):
        """Print a message.

        Args:
            is_verbose (bool): If set, a message is printed.
        """
        if not hasattr(self, "is_verbose"):
            self.is_verbose = is_verbose

        if self.is_verbose:
            logger.OUT(self.__str__())

    def __str__(self):
        return json_module.dumps(self.json, sort_keys=True, indent=4)

    def __repr__(self):
        return ""


class GetAccount(interface.Account, Command):
    """Retrieve an account from the blockchain.

    Args:
        account (str or .interface.Account): The account to retrieve.
        json: If set, prints the json representation of the object.
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        name (str): The EOSIO name of the account.
        owner_key (str) The ``owner`` public key.
        active_key (str) The ``active`` public key.
        json: The json representation of the object.
        json: The json representation of the object.
    """
    def __init__(self, account, json=True, is_verbose=True):
        interface.Account.__init__(self, interface.account_arg(account))
        Command.__init__(self, config_rpc(),
            """
        (async (account_name) => {
            result = await rpc.get_account(account_name)
            console.log(JSON.stringify(result))
        })("%s")
            """ % (self.name), is_verbose)

        self.owner_key = self.json['permissions'][0]['required_auth'] \
            ['keys'][0]['key']
        self.active_key = self.json['permissions'][1]['required_auth'] \
            ['keys'][0]['key']

        self.printself()

    def __str__(self):
        return str(get_account_str.GetAccount(self.json))


class GetTransaction(Command):
    """Retrieve a transaction from the blockchain.

    - **parameters**::

        transaction_id: ID of the transaction to retrieve.
        block_num_hint: A non-zero block number allows shorter transaction IDs 
            (8 hex, 4 bytes). Default is ``0``.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        transaction_id: ID of the transaction retrieved.
        json: The json representation of the object.
    """
    def __init__(self, transaction_id, block_num_hint=0, is_verbose=True):
        Command.__init__(self, 
            """
        (async (is, block_num_hint) => {
            result = await rpc.history_get_transaction(is, block_num_hint)
            console.log(JSON.stringify(result))

        })("%s", %d)
            """.format(transaction_id, block_num_hint), is_verbose)


class WalletCreate(wm.Wallet):
    """Create a new wallet locally.

    If the ``password`` argument is set, try to open a wallet. Otherwise, create
    a new wallet.

    Args:
        name (str): The name of the wallet. If not set, defaults to the value `.setup.wallet_default_name`
        password (str): The password to the wallet, if the wallet exists. 
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        name (str): The name of the wallet.
        password (str): The password returned by the ``wallet create`` 
            EOSIO cleos command.
        is_created (bool): True, if the wallet created.
    """
    def __init__(self, name=None, password="", is_verbose=True):
        wm.Wallet.__init__(self, name, password, is_verbose)


class WalletStop:
    """Close all open wallets.
    """
    def __init__(self, is_verbose=True):
        wm.stop()


class WalletList:
    """List opened wallets, * marks unlocked.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, is_verbose=True):
        wm.list()


class WalletImport:
    """Import a private key into wallet.

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        key: A key object or a private key in WIF format to import.
        is_verbose: If ``False`` do not print. Default is ``True``.

    - **attributes**::

        json: The json representation of the object.
    """
    def __init__(self, key, wallet="default", is_verbose=True):
        wm.import_key(wallet, key, is_verbose)


class WalletRemove_key:
    """Remove key from wallet
    - **parameters**::

        password: The password returned by wallet create.
        key: A key object or a public key in WIF format to remove.
        is_verbose: If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, key, password, is_verbose=True):
        wm.remove_key(wallet, key, is_verbose)


class WalletKeys:
    """List of public keys from all unlocked wallets.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.

    - **parameters**::

        json: The json representation of the object.
        is_verbose: If set, print output.

    - **attributes**::

        json: The json representation of the object.
    """
    def __init__(self, is_verbose=True):
        self.json = wm.keys(None, is_verbose)

    def __str__(self):
        out = "Keys in all opened wallets:\n"
        out = out + str(self.json)
        return out


class WalletPrivateKeys:
    """List of private keys from all unlocked wallets.

    - **parameters**::

        is_verbose: If ``False`` do not print. Default is ``True``.

    - **parameters**::

        json: The json representation of the object.
        is_verbose: If set, print output.

    - **attributes**::

        json: The json representation of the object.
    """
    def __init__(self, is_verbose=True):
        self.json = wm.private_keys(None, is_verbose)

    def __str__(self):
        out = "Private keys in all opened wallets:\n"
        out = out + str(self.json)
        return out


class WalletOpen:
    """Open an existing wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, wallet="default", is_verbose=True):
        wm.open_wallet(wallet, is_verbose)


class WalletLockAll:
    """Lock all unlocked wallets.
    """
    def __init__(self, is_verbose=True):
        wm.lock_all(is_verbose)


class WalletLock:
    """Lock wallet.

    - **parameters**::

        wallet: The name of the wallet to import key into. May be an object 
            having the  May be an object having the attribute `name`, like 
            `CreateAccount`, or a string. 
        is_verbose: If ``False`` do not print. Default is ``True``.
    """
    def __init__(self, wallet="default", is_verbose=True):
        wm.lock(wallet, is_verbose)


class WalletUnlock():
    """Unlock wallet.

    - **parameters**::

        wallet: The name of the wallet. May be an object 
            having the  May be an object having the attribute `name`, 
            like `CreateAccount`, or a string.
        password: If the wallet argument is not a wallet object, the password 
            returned by wallet create, else anything, defaults to "".
        is_verbose: If ``False`` do not print. Default is ``True``.
    """
    def __init__(
            self, wallet="default", password="", is_verbose=True):
        wm.unlock(wallet, password, is_verbose)


class GetCode(Command):
    """Retrieve the code and ABI for an account.

    - **parameters**::

        account: The name of an account whose code should be retrieved. 
            May be an object having the  May be an object having the attribute 
            `name`, like `CreateAccount`, or a string.

    - **attributes**::

        json: The json representation of the object.
    """
    def __init__(self, account, is_verbose=True):

        Command.__init__(self, config_rpc(),
            """
        async function get_code(account_name) {
            result = await rpc.get_code(account_name)
            console.log(JSON.stringify(result))
        }

        get_code("%s")
            """ % (interface.account_arg(account)), is_verbose)

        self.code_hash = self.json["code_hash"]
        self.printself()

    def __str__(self):
        return "code hash: {}".format(self.code_hash)


class GetTable(Command):
    """Retrieve the contents of a database table

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
    """
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
        """
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

        """ % {
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
    """Create a new keypair and print the public and private keys.

    Args:
        key_private (str): If set, a private key to set, otherwise random.
        key_public (str): If set, a public key to set, otherwise random.
        r1: Generate a key using the R1 curve (iPhone), instead of the 
            K1 curve (Bitcoin)
        is_verbose (bool): If ``False`` do not print. Default is ``True``.

    Attributes:
        key_private (str): The private key set.
        key_public (str): The public key set.
    """
    def __init__(
                    self, key_public=None, key_private=None, r1=False, 
                    is_verbose=True):
        interface.Key.__init__(self, key_public, key_private)

        if self.key_public or self.key_private:
            self.json = {}
            self.json["key_public"] = self.key_public           
            self.json["key_private"] = self.key_private
            self.out_msg = "Private key: {0}\nPublic key: {1}\n" \
                .format(self.key_private, self.key_public)
        else:
            if r1:
                raise errors.Error(
                            "``eosjs`` does not support using the R1 curve?")

            Command.__init__(self, "",
                """
        const ecc = require('eosjs-ecc')

        ;(async () => {
            private_key = await ecc.randomKey()
            public_key = ecc.privateToPublic(private_key)
            const result = {
                key_private: private_key,
                key_public: public_key
            }
            console.log(JSON.stringify(result))
        })()
                """,
                is_verbose)
        self.key_private = self.json["key_private"]
        self.key_public = self.json["key_public"]

        self.printself(is_verbose)


class RestoreAccount(GetAccount):

    def __init__(self, account, is_verbose=True):
        GetAccount.__init__(self, account, is_verbose=False, json=True)

        self.name = self.json["account_name"]
        self.owner_key = ""
        self.active_key = ""
        
    def info(self):
        print(str(GetAccount(self.name, is_verbose=False)))

    def __str__(self):
        return self.name


class CreateAccount(interface.Account, Command):
    """Create an account, buy ram, stake for bandwidth for the account.

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
    """
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
        interface.Account.__init__(self, name, owner_key, active_key)

        if not expiration_sec:
            expiration_sec = 30

        # if not permission is None:
        #     p = interface.permission_arg(permission)
        #     for perm in p:
        #         args.extend(["--permission", perm])             
        # if force_unique:
        #     args.append("--force-unique")
        # if max_cpu_usage:
        #     args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        # if  max_net_usage:
        #     args.extend(["--max-net-usage", str(max_net_usage)])
        # if  ref_block:
        #     args.extend(["--ref-block", ref_block])

        Command.__init__(
                            self, config_api(),
                            """
        ;(async () => {
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
                    blocksBehind: %(blocksBehind)d,
                    expireSeconds: %(expiration_sec)d,
                    broadcast: %(broadcast)s,
                    sign: %(sign)s, 
                }
            );
            console.log(JSON.stringify(result))
        })();
            """ % {
                "creator": creator, 
                "name": name, 
                "owner_key_public": interface.key_arg(
                            owner_key, is_owner_key=True, is_private_key=False),
                "active_key_public": interface.key_arg(
                        active_key, is_owner_key=False, is_private_key=False),
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2,
            }, is_verbose)

        self.printself(is_verbose)
        
    def __repr__(self):
        return self.name

    def __str__(self):
        import eosfactory.core.to_string.actions
        str(eosfactory.core.to_string.actions.Actions(self.json))


def account_name():
    letters = "abcdefghijklmnopqrstuvwxyz12345"
    name = ""
    for i in range(0, 12):
        name += letters[random.randint(0, 30)]

    return name


class PushAction(Command):
    """Push a transaction with a single action

    Args:
        account (str or .interface.Account): The account to publish a contract 
            for.
        action (str or json or filename): Definition of the action to execute on 
            the contract.
        data (str): The arguments to the contract.

    See definitions of the remaining parameters: \
    :func:`.cleos.base.common_parameters`.

    Attributes:
        account_name (str): The EOSIO name of the contract's account.
        console (str): Sum of all *["processed"]["action_traces"][]["console"]* \
            components of EOSIO cleos responce.
        act (str): Summary of all actions, like \
            *eosio.null::nonce <= 5d0a572c49880500*.
    """
    def __init__(
            self, account, action, data,
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0,
            is_verbose=True,
            json=True
        ):
        self.account_name = interface.account_arg(account)
        if not permission is None:
            permission = interface.permission_arg(permission)
        if not expiration_sec:
            expiration_sec = 30

        # if force_unique:
        #     args.append("--force-unique")
        # if max_cpu_usage:
        #     args.extend(["--max-cpu-usage-ms", str(max_cpu_usage)])
        # if  max_net_usage:
        #     args.extend(["--max-net-usage", str(max_net_usage)])
        # if  not ref_block is None:
        #     args.extend(["--ref-block", ref_block])

        Command.__init__(
            self,
            config_api(),
            """
    ;(async () => {
        const permissions = JSON.parse('%(permissions)s')
        const data = JSON.parse('%(data)s')

        const result = await api.transact({
            actions: [
                {
                    account: '%(account_name)s',
                    name: '%(action)s',
                    authorization: permissions,
                    data: data,
                }
            ]
        }, 
        {
            blocksBehind: %(blocksBehind)d,
            expireSeconds: %(expiration_sec)d,
            broadcast: %(broadcast)s,
            sign: %(sign)s,
        });
        console.log(JSON.stringify(result))
    })()
            """ % {
                "account_name": self.account_name,
                "action": action,
                "data": data,
                "permissions": permission_str(permission, self.account_name),
                "expiration_sec": expiration_sec,
                "broadcast": "false" if dont_broadcast else "true",
                "sign": "false" if skip_sign else "true",
                "blocksBehind": delay_sec * 2,
            }, is_verbose)

        self.console = ""
        self.act = ""
        if not dont_broadcast:
            
            for act in self.json["processed"]["action_traces"]:
                self.console += common.gather_console_output(act)

            for trace in self.json["processed"]["action_traces"]:
                if trace["act"]["data"]:
                    if self.act:
                        self.act += "\n"
                    self.act += "{} <= {}::{} {}".format( 
                                                        trace["act"]["account"], 
                                                        trace["act"]["account"],
                                                        trace["act"]["name"],
                                                        trace["act"]["data"])

        self.printself()

    def get_transaction(self):
        return GetTransaction(self.transaction)

    def __str__(self):
            import eosfactory.core.to_string.push
            return str(eosfactory.core.to_string.push.Push(self.json))