import json as json_module
import inspect
import types
import time
import re

import setup
import teos
import cleos
import cleos_system
import eosf_control
import eosf_wallet
import eosf_testnet
import eosf_ui


def reboot():
    eosf_ui.Logger().INFO('''
    ######### Reboot EOSFactory session.
    ''')
    eosf_control.stop([])
    cleos.reboot()

    global wallet_singleton
    if wallet_singleton:
        wallet_singleton.delete_globals()
    eosf_wallet.Wallet.wallet = None

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
        data_json = eosf_control.object_names_2_accout_names(data_json)
    return data_json

'''The namespace where account objects go.
'''
wallet_globals = None
'''The singleton ``Wallet`` object.
'''
wallet_singleton = None


def is_wallet_defined(logger, globals=None):
    '''
    '''
    global wallet_globals   
    if not wallet_globals is None:
        return
    
    global wallet_singleton
    wallet_singleton = eosf_wallet.Wallet.wallet

    if wallet_singleton is None:
        eosf_wallet.create_wallet(globals=globals)
        wallet_singleton = eosf_wallet.Wallet.wallet

        if wallet_singleton is None:
            logger.ERROR('''
                Cannot find any `Wallet` object.
                Add the definition of an `Wallet` object, for example:
                `create_wallet()`
                ''')

    wallet_globals = eosf_wallet.Wallet.globals


