""" 
This is a Python front-end for Tokenika 'Teos'. Tokenika Teos is an 
alternative for EOSIO 'cleos'.
"""

# import teos

# import importlib
# importlib.reload(teos)

import os
import subprocess
import json
import pprint
import textwrap
import time
import glob
import re
import pathlib

__setupFile__ = "teos.json"
_is_verbose = True

## If set False, TEOS commands print error messages only. 
def set_verbose(is_verbose):
  global _is_verbose
  _is_verbose = is_verbose

def output__(msg):
  if _is_verbose:
    print("#  " + msg.replace("\n", "\n#  "))

class Setup:
    """ Interface to the json configuration file.

    The configuration file is expected in the same folder as the current file.
    """
    __setupFile = "teos.json"
    __TEOS_EXE = "TEOS_executable"
    __review = False              
    teos_exe = ""

    def __init__(self):
        path = "../teos/build/teos"
        
        if os.path.isfile(path):
            self.teos_exe = os.path.realpath(path)

        if not self.teos_exe:         
            try: 
                if os.path.isfile(self.__setupFile) \
                            and os.path.getsize(__setupFile__) > 0 :
                    with open(self.__setupFile) as json_data:
                        print("Reading setup from file:\n   {}" \
                                .format(os.path.realpath(self.__setupFile)))
                        setup_json = json.load(json_data)
                    path = setup_json[self.__TEOS_EXE]
                    if os.path.isfile(path):
                        self.teos_exe = os.path.realpath(path)
            except:
                pass
        
        if self.teos_exe:
            print("teos exe: " + self.teos_exe)
        else:
            print(
                'ERROR!'
                '\nDo not know the teos exe!'
                '\nIt is expected to be in the config file named\n'
                '{0}'
                '\nas {{"{1}":"absolute-path-to-the-teos.exe"}} '
                '\n'
                .format(                 
                    os.path.realpath(self.__setupFile),
                    self.__TEOS_EXE,
                    ))        

setup = Setup()


##############################################################################
# teos commands
##############################################################################

class _Command:
    """ A prototype for the command classes.

    Each command class represents a call to a Tokenika 'teos' instance that
    is launched to responce just this call. 
    """
    global _is_verbose 
    global setup    
   
    _jarg = json.loads("{}")
    _out = ""
    error = False 

    def __init__(self, first, second, is_verbose=True):
        cl = [setup.teos_exe, first, second,
            "--jarg", str(self._jarg).replace("'", '"'), "--both"]
        if _is_verbose and is_verbose:
            cl.append("-V")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=str(pathlib.Path(setup.teos_exe).parent)) 

        # Both, right and error output is passed with stdout:
        self._out = process.stdout.decode("utf-8")

        # With "--both", json output is passed with stderr: 
        json_resp = process.stderr.decode("utf-8")

        if _is_verbose and is_verbose:
            print(self._out)
     
        if re.match(r'^ERROR', self._out):
            self.error = True
            width = 80
            longest = max(self._out.split("\n"), key=len)
            if len(longest) < width:
                print(self._out)
            else:
                wrapper = textwrap.TextWrapper(width=width)
                print(wrapper.fill(self._out))

        try:
            self.json = json.loads(json_resp)
        except:
            self.json = json_resp

    def __str__(self):
        return self._out
    
    def __repr__(self):
        return repr(self.json)


class GetAccount(_Command):
    """
    Retrieve an account from the blockchain.

    Generic 'str' method returns a formatted output of the EOSIO node.
    Generic 'repr' method returns the json output of the EOSIO node.

    - **parameters**::

        account: The account object or the name of the account to retrieve.
        is_verbose: If 'False', do not print stdout, default is 'True'.

    - **attributes**::

        name: The name of the account.
        error: Whether any error ocurred.
        json: The json representation of the account, if 'error; is not set.
    """
    def __init__(self, account, is_verbose=True):
        try:
            account = account.name
        except:
            pass
        
        self._jarg["account_name"] = account
        _Command.__init__(self, "get", "account", is_verbose)
        if not self.error:
            self.name = self.json["account_name"]


