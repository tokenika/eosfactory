""" 
This is a Python front-end for Tokenika 'Teos'. Tokenika Teos is an 
alternative for EOSIO 'cleos'.
"""

# import importlib
# import teos
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
    __review = False

    def review(self):
        self.__review = True
        self.__setup()
        with open(self.__setupFile, 'w') as outfile:
            json.dump(self.__setupJson, outfile)
        self.__review = False        
    
    def  __setup(self):
        self.EOSIO_SOURCE_DIR = self.setParam(
            "EOSIO_SOURCE_DIR", os.environ['EOSIO_SOURCE_DIR'])
        self.teos_exe = self.setParam(
            "TEOS executable", os.environ['LOGOS_DIR'] \
                                + "/teos/build/teos")
        self.http_server_address = self.setParam(
            "EOS node http address", os.environ['EOSIO_DAEMON_ADDRESS'])       

    def __init__(self):

        if os.path.isfile(self.__setupFile) \
                    and os.path.getsize(__setupFile__) > 0 :
            with open(self.__setupFile) as json_data:
                print("Reading setup from file:\n   {}" \
                        .format(self.__setupFile))
                self.__setupJson = json.load(json_data)
        
        self.__setup()
        with open(self.__setupFile, 'w') as outfile:
            json.dump(self.__setupJson, outfile)

    __setupJson = json.loads("{}")

    def setParam(self, label, value):
        if label in self.__setupJson:
            value = self.__setupJson[label]
        
        if label in self.__setupJson and not self.__review:
            return value
        else:
            while True:
                print("{} is \n   {}".format(label, value))
                newValue \
                    = input("Enter an empty line to confirm, or a value:\n")
                if not newValue:
                    self.__setupJson[label] = value
                    return value
                value = newValue

    def __str__(self):
        return pprint.pformat(self.__setupJson)

    def delete(self):
        """ Deletes the setup file.

        If there is no 'teos.json' file, upon importing the module, a new 
        setup is proposed and a new copy of the setup file is created. 
        """
        os.remove(self.__setupFile)


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

        self._out = process.stdout.decode("utf-8")
        json_resp = process.stderr.decode("utf-8")

        if _is_verbose and is_verbose:
            print(self._out)
     
        if re.match(r'^ERROR', self._out):
            self.error = True
            self._this = self._out
            print(textwrap.fill(self._this, 80))
            return 
        try:
            self._this = json.loads(json_resp)
        except:
            self._this = json_resp

    def __str__(self):
        return self._out
    
    def __repr__(self):
        return repr(self._this)


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
            account = account
        
        self._jarg["account_name"] = account
        _Command.__init__(self, "get", "account", is_verbose)
        if not self.error:
            self.name = self._this["account_name"]


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
            self._this["name"] = name
            self.password = self._this["password"]



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
    def __init__(self, wallet, key, is_verbose=True):
        try:
            name = wallet.name
        except:
            name = wallet

        try:
            key_private = key.private_key
        except:
            key_private = key

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
    def __init__(self, wallet, is_verbose=True):
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
    def __init__(self, name, is_verbose=True):
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
    def __init__(self, wallet, password="", is_verbose=True):
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
            self.head_block = self._this["head_block_num"]
            self.head_block_time = self._this["head_block_time"]
            self.last_irreversible_block_num \
                = self._this["last_irreversible_block_num"]


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
            self.block_num = self._this["block_num"]
            self.ref_block_prefix = self._this["ref_block_prefix"]
            self.timestamp = self._this["timestamp"]


class GetCode(_Command):
    def __init__(
        self, account_name, wast_file="", abi_file="", is_verbose=True
        ):
        self._jarg["account_name"] = account_name
        self._jarg["wast"] = wast_file        
        self._jarg["abi"] = abi_file
        _Command.__init__(self, "get", "code", is_verbose)
        if not self.error:
            self.code_hash = self._this["code_hash"]
            self.wast = self._this["wast"] 
            if "abi" in self._this:          
                self.abi = self._this["abi"]
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
            self.private_key = self._this["privateKey"]
            self.public_key = self._this["publicKey"]
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
        self._jarg["ownerKey"] = owner_key.public_key
        self._jarg["activeKey"] = active_key.public_key
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

        owner: An account object or the name of an account that 
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
            self, owner, contract_dir, 
            wast_file="", abi_file="", 
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True
            ):

        try:
            owner_name = owner.name
        except:
            owner_name = owner
               
        try:
            permission = permission.name
        except:
            permission = permission 

        self._jarg["account"] = owner_name
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
            self.owner_name = owner_name


class PushAction(_Command):
    def __init__(
            self, contract_name, action, data,
            permission="", expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            is_verbose=True        
        ):   
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
        if not self.error and not "head_block_num" in self._this:
            if(self._this["is_windows_ubuntu"] == "true"):
                subprocess.call(
                    ["cmd.exe", "/c", "start", "/MIN", "bash.exe", "-c", 
                    self._this["command_line"]])
            else:
                subprocess.call(
                    ["gnome-terminal", "--", self._this["command_line"]]) 

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
        self._this = daemon._this              


class DaemonClear(_Command):
    def __init__(self, is_verbose=True):
        daemon = _Daemon(1, is_verbose)
        self._this = daemon._this


class DaemonStop(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "daemon", "stop", is_verbose)


class DaemonDeleteWallets(_Command):
    def __init__(self, name="*", is_verbose=True):
        self._jarg["name"] = name
        _Command.__init__(self, "daemon", "delete_wallets", is_verbose)


class _Commands:
    _this = json.loads("{}")
    def __repr__(self):
        return repr(self._this)

    def __str__(self):
        return pprint.pformat(self._this) 


class Wallet(WalletCreate):
    def __init__(self, name="default"):
        super().__init__(name)
        self._this["keys"] = []

    def list(self):
        WalletList()

    def lock(self):
        WalletLock(self.name, is_verbose=False)

    def unlock(self):
        WalletUnlock(self.name, self._this["password"]
                    , is_verbose=False)

    def import_key(self, key_pair):
        WalletImport(self.name, key_pair.private_key
                    , is_verbose=False)
        self._this["keys"].append([key_pair.name, key_pair.private_key])
        
    def delete(self):
        DaemonDeleteWallets(self.name, is_verbose=False)

    def open(self):
        WalletOpen(self.name, is_verbose=False)

    def __str__(self):
        return pprint.pformat(self._this)


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
        self._this = json.loads("{}")
        self._this["privateKey"] = \
            "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self._this["publicKey"] = \
            "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
        self.private_key = self._this["privateKey"]
        self.public_key = self._this["publicKey"]
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
        
    def action(self, action, data):
        """ Implements the 'cloes push action' command. 

        """
        PushAction(
            self.owner_name, action, data,
            permission=self.owner_name+"@active", 
            expiration_sec=30, 
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0
            )


class Daemon(_Commands):
    """ A front-end to the EOSIO test node.
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
