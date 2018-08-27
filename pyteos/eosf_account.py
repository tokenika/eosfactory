import json as json_module
import inspect
import types
import time
import re

import setup
import teos
import front_end
import cleos
import cleos_system
import eosf
import eosf_wallet

def restart():
    eosf.restart()
    eosf_wallet.Wallet.wallet = None

    global wallet_singleton
    try:
        del wallet_singleton
    except:
        pass    
    wallet_singleton = None

    global wallet_globals
    wallet_globals = None

def is_local_testnet_running():
        account_ = cleos.GetAccount(self.name, json=True, is_verbose=-1)
        if not account_.error and \
            self.key_public == \
                account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"]:
            self.account_info = str(account_)
            self.TRACE('''
                Local testnet is ON: the `eosio` account is master.
                ''')
            return True
        else:
            return False

def _data_json(data):
    class Encoder(json_module.JSONEncoder):
        def default(self, o):
            if isinstance(o, cleos.Account):
                return str(o)
            else:
                json_module.JSONEncoder.default(self, o) 

    if isinstance(data, dict) or isinstance(data, list):
        data_json = json_module.dumps(data, cls=Encoder)
    else:
        data_json = re.sub("\s+|\n+|\t+", " ", data)
        data_json = eosf.object_names_2_accout_names(data_json)
    return data_json

'''The namespace where account objects go.
'''
wallet_globals = None
'''The singleton ``Wallet`` object.
'''
wallet_singleton = None

def is_wallet_defined(logger):
    '''
    '''
    global wallet_globals    
    if not wallet_globals is None:
        return
    wallet_globals = eosf_wallet.Wallet.globals
    
    global wallet_singleton        

    wallet_globals = eosf_wallet.Wallet.globals
    wallet_singleton = eosf_wallet.Wallet.wallet

    if wallet_singleton is None:
        logger.ERROR('''
            Cannot find any `Wallet` object.
            Add the definition of an `Wallet` object, for example:
            `create_wallet()`
            ''')
    
def is_local_testnet_running(account_eosio):
    account_ = cleos.GetAccount(account_eosio.name, json=True, is_verbose=-1)
    if account_.error:
        return False
    else:
        try: # remote eosio may have the ["keys"] array empty.
            return account_eosio.owner_key.key_public == \
                account_.json["permissions"][0]["required_auth"]["keys"] \
                    [0]["key"]
        except:
            False        

def put_account_to_wallet_and_on_stack(
        account_object_name, account_object, logger=None):
    if logger is None:
        logger = account_object

    global wallet_singleton
    global wallet_globals

    if account_object.owner_key:
        if wallet_singleton.keys_in_wallets([account_object.owner_key.key_private, \
                account_object.active_key.key_private]):
            wallet_singleton.map_account(account_object_name, account_object)
        else:
            if wallet_singleton.import_key(account_object):
                wallet_singleton.map_account(account_object_name, 
                account_object)
            else:
                logger.TRACE('''
                Wrong or missing keys for the account ``{}`` in the wallets.
                '''.format(account_object.name))
                return False

    # export the account object to the globals in the wallet module:
    global wallet_globals      
    wallet_globals[account_object_name] = account_object
    account_object.in_wallet_on_stack = True
    return True


class Eosio(cleos.Account):
    def __init__(self, account_object_name):
        self.name = "eosio"
        self.account_object_name = account_object_name
        config = teos.GetConfig(is_verbose=0)
        self.owner_key = cleos.CreateKey(
            "owner",
            config.json["EOSIO_KEY_PUBLIC"],
            config.json["EOSIO_KEY_PRIVATE"]
            )
        self.active_key = self.owner_key

    def info(self):
        print("account object name: {}\nname: {}\n{}".format(
                self.account_object_name, 
                self.name,
                cleos.GetAccount(self.name, is_verbose=-1).out_msg))

    def __str__(self):
        return self.name


