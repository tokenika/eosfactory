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

"""The namespace where account objects go.
"""
wallet_globals = None
"""The singleton ``Wallet`` object.
"""
wallet_singleton = None
def is_wallet_defined(logger):
    """
    """
    inspect_stack = inspect.stack()
    size = len(inspect_stack)
    global wallet_singleton
    global wallet_globals
    for index in range(size):
        locals = inspect_stack[index][0].f_locals
        globals = inspect_stack[index][0].f_globals
        
        objects = {**globals, **locals}
        for name in objects:
            if isinstance(objects[name], eosf_wallet.Wallet):
                wallet_singleton = objects[name] 
                wallet_globals = globals
        if not wallet_singleton is None:
            break

    if wallet_singleton is None:
        logger.ERROR("""
            Cannot find any `Wallet` object.
            Add the definition of an `Wallet` object, for example:
            `wallet = eosf.Wallet()`
            """)
    
def is_local_testnet_running(account_eosio):
    account_ = cleos.GetAccount(account_eosio.name, json=True, is_verbose=-1)
    if not account_.error and \
        account_eosio.owner_key.key_public == \
            account_.json["permissions"][0]["required_auth"]["keys"] \
                [0]["key"]:
        return True
    else:
        return False

def put_account_to_wallet_and_on_stack(
        account_object, account_object_name, logger):

    global wallet_singleton
    global wallet_globals    
    wallet_singleton.open()
    wallet_singleton.unlock()
    if wallet_singleton.keys_in_wallets([account_object.owner_key.key_private, \
            account_object.active_key.key_private]):
        wallet_singleton.map_account(account_object_name, account_object)
        # export the account object to the globals in the wallet module:
        wallet_globals[account_object_name] = account_object
        account_object.in_wallet = True
        return True
    else:
        if wallet_singleton.import_key(account_object):
            wallet_singleton.map_account(account_object_name, account_object)
            # export the account object to the globals in the wallet module:
            wallet_globals[account_object_name] = account_object
            account_object.just_put_into_wallet = True
            return True
        else:
            logger.EOSF("""
            Wrong or missing keys for the account ``{}`` in the wallets.
            """.format(account_object.name))
            return False        

class Eosio():
    def __init__(self):
        self.name = "eosio"
        config = teos.GetConfig(is_verbose=0)
        self.owner_key = cleos.CreateKey(
            "owner",
            config.json["EOSIO_KEY_PUBLIC"],
            config.json["EOSIO_KEY_PRIVATE"]
            )
        self.active_key = self.owner_key

    def info(self):
        print(cleos.GetAccount(
            self.name, is_verbose=-1).out_msg)

class AccountMaster():
    """Look for the account of the given name, put it into the wallet.

    - **parameters**::

        account_object_name: the name of the account object
        account_name: the name of the account
        owner_key_private: private owner key, if not ``None``, used for 
            adding any orphan account, when preivate keys are restored from
            a safe
        active_key_private: private active key, if not ``None``, used for 
            adding any orphan account, when preivate keys are restored from
            a safe 

    - **return**::
        account object, if account exists, ``None`` otherwise
        
    """    
    def __init__(
        account_object_name, account_name, 
        owner_key_private, active_key_private, verbosity=None):

        if not account_name: 
            account_name = cleos.account_name()
        self.account_name = account_name
        self.exists = False
        self.in_wallet = False
        self.just_put_into_wallet = False
        self.fatal_error = False
        self.logger = eosf.Logger(verbosity)

        account_object = cleos.GetAccount(
            account_name, json=True, is_verbose=-1)
        if logger.ERROR(account_object):
                self.fatal_error = True
        else:
            self.exists = True

            if owner_key_private is None:
                self.owner_key = cleos.CreateKey(
                    "owner", 
                    self.json["permissions"][1]["required_auth"]["keys"] \
                    [0]["key"], 
                    is_verbose=0)
            else: # an orphan account, private key is restored from a safe
                self.owner_key = cleos.CreateKey(
                    "owner", 
                    self.json["permissions"][1]["required_auth"]["keys"] \
                    [0]["key"], owner_key_private,
                    is_verbose=0) 

            if active_key_private is None:
                self.owner_key = cleos.CreateKey(
                    "owner", 
                    self.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"], 
                    is_verbose=0)
            else: # an orphan account, private key is restored from a safe
                self.active_key = cleos.CreateKey(
                    "active", 
                    self.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"], active_key_private,
                    is_verbose=0)

            def info(self):
                ao = cleos.GetAccount(self.name, is_verbose=-1)
                print(ao.out_msg)

            logger.EOSF("""
            Account ``{}`` exists in the blockchain. Checking whether the wallet
            has keys to it ... 
            """.format(self.account_name))

            if put_account_to_wallet_and_on_stack(
                    self, account_object_name, logger):
                self.in_wallet = True

            if self.in_wallet:
                logger.EOSF("""
                ... indeed, there are proper keys in the wallet.
                """)