class GetAccounts(_Command):
    def __init__(self, key, is_verbose=True):
        try:
            key = key.key_public
        except:
            pass

        self._jarg["public_key"] = key
        _Command.__init__(self, "get", "accounts", is_verbose)


class WalletCreate(_Command):
    """
    Create a new wallet locally.

    Generic 'str' method returns a formatted output of the EOSIO node.
    Generic 'repr' method returns the json output of the EOSIO node.

    - **parameters**::

        name: The name of the new wallet, defaults to 'default'.
        is_verbose: If 'False', do not print stdout, default is 'True'.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred.
        json: The json representation of the wallet, if 'error; is not set.
    """
    def __init__(self, name="default", is_verbose=True):
        self._jarg["name"] = name
        _Command.__init__(self, "wallet", "create", is_verbose)
        if not self.error:
            self.name = name
            self.json["name"] = name
            self.password = self.json["password"]


class WalletList(_Command):
    """
    List opened wallets, unlocked mark '*'. 

    - **parameters**::
        is_verbose: If 'False', do not print stdout, default is 'True'.
    """
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "wallet", "list", is_verbose)


class WalletImport(_Command):
    """
    Import private key into wallet.

    - **parameters**::
        wallet: A wallet object or the name of the wallet to import key into.
        key: A key object or a private key in WIF format to import.
        is_verbose: If 'False', do not print stdout, default is 'True'.
    """
    def __init__(self, key, wallet="default", is_verbose=True):
        try:
            key_private = key.key_private
        except:
            key_private = key 

        try:
            name = wallet.name
        except:
            name = wallet

        self._jarg["name"] = name
        self._jarg["key"] = key_private
        _Command.__init__(self, "wallet", "import", is_verbose)
        if not self.error:       
            self.key_private = key_private


class WalletKeys(_Command):
    """
    Print list of private keys from all unlocked wallets, in WIF format.

    - **parameters**::    
        is_verbose: If 'False', do not print stdout, default is 'True'.
    """
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "wallet", "keys", is_verbose)         


class WalletOpen(_Command):
    """
    Open an existing wallet.

    - **parameters**::
        wallet: A wallet object or the name of the wallet to import key into.
        is_verbose: If 'False', do not print stdout, default is 'True'.
    """
    def __init__(self, wallet="default", is_verbose=True):      
        try:
            name = wallet.name
        except:
            name = wallet
        
        self._jarg["name"] = name
        _Command.__init__(self, "wallet", "open", is_verbose)


class WalletLock(_Command):
    """
    Lock wallet.

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        is_verbose: If 'False', do not print stdout, default is 'True'.    
    """
    def __init__(self, wallet="default", is_verbose=True):
        try:
            name = wallet.name
        except:
            name = wallet
        
        self._jarg["name"] = name
        _Command.__init__(self, "wallet", "lock", is_verbose)


class WalletUnlock(_Command):
    """
    Unlock wallet.

    - **parameters**::

        wallet: A wallet object or the name of the wallet to import key into.
        password: If the wallet argument is not a wallet object, the password 
            returned by wallet create, else anything, defaults to "".
        is_verbose: If 'False', do not print stdout, default is 'True'.    
    """
    def __init__(self, wallet="default", password="", is_verbose=True):
        try:
            name = wallet.name
            password = wallet.password
        except:
            name = wallet

        self._jarg["name"] = name
        self._jarg["password"] = password
        _Command.__init__(self, "wallet", "unlock", is_verbose)


class GetInfo(_Command):
    """
    Get current blockchain information.

    - **parameters**::
        is_verbose: If 'False', do not print stdout, default is 'True'.
    """
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "get", "info", is_verbose)
        if not self.error:    
            self.head_block = self.json["head_block_num"]
            self.head_block_time = self.json["head_block_time"]
            self.last_irreversible_block_num \
                = self.json["last_irreversible_block_num"]