class GetAccount(cleos.GetAccount):
    '''Look for the account of the given name, put it into the wallet.

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
        
    '''    
    def __init__(
            self,
            account_object_name, name=None, 
            owner_key_private=None, active_key_private=None, verbosity=None):

        self.account_object_name = account_object_name
        if name is None: 
            self.name = cleos.account_name()
        else:
            self.name = name
            
        if active_key_private is None:
            active_key_private = owner_key_private

        self.exists = False
        self.in_wallet_on_stack = False
        self.fatal_error = False
        self.has_keys = not owner_key_private is None
        
        cleos.GetAccount.__init__(
            self, self.name, json=True, is_verbose=-1)

        self.ERROR_OBJECT(self)
        if not self.error_object is None:
            if not isinstance(self.error_object, front_end.AccountNotExist):
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

        self.TRACE('''
            * cleos.Account ``{}`` exists in the blockchain.
            '''.format(self.name))

    def info(self):
        get_account = cleos.GetAccount(self.name, is_verbose=-1)
        if not self.ERROR(get_account):
            print("account object name: {}\n{}".format(
                self.account_object_name, get_account))

    def __str__(self):
        return self.name


class RestoreAccount(front_end.Logger, cleos.Account, cleos.RestoreAccount):
    def __init__(self, name, verbosity=None):
        cleos.RestoreAccount.__init__(self, name, is_verbose=-1)
        front_end.Logger.__init__(self, verbosity)


class CreateAccount(cleos.CreateAccount):
    def __init__(
            self, creator, name, owner_key, 
            active_key="",
            permission=None,
            expiration_sec=30, 
            skip_signature=0, 
            dont_broadcast=0,
            forceUnique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            ref_block=None,
            verbosity=None):
        cleos.CreateAccount.__init__(
            self, creator, name, owner_key, active_key, permission,
            expiration_sec, skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block, is_verbose=-1
            )


class SystemNewaccount(cleos_system.SystemNewaccount):
    def __init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu,
            permission=None,
            buy_ram_kbytes=0, buy_ram="",
            transfer=False,
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            verbosity=None):
            
        cleos_system.SystemNewaccount.__init__(
            self, creator, name, owner_key, active_key,
            stake_net, stake_cpu, permission, buy_ram_kbytes, buy_ram,
            transfer, expiration_sec, skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage, ref_block, is_verbose=-1)
        