def account_master_create(
            account_object_name, account_name="", 
            owner_key=None, active_key=None,
            verbosity=None):
    """Create account object in caller's global namespace.

    - **parameters**::

        account_object_name:: the name of the account object
        account_name: the name of the account; random, if not set
        verbosity: argument to the internal logger

    Preconditions
    #############

    Check the following conditions:
    * ``eosf.use_keosd(True)`` or the local testnet is running.
    * precisely one ``Wallet`` object is defined;
    
    Local testnet
    #############

    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.

    Remote testnet
    ##############

    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``, and must be ``eosf.use_keosd(True)``.

    Existing account
    ****************

    If the ``account_name`` argument is set, check the testnet for presence of the 
    account. If present, create the corresponding object and put the account 
    into the wallet, and put the account object into the global namespace of 
    the caller. and **return**. Otherwise start a  registration procedure, 
    described in the next paragraph.

    Registration to a remote testnet
    ********************************

    If the ``account_name`` argument is not set or it does not address any existing
    account, see the previous paragraph, start a registration procedure.

    * if the ``account_name`` argument is not set, make it random
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
        ######### Create the master account object named `{}`...
        """.format(account_object_name))

    """
    Check the following conditions:
    * ``eosf.use_keosd(True)`` or the local testnet is running;
    * a ``Wallet`` object is defined;
    """  
    cleos.is_notrunningnotkeosd_error(logger)
    if logger.ERROR():
        return logger
    
    is_wallet_defined(logger)
    global wallet_singleton
    if wallet_singleton is None:
        return logger

    """
    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.
    """
    account_object = Eosio()

    if is_local_testnet_running(account_object):
        put_account_to_wallet_and_on_stack(
            account_object, account_object_name, logger)
        return

    """
    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``, and must be ``eosf.use_keosd(True)``.
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
        Wallet Manager. Use 'eosf.use_keosd(True)' command.
        """)
        return logger

    """
    If the ``account_name`` argument is not set, it is randomized. Check the testnet for 
    presence of the account. If present, create the corresponding object and see 
    whether it is in the wallets. If so, put the account object into the global 
    namespace of the caller. and **return**. 
    """
    while True:
        account_object = AccountMaster(
            account_object_name, account_name, 
            owner_key, active_key, verbosity
        )
        
        if account_object.in_wallet \
                or account_object.just_put_into_wallet \
                or account_object.fatal_error:
            return
  
        if not account_object.exists:
            if owner_key is None:
                account_object.owner_key = cleos.CreateKey(
                    "owner", is_verbose=-1)
            else:
                account_object.owner_key = cleos.CreateKey(
                    "owner", "", owner_key, is_verbose=-1)

            if active_key is None:
                account_object.active_key = cleos.CreateKey(
                    "active", is_verbose=-1)
            else:
                account_object.active_key = cleos.CreateKey(
                    "active", "", active_key, is_verbose=-1)

            logger.OUT("""
            Use the following data to register a new account on a public testnet:
            Accout Name: {}
            Owner Public Key: {}
            Active Public Key: {}

            Owner Private Key: {}
            Active Private Key: {}
            """.format(
                account_object.name,
                account_object.owner_key.key_public,
                account_object.active_key.key_public,
                account_object.owner_key.key_private,
                account_object.active_key.key_private
                ))

            while True:
                is_ready = input("enter 'go' when ready or 'q' to quit <<< ")
                if is_ready == "q":
                    return
                else: 
                    if is_ready == "go":
                        break
        else:
            logger.EOSF("""
            ###
            You can try another name. Do you wish to do this?
            """)
            decision = input("y/n <<< ")
            if decision == "y":
                account_name = input(
                    "enter the account name or nothing to make the name random <<< ")
            else:
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
        verbosity=None):

    logger = eosf.Logger(verbosity)
    logger.EOSF_TRACE("""
        ######### Create the account object `{}` ...
        """.format(account_object_name))

    """
    Check the following conditions:
    * ``eosf.use_keosd(True)`` or the local testnet is running;
    * a ``Wallet`` object is defined;
    * the account object name is not in use, already.
    """
    cleos.is_notrunningnotkeosd_error(logger)
    if logger.ERROR():
        return logger

    is_wallet_defined(logger)
    global wallet_singleton
    if wallet_singleton is None:
        return
        
    if wallet_singleton.is_name_taken(account_object_name, account_name):
        return wallet_singleton.logger

    """
    Create an account object.
    """
    account_object = None
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
            logger.EOSF("""The account object is created.""")

        account_object.owner_key = owner_key
        account_object.active_key = active_key
        put_account_to_wallet_and_on_stack(
            account_object, account_object_name, logger)

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



