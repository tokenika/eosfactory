import json
import inspect
import types

import setup
import teos
import cleos
import cleos_system
import eosf
import eosf_wallet


def is_local_testnet_running():
        account_ = cleos.GetAccount(self.name, json=True, is_verbose=-1)
        # print(cleos._wallet_address_arg)
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


def precisely_one_wallet(logger, levels_below=2):
    objects = None    
    context_locals = inspect.stack()[levels_below][0].f_locals
    context_globals = inspect.stack()[levels_below][0].f_globals
    objects = {**context_globals, **context_locals}

    wallet = None
    wallets = []
    for name in objects:
        if isinstance(objects[name], eosf_wallet.Wallet):
            wallets.append(name)
            wallet = objects[name]

    if len(wallets) == 0:
        logger.ERROR("""
            Cannot find any `Wallet` object.
            Add the definition of an `Wallet` object, for example:
            `wallet = eosf.Wallet()`
            """)
        return None

    if len(wallets) > 1:
        logger.ERROR("""
            Too many `Wallet` objects.
            It can be precisely one wallet object in the scope, but there is many: 
            {}
            """.format(wallets))
        return None

    return wallet
    

def is_local_testnet_running(account_eosio):
    account_ = cleos.GetAccount(account_eosio.name, json=True, is_verbose=-1)
    if not account_.error and \
        account_eosio.owner_key.key_public == \
            account_.json["permissions"][0]["required_auth"]["keys"] \
                [0]["key"]:
        return True
    else:
        return False


def put_account_to_wallet(
        account_object, wallet, account_object_name, levels_below):
    # export the account object to the globals in the calling module:
    inspect.stack()[levels_below][0].f_globals[account_object_name] \
        = account_object

    # put the account object to the wallet:
    wallet.open()
    wallet.unlock()
    wallet.import_key(account_object)
    wallet.map_account(account_object_name, account_object)        


def account_master_factory(
            account_object_name="", name="", verbosity=None, levels_below=1):
    """
    If `account_object_name` is not defined, prints data for 
    registration on a testnet. Then, if the name is not set, the registration 
    name is random.

    Otherwise the following conditions are checked:
    * precisely one `Wallet` object is defined;
    * setup.use_keosd(True) or the local testnet is running.

    If the local testnet is running then an account object, representing 
    the `eosio` account, is created in the global namespace of the calling
    module.

    If the local testnet is stopped then an outer testnet has to be defined
    with `setup.set_nodeos_address(<url>)`, and must be 
    `setup.use_keosd(True)`.

    
    """

    logger = eosf._Eosf(verbosity)

    if not account_object_name: # print data for registration
        if not name: 
            name = cleos.account_name()
        else:
            name = name

        owner_key = cleos.CreateKey("owner", is_verbose=0)
        active_key = cleos.CreateKey("active", is_verbose=0)
        logger.OUT("""
            Use the following data to register a new account on a public testnet:
            Accout Name: {}
            Owner Public Key: {}
            Owner Private Key: {}
            Active Public Key: {}
            Active Private Key: {}
            """.format(
                name,
                owner_key.key_public, owner_key.key_private,
                active_key.key_public, active_key.key_private
                ))

        return logger

    if account_object_name: # 
        logger.EOSF_TRACE("""
            ######### 
            Create the master account object named `{}`...
            """.format(account_object_name))
    else:
        logger.EOSF_TRACE("""
            ######### 
            Create a master account object ...
            """.format(account_object_name))
    
    if cleos.is_notrunningnotkeosd_error(logger):
        logger.ERROR()
        return logger
    
    wallet = precisely_one_wallet(logger, levels_below=levels_below+1)
    if wallet is None:
        return logger
   
    account_object = types.SimpleNamespace()
    account_object.name = "eosio"
    config = teos.GetConfig(is_verbose=0)
    account_object.owner_key = cleos.CreateKey(
        "owner",
        config.json["EOSIO_KEY_PUBLIC"],
        config.json["EOSIO_KEY_PRIVATE"]
        )

    if is_local_testnet_running(account_object):
        put_account_to_wallet(
            account_object, wallet, account_object_name, levels_below+1)
        return

    # not local testnet
    if setup.is_local_address():
        logger.ERROR("""
        Node address is not set.
        Use 'setup.set_nodeos_address(<URL>)'
        """)
        return logger

    account_object = cleos.GetAccount(name, json=True, is_verbose=-1) 
    if not account_object.error:
        account_object.name = name
        account_object.account_info = str(account_object)
        account_object.owner_key = cleos.CreateKey(
            "active", 
            account_object.json["permissions"][0]["required_auth"]["keys"] \
            [0]["key"], 
            is_verbose=0)

        account_object.owner_key = cleos.CreateKey(
            "owner", 
            account_object.json["permissions"][1]["required_auth"]["keys"] \
            [0]["key"], 
            is_verbose=0)

        put_account_to_wallet(
            account_object, wallet, account_object_name, levels_below+1)
        return
    else:
        logger.ERROR(account_object.err_msg)
        return logger