def is_local_testnet_running(account_eosio):
    account_ = cleos.GetAccount(account_eosio.name, json=True, is_verbose=-1)
    if account_.error:
        return False
    else:
        try: # remote eosio may have the ["keys"] array empty.
            return account_eosio.owner_key.key_public == \
                account_.json["permissions"][1]["required_auth"]["keys"] \
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
        if wallet_singleton.keys_in_wallets(                [account_object.owner_key.key_private, \
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

    def delegate_bw(
            self, stake_net_quantity, stake_cpu_quantity,
            receiver=None,
            permission=None,
            transfer=False,
            expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            is_verbose=1):
        pass

    def buy_ram(
            account_object, amount_kbytes, receiver=None,
            expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None):
        pass


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
            if not isinstance(self.error_object, eosf_ui.AccountNotExist):
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


class RestoreAccount(eosf_ui.Logger, cleos.Account, cleos.RestoreAccount):
    def __init__(self, name, verbosity=None):
        cleos.RestoreAccount.__init__(self, name, is_verbose=-1)
        eosf_ui.Logger.__init__(self, verbosity)


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

    ### Preconditions

    Check the following conditions:
    * precisely one ``Wallet`` object is defined;
    
    ### Local testnet

    If the local testnet is running, create an account object representing 
    the ``eosio`` account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and **return**.

    ### Remote testnet

    Otherwise, an outer testnet has to be defined with 
    ``setup.set_nodeos_address(<url>)``.

    ### Existing account

    If the ``account_name`` argument is set, check the testnet for presence of the 
    account. If present, create the corresponding object and put the account 
    into the wallet, and put the account object into the global namespace of 
    the caller. and **return**. Otherwise start a  registration procedure, 
    described in the next paragraph.

    ### Registration to a remote testnet

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
    
    ### Name conflict between account objects

    If the new account object is going to be added to the wallet, an error
    is reported. Then an offer is given to edith the mapping file in order
    to resolve the conflict. When the conflict is resolved, the procedure
    finishes successfully.
    '''


    logger = eosf_ui.Logger(verbosity)

    globals = inspect.stack()[1][0].f_globals
    if account_object_name in globals:

        if not isinstance(globals[account_object_name], cleos.Account):
            logger.ERROR('''
            The global variable {} type is not ``Account``.
            '''.format(account_object_name))
            return

        logger.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format(account_object_name)) 
        return

    if isinstance(account_name, eosf_testnet.Testnet):
        owner_key = account_name.owner_key
        active_key = account_name.active_key
        account_name = account_name.account_name

    logger.INFO('''
        ######### Create the master account object named ``{}``...
        '''.format(account_object_name))
    '''
    Check the following conditions:
    * a ``Wallet`` object is defined.
    '''  
    is_wallet_defined(logger, globals)

    global wallet_singleton
    if wallet_singleton is None:
        return

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
            owner_key_new = cleos.CreateKey("owner", is_verbose=-1)
            active_key_new = cleos.CreateKey("active", is_verbose=-1)

            logger.OUT('''
            Use the following data to register a new account on a public testnet:
            Account Name: {}
            Owner Public Key: {}
            Active Public Key: {}

            Owner Private Key: {}
            Active Private Key: {}
            '''.format(
                account_object.name,
                owner_key_new.key_public,
                active_key_new.key_public,
                owner_key_new.key_private,
                active_key_new.key_private
                ))
                
            while True:
                is_ready = input("enter 'go' when ready or 'q' to quit <<< ")
                if is_ready == "q":
                    return
                else: 
                    if is_ready == "go":
                        break
            account_name = account_object.name
            owner_key = owner_key_new.key_private
            active_key = active_key_new.key_private

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
                ' +',' ', eosf_control.accout_names_2_object_names(data))))

            account_object.action = result
            try:
                account_object._console = result.console
                account_object.DEBUG(eosf_control.accout_names_2_object_names(
                    account_object._console))
            except:
                pass
            if json:
                account_object.OUT(
                    eosf_control.accout_names_2_object_names(result.out_msg))

        account_object.action = result

    account_object.push_action = types.MethodType(
                                    push_action, account_object)

    def show_action(account_object, action, data, permission=None):
        ''' Implements the `push action` command without broadcasting. 
        '''
        account_object.push_action(
            action, data, permission, dont_broadcast=1, json=True)

    account_object.show_action = types.MethodType(
                                    show_action, account_object)

    def table(
            account_object, table_name, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):

        account_object.INFO('''
        * Table ``{}`` for ``{}``
        '''.format(table_name, scope))
        
        result = cleos.GetTable(
                    account_object, table_name, scope,
                    binary, 
                    limit, key, lower, upper,
                    is_verbose=-1)

        if not account_object.ERROR(result):
            try:
                account_map = eosf_control.account_map()
                scope = account_map[str(scope)]
            except:
                pass

            account_object.OUT(eosf_control.accout_names_2_object_names(result.out_msg))
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

    def delegate_bw(
        account_object, stake_net_quantity, stake_cpu_quantity,
        receiver=None,
        permission=None,
        transfer=False,
        expiration_sec=30, 
        skip_signature=0, dont_broadcast=0, forceUnique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        is_verbose=1):

        if setup.is_local_address:
            return

        if receiver is None:
            receiver = account_object

        delegate_bw = cleos_system.DelegateBw(
            account_object, receiver,
            stake_net_quantity, stake_cpu_quantity,
            permission,
            transfer,
            expiration_sec,
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=0
            )
        if not delegate_bw.error:
            account_object.INFO('''
            * Transfered from {} to {} net: {} cpu: {}
            '''.format(
                delegate_bw.payer, delegate_bw.receiver,
                delegate_bw.stake_net_quantity, delegate_bw.stake_cpu_quantity))

    account_object.delegate_bw = types.MethodType(delegate_bw, account_object)

    def info(account_object):
        print("account object name: {}\n{}".format(
            account_object_name,
            str(cleos.GetAccount(account_object.name, is_verbose=0))))

    account_object.info = types.MethodType(info, account_object)

    get_account = cleos.GetAccount(account_object, is_verbose=0)
    if not account_object.ERROR(get_account):
        account_object.TRACE('''
        * Cross-checked: account {} is in the blockchain.
        '''.format(account_object_name))
    return put_account_to_wallet_and_on_stack(
        account_object_name, account_object)


def create_account(
        account_object_name,
        creator, 
        account_name="",
        owner_key="", active_key="",
        stake_net=3, stake_cpu=3,
        permission=None,
        buy_ram_kbytes=8, buy_ram="",
        transfer=False,
        expiration_sec=30,
        skip_signature=0, dont_broadcast=0, forceUnique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        restore=False,
        verbosity=None):

    logger = eosf_ui.Logger(verbosity)

    globals = inspect.stack()[1][0].f_globals
    if account_object_name in globals:

        if not isinstance(globals[account_object_name], cleos.Account):
            logger.ERROR('''
            The global variable {} type is not ``Account``.
            '''.format(account_object_name))
            return

        logger.INFO('''
            ######## {} account object restored from the blockchain.
            '''.format(account_object_name)) 
        return

    if restore:
        if creator:
            account_name = creator

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

    '''
    Create an account object.
    '''
    account_object = None
    if restore:
        logger.INFO('''
                    ... for the existing blockchain account ``{}`` ({}).
                    '''.format(account_object_name, account_name), 
                    translate=False)
        account_object = RestoreAccount(account_name, verbosity)
        account_object.account_object_name = account_object_name
    else:
        if not account_name:
            account_name = cleos.account_name()
        if owner_key:
            if not active_key:
                active_key = owner_key
        else:
            owner_key = cleos.CreateKey("owner", is_verbose=-1)
            active_key = cleos.CreateKey("active", is_verbose=-1)

        if stake_net and not setup.is_local_address:
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
                if isinstance(account_object.error_object, eosf_ui.LowRam):
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

        account_object.account_object_name = account_object_name
        account_object.owner_key = owner_key
        account_object.active_key = active_key

    if not account_object.ERROR():
        account_object.TRACE('''
            * The account object is created.
            ''')
        append_account_methods_and_finish(
            account_object_name, account_object, logger)


def stats(
        accounts, params, 
        last_col="%s", col="%15s"
    ):
    def find(element, json):
        try:
            keys = element.split('.')
            rv = json
            for key in keys:
                rv = rv[key]
        except:
            rv = "n/a"
        return rv

    jsons = []
    for account in accounts:
        json = cleos.GetAccount(account, json=True, is_verbose=0).json
        json["account_object_name"] = account.account_object_name
        jsons.append(json)

    header = ""
    for json in jsons:
        header = header + col % (json["account_object_name"])
    output = header + "\n\n"

    for param in params:
        for json in jsons:
            output = output + col % find(param, json)
        output = output + "  " + last_col % (param) + "\n" 

    eosf_ui.Logger().OUT(output, translate=False)