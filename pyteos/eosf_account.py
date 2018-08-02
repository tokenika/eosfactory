import json
import inspect
import types
import time
import re

import setup
import teos
import cleos
import cleos_system
import eosf
import eosf_wallet

def restart():
    eosf.restart()

    eosf_wallet.wallet = None
    try:
        global wallet_singleton
        del wallet_singleton
    except:
        pass
    try:
        global wallet_globals
        del wallet_globals
    except:
        pass
    try:
        global account_master_test
        del account_master_test
    except:
        pass

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
account_master_test = None

def is_wallet_defined(logger):
    """
    """
    if not wallet_globals is None:
        return
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
        account_object_name, account_object, logger=None):

    if logger is None:
        logger = account_object

    global wallet_singleton
    global wallet_globals    
    wallet_singleton.open()
    wallet_singleton.unlock()

    if wallet_singleton.keys_in_wallets([account_object.owner_key.key_private, \
            account_object.active_key.key_private]):
        wallet_singleton.map_account(account_object_name, account_object)
        # export the account object to the globals in the wallet module:
        wallet_globals[account_object_name] = account_object
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

    def __str__(self):
        return self.name

class GetAccount(cleos.GetAccount, eosf.Logger):
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
            self,
            account_object_name, name=None, 
            owner_key_private=None, active_key_private=None, verbosity=None):

        eosf.Logger.__init__(self, verbosity)
        if name is None: 
            self.name = cleos.account_name()
        else:
            self.name = name
            
        if active_key_private is None:
            active_key_private = owner_key_private

        self.exists = False
        self.just_put_into_wallet = False
        self.fatal_error = False
        self.has_keys = not owner_key_private is None
        
        cleos.GetAccount.__init__(
            self, self.name, json=True, is_verbose=-1)

        self.ERROR_OBJECT(self)
        if not self.error_object is None:
            if not isinstance(self.error_object, eosf.AccountNotExist):
                self.fatal_error = True            
            return

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

        self.EOSF("""
            * Account ``{}`` exists in the blockchain.
            """.format(self.name))

    def info(self):
        result = cleos.GetAccount(self.name, is_verbose=-1)
        if not self.ERROR(result):
            print(ao.out_msg)

    def __str__(self):
        return self.name

class RestoreAccount(cleos.RestoreAccount, eosf.Logger):
    def __init__(self, name, verbosity=None):
        cleos.RestoreAccount.__init__(self, name, is_verbose=-1)
        eosf.Logger.__init__(self, verbosity)

class CreateAccount(cleos.CreateAccount, eosf.Logger):
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
            verbosity=None):
        cleos.CreateAccount.__init__(
            self, creator, name, owner_key, active_key, permission,
            expiration_sec, skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block, is_verbose=-1
            )
        eosf.Logger.__init__(self, verbosity)

class SystemNewaccount(cleos_system.SystemNewaccount, eosf.Logger):
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu,
            permission="",
            buy_ram_kbytes=0, buy_ram="",
            transfer=False,
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            verbosity=None):
        cleos_system.__init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu, permission, buy_ram_kbytes, buy_ram,
            transfer, expiration_sec, skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage, ref_block, is_verbose=-1)
        eosf.Logger.__init__(self, verbosity)
        