class GetBlock(_Command):
    """
    Retrieve a full block from the blockchain.

    - **parameters**::
        block_number: The number of the block to retrieve.
        block_id: The ID of the block to retrieve, if set, defaults to "".
        is_verbose: If 'False', do not print stdout, default is 'True'.    
    """
    def __init__(self, block_number, block_id="", is_verbose=True):
        if(block_id == ""):
            self._jarg["block_num_or_id"] = block_number
        else:
            self._jarg["block_num_or_id"] = block_id
        
        _Command.__init__(self, "get", "block", is_verbose)
        if not self.error:   
            self.block_num = self.json["block_num"]
            self.ref_block_prefix = self.json["ref_block_prefix"]
            self.timestamp = self.json["timestamp"]


class GetCode(_Command):
    def __init__(
        self, account_name, wast_file="", abi_file="", is_verbose=True
        ):
        self._jarg["account_name"] = account_name
        self._jarg["wast"] = wast_file        
        self._jarg["abi"] = abi_file
        _Command.__init__(self, "get", "code", is_verbose)
        if not self.error:
            self.code_hash = self.json["code_hash"]
            self.wast = self.json["wast"] 
            if "abi" in self.json:          
                self.abi = self.json["abi"]
            else:
                self.abi = ""


class GetTable(_Command):
    def __init__(
        self, contract, scope, table, 
        limit=10, key="", lower="", upper="",
        is_verbose=True
        ):
        self._jarg["code"] = contract
        self._jarg["scope"] = scope        
        self._jarg["table"] = table
        self._jarg["limit"] = limit
        self._jarg["table_key"] = key        
        self._jarg["lower_bound"] = lower
        self._jarg["upper_bound"] = upper
        _Command.__init__(self, "get", "table", is_verbose)


class CreateKey(_Command):
    def __init__(self, keyPairName, is_verbose=True):
        self._jarg["name"] = keyPairName
        _Command.__init__(self, "create", "key", is_verbose)
        if not self.error:  
            self.key_private = self.json["privateKey"]
            self.key_public = self.json["publicKey"]
            self.name = keyPairName       


class CreateAccount(_Command):
    """
    Creates a new account on the blockchain.

    - **parameters**::

        creator: an account object or the name of an account that 
            creates the account.
        name: The name of the new account.
        owner_key: The owner key object for the new account.
        active_key: The active key object for the new account.
        permission: An account object or the name of an account that 
            authorizes the creation.
        expiration_sec: The time in seconds before a transaction expires, 
            defaults to 30s.
        skip_signature:  If unlocked wallet keys should be used to sign 
            transaction, defaults to 0.
        dont_broadcast: Whether to broadcast transaction to the network (or 
            print to stdout), defaults to 0.
        forceUnique: Whether to force the transaction to be unique, what will 
            consume extra bandwidth and remove any protections against 
            accidently issuing the same transaction multiple times, defaults 
            to 0.
        max_cpu_usage: An upper limit on the cpu usage budget, in 
            instructions-retired, for the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: An upper limit on the net usage budget, in bytes, for 
            the transaction (defaults to 0 which means no limit).
    """

    def __init__(
            self, creator, name, owner_key, active_key,
            permission = "",
            expiration_sec=30, 
            skip_signature=0, 
            dont_broadcast=0,
            forceUnique=0,
            max_cpu_usage=0,
            max_net_usage=0,
            is_verbose=True
            ):
        try:
            creator = creator.name
        except:
            creator = creator

        try:
            permission = permission.name
        except:
            permission = permission
        
        self._jarg["creator"] = creator
        self._jarg["name"] = name
        self._jarg["ownerKey"] = owner_key.key_public
        self._jarg["activeKey"] = active_key.key_public
        self._jarg["permission"] = permission
        self._jarg["expiration"] = expiration_sec        
        self._jarg["skip-sign"] = skip_signature        
        self._jarg["dont-broadcast"] = dont_broadcast
        self._jarg["force-unique"] = forceUnique
        self._jarg["max-cpu-usage"] = max_cpu_usage
        self._jarg["max-net-usage"] = max_net_usage          
        _Command.__init__(self, "create", "account", is_verbose)
        if not self.error:
            self.name = name


