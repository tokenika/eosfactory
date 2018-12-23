'''
.. module:: eosfactory.shell.account
    :platform: Unix, Darwin
    :synopsis: Account object factories.

.. moduleauthor:: Tokenika
'''

import json
import inspect
import time
import re

import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.errors as errors
import eosfactory.core.interface as interface
import eosfactory.core.teos as teos
import eosfactory.core.interface as interface
import eosfactory.core.cleos as cleos
import eosfactory.core.cleos_get as cleos_get
import eosfactory.core.cleos_set as cleos_set
import eosfactory.core.cleos_sys as cleos_sys
import eosfactory.core.manager as manager
import eosfactory.core.testnet as testnet
import eosfactory.core.account as account
import eosfactory.shell.wallet as wallet


wallet_globals = None
wallet_singleton = None


class Account():
    '''Methods to be ascribed to account objects, produced with 
    :func:`.create_master_account` factories and :func:`.create_account`.
    '''
    @classmethod
    def add_methods_and_finalize(cls, account_object_name, account):
        '''Ascribes methodes to the given *account*, and finalizes the creation 
        of this *account*.
        '''
        account.account_object_name = account_object_name

        if not isinstance(account, cls): 
            account.__class__.__bases__ += (cls,)

        get_account = cleos.GetAccount(account, is_info=False, is_verbose=0)

        logger.TRACE('''
        * Cross-checked: account object *{}* mapped to an existing account *{}*.
        '''.format(account_object_name, account.name), translate=False)

        return put_account_to_wallet_and_on_stack(account_object_name, account)

    def code(self, code=None, abi=None, wasm=False):
        '''Retrieve the code and ABI

        Args:
            code (str): If set, the name of the file to save the contract 
                .wast/wasm to.
            abi (str): If set, the name of the file to save the contract .abi to.
            wasm (bool): Save contract as wasm.
        '''
        result = cleos_get.GetCode(self, is_verbose=False)
        logger.INFO('''
        * code()
        ''')
        logger.OUT(str(result))

    def is_code(self):
        '''Determine whether contract is set to the account.

        Return:
            True if the retrieved hash code of the contract code is not null.    
        '''
        get_code = cleos_get.GetCode(self.name, is_verbose=False)
        if get_code.code_hash == \
        "0000000000000000000000000000000000000000000000000000000000000000":
            return ""
        else:
            return get_code.code_hash

    def set_contract(
            self, contract_dir, 
            wasm_file="", abi_file="", 
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0
        ):
        '''Create or update the contract.

        Call *EOSIO cleos* with the *set contract* command. Store the result,
        which is an object of the class :class:`.cleos_set.SetContract`, as
        the value of the *set_contract* attribute.

        Args:
            contract_dir (str): A path to a directory.
            wasm_file (str): The WASM file relative to the contract_dir.
            abi_file (str): The ABI file for the contract, relative to the 
                contract-dir.

        See definitions of the remaining parameters: :func:`.cleos.common_parameters`.
        '''
        result = cleos_set.SetContract(
                    self, contract_dir, 
                    wasm_file, abi_file, 
                    permission, expiration_sec, 
                    skip_sign, dont_broadcast, force_unique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    delay_sec,
                    is_verbose=False, json=True
                )

        logger.OUT(result)
        self.set_contract = result

    def set_account_permission(
                self, permission_name, authority, parent_permission_name,
                permission=None,
                expiration_sec=None, 
                skip_sign=0, dont_broadcast=0, return_packed=0, force_unique=0,
                max_cpu_usage=0, max_net_usage=0,
                ref_block=None,
                delay_sec=0
        ):
        '''Set parameters dealing with account permissions.

        Call *EOSIO cleos* with the *set account permission* command. Store
        the result, which is an object of the 
        class :class:`.cleos_set.SetAccountPermission`, as the value of the *account_permission* attribute.

        Args:
            permission_name (str or .Permission): The permission to set/delete an 
                authority for.
            parent_permission_name (str or .Permission): The permission name of 
                this parents permission (defaults to: "active").
            authority (str or dict or filename):  None to delete.

        Exemplary values of the argument *authority*::

            # bob, carol are account objects created with 
            # shell.account.create_account factory function

            "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"

            bob.active()

            {
                "threshold" : 100, 
                "keys" : [], 
                "accounts" : 
                    [
                        {
                            "permission":
                                {
                                    "actor": bob.active(),
                                    "permission":"active"
                                },
                            "weight":100
                        }
                    ]
            }

        See definitions of the remaining parameters: 
        \:func:`.cleos.common_parameters`.
        '''
        logger.TRACE('''
            * Set action permission.
            ''')
        result = SetAccountPermission(
                self, permission_name, authority, parent_permission_name,
                permission,
                expiration_sec, 
                skip_sign, dont_broadcast, return_packed, force_unique,
                max_cpu_usage, max_net_usage,
                ref_block,
                delay_sec,
                is_verbose=False, json=True
            )

        logger.INFO('''
            * account permission *{}*:
            '''.format(authority))

        self.account_permission = result
    
    def set_action_permission(
                self, code, type, requirement,
                permission=None,
                expiration_sec=None, 
                skip_sign=0, dont_broadcast=0, return_packed=0, force_unique=0,
                max_cpu_usage=0, max_net_usage=0,
                ref_block=None,
                delay_sec=0
        ):
        '''Set parameters dealing with account permissions.

        Call *EOSIO cleos* with the *set action permission* command. Store the 
        result, which is an object of the 
        class :class:`.cleos_set.SetActionPermission`, as the value of the *action_permission* attribute.

        Args:
            code (str or .interface.Account): The account that owns the code for \
                the action.
            type (str): The type of the action.
            requirement (str): The permission name require for executing the given 
                action.

        See definitions of the remaining parameters: \:func:`.cleos.common_parameters`.
        '''
        logger.TRACE('''
        * Set action permission.
        ''')

        result = SetActionPermission(
                self, code, type, requirement,
                permission,
                expiration_sec, 
                skip_sign, dont_broadcast, return_packed, force_unique,
                max_cpu_usage, max_net_usage,
                ref_block,
                delay_sec,
                is_verbose=False,
                json=True
            )

        logger.INFO('''
            * action permission *{}*:
            '''.format(type))

        self.action_permission = result


    def push_action(
            self, action, data,
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None, delay_sec=0):
        '''Push a transaction with a single action.

        Call *EOSIO cleos* with the *push action* command. Store the result,
        which is an object of the class :class:`.cleos.PushAction`,  as
        the value of the *action* attribute.

        Args:
            action (str or json or filename): Definition of the action to 
                execute on the contract.
            data (str): The arguments to the contract.

        See definitions of the remaining parameters: 
        \:func:`.cleos.common_parameters`.

        Attributes:
            account_name (str): The EOSIO name of the contract's account.
            console (str): *["processed"]["action_traces"][0]["console"]* \
                component of EOSIO cleos responce.
            data (str): *["processed"]["action_traces"][0]["act"]["data"]* \
                component of EOSIO cleos responce.
        '''
        data = manager.data_json(data)

        result = cleos.PushAction(
            self, action, data,
            permission, expiration_sec, 
            skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=False, json=True)

        logger.INFO('''
            * push action *{}*:
            '''.format(action))

        logger.INFO('''
            {}
        '''.format(re.sub(' +',' ', data)))

        self.action = result
        try:
            self._console = result.console
            logger.DEBUG(self._console)
        except:
            pass
        if json:
            logger.OUT(result.out_msg)

        self.action = result

    def show_action(
            self, action, data, permission=None,
            expiration_sec=None, 
            skip_sign=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None, delay_sec=0
            ):
        ''' Implement the `push action` command without broadcasting. 
        '''
        self.push_action(
            action, data,
            permission, expiration_sec, 
            skip_sign, dont_broadcast=1, force_unique=force_unique,
            max_cpu_usage=max_cpu_usage, max_net_usage=max_net_usage,
            ref_block=ref_block, delay_sec=delay_sec)

    def table(
            self, table_name, scope="", 
            binary=False, 
            limit=10, key="", lower="", upper=""):
        '''Retrieve the contents of a database table

        Args:
            scope (str or .interface.Account): The scope within the account in 
                which the table is found.
            table (str): The name of the table as specified by the contract abi.
            binary (bool): Return the value as BINARY rather than using abi to 
                interpret as JSON. Default is *False*.
            limit (int): The maximum number of rows to return. Default is 10.
            lower (str): JSON representation of lower bound value of key, 
                defaults to first.
            upper (str): JSON representation of upper bound value value of key, 
                defaults to last.

        Returns:
            :class:`.cleos_set.SetTable` object
        '''            
        logger.INFO('''
        * Table *{}* for *{}*
        '''.format(table_name, scope))

        result = cleos_get.GetTable(
                    self, table_name, scope,
                    binary, 
                    limit, key, lower, upper,
                    is_verbose=False)

        try:
            account_map = manager.account_map()
            scope = account_map[str(scope)]
        except:
            pass

        logger.OUT(result.out_msg)

        return result

    def buy_ram(
            self, amount_kbytes, receiver=None,
            expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None):

        if manager.is_local_testnet():
            return

        if receiver is None:
            receiver = self

        buy_ram_kbytes = 1
        
        result = cleos_sys.BuyRam(
            self, receiver, amount_kbytes,
            buy_ram_kbytes,
            expiration_sec,
            skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=0
            )

        logger.INFO('''
            * Transfered RAM from {} to {} kbytes: {}
            '''.format(result.payer, result.receiver, result.amount))

    def delegate_bw(
        self, stake_net_quantity, stake_cpu_quantity,
        receiver=None,
        permission=None,
        transfer=False,
        expiration_sec=None, 
        skip_sign=0, dont_broadcast=0, force_unique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        is_verbose=1):

        if manager.is_local_testnet():
            return

        if receiver is None:
            receiver = self

        result = cleos_sys.DelegateBw(
            self, receiver,
            stake_net_quantity, stake_cpu_quantity,
            permission,
            transfer,
            expiration_sec,
            skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=0
            )

        logger.INFO('''
        * Delegated stake from {} to {} NET: {} CPU: {}
        '''.format(
            result.payer, result.receiver,
            result.stake_net_quantity, result.stake_cpu_quantity))

    def info(self):
        msg = manager.accout_names_2_object_names(
            "Account object name: {}\n{}".format(
            self.account_object_name,
            str(cleos.GetAccount(self.name, is_verbose=0))),
            True
        )
        print(msg)

    def __str__(self):
        return self.name
        

