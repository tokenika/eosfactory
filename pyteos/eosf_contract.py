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
import eosf_account

class ContractBuilder(eosf.Logger):
    """
    """
    def __init__(
            self, contract_dir,
            wast_file="", abi_file="",
            is_mutable = True,
            verbosity=None):

        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.is_mutable = is_mutable

        eosf.Logger.__init__(self, verbosity)

    def path(self):
        return self.contract_dir

    def build_wast(self, json=False):
        if self.is_mutable:
            result = teos.WAST( self.contract_dir, "", is_verbose=0)
            if not self.ERROR(result):
                self.EOSF_TRACE("""
                * WAST file build and saved.
                """)
                if json:
                    return result.json
        else:
            self.ERROR("Cannot modify system contracts.")

    def build_abi(self, json=False):
        if self.is_mutable:
            result = teos.ABI(self.contract_dir, "", is_verbose=0)
            if not self.ERROR(result):
                self.EOSF_TRACE("""
                * ABI file build and saved.
                """)
                if "ABI exists in the source directory" in result.out_msg:
                   self.EOSF(result.out_msg) 
                if json:
                    return result.json           
        else:
            self.ERROR("Cannot modify system contracts.")

    def build(self):
        self.build_abi()
        self.build_wast()

def contract_workspace_from_template(
        name, template="", user_workspace=None, remove_existing=False, 
        visual_studio_code=False, verbosity=None):
    """Given the template type and a name, create a contract workspace. 

    - **parameters**::

        name: The name of the new wallet, defaults to ``default``.
        template: The name of the template used.
        user_workspace: If set, the folder for the work-space. Defaults to the 
            value of the ``EOSIO_CONTRACT_WORKSPACE`` env. variable.
        remove_existing: If set, overwrite any existing workspace.
        visual_studio_code: If set, open the ``VSCode``, if available.
        verbosity: The logging configuration.
    """
    logger = eosf.Logger(verbosity)

    logger.EOSF_TRACE("""
    ######### Create template ``{}`` contract workspace named ``{}``.
    """.format(name, template))

    result = teos.TemplateCreate(
        name, template, user_workspace, remove_existing, visual_studio_code, is_verbose=0)
    

    if not logger.ERROR(result):
        logger.EOSF("""
        * The directory is
            {}
        """.format(result.contract_path_absolute))
        return result.contract_path_absolute
    else:
        return None

class Contract(eosf.Logger):

    def __init__(
            self, account, contract_dir,
            wast_file="", abi_file="",
            permission="",
            expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            verbosity=None):

        self.account = account
        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.expiration_sec = expiration_sec
        self.skip_signature = skip_signature
        self.dont_broadcast = dont_broadcast
        self.forceUnique = forceUnique
        self.max_cpu_usage = max_cpu_usage
        self.max_net_usage = max_net_usage
        self.ref_block = ref_block
        self.is_mutable = True
        self.verbosity = verbosity
        self.contract = None
        self._console = None
        self.error = self.account.error

        eosf.Logger.__init__(self, verbosity)
        self.EOSF_TRACE("""
                ######### Create a `Contract` object.
                """)
        config = teos.GetConfig(self.contract_dir, is_verbose=0)
        self.contract_dir = config.json["contract-dir"]
        self.contract_abi = None
        self.contract_wast = None
        try:
            self.contract_abi = config.json["contract-abi"]
            self.contract_wast = config.json["contract-wast"]
        except:
            pass

        self.EOSF("""
                * Contract directory is
                    {}
                """.format(self.contract_dir))

    def error_map(self, err_msg):
        if not err_msg:
            return None
        return eosf.Error(err_msg)

    def deploy(self, permission="", dont_broadcast=None):
        if dont_broadcast is None:
            dont_broadcast = self.dont_broadcast

        result = cleos.SetContract(
            self.account, self.contract_dir, 
            self.wast_file, self.abi_file, 
            permission, self.expiration_sec, 
            self.skip_signature, dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.ref_block,
            is_verbose=-1,
            json=True
        )
        if not self.ERROR(result):
            import pdb; pdb.set_trace()
            if not dont_broadcast:
                is_code = self.account.is_code()
                if not is_code:
                    self.ERROR("""
                Error in contract deployment:
                Despite the ``set contract`` command returned without any error,
                the code hash of the associated account is null
                    """)                
                    return
                else:
                    self.EOSF("""
                    * Contract deployed. Code hash is checked not null.
                    """)
            # print(eosf_account.translate(json.dumps(result.json, indent=3)))
            self.contract = result
        else:
            self.contract = None

    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error

    def build_wast(self, json=False):
        return ContractBuilder(
            self.contract_dir, "", "",
            self.is_mutable, self.verbosity).build_wast(json)

    def build_abi(self, json=False):
        return ContractBuilder(
            self.contract_dir, "", "", 
            self.is_mutable, self.verbosity).build_abi(json)

    def build(self):
        return ContractBuilder(
            self.contract_dir, "", "", 
            self.is_mutable, self.verbosity).build()

    def push_action(
            self, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="", json=False):
        self.account.push_action(action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block, json)

    def show_action(self, action, data, permission=""):
        """ Implements the `push action` command without broadcasting. 
        """
        return self.push_action(action, data, permission, dont_broadcast=1)

    def table(
            self, table_name, scope="",
            binary=False, 
            limit=10, key="", lower="", upper=""):
        """ Return contract's table object.
        """
        return self.account.table(
            table_name, scope,
            binary, 
            limit, key, lower, upper)

    def code(self, code="", abi="", wasm=False):
        return self.account.code(code, abi, wasm)

    def console(self):
        return self._console

    def path(self):
        """ Return contract directory path.
        """
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str(self.contract_dir)

    def delete(self):
        try:
            if self.contract:
                shutil.rmtree(str(self.contract.contract_path_absolute))
            else:
                shutil.rmtree(str(self.contract_dir))
            return True
        except:
            return False

    def __str__(self):
        if self.is_deployed():
            return str(self.contract)
        else:
            return str(self.account)