class SetContract(_Command):
    """ Creates the contract on an account.
    
    Creates the contract on an account, and provides methodes that modify
    this contract.

    - **parameters**::

        account: An account object or the name of an account that 
            takes this contract.
        contract_dir: A directory containing the WAST and ABI files 
            of the contract.
        wast_file: The file containing the contract WAST, relative 
            to contract-dir, defaults to "".
        abi_file: The file containing the contract ABI, relative 
            to contract-dir, defaults to "".
        permission: An account object or the name of an account that 
            authorizes the creation.
        expiration_sec: The time in seconds before a transaction expires, 
            defaults to 30s.
        skip_signature:  If unlocked wallet keys should be used to sign 
            transaction, defaults to 0.
        dont_broadcast: Whether to broadcast transaction to the network (or 
            print to stdout), defaults to 0.
        forceUnique: Whether to force the transaction to be unique, what will 
            consume extra bandwidth and remove any protections against 
            accidently issuing the same transaction multiple times, defaults 
            to 0.
        max_cpu_usage: An upper limit on the cpu usage budget, in 
            instructions-retired, for the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: An upper limit on the net usage budget, in bytes, for 
            the transaction (defaults to 0 which means no limit).
    """    
    def __init__(
            self, account, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True
            ):

        try:
            account = account.name
        except:
            pass
               
        try:
            permission = permission.name
        except:
            pass 

        self._jarg["account"] = account
        self._jarg["contract-dir"] = contract_dir
        self._jarg["wast-file"] = wast_file
        self._jarg["abi-file"] = abi_file
        self._jarg["permission"] = permission
        self._jarg["expiration"] = expiration_sec
        self._jarg["skip-sign"] = skip_signature
        self._jarg["dont-broadcast"] = dont_broadcast
        self._jarg["force-unique"] = forceUnique
        self._jarg["max-cpu-usage"] = max_cpu_usage
        self._jarg["max-net-usage"] = max_net_usage        
        _Command.__init__(self, "set", "contract", is_verbose)
        if not self.error:
            self.account = account


class PushAction(_Command):
    def __init__(
            self, contract, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True        
        ):
        try:
            contract_name = contract.name
        except:
            contract_name = contract

        if permission:
            try:
                permission = permission.name
            except:
                pass

        self._jarg["contract"] = contract_name
        self._jarg["action"] = action
        self._jarg["data"] = data.replace('"', '\\"')
        self._jarg["permission"] = permission
        self._jarg["expiration"] = expiration_sec
        self._jarg["skip-sign"] = skip_signature
        self._jarg["dont-broadcast"] = dont_broadcast
        self._jarg["force-unique"] = forceUnique
        self._jarg["max-cpu-usage"] = max_cpu_usage
        self._jarg["max-net-usage"] = max_net_usage              
        _Command.__init__(self, "push", "action", is_verbose)
        if not self.error:
            self.name = contract_name


class _Daemon(_Command):
    def start(self, clear, is_verbose):
        super().__init__("daemon", "start", False)
        if not self.error and not "head_block_num" in self.json:
            if(self.json["is_windows_ubuntu"] == "true"):
                subprocess.call(
                    ["cmd.exe", "/c", "start", "/MIN", "bash.exe", "-c", 
                    self.json["command_line"]])
            else:
                subprocess.call(
                    ["gnome-terminal", "--", self.json["command_line"]]) 

            del self._jarg["DO_NOT_WAIT"]
            super().__init__("daemon", "start", is_verbose)      
            
    def __init__(self, clear, is_verbose=True):
        self._jarg["resync-blockchain"] = clear
        self._jarg["DO_NOT_WAIT"] = 1
        self._jarg["DO_NOT_LAUNCH"] = 1
        self.start(clear, is_verbose)
        # if self.error:
        #     self.start(1, is_verbose)
    
      
class DaemonStart(_Command):
    def __init__(self, is_verbose=True):
        daemon = _Daemon(0, is_verbose)
        self.json = daemon.json              