def create_master_account(
            account_object_name, account_name=None, 
            owner_key=None, active_key=None):
    '''Create master account object in caller's global namespace.

    Start a singleton :class:`.shell.wallet.Wallet` object if there is no one 
    in the global namespace already.

    If a local testnet is running, create an account object representing 
    the *eosio* account. Put the account into the wallet. Put the account
    object into the global namespace of the caller, and return.

    Otherwise, an outer testnet has to be defined with the function
    :func:`.core.setup.set_nodeos_address`.

    If the *account_name* argument is set, check the testnet for presence of the 
    account. If present, create a corresponding object and put the account 
    into the wallet, and put the account object into the global namespace of 
    the caller, and return. 
    
    Otherwise start a registration procedure:    
    
        - if the argument *account_name* is not set, make it random
        - print registration data, namely:
            - account name
            - owner public key
            - active public key
            - owner private key
            - active private key
        - wait for the user to register the master account
        - . . . . 
        - detect the named account on the remote testnet
        - put the account into the wallet
        - put the account object into the global namespace of the caller and \
            return

    Note: Name conflict:
        If a new account object, named as an existing one, is going to be added to 
        the wallet, an error is reported. Then an offer is given to edith the 
        mapping file in order to resolve the conflict. When the conflict is 
        resolved, the procedure finishes successfully.   

    Args:
        account_object_name (str): The name of the account object returned.
        account_name (str): The name of an valid EOSIO account. Must be set if 
            the testnode is not local.
        owner_key (str or .core.interface.Key): The owner public key. Must 
            be set if the testnode is not local.
        active_key (str or .core.interface.Key): The active public key. Must 
            be set if the testnode is not local.
    '''

    globals = inspect.stack()[1][0].f_globals
 
    if account_object_name: # account_object_name==None in register_testnet
        '''
        Check the conditions:
        * a *Wallet* object is defined.
        * the account object name is not in use, already.    
        ''' 
        is_wallet_defined(logger, globals)

        global wallet_singleton
        if wallet_singleton is None:
            return

        if account_object_name in globals:

            if not isinstance(globals[account_object_name], interface.Account):
                raise errors.Error('''
                The global variable {} type is not *Account*.
                '''.format(account_object_name))
                return

            logger.INFO('''
                ######## Account object *{}* restored from the blockchain.
                '''.format(account_object_name)) 
            return

            #wallet_singleton.is_name_taken(account_object_name, account_name)

    if isinstance(account_name, testnet.Testnet):
        owner_key = account_name.owner_key
        active_key = account_name.active_key
        account_name = account_name.account_name

    logger.INFO('''
        ######### Create a master account object *{}*.
        '''.format(account_object_name))                

    '''
    If the local testnet is running, create an account object representing the 
    *eosio* account. Put the account into the wallet. Put the account object into 
    the global namespace of the caller, and **return**.
    '''
    account_object = account.Eosio(account_object_name)

    if is_local_testnet_running(account_object):
        put_account_to_wallet_and_on_stack(
            account_object_name, account_object, logger)
        return

    '''
    Otherwise, an outer testnet has to be defined with 
    *setup.set_nodeos_address(<url>)*.
    '''

    if manager.is_local_testnet():
        if teos.is_local_node_process_running():
            raise errors.Error('''
    There is an local testnode process running, but its 'eosio` account is not like 
    expected.
            ''')

        raise errors.Error('''
    If the local testnet is not running, an outer testnet has to be defined with 
    `setup.set_nodeos_address(<url>)`: use 'setup.set_nodeos_address(<URL>)'
        ''')

    '''
    If the *account_name* argument is not set, it is randomized. Check the 
    testnet for presence of the account. If present, create the corresponding 
    object and see whether it is in the wallets. If so, put the account object into 
    the global namespace of the caller. and **return**. 
    '''
    first_while = True
    while True:
        account_object = account.GetAccount(
            account_object_name, account_name, owner_key, active_key)

        if first_while and account_name and owner_key and active_key \
                        and not account_object.exists:
            raise errors.Error('''
            There is no account named *{}* in the blockchain.
            '''.format(account_name))
            return
        first_while = False

        if account_object.exists:
            if account_object.has_keys: # it is your account
                logger.TRACE('''
                    * Checking whether the wallet has keys to the account *{}*
                    '''.format(account_object.name))

                logger.TRACE('''
                    * The account object is created.
                    ''')

                if account_object_name:
                    if Account.add_methods_and_finalize(
                        account_object_name, account_object):
                        logger.TRACE('''
                            * The account *{}* is in the wallet.
                            '''.format(account_object.name))
                        return
                else:
                    return account_object

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
            owner_key_new = cleos.CreateKey(is_verbose=False)
            active_key_new = cleos.CreateKey(is_verbose=False)

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
            owner_key = owner_key_new
            active_key = active_key_new


