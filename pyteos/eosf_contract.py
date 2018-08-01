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

    def build_wast(self):
        if self.is_mutable:
            result = teos.WAST( self.contract_dir, "", is_verbose=0)
            if not self.ERROR(result):
                self.EOSF_TRACE("""
                * WAST file build and saved.
                """)
        else:
            self.ERROR("Cannot modify system contracts.")

    def build_abi(self):
        if self.is_mutable:
            result = teos.ABI(self.contract_dir, "", is_verbose=0)
            if not self.ERROR(result):
                self.EOSF_TRACE("""
                * ABI file build and saved.
                """)
                if "ABI exists in the source directory" in result.out_msg:
                   self.EOSF(result.out_msg)            
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
        self.EOSF("""
                * Contract directory is
                    {}
                """.format(config.json["contract-dir"]))

    def error_map(self, err_msg):
        if not err_msg:
            return None
        return eosf.Error(err_msg)

    def deploy(self, permission=""):
        result = cleos.SetContract(
            self.account, self.contract_dir, 
            self.wast_file, self.abi_file, 
            permission, self.expiration_sec, 
            self.skip_signature, self.dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.ref_block,
            is_verbose=-1
        )
        if not self.ERROR(result):
            code = cleos.GetCode(self.account.name, is_verbose=-1)
            if code.code_hash == \
            "0000000000000000000000000000000000000000000000000000000000000000":
                self.ERROR("""
Error in contract deployment:
Despite the ``set contract`` command returned without any error,
the code hash of the associated account is null:
{}
                """.format(code.code_hash))                

                return
            else:
                self.EOSF("""
                * Contract deployed. Code hash is checked not null.
                """)
            try:
                result.json = json.loads(result.err_msg)
                for action in result.json["actions"]:
                    action["data"] = "contract code data, deleted for readability ..................."
            except:
                pass

            self.contract = result
        else:
            self.contract = None

    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error

    def build_wast(self):
        return ContractBuilder(
            self.contract_dir, "", "",
            self.is_mutable, self.verbosity).build_wast()

    def build_abi(self):
        return ContractBuilder(
            self.contract_dir, "", "", 
            self.is_mutable, self.verbosity).build_abi()

    def build(self):
        return ContractBuilder(
            self.contract_dir, "", "", 
            self.is_mutable, self.verbosity).build()

    def push_action(
            self, action, data,
            permission="", expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=1,
            json=False,
            output=False
        ):
        if not permission:
            permission = self.account.name
        else:
            try: # permission is an account:
                permission = permission.name
            except: # permission is the name of an account:
                permission = permission

        if output:
            is_verbose = 0
            json = True
    
        result = cleos.PushAction(
            self.account.name, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            is_verbose=-1, json=True)
            
        if not self.ERROR(result):
            self.EOSF_TRACE("""
            * Push action:
                {}
            """.format(re.sub(' +',' ',data)))
            #self.OUT(result.out_msg)
            self.action = result
            try:
                self._console = result.console
                self.DEBUG(self._console)
            except:
                pass
        else:
            self.action = None

    def show_action(self, action, data, permission=""):
        """ Implements the `push action` command without broadcasting. 

        """
        return self.push_action(action, data, permission, dont_broadcast=1)

    def table(
            self, table_name, scope="",
            binary=False, 
            limit=10, key="", lower="", upper=""):
        """ Return a contract's table object.
        """
        self._table = cleos.GetTable(
                    self.account.name, table_name, scope,
                    binary=False, 
                    limit=10, key="", lower="", upper="", 
                    is_verbose=-1)

        return self._table

    def code(self, code="", abi="", wasm=False):
        return cleos.GetCode(
            self.account.name, code, abi, wasm, is_verbose=-1)

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