class DaemonClear(_Command):
    def __init__(self, is_verbose=True):
        daemon = _Daemon(1, is_verbose)
        self.json = daemon.json


class DaemonStop(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "daemon", "stop", is_verbose)


class _Commands:
    json = json.loads("{}")
    def __repr__(self):
        return repr(self.json)

    def __str__(self):
        return pprint.pformat(self.json) 


class Wallet(WalletCreate):

    def __init__(self, name="default"):
        super().__init__(name)
        self.json["keys"] = []

    def list(self):
        WalletList()

    def open(self):
        WalletOpen(self.name)

    def lock(self):
        WalletLock(self.name)

    def unlock(self):
        WalletUnlock(self.name, self.json["password"])

    def import_key(self, key_pair):
        wallet_import = WalletImport(
            key_pair, self.name, is_verbose=False)
        if not wallet_import.error:
            self.json["keys"].append([key_pair.name, key_pair.key_private])

    def keys(self):
        WalletKeys()

    def open(self):
        WalletOpen(self.name)

    def __str__(self):
        return pprint.pformat(self.json)


class Account(CreateAccount):
    """ A representation of an EOSIO account.
    
    Creates a new account on the blockchain, and provides methodes that modify
    this account.

    - **parameters**::

        creator: An account object or the name of an account that 
            creates the account.
        name: The name of the new account.
        owner_key: The owner key object for the new account.
        active_key: The active key object for the new account.
        permission: An account object or the name of an account that 
            authorizes the creation.
        expiration_sec: The time in seconds before a transaction expires, 
            defaults to 30s.
        skip_signature:  If unlocked wallet keys should be used to sign 
            transaction, defaults to 0.
        dont_broadcast: Whether to broadcast transaction to the network (or 
            print to stdout), defaults to 0.
        forceUnique: Whether to force the transaction to be unique, what will 
            consume extra bandwidth and remove any protections against 
            accidently issuing the same transaction multiple times, defaults 
            to 0.
        max_cpu_usage: An upper limit on the cpu usage budget, in 
            instructions-retired, for the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: An upper limit on the net usage budget, in bytes, for 
            the transaction (defaults to 0 which means no limit).
    """
    
    def code(self, wast_file="", abi_file=""):
        """ Retrieve the WAST and ABI files for the account.
        """
        code = GetCode(self.name, wast_file, abi_file, is_verbose=False)
        return code

    def set_contract(
            self, contract_dir, wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0):
        """ Creates or update the contract on the account

        """
        return SetContract(
            self.name, contract_dir, wast_file, abi_file,
            permission, expiration_sec, forceUnique,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=False 
            )

    def accounts(self, account=""):
        """ Prints accounts.

        """
        if account == "":
            account = self.name
        else:
            try:
                account = account.name
            except:
                account = account                        
        GetTable(account, self.name, "accounts")

    def __str__(self):
        return str(GetAccount(self.name, is_verbose=False)) 
    
    def __repr__(self):
        return repr(GetAccount(self.name, is_verbose=False))


class EosioAccount(Account):
    """ A representation of the 'eosio' testing account.

    EOSIO offers an account, called 'eosio', that can be used for tests. 
    Without any such, it is not possible to execute commands that need 
    authorizations.

    account_eosio = teos.EosioAccount()
    contract_eosio_bios = teos.SetContract(
        account_eosio, "eosio.bios", permission=account_eosio)
    #        transaction id: 7d5d9c7f56d46d6eab95f2dea6aaab667b5eb3d0877...
    """
    def __init__(self, is_verbose=True): 
        self.json = json.loads("{}")
        self.json["privateKey"] = \
            "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.json["publicKey"] = \
            "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
        self.key_private = self.json["privateKey"]
        self.key_public = self.json["publicKey"]
        self.name = "eosio"
        self._out = "#       transaction id: eosio"   