def create_account(
        account_object_name,
        creator, 
        account_name="",
        owner_key="", active_key="",
        stake_net=3, stake_cpu=3,
        permission=None,
        expiration_sec=None,
        skip_sign=0, dont_broadcast=0, force_unique=0,
        max_cpu_usage=0, max_net_usage=0,
        ref_block=None,
        delay_sec=0,        
        buy_ram_kbytes=8, buy_ram="",
        transfer=False,
        restore=False):
    '''Create master account object in caller's global namespace.
    
    Args:
        account_object_name (str): The name of the account object returned.
        creator (str or .core.interface.Account): The account creating the new 
            account
        account_name (str): The name of an valid EOSIO account. If not set, it 
            is random.
        owner_key (.core.interface.Key): The *owner* key pair. If not set, it
            is random.
        active_key (.core.interface.Key): The *active* key pair. If not set, 
            and the *owner_key* is set, it is substituted with the *owner_key*.
            Otherwise, it is random.
        stake_net (int): The amount of EOS delegated for net bandwidth.
        stake_cpu (int): The amount of EOS delegated for CPU bandwidth.
        buy_ram_kbytes (int): The amount of RAM bytes to purchase.
        transfer (bool): Transfer voting power and right to unstake EOS to 
            receiver.

    See definitions of the remaining parameters: :func:`.cleos.common_parameters`.
    '''

    global wallet_singleton
    globals = inspect.stack()[1][0].f_globals

    '''
    Check the conditions:
    * a *Wallet* object is defined;
    * the account object name is not in use, already.
    '''
    is_wallet_defined(logger)
    if wallet_singleton is None:
        return
    #wallet_singleton.is_name_taken(account_object_name, account_name)

    if account_object_name in globals:

        if not isinstance(globals[account_object_name], interface.Account):
            raise errors.Error('''
            The global variable *{}* type is not *Account*.
            '''.format(account_object_name))
            return

        logger.INFO('''
            ######## Account object *{}* restored from the blockchain.
            '''.format(account_object_name)) 
        return        

    logger.INFO('''
        ######### Create an account object *{}*.
        '''.format(account_object_name))

    '''
    Create an account object.
    '''
    account_object = None

    if restore:
        if creator:
            account_name = creator
        logger.INFO('''
                    ... for an existing blockchain account *{}* mapped as *{}*.
                    '''.format(account_name, account_object_name), 
                    translate=False)
        account_object = account.RestoreAccount(account_name)
        account_object.account_object_name = account_object_name
    else:
        if not account_name:
            account_name = cleos.account_name()
        if owner_key:
            if not active_key:
                active_key = owner_key
        else:
            owner_key = cleos.CreateKey(is_verbose=False)
            active_key = cleos.CreateKey(is_verbose=False)

        if stake_net and not manager.is_local_testnet():
            logger.INFO('''
                        ... delegating stake to a new blockchain account *{}* mapped as *{}*.
                        '''.format(account_name, account_object_name))

            try:
                account_object = SystemNewaccount(
                        creator, account_name, owner_key, active_key,
                        stake_net, stake_cpu,
                        permission,
                        buy_ram_kbytes, buy_ram,
                        transfer,
                        expiration_sec, 
                        skip_sign, dont_broadcast, force_unique,
                        max_cpu_usage, max_net_usage,
                        ref_block,
                        delay_sec
                        )
            except errors.LowRamError as e:
                logger.TRACE('''
                * RAM needed is {}.kByte, buying RAM {}.kByte.
                '''.format(
                    e.needs_kbyte,
                    e.deficiency_kbyte))

                buy_ram_kbytes = str(
                    e.deficiency_kbyte + 1)
                account_object = SystemNewaccount(
                        creator, account_name, owner_key, active_key,
                        stake_net, stake_cpu,
                        permission,
                        buy_ram_kbytes, buy_ram,
                        transfer,
                        expiration_sec, 
                        skip_sign, dont_broadcast, force_unique,
                        max_cpu_usage, max_net_usage,
                        ref_block,
                        delay_sec
                        )
        else:
            logger.INFO('''
                        ... for a new blockchain account *{}*.
                        '''.format(account_name))
            account_object = account.CreateAccount(
                    creator, account_name, 
                    owner_key, active_key,
                    permission,
                    expiration_sec, skip_sign, dont_broadcast, force_unique,
                    max_cpu_usage, max_net_usage,
                    ref_block,
                    delay_sec
                    )

        account_object.account_object_name = account_object_name
        account_object.owner_key = owner_key
        account_object.active_key = active_key

    logger.TRACE('''
        * The account object is created.
        ''')
    Account.add_methods_and_finalize(account_object_name, account_object)


