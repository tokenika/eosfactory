import shutil
import os

import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.config as config
import eosfactory.core.teos as teos
import eosfactory.core.cleos as cleos
import eosfactory.core.cleos_set as cleos_set
import eosfactory.shell.account


class ContractBuilder():
    '''Build or delete a contract project.

    Args:
        contract_dir (str): If set, a hint to the root directory of a contract 
            project, otherwise the current working directory.
        c_cpp_properties_path (str): If set, the directory of a C/CPP VSCode 
            extension configuration file.
        abi_file (str): If set, the path to the ABI file, absolute, 
            or relative to *contract_dir*.
        wasm_file (str): If set, the path to the WASM file, absolute, 
            or relative to *contract_dir*.    
    '''
    def __init__(
            self, contract_dir=None,
            c_cpp_properties_path=None,
            abi_file=None,
            wasm_file=None):

        if not contract_dir:
            contract_dir = os.getcwd()
            
        if not c_cpp_properties_path:
            c_cpp_properties_path = os.path.join(
                            contract_dir, ".vscode", "c_cpp_properties.json")
            if not os.path.exists(c_cpp_properties_path):
                c_cpp_properties_path = None

        self.contract_dir = config.contract_dir(contract_dir)
        self.c_cpp_properties_path = c_cpp_properties_path
        
        if not self.contract_dir:
            raise errors.Error("""
                Cannot determine the contract directory. The path is 
                ``{}``.
                """.format(contract_dir))

        self.abi_file = abi_file
        self.wasm_file = wasm_file        


    def build(self, force=True):
        '''Make both, ABI and WASM files.
        '''
        if force or not self.is_built():
            teos.build(self.contract_dir, self.c_cpp_properties_path)

    def is_built(self):
        '''Check whether both the ABI and WASM files exist.
        '''
        return cleos.contract_is_built(
            self.contract_dir, self.wasm_file, self.abi_file)

    def path(self):
        ''' Return the path to the contract.
        '''
        return str(self.contract_dir)

    def delete(self):
        '''Delete the project.
        '''
        try:
            shutil.rmtree(str(self.contract_dir))
            return True
        except:
            return False


class Contract(ContractBuilder):
    '''Add a contract to the given account.

    Args:
        account (.shell.Account): The *Account* object to be fitted with a 
            contract.
        contract_dir (str): The path to a directory.
        wasm_file (str): The WASM file relative to the contract_dir.
        abi_file (str): The ABI file for the contract relative to the 
            contract-dir.

    See definitions of the remaining parameters: \
    :func:`.cleos.common_parameters`.
    '''
    def __init__(
            self, account, contract_dir=None,
            abi_file=None, wasm_file=None,
            permission=None,
            expiration_sec=None,
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            delay_sec=0):
        
        if not isinstance(account, eosfactory.shell.account.Account):
            raise errors.Error("""
            The account object has to be of the type 
            ``eosfactory.shell.account.Account``.
            """)

        super().__init__(
            contract_dir, abi_file=abi_file, wasm_file=wasm_file)
        self.account = account
        self.permission = permission
        self.expiration_sec = expiration_sec
        self.skip_sign = skip_sign
        self.dont_broadcast = dont_broadcast
        self.force_unique = force_unique
        self.max_cpu_usage = max_cpu_usage
        self.max_net_usage = max_net_usage
        self.ref_block = ref_block
        self.delay_sec = delay_sec
        self.contract = None
        self._console = None

    def clear(self):
        '''Remove contract on an account
        '''
        result = cleos_set.SetContract(
            self.account, self.contract_dir, 
            self.wasm_file, self.abi_file,
            True,
            json=False)
            
        self.contract = result

    def deploy(
        self, permission=None, dont_broadcast=None, payer=None):
        '''Deploy the contract.
        '''
        if not self.is_built():
            raise errors.Error('''
            Contract needs to be built before deployment.
            ''')

        if permission is None:
            permission = self.permission
        if dont_broadcast is None:
            dont_broadcast = self.dont_broadcast
        try:
            result = cleos_set.SetContract(
                self.account, self.contract_dir, 
                self.wasm_file, self.abi_file,
                False, 
                permission, self.expiration_sec, 
                self.skip_sign, dont_broadcast, self.force_unique,
                self.max_cpu_usage, self.max_net_usage,
                self.ref_block,
                self.delay_sec,
                is_verbose=False,
                json=False)

        except errors.LowRamError as e:
            logger.TRACE('''
            * RAM needed is {}.kByte, buying RAM {}.kByte.
            '''.format(
                e.needs_kbyte,
                e.deficiency_kbyte))

            buy_ram_kbytes = str(
                e.deficiency_kbyte + 1)
            if not payer:
                payer = self.account

            payer.buy_ram(buy_ram_kbytes, self.account)
        
            result = cleos_set.SetContract(
                self.account, self.contract_dir, 
                self.wasm_file, self.abi_file,
                False, 
                permission, self.expiration_sec, 
                self.skip_sign, dont_broadcast, self.force_unique,
                self.max_cpu_usage, self.max_net_usage,
                self.ref_block,
                self.delay_sec,
                is_verbose=False,
                json=False)

        logger.INFO('''
        * Contract {} 
            is deployed. 
        '''.format(self.contract_dir))            
        
        self.contract = result

    def push_action(
            self, action, data,
            permission=None, expiration_sec=None, 
            skip_sign=0, dont_broadcast=0, force_unique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None, json=False):
        '''Push a transaction with a single action.

        Call *EOSIO cleos* with the *push action* command. Store the result,
        which is an object of the class :class:`.cleos.PushAction`,  as
        the value of the *action* attribute.

        Args:
            action (str or json or filename): Definition of the action to 
                execute on the contract.
            data (str): The arguments to the contract.

        See definitions of the remaining parameters: \
        :func:`.cleos.common_parameters`.
        '''            
        self.account.push_action(action, data,
            permission, expiration_sec,
            skip_sign, dont_broadcast, force_unique,
            max_cpu_usage, max_net_usage,
            ref_block, json)

    def show_action(self, action, data, permission=None):
        ''' Implements the `push action` command without broadcasting. 
        '''
        self.account.show_action(action, data, permission)

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
        return self.account.table(
            table_name, scope,
            binary, 
            limit, key, lower, upper)

    def code(self, code=None, abi=None, wasm=False):
        '''Retrieve the code and ABI

        Args:
            code (str): If set, the name of the file to save the contract 
                WAST/WASM to.
            abi (str): If set, the name of the file to save the contract ABI to.
            wasm (bool): Save contract as wasm.
        '''        
        return self.account.code(code, abi, wasm)

    def console(self):
        return self._console

    def path(self):
        ''' Return the path to the contract.
        '''
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str(self.contract_dir)
            
    def __str__(self):
        if self.contract and not self.contract.err_msg:
            return str(self.contract)
        else:
            return str(self.account)
