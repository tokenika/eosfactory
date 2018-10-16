import shutil

import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.config as config
import eosfactory.core.setup as setup
import eosfactory.core.teos as teos
if setup.node_api == "cleos":
    import eosfactory.core.cleos as cleos
elif setup.node_api == "eosjs":
    import eosfactory.core.eosjs as cleos


def project_from_template(
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

    logger.INFO('''
    ######### Create contract ``{}`` from template ``{}``.
    '''.format(name, template))

    contract_path_absolute = teos.template_create(
        name, template, user_workspace, remove_existing, visual_studio_code)

    return contract_path_absolute


class ContractBuilder():
    '''
    '''
    def __init__(
            self, contract_dir,
            verbosity=None,
            abi_file=None,
            wasm_file=None):

        self.contract_dir = config.contract_dir(contract_dir)
        
        if not self.contract_dir:
            raise errors.Error("""
                Cannot determine the contract directory. The path is 
                ``{}``.
                """.format(contract_dir))
            return

        self.abi_file = abi_file
        self.wasm_file = wasm_file

    def path(self):
        return self.contract_dir

    def build_wast(self):
        teos.WAST(self.contract_dir)

    def build_abi(self):
        teos.ABI(self.contract_dir)

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
        
        super().__init__(
            contract_dir, verbosity=verbosity,
            abi_file=abi_file, wasm_file=wasm_file)
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

    def deploy(
        self, permission=None, dont_broadcast=None, payer=None):
        if not self.is_built():
            raise errors.Error('''
            Contract needs to be built before deployment.
            ''')
            return
        if dont_broadcast is None:
            dont_broadcast = self.dont_broadcast
        try:
            result = cleos.SetContract(
                self.account, self.contract_dir, 
                self.wasm_file, self.abi_file, 
                permission, self.expiration_sec, 
                self.skip_signature, dont_broadcast, self.forceUnique,
                self.max_cpu_usage, self.max_net_usage,
                self.ref_block,
                is_verbose=False,
                json=True)

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
        
            result = cleos.SetContract(
                self.account, self.contract_dir, 
                self.wasm_file, self.abi_file, 
                permission, self.expiration_sec, 
                self.skip_signature, dont_broadcast, self.forceUnique,
                self.max_cpu_usage, self.max_net_usage,
                self.ref_block,
                is_verbose=False,
                json=True)

        logger.INFO('''
        * Contract {} is deployed. 
        '''.format(self.contract_dir))            
        
        self.contract = result

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
