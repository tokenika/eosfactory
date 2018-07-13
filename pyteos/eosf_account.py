import json
import inspect
import types

import setup
import teos
import cleos
import cleos_system
import eosf
import eosf_wallet

class AccountEosio():

    json = {}
    error = False
    err_msg = ""
    account_info = "The account is not opened yet!"

    def __init__(
            self, is_verbose=1):

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

    
    def info(self):
        return self.account_info


    def __str__(self):
        return self.name


class AccountMaster(AccountEosio, eosf._Eosf):

    def is_local_testnet(self):
        account_ = cleos.GetAccount(self.name, json=True, is_verbose=-1)
        # print(cleos._wallet_url_arg)
        # print(account_)
        if not account_.error and \
            self.key_public == \
                account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"]:
            self.account_info = str(account_)
            self.EOSF("""
                Local testnet is ON: the `eosio` account is master.
                """)
            return True
        else:
            return False

    def __init__(
            self, name="", account_object_name="", 
            is_verbose=1, verbosity=None):

        is_verbose = self.verify_is_verbose(verbosity)
    
        self.EOSF_TRACE("""
            ######### 
            Get master account.
            """)

        self.DEBUG("""
            Local node is running: {}
            """.format(cleos.node_is_running()))

        AccountEosio.__init__(self, is_verbose)

        self.DEBUG("""
            Name is `{}`
            Wallet URL is {}
            Use keosd status is {}
            self._out:
            {}

            self.err_msg:
            {}

            """.format(
                self.name,
                cleos.wallet_url(), setup.is_use_keosd(),
                self._out,
                self.err_msg
                ))

        if cleos.is_notrunningnotkeosd_error(self):
            self.ERROR(self.err_msg)
            return

        if self.is_local_testnet():
            return

        self.account_info = "The account is not opened yet!"
        self.DEBUG("It is not the local testnet.")
        #cleos.set_wallet_url_arg(node, "")

        # not local testnet:
        if not account_object_name: # print data for registration
            if not name: 
                self.name = cleos.account_name()
            else:
                self.name = name

            self.owner_key = cleos.CreateKey("owner", is_verbose=0)
            self.active_key = cleos.CreateKey("active", is_verbose=0)
            self.OUT("""
                Use the following data to register a new account on a public testnet:
                Accout Name: {}
                Owner Public Key: {}
                Owner Private Key: {}
                Active Public Key: {}
                Active Private Key: {}
                """.format(
                    self.name,
                    self.owner_key.key_public, self.owner_key.key_private,
                    self.active_key.key_public, self.active_key.key_private
                    ))
        else: # restore the master account

            account_ = cleos.GetAccount(name, json=True, is_verbose=-1)
            if not account_.error:
                self.account_info = str(account_)
                self.name = name
                self.key_public = \
                account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"]

                self.owner_key = cleos.CreateKey(
                    "active", 
                    account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"], 
                    is_verbose=0)

                self.owner_key = cleos.CreateKey(
                    "owner", 
                    account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"], 
                    is_verbose=0)

                account_map_json = eosf.account_map()
                for acc_n in account_map_json:
                    if account_map[acc_n] == account_object_name:
                        account_map[acc_n] = account_object_name + "_" + acc_n
                    
                account_map_json[self.name] = account_object_name
                context_globals = inspect.stack()[1][0].f_globals
                context_globals[account_object_name] = self


    def info(self):
        return self.account_info


    def __str__(self):
        return self.name


def is_local_testnet():
        account_ = cleos.GetAccount(self.name, json=True, is_verbose=-1)
        # print(cleos._wallet_url_arg)
        # print(account_)
        if not account_.error and \
            self.key_public == \
                account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"]:
            self.account_info = str(account_)
            self.EOSF("""
                Local testnet is ON: the `eosio` account is master.
                """)
            return True
        else:
            return False


def account_master_factory(
            name="", account_object_name="", verbosity=None):
    pass


def account_factory(
        account_object_name,
        creator="", 
        stake_net="", stake_cpu="",
        account_name="", 
        owner_key="", active_key="",
        permission = "",
        buy_ram_kbytes=0, buy_ram="",
        transfer=False,
        expiration_sec=30,
        skip_signature=0, dont_broadcast=0, forceUnique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block="",
        restore=False,
        verbosity=None):

    account_object = self = eosf._Eosf()
    is_verbose = self.verify_is_verbose(verbosity)

    objects = None    
    context_locals = inspect.stack()[1][0].f_locals
    context_globals = inspect.stack()[1][0].f_globals
    objects = {**context_globals, **context_locals}

    wallet = None
    wallets = []
    for name in objects:
        if isinstance(objects[name], eosf_wallet.Wallet):
            wallets.append(name)
            wallet = objects[name]

    error = False

    if len(wallets) == 0:
        account_object.ERROR("""
            Cannot find any `Wallet` object.
            Add the definition of an `Wallet` object, for example:
            `wallet = eosf.Wallet()`
            """)
    if len(wallets) > 1:
        account_object.ERROR("""
            Too many `Wallet` objects.
            Can be precisely one wallet object in the scope, but there is many: 
            {}
            """.format(wallets))

    if not wallet.is_name_taken(account_object_name):
        context_globals[account_object_name] = account_object
        account_object.error = True
        return

    if restore:
        if creator:
            account_name = creator

        account_object.EOSF_TRACE("""
                    ######### 
                    Create the account object named `{}`, for the blockchain account `{}`.
                    """.format(account_object_name, account_name))        
        account_object = cleos.RestoreAccount(account_name, is_verbose)
    else:
        if not account_name:
            account_name = cleos.account_name()
        if owner_key:
            if not active_key:
                active_key = owner_key
        else:
            owner_key = cleos.CreateKey("owner", is_verbose=-1)
            active_key = cleos.CreateKey("active", is_verbose=-1)

        if not creator:
            creator = AccountMaster()

        if stake_net:
            account_object.EOSF_TRACE("""
                        ######### 
                        Create the account object named `{}`, for the new, properly paid, 
                        blockchain account `{}`.
                        """.format(account_object_name, account_name))

            account_object = cleos_system.SystemNewaccount(
                    creator, account_name, owner_key, active_key,
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
            account_object.EOSF_TRACE("""
                        ######### 
                        Create the account object named `{}' for the new local testnet account `{}`.
                        """.format(account_object_name, account_name))            
            account_object = cleos.CreateAccount(
                    creator, account_name, 
                    owner_key, active_key,
                    permission,
                    expiration_sec, skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    is_verbose=is_verbose
                    )

        if account_object.error:
            account_object.ERROR(account_object.err_msg)
        else:
            account_object.EOSF("""The account object created.""")

        account_object.owner_key = owner_key
        account_object.active_key = active_key

    # append account methodes to the account_object:

    def code(account_object, code="", abi="", wasm=False):
        return cleos.GetCode(
            account_object, code, abi, 
            is_verbose=account_object.is_verbose)

    account_object.code = types.MethodType(code, account_object)

    def set_contract(
            account_object, contract_dir, 
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
            account_object, action, data,
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
            account_object, table_name, scope="", 
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

    def __str__(account_object):
        return account_object.name

    account_object.__str__ = types.MethodType(
                                        __str__, account_object)

    # export the account object to the globals in the calling module:
    context_globals[account_object_name] = account_object

    # put the account object to the wallet:
    wallet.open()
    wallet.unlock()
    wallet.import_key(account_object)

    if not account_object.error and not wallet.error:
        wallet.map_account(account_object_name, account_object)

    return account_object