class Contract(SetContract):
    """ A representation of an EOSIO smart contract.
    
    Creates the contract on an account, and provides methodes that modify
    this contract.

    - **parameters**::

        owner: An account object or the name of an account that takes this 
            contract.
        contract_dir: A directory containing the WAST and ABI files of the 
            contract.
        wast_file: The file containing the contract WAST, relative to 
            contract-dir, defaults to "".
        abi_file: The file containing the contract ABI, relative to 
            contract-dir, defaults to "".
        permission: An account object or the name of an account that 
            authorizes the creation.
        expiration_sec: The time in seconds before a transaction expires, 
            defaults to 30s.
        skip_signature:  If unlocked wallet keys should be used to sign 
            transaction, defaults to 0.
        dont_broadcast: Whether to broadcast transaction to the network (or 
            print to stdout), defaults to 0.
        forceUnique: Whether to force the transaction to be unique, what will 
            consume extra bandwidth and remove any protections against 
            accidently issuing the same transaction multiple times, defaults 
            to 0.
        max_cpu_usage: An upper limit on the cpu usage budget, in 
            instructions-retired, for the execution of the transaction 
            (defaults to 0 which means no limit).
        max_net_usage: An upper limit on the net usage budget, in bytes, for 
            the transaction (defaults to 0 which means no limit).
    """

    def __str__(self):
        return self._out
        
    def action(
            self, action, data,
            permission="",
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0, is_verbose=False
        ):
        """ Implements the 'cloes push action' command. 

        """
        if not permission:
            permission=self.account
        else:
            try: # permission is an account:
                permission=permission.name
            except: # permission is the name of an account:
                permission=permission

        push_action = PushAction(
            self.account, action, data,
            permission, 
            expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage
            )
        if dont_broadcast and not push_action.error:
            pprint.pprint(push_action.json)

class Daemon(_Commands):
    """ A representation of the local EOSIO node.

    Any Daemon class object depends on external configuration parameters. They
    are organized on two levels: this module level and the level of a TEOS 
    executable that powers methodes of this python module.

    - **TEOS-python configuration**::

        TEOS_executable: Where is the TEOS executable. The parameter is set in 
            the configuration file of this script, which is "teos.json" in the 
            directory of this module, for example: 
            {"TEOS_executable":"absolute-path-to-the-teos.exe"}.

    Other relevant onfiguration parameters can be defined in a configuration 
    file of the TEOS executable, and/or as environment variables, and/or are 
    hard-codded (in the "config.cpp" file of the "teos library"). The first 
    definition in this sequence prevails.

    The configuration file of the TEOS executable is named "config.json". It
    exists in the TEOS executable directory.    

    - **TEOS configuration**::

        EOSIO_SOURCE_DIR: Where is the EOS repository. 
        EOSIO_DAEMON_ADDRESS: The local IP and port to listen for incoming http 
            connections, defaults to "127.0.0.1:8888".
        EOSIO_WALLET_ADDRESS: The local IP and port to listen for incoming http 
            connections to the local wallet, defaults to "127.0.0.1:8888".
        data-dir: Directory containing program runtime data (absolute path or
            relative to ${EOSIO_SOURCE_DIR}), defaults to 
            "${EOSIO_SOURCE_DIR}/build/daemon/data-dir".
        config-dir: Directory containing configuration files such as config.ini
            (absolute path or relative to ${EOSIO_SOURCE_DIR}),
            defaults to "${data-dir}"
        wallet-dir: The path of the wallet files (absolute path or relative 
            to ${data-dir}, defaults to "${data-dir}/wallet"
        genesis-json: File to read genesis state from, defaults to "genesis.json"
            (relative to ${config-dir}).
    """

    def clear(self):
        """ Starts the EOSIO test node cleared.

        Stops the node, if running, deletes all wallets, and starts test node
        resetted. 
        """
        _Daemon(1, True)

    def start(self):
        """ Starts the EOSIO test node, if not running.
        """
        _Daemon(0, True)

    def stop(self):
        """ Stops the EOSIO test node.
        """
        DaemonStop()

    def info(self):
        """ Prints the node info.
        """
        GetInfo(True)

    def __str__(self):
        return str(GetInfo(False))