def account_factory(
        account_object_name,
        creator, 
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
        verbosity=None,
        levels_below=1):

    logger = eosf._Eosf(verbosity)
    
    logger.EOSF_TRACE("""
        ######### 
        Create the account object named `{}` ...
        """.format(account_object_name))

    wallet = precisely_one_wallet(logger, levels_below=levels_below+1)
    if wallet is None:
        return logger
        
    account_object = None
    if not wallet.is_name_taken(account_object_name):
        inspect.stack()[levels_below][0].f_globals[account_object_name] = account_object
        return wallet.logger

    if restore:
        if creator:
            account_name = creator

        logger.EOSF_TRACE("""
                    ... for the blockchain account `{}`.
                    """.format(account_object_name, account_name))      
    
        account_object = cleos.RestoreAccount(account_name, is_verbose=-1)
    else:
        if not account_name:
            account_name = cleos.account_name()
        if owner_key:
            if not active_key:
                active_key = owner_key
        else:
            owner_key = cleos.CreateKey("owner", is_verbose=-1)
            active_key = cleos.CreateKey("active", is_verbose=-1)

        if stake_net:
            logger.EOSF_TRACE("""
                        ... for the new, properly paid, 
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
                    is_verbose=-1
                    )
        else:
            logger.EOSF_TRACE("""
                        ... for the new local testnet account `{}`.
                        """.format(account_object_name, account_name))

            account_object = cleos.CreateAccount(
                    creator, account_name, 
                    owner_key, active_key,
                    permission,
                    expiration_sec, skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    is_verbose=-1
                    )

        if account_object.error:
            logger.ERROR(account_object.err_msg)
        else:
            logger.EOSF("""The account object created.""")

        account_object.owner_key = owner_key
        account_object.active_key = active_key

    # append account methodes to the account_object:

    def code(account_object, code="", abi="", wasm=False):
        return cleos.GetCode(
            account_object, code, abi, 
            is_verbose=-1)

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
            is_verbose=-1
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
            is_verbose=-1)

        if not account_object.action.error:
            try:
                account_object._console = account_object.action.console
                logger.OUT(account_object._console)
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
                                is_verbose=-1)
        return account_object._table

    account_object.table = types.MethodType(table, account_object)

    def __str__(account_object):
        return account_object.name

    account_object.__str__ = types.MethodType(__str__, account_object)

    # export the account object to the globals in the calling module:
    inspect.stack()[levels_below][0].f_globals[account_object_name] = account_object

    # put the account object to the wallet:
    wallet.open()
    wallet.unlock()
    wallet.import_key(account_object)

    if not account_object.error and not wallet.error:
        wallet.map_account(account_object_name, account_object)

    return account_object