def reboot():
    global wallet_singleton
    if wallet_singleton:
        wallet_singleton.delete_globals()
    wallet.Wallet.wallet = None
    try:
        del wallet_singleton
    except:
        pass
    wallet_singleton = None

    global wallet_globals
    wallet_globals = None


def is_local_testnet_running(account_eosio):
    try:
        account_ = cleos.GetAccount(
            account_eosio.name, is_info=False, is_verbose=0)
    except:
        return False

    try: # remote eosio may have the ["keys"] array empty.
        return account_eosio.owner_key.key_public == account_.owner_key
    except:
        False


def is_wallet_defined(logger, globals=None):
    global wallet_globals   
    if not wallet_globals is None:
        return
    
    global wallet_singleton
    wallet_singleton = wallet.Wallet.wallet

    if wallet_singleton is None:
        wallet.create_wallet(globals=globals)
        wallet_singleton = wallet.Wallet.wallet

        if wallet_singleton is None:
            raise errors.Error('''
                Cannot find any `Wallet` object.
                ''')

    wallet_globals = wallet.Wallet.globals


def put_account_to_wallet_and_on_stack(
        account_object_name, account_object, logger=None):
    if logger is None:
        logger = account_object

    global wallet_singleton
    global wallet_globals

    if account_object.owner_key:
        if wallet_singleton.keys_in_wallets(
                [account_object.owner_key.key_private,
                account_object.active_key.key_private]):
            wallet_singleton.map_account(account_object_name, account_object)
        else:
            if wallet_singleton.import_key(account_object):
                wallet_singleton.map_account(account_object_name, 
                account_object)
            else:
                logger.TRACE('''
                Wrong or missing keys for the account *{}* in the wallets.
                '''.format(account_object.name))
                return False

    # export the account object to the globals in the wallet module:
    global wallet_globals      
    wallet_globals[account_object_name] = account_object
    account_object.in_wallet_on_stack = True
    return True


def print_stats(
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
        json = cleos.GetAccount(account, is_info=False, is_verbose=0).json
        json["account_object_name"] = account.account_object_name
        jsons.append(json)

    header = ""
    for json in jsons:
        header = header + col % (json["account_object_name"])
    output = ".\n" + header + "\n"

    for param in params:
        for json in jsons:
            output = output + col % find(param, json)
        output = output + "  " + last_col % (param) + "\n" 

    logger.OUT(output, translate=False)
    