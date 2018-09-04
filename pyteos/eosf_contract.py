import shutil

import teos
import cleos
import eosf_ui

def workspace_from_template(
        name, template="", user_workspace=None, remove_existing=False, 
        visual_studio_code=False, verbosity=None):
    '''Given the template type and a name, create a contract workspace. 

    - **parameters**::

        name: The name of the new wallet, defaults to ``default``.
        template: The name of the template used.
        user_workspace: If set, the folder for the work-space. Defaults to the 
            value of the ``EOSIO_CONTRACT_WORKSPACE`` env. variable.
        remove_existing: If set, overwrite any existing workspace.
        visual_studio_code: If set, open the ``VSCode``, if available.
        verbosity: The logging configuration.
    '''
    logger = eosf_ui.Logger(verbosity)

    logger.INFO('''
    ######### Create contract ``{}`` from template ``{}``.
    '''.format(name, template))

    result = teos.TemplateCreate(
        name, template, user_workspace, remove_existing, visual_studio_code, is_verbose=0)

    if not logger.ERROR(result):
        logger.INFO('''
        * Contract directory is
            {}
        '''.format(result.contract_path_absolute))
        return result.contract_path_absolute
    else:
        return None


class ContractBuilder(eosf_ui.Logger):
    '''
    '''
    def __init__(
            self, contract_dir,
            verbosity=None,
            abi_file=None,
            wasm_file=None):
        super().__init__(verbosity)
        self.INFO('''
                ######### Create a ``Contract`` object.
                ''')
        config = teos.GetConfig(contract_dir, is_verbose=0)
        self.contract_dir = config.json["contract-dir"]
        
        if not self.contract_dir:
            self.ERROR("""
                Cannot determine the contract directory. The path is 
                ``{}``.
                """.format(contract_dir))
            return
        self.INFO('''
            * Contract directory is
                {}
            '''.format(self.contract_dir))

        self.abi_file = abi_file
        self.wasm_file = wasm_file

    def path(self):
        return self.contract_dir

    def build_wast(self, json=False):
        result = teos.WAST( 
            self.contract_dir, "", is_verbose=0, json=json)
        
        if not self.ERROR(result):
            self.INFO('''
            * WAST file build and saved.
            ''')
        if json:
            return result.json

    def build_abi(self, json=False):
        result = teos.ABI(self.contract_dir, "", is_verbose=0)
        if not self.ERROR(result):
            self.INFO('''
            * ABI file build and saved.
            ''')
            if "ABI exists in the source directory" in result.out_msg:
                self.TRACE(result.out_msg)
            if json:
                return result.json

    def build(self, force=True):
        if force or not self.is_built():
            self.build_abi()
            self.build_wast()

    def is_built(self):
        return cleos.contract_is_built(
            self.contract_dir, self.wasm_file, self.abi_file)

    def delete(self):
        try:
            shutil.rmtree(str(self.contract_dir))
            return True
        except:
            return False


class Contract(ContractBuilder):

    def __init__(
            self, account, contract_dir,
            abi_file=None, wasm_file=None,
            permission=None,
            expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None,
            verbosity=None):
        super().__init__(contract_dir, verbosity=verbosity, abi_file=abi_file, wasm_file=wasm_file)
        self.account = account
        self.expiration_sec = expiration_sec
        self.skip_signature = skip_signature
        self.dont_broadcast = dont_broadcast
        self.forceUnique = forceUnique
        self.max_cpu_usage = max_cpu_usage
        self.max_net_usage = max_net_usage
        self.ref_block = ref_block
        self.verbosity = verbosity
        self.contract = None
        self._console = None
        self.error = self.account.error

    def deploy(self, force=True, permission=None, dont_broadcast=None, payer=None):
        if not self.is_built():
            self.ERROR('''
            Contract needs to be built before deployment.
            ''')
            return
        if dont_broadcast is None:
            dont_broadcast = self.dont_broadcast
        result = cleos.SetContract(
            self.account, self.contract_dir, 
            self.wasm_file, self.abi_file, 
            permission, self.expiration_sec, 
            self.skip_signature, dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.ref_block,
            is_verbose=-1,
            json=True)

        if self.ERROR(result, is_silent=True, is_fatal=False):
            if isinstance(result.error_object, eosf_ui.ContractRunning) and not force:
                self.TRACE('''
                * Contract is already running this version of code.
                ''')
                return
                
            if isinstance(result.error_object, eosf_ui.LowRam):
                self.TRACE('''
                * RAM needed is {}.kByte, buying RAM {}.kByte.
                '''.format(
                    result.error_object.needs_kbyte,
                    result.error_object.deficiency_kbyte))

                buy_ram_kbytes = str(
                    result.error_object.deficiency_kbyte + 1)
                if not payer:
                    payer = self.account

                payer.buy_ram(buy_ram_kbytes, self.account)
            
                result = cleos.SetContract(
                    self.account, self.contract_dir, 
                    self.wasm_file, self.abi_file, 
                    permission, self.expiration_sec, 
                    self.skip_signature, dont_broadcast, self.forceUnique,
                    self.max_cpu_usage, self.max_net_usage,
                    self.ref_block,
                    is_verbose=-1,
                    json=True)

        if not self.ERROR(result):
            if not dont_broadcast:
                is_code = self.account.is_code()
                if not is_code:
                    self.ERROR('''
                    Error in contract deployment:
                    Despite the ``set contract`` command returning without any error,
                    the code hash of the associated account is null.
                    ''')
                    return
                else:
                    self.INFO('''
                    * The contract {} deployed. 
                    '''.format(self.contract_dir))
                    self.TRACE('''
                    * Code hash is cross-checked to be non-zero.
                    ''')
            self.contract = result
        else:
            self.contract = None

    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error

    def push_action(
            self, action, data,
            permission=None, expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block=None, json=False):
        self.account.push_action(action, data,
            permission, expiration_sec,
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block, json)

    def show_action(self, action, data, permission=None):
        ''' Implements the `push action` command without broadcasting. 
        '''
        self.account.show_action(self, action, data, permission)

    def table(
            self, table_name, scope="",
            binary=False, 
            limit=10, key="", lower="", upper=""):
        ''' Return contract's table object.
        '''
        return self.account.table(
            table_name, scope,
            binary, 
            limit, key, lower, upper)

    def code(self, code="", abi="", wasm=False):
        return self.account.code(code, abi, wasm)

    def console(self):
        return self._console

    def path(self):
        ''' Return contract directory path.
        '''
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str(self.contract_dir)

    def __str__(self):
        if self.is_deployed():
            return str(self.contract)
        else:
            return str(self.account)
