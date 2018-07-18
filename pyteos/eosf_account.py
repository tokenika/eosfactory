import json
import inspect
import types
import time

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

def add_account_object(account_object_name, name, wallet, levels_below):
    """Look for an account, if found, put it into the wallet.

    - **parameters**::

        account_object_name: the name of the account object
        name: the name of the account

    - **return**::
        account object, if account exists, ``None`` otherwise
        
    """
    account_object_ = cleos.GetAccount(name, json=True, is_verbose=-1) 
    if not account_object_.error:
        account_object_.name = name
        account_object_.account_info = str(account_object_)
        account_object_.owner_key = cleos.CreateKey(
            "active", 
            account_object_.json["permissions"][0]["required_auth"]["keys"] \
            [0]["key"], 
            is_verbose=0)

        account_object_.owner_key = cleos.CreateKey(
            "owner", 
            account_object_.json["permissions"][1]["required_auth"]["keys"] \
            [0]["key"], 
            is_verbose=0)

        put_account_to_wallet(
            account_object_, wallet, account_object_name, levels_below+1)

        def info(account_object):
            ao = cleos.GetAccount(account_object.name, is_verbose=-1)
            return ao.out_msg

        account_object_.info = types.MethodType(info, account_object_)

        return True
    return False

def account_master_create(
            account_object_name, name="", verbosity=None, levels_below=1):
    """Create account object in caller's global namespace.

    - **parameters**::

        account_object_name:: the name of the account object
        name: the name of the account; random, if not set
        verbosity: argument to the internal logger
        levels_below: experimental argument

    Preconditions
    #############

    Check the following conditions:
    * ``setup.use_keosd(True)`` or the local testnet is running.
    * precisely one ``Wallet`` object is defined;
    
    Local testnet
    #############

    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.

    Remote testnet
    ##############

    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``, and must be ``setup.use_keosd(True)``.

    Existing account
    ****************

    If the ``name`` argument is set, check the testnet for presence of the 
    account. If present, create the corresponding object and put the account 
    into the wallet, and put the account object into the global namespace of 
    the caller. and **return**. Otherwise start a  registration procedure, 
    described in the next paragraph.

    Registration to a remote testnet
    ********************************

    If the ``name`` argument is not set or it does not address any existing
    account, see the previous paragraph, start a registration procedure.

    * if the ``name`` argument is not set, make it random
    * print registration data, namely:
        * account name
        * owner public key
        * active public key
        * owner private key
        * active private key
    * wait for the user to register the master account
    * . . . . 
    * detect the named account on the remote testnet
    * put the account into the wallet
    * put the account object into the global namespace of the caller
    
    Name conflict between account objects
    #####################################

    If the new account object is going to be added to the wallet, an error
    is reported. Then an offer is given to edith the mapping file in order
    to resolve the conflict. When the conflict is resolved, the procedure
    finishes successfully.
    """

    logger = eosf.Logger(verbosity)
    logger.EOSF_TRACE("""
        ######### 
        Create the master account object named `{}`...
        """.format(account_object_name))

    """
    Check the following conditions:
    * ``setup.use_keosd(True)`` or the local testnet is running.
    * precisely one ``Wallet`` object is defined;
    """
    
    cleos.is_notrunningnotkeosd_error(logger)
    if logger.ERROR():
        return logger
    
    wallet = precisely_one_wallet(logger, levels_below=levels_below+1)
    if wallet is None:
        return logger

    """
    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.
    """
   
    account_object = types.SimpleNamespace()
    account_object.name = "eosio"
    config = teos.GetConfig(is_verbose=0)
    account_object.owner_key = cleos.CreateKey(
        "owner",
        config.json["EOSIO_KEY_PUBLIC"],
        config.json["EOSIO_KEY_PRIVATE"]
        )

    def info(account_object):
        ao = cleos.GetAccount(account_object.name, is_verbose=-1)
        return ao.out_msg

    account_object.info = types.MethodType(info, account_object)

    if is_local_testnet_running(account_object):
        put_account_to_wallet(
            account_object, wallet, account_object_name, levels_below+1)
        return

    """
    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``, and must be ``setup.use_keosd(True)``.
    """

    if setup.is_local_address():
        logger.ERROR("""
        If the local testnet is not running, an outer testnet has to be 
        defined with `setup.set_nodeos_address(<url>)`.
        Use 'setup.set_nodeos_address(<URL>)'
        """)
        return logger

    if not setup.is_use_keosd():
        logger.ERROR("""
        If the local testnet is not running, you have to use the 'keosd' 
        Wallet Manager. Use 'setup.use_keosd(True)' command.
        """)
        return logger

    """
    If the ``name`` argument is set, check the testnet for presence of the 
    account. If present, create the corresponding object and put the account 
    into the wallet, and put the account object into the global namespace of 
    the caller. and **return**.
    """
    if add_account_object(account_object_name, name, wallet, levels_below+1):
        return

    """
    If the ``name`` argument is not set or it does not address any existing
    account, see the previous paragraph, start a registration procedure.

    * if the ``name`` argument is not set, make it random
    * print registration data, namely:
        * account name
        * owner public key
        * active public key
        * owner private key
        * active private key
    """
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

    """
    * wait for the user to register the master account
    * . . . . 
    * detect the named account on the remote testnet
    * put the account into the wallet
    * put the account object into the global namespace of the caller
    """
    while True:
        time.sleep(2)
        if add_account_object(account_object_name, name, wallet, levels_below+1):
            return

def account_create(
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

    logger = eosf.Logger(verbosity)
    
    logger.EOSF_TRACE("""
        ######### 
        Create the account object named `{}` ...
        """.format(account_object_name))

    wallet = precisely_one_wallet(logger, levels_below=levels_below+1)
    if wallet is None:
        return
        
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

        if not logger.ERROR(account_object):
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