def account_master_create(
            account_object_name, account_name=None, 
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
        ######### Create the master account object named ``{}``...
        """.format(account_object_name))

    """
    Check the following conditions:
    * ``eosf.use_keosd(True)`` or the local testnet is running;
    * a ``Wallet`` object is defined;
    """  
    if logger.ERROR(cleos.is_notrunningnotkeosd_error()):
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
            account_object_name, account_object, logger)
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
        account_object = GetAccount(
            account_object_name, account_name, 
            owner_key, active_key, verbosity)
        
        if account_object.fatal_error:
            return

        if account_object.exists:
            if account_object.has_keys: # it is your account
                account_object.EOSF("""
                    * Checking whether the wallet has keys to the account ``{}``
                    """.format(account_object.name))

                if append_account_methods_and_finish(
                    account_object_name, account_object, account_object):
                    account_object.EOSF("""
                        * The account ``{}`` is in the wallet.
                        """.format(account_object.name))
                    return
            else: # the name is taken by somebody else
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
        else:
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

            global account_master_test
            if not account_master_test is None:
                account_name = account_master_test.name
                owner_key = account_master_test.owner_key.key_private
                active_key = account_master_test.active_key.key_private
                
            while True:
                is_ready = input("enter 'go' when ready or 'q' to quit <<< ")
                if is_ready == "q":
                    return
                else: 
                    if is_ready == "go":
                        break

def append_account_methods_and_finish(
        account_object_name, account_object, logger):

    def error_map(account_object, err_msg):

        if "main.cpp:2888" in err_msg:
            return eosf.AccountNotExist(
                eosf.AccountNotExist.msg_template.format(account_object.name))

        if "transaction executed locally, but may not be" in err_msg:
            return None

        if not err_msg:
            return None
        return eosf.Error(err_msg)

    account_object.error_map = types.MethodType(error_map, account_object)

    if not logger.ERROR(account_object):
        logger.EOSF("""
            * The account object is created.
            """)    

    def code(account_object, code="", abi="", wasm=False):
        result = cleos.GetCode(account_object, code, abi, is_verbose=-1)
        if not account_object.ERROR(result):
            account_object.EOSF_TRACE("""
            * code()
            """)
            account_object.OUT(result.out_msg)

    account_object.code = types.MethodType(code, account_object)

    def set_contract(
            account_object, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=""):

        result = cleos.SetContract(
            account_object, contract_dir, 
            wast_file, abi_file, 
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=-1
            )
        if not logger.ERROR(result):
            logger.OUT(result)
            account_object.set_contract = result
        else:
            account_object.set_contract = None

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

        result = cleos.PushAction(
            account_object, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=-1, json=True)
        if not account_object.ERROR(result):
            account_object.EOSF_TRACE("""
            * Push action:
                {}
            """.format(re.sub(' +',' ',data)))
            #account_object.OUT(result.out_msg)
            account_object.action = result
            try:
                account_object._console = result.console
                account_object.DEBUG(account_object._console)
            except:
                pass
        else:
            account_object.action = None

    account_object.push_action = types.MethodType(
                                    push_action , account_object)

    def table(
            account_object, table_name, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        result = cleos.GetTable(
                    account_object, table_name, scope,
                    binary, 
                    limit, key, lower, upper,
                    is_verbose=-1)
        if not account_object.ERROR(result):
            try:
                account_map = eosf.account_map()
                scope = account_map[str(scope)]
            except:
                pass

            account_object.EOSF_TRACE("""
            * Table ''{}'' for ``{}``
            """.format(table_name, scope))
            account_object.OUT(result.out_msg)
            return result
        return None

    account_object.table = types.MethodType(table, account_object)

    def __str__(account_object):
        return account_object.name

    account_object.__str__ = types.MethodType(__str__, account_object)

    return put_account_to_wallet_and_on_stack(
            account_object_name, account_object)



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
    if logger.ERROR(cleos.is_notrunningnotkeosd_error()):
        return logger

    is_wallet_defined(logger)
    global wallet_singleton
    if wallet_singleton is None:
        return
        
    if wallet_singleton.is_name_taken(account_object_name, account_name):
        return wallet_singleton

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
        account_object = RestoreAccount(account_name, verbosity)
             
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

            account_object = SystemNewaccount(
                    creator, account_name, owner_key, active_key,
                    stake_net, stake_cpu,
                    permission,
                    buy_ram_kbytes, buy_ram,
                    transfer,
                    expiration_sec, 
                    skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    verbosity
                    )
        else:
            logger.EOSF_TRACE("""
                            ... for the local testnet account.
                        """)
            account_object = CreateAccount(
                    creator, account_name, 
                    owner_key, active_key,
                    permission,
                    expiration_sec, skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    verbosity
                    )
            account_object


        account_object.owner_key = owner_key
        account_object.active_key = active_key

    append_account_methods_and_finish(
        account_object_name, account_object, logger)