def create_master_account(
            account_object_name, account_name=None, 
            owner_key=None, active_key=None,
            verbosity=None):
    '''Create account object in caller's global namespace.

    - **parameters**::

        account_object_name:: the name of the account object
        account_name: the name of the account; random, if not set
        verbosity: argument to the internal logger

    Preconditions
    #############

    Check the following conditions:
    * precisely one ``Wallet`` object is defined;
    
    Local testnet
    #############

    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.

    Remote testnet
    ##############

    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``.

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
    '''

    logger = front_end.Logger(verbosity)
    logger.INFO('''
        ######### Create the master account object named ``{}``...
        '''.format(account_object_name))
    '''
    Check the following conditions:
    * a ``Wallet`` object is defined.
    '''  
    is_wallet_defined(logger)
    global wallet_singleton
    if wallet_singleton is None:
        return

    wallet_singleton.open_unlock()

    '''
    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.
    '''
    account_object = Eosio(account_object_name)
    if is_local_testnet_running(account_object):
        put_account_to_wallet_and_on_stack(
            account_object_name, account_object, logger)
        return

    '''
    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``.
    '''

    if setup.is_local_address:
        logger.ERROR('''
        If the local testnet is not running, an outer testnet has to be 
        defined with `setup.set_nodeos_address(<url>)`.
        Use 'setup.set_nodeos_address(<URL>)'
        ''')
        return

    '''
    If the ``account_name`` argument is not set, it is randomized. Check the testnet for 
    presence of the account. If present, create the corresponding object and see 
    whether it is in the wallets. If so, put the account object into the global 
    namespace of the caller. and **return**. 
    '''
    while True:
        account_object = GetAccount(
            account_object_name, account_name, 
            owner_key, active_key, verbosity)

        if account_object.fatal_error:
            logger.ERROR(account_object)
            return

        if account_object.exists:
            if account_object.has_keys: # it is your account
                account_object.TRACE('''
                    * Checking whether the wallet has keys to the account ``{}``
                    '''.format(account_object.name))

                if not account_object.ERROR():
                    account_object.TRACE('''
                        * The account object is created.
                        ''')  

                if append_account_methods_and_finish(
                    account_object_name, account_object, account_object):
                    account_object.TRACE('''
                        * The account ``{}`` is in the wallet.
                        '''.format(account_object.name))
                    return
            else: # the name is taken by somebody else
                logger.TRACE('''
                ###
                You can try another name. Do you wish to do this?
                ''')
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

            logger.OUT('''
            Use the following data to register a new account on a public testnet:
            Accout Name: {}
            Owner Public Key: {}
            Active Public Key: {}

            Owner Private Key: {}
            Active Private Key: {}
            '''.format(
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

def append_account_methods_and_finish(
        account_object_name, account_object, logger): 

    def code(account_object, code="", abi="", wasm=False):
        result = cleos.GetCode(account_object, code, abi, is_verbose=-1)
        if not account_object.ERROR(result):
            account_object.INFO('''
            * code()
            ''')
            account_object.OUT(result.out_msg)

    account_object.code = types.MethodType(code, account_object)

    def is_code(account_object):
        get_code = cleos.GetCode(account_object.name, is_verbose=-1)
        if not account_object.ERROR(get_code):
            if get_code.code_hash == \
            "0000000000000000000000000000000000000000000000000000000000000000":
                return ""
            else:
                return get_code.code_hash
        else:
            return None

    account_object.is_code = types.MethodType(is_code, account_object)        

    def set_contract(
            account_object, contract_dir, 
            wast_file="", abi_file="", 
            permission=None, expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None):

        wallet_singleton.open_unlock()

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
            permission=None, expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None, json=False, payer=None):
        data = _data_json(data)

        wallet_singleton.open_unlock()
        
        result = cleos.PushAction(
            account_object, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=-1, json=True)

        if account_object.ERROR(result, is_silent=True, is_fatal=False):
            if isinstance(result.error_object, front_end.LowRam):
                account_object.TRACE('''
                * RAM needed is {}.kByte, buying RAM {}.kByte.
                '''.format(
                    result.error_object.needs_kbyte,
                    result.error_object.deficiency_kbyte))
                import pdb; pdb.set_trace()
                buy_ram_kbytes = str(
                    result.error_object.deficiency_kbyte + 1)
                if not payer:
                    payer = account_object

                receiver = None
                if not permission is None:
                    receiver = result._permission_arg(permission)[0]
                    if not receiver.find("@") == -1:
                        receiver = receiver[:receiver.find("@")]
                    receiver = account_object

                payer.buy_ram(buy_ram_kbytes, receiver)
            
                result = cleos.PushAction(
                    account_object, action, data,
                    permission, expiration_sec, 
                    skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    is_verbose=-1, json=True)    


        account_object.INFO('''
            * Push action ``{}``:
            '''.format(action))

        if not account_object.ERROR(result):
            account_object.INFO('''
                {}
            '''.format(re.sub(
                ' +',' ', eosf.accout_names_2_object_names(data))))

            account_object.action = result
            try:
                account_object._console = result.console
                account_object.DEBUG(eosf.accout_names_2_object_names(
                    account_object._console))
            except:
                pass

            if json:
                account_object.OUT('''
                push action responce:

                {}
                '''.format(eosf.accout_names_2_object_names(
                        result.out_msg, keys=True)))

        account_object.action = result

    account_object.push_action = types.MethodType(
                                    push_action , account_object)

    def show_action(self, action, data, permission=None):
        ''' Implements the `push action` command without broadcasting. 
        '''
        return self.push_action(action, data, permission, dont_broadcast=1)

    account_object.show_action = types.MethodType(
                                    show_action , account_object)

    def table(
            account_object, table_name, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        account_object.INFO('''
        * Table ``{}`` for ``{}``
        '''.format(table_name, scope))

        wallet_singleton.open_unlock()
        
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

            account_object.OUT(eosf.accout_names_2_object_names(result.out_msg))
            return result
        return None

    account_object.table = types.MethodType(table, account_object)

    def __str__(account_object):
        return account_object.name

    account_object.__str__ = types.MethodType(__str__, account_object)

    def buy_ram(
            account_object, amount_kbytes, receiver=None,
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None):
            
        if receiver is None:
            receiver = account_object
        buy_ram_kbytes = 1

        wallet_singleton.open_unlock()
        
        result = cleos_system.BuyRam(
            account_object, receiver, amount_kbytes,
            buy_ram_kbytes,
            expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=0
            )

        account_object.ERROR(result)

    account_object.buy_ram = types.MethodType(buy_ram, account_object)

    def info(account_object):
        print("account object name: {}\n{}".format(
            account_object_name,
            str(cleos.GetAccount(account_object.name, is_verbose=0))))

    account_object.info = types.MethodType(info, account_object)

    get_account = cleos.GetAccount(account_object, is_verbose=0)
    if not account_object.ERROR(get_account):
        account_object.TRACE('''
        * Cross-checked: account {}({}) is in the blockchain.
        '''.format(account_object_name, account_object.name))
    return put_account_to_wallet_and_on_stack(
        account_object_name, account_object)


def create_account(
        account_object_name,
        creator, 
        stake_net="", stake_cpu="",
        account_name="",
        owner_key="", active_key="",
        permission=None,
        buy_ram_kbytes=1, buy_ram="",
        transfer=False,
        expiration_sec=30,
        skip_signature=0, dont_broadcast=0, forceUnique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        restore=False,
        verbosity=None):

    if restore:
        if creator:
            account_name = creator

    logger = front_end.Logger(verbosity)
    logger.INFO('''
        ######### Create the account object ``{}`` ...
        '''.format(account_object_name))

    '''
    Check the following conditions:
    * a ``Wallet`` object is defined;
    * the account object name is not in use, already.
    '''
    is_wallet_defined(logger)
    global wallet_singleton
    if wallet_singleton is None:
        return
        
    if wallet_singleton.is_name_taken(account_object_name, account_name):
        return

    wallet_singleton.open_unlock()

    '''
    Create an account object.
    '''
    account_object = None
    if restore:
        logger.INFO('''
                        ... for the blockchain account ``{}``.
                        '''.format(account_name))                       
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
            logger.INFO('''
                        ... paying stake for a new blockchain account ``{}``.
                        '''.format(account_name))
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

            if account_object.ERROR(is_silent=True, is_fatal=False):
                if isinstance(account_object.error_object, front_end.LowRam):
                    account_object.TRACE('''
                    * RAM needed is {}.kByte, buying RAM {}.kByte.
                    '''.format(
                        account_object.error_object.needs_kbyte,
                        account_object.error_object.deficiency_kbyte))

                    buy_ram_kbytes = str(
                        account_object.error_object.deficiency_kbyte + 1)
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
            logger.INFO('''
                        ... for a new blockchain account ``{}``.
                        '''.format(account_name))
            account_object = CreateAccount(
                    creator, account_name, 
                    owner_key, active_key,
                    permission,
                    expiration_sec, skip_signature, dont_broadcast, forceUnique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    verbosity
                    )


        account_object.owner_key = owner_key
        account_object.active_key = active_key

    if not account_object.ERROR():
        account_object.TRACE('''
            * The account object is created.
            ''')
        append_account_methods_and_finish(
            account_object_name, account_object, logger)



