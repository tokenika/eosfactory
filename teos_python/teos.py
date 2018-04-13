""" @package teos
This is a Python front-end for the Tokenika 'Teos'. Tokenika Teos is an 
alternative for the EOSIO 'cleos'.
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

    def print(self):
        pprint.pprint(self.__setupJson)

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
   
    _args = json.loads("{}")
    _out = ""
    error = False 

    def __init__(self, first, second, is_verbose=True):
        cl = [setup.teos_exe, first, second,
            "--jarg", str(self._args).replace("'", '"'), "--both"]
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
    def __init__(self, accountName, is_verbose=True):
        self._args["account_name"] = accountName
        _Command.__init__(self, "get", "account", is_verbose)
        # if not self.error:
        #     self.account_name = self._this["account_name"]
        #     self.staked_balance = self._this["staked_balance"]
        #     self.eos_balance = self._this["eos_balance"]
        #     self.unsteostaking_balance = self._this["unstaking_balance"]
        #     self.last_unstaking_time = self._this["last_unstaking_time"]


class WalletCreate(_Command):
    def __init__(self, wallet_name="default", is_verbose=True):
        self._args["name"] = wallet_name
        _Command.__init__(self, "wallet", "create", is_verbose)
        if not self.error:
            self.name = wallet_name
            self._this["name"] = wallet_name
            self.password = self._this["password"]


class WalletList(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "wallet", "list", is_verbose)


class WalletImport(_Command):
    def __init__(self, wallet_name, key_private, is_verbose=True):
        self._args["name"] = wallet_name
        self._args["key"] = key_private
        _Command.__init__(self, "wallet", "import", is_verbose)
        if not self.error:       
            self.key_private = key_private


class WalletKeys(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "wallet", "keys", is_verbose)         


class WalletOpen(_Command):
    def __init__(self, wallet_name, is_verbose=True):
        self._args["name"] = wallet_name
        _Command.__init__(self, "wallet", "open", is_verbose)


class WalletLock(_Command):
    def __init__(self, wallet_name, is_verbose=True):
        self._args["name"] = wallet_name
        _Command.__init__(self, "wallet", "lock", is_verbose)


class WalletUnlock(_Command):
    def __init__(self, wallet_name, pswd, is_verbose=True):
        self._args["name"] = wallet_name
        self._args["password"] = pswd
        _Command.__init__(self, "wallet", "unlock", is_verbose)


class GetInfo(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "get", "info", is_verbose)
        if not self.error:    
            self.head_block = self._this["head_block_num"]
            self.head_block_time = self._this["head_block_time"]
            self.last_irreversible_block_num \
                = self._this["last_irreversible_block_num"]


class GetBlock(_Command):
    def __init__(self, block_number, is_verbose=True):
        self._args["block_num_or_id"] = block_number
        _Command.__init__(self, "get", "block", is_verbose)
        if not self.error:   
            self.block_num = self._this["block_num"]
            self.ref_block_prefix = self._this["ref_block_prefix"]
            self.timestamp = self._this["timestamp"]


class GetCode(_Command):
    def __init__(
        self, account_name, wast_file="", abi_file="", is_verbose=True
        ):
        self._args["account_name"] = account_name
        self._args["wast"] = wast_file        
        self._args["abi"] = abi_file
        _Command.__init__(self, "get", "code", is_verbose)
        if not self.error:
            self.code_hash = self._this["code_hash"]
            self.wast = self._this["wast"] 
            if "abi" in self._this:          
                self.abi = self._this["abi"]


class GetTable(_Command):
    def __init__(
        self, contract, scope, table, 
        limit=10, key="", lower="", upper="",
        is_verbose=True
        ):
        self._args["code"] = contract
        self._args["scope"] = scope        
        self._args["table"] = table
        self._args["limit"] = limit
        self._args["table_key"] = key        
        self._args["lower_bound"] = lower
        self._args["upper_bound"] = upper
        _Command.__init__(self, "get", "table", is_verbose)


class CreateKey(_Command):
    def __init__(self, keyPairName, is_verbose=True):
        self._args["name"] = keyPairName
        _Command.__init__(self, "create", "key", is_verbose)
        if not self.error:  
            self.private_key = self._this["privateKey"]
            self.public_key = self._this["publicKey"]
            self.name = keyPairName       


class CreateAccount(_Command):
    def __init__(
            self, creator, account_name, owner_key, active_key,
            permission = "",
            expirationSec=30, 
            skipSignature=0, 
            dontBroadcast=0,
            forceUnique=0,
            is_verbose=True
            ):
        try:
            creator = creator.name
        except:
            creator = creator
        
        self._args["creator"] = creator
        self._args["name"] = account_name
        self._args["ownerKey"] = owner_key.public_key
        self._args["activeKey"] = active_key.public_key
        self._args["permission"] = permission
        self._args["expiration"] = expirationSec        
        self._args["skip-sign"] = skipSignature        
        self._args["dont-broadcast"] = dontBroadcast
        self._args["force-unique"] = forceUnique
        _Command.__init__(self, "create", "account", is_verbose)
        if not self.error:
            self.name = account_name


class SetContract(_Command):
    def __init__(
            self, owner_name, contractDir, 
            wast_file="", abi_file="", 
            permission="", expirationSec=30, 
            skipSignature=0, dontBroadcast=0, forceUnique=0,
            maxCpuUsage=0, maxNetUsage=0,
            is_verbose=True
            ):
        try:
            permission = permission.name
        except:
            permission = permission 

        self._args["account"] = owner_name
        self._args["contract-dir"] = contractDir
        self._args["wast-file"] = wast_file
        self._args["abi-file"] = abi_file
        self._args["permission"] = permission
        self._args["expiration"] = expirationSec
        self._args["skip-sign"] = skipSignature
        self._args["dont-broadcast"] = dontBroadcast
        self._args["force-unique"] = forceUnique
        self._args["max-cpu-usage"] = maxCpuUsage
        self._args["max-net-usage"] = maxNetUsage        
        _Command.__init__(self, "set", "contract", is_verbose)
        if not self.error:
            self.owner_name = owner_name


class PushAction(_Command):
    def __init__(
            self, contract_name, action, data,
            permission="", expirationSec=30, 
            skipSignature=0, dontBroadcast=0, forceUnique=0,
            maxCpuUsage=0, maxNetUsage=0,
            is_verbose=True        
        ):   
        self._args["contract"] = contract_name
        self._args["action"] = action
        self._args["data"] = data.replace('"', '\\"')
        self._args["permission"] = permission
        self._args["expiration"] = expirationSec
        self._args["skip-sign"] = skipSignature
        self._args["dont-broadcast"] = dontBroadcast
        self._args["force-unique"] = forceUnique
        self._args["max-cpu-usage"] = maxCpuUsage
        self._args["max-net-usage"] = maxNetUsage              
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

            del self._args["DO_NOT_WAIT"]
            super().__init__("daemon", "start", is_verbose)      
            
    def __init__(self, clear, is_verbose=True):
        self._args["resync-blockchain"] = clear
        self._args["DO_NOT_WAIT"] = 1
        self._args["DO_NOT_LAUNCH"] = 1
        self.start(clear, is_verbose)
        if self.error:
            self.start(1, is_verbose)
    
      
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
        self._args["name"] = name
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
    def update(self):
        account = GetAccount(self.name, is_verbose=False)
        self._this = account._this

    def code(self, wast_file="", abi_file=""):
        code = GetCode(self.name, wast_file, abi_file, is_verbose=False)
        return code

    def set_contract(
            self, contractDir, wast_file="", abi_file="", 
            permission="", expirationSec=30, 
            skipSignature=0, dontBroadcast=0, forceUnique=0,
            maxCpuUsage=0, maxNetUsage=0):
        return SetContract(
            self.name, contractDir, wast_file, abi_file,
            permission, expirationSec, forceUnique,
            maxCpuUsage=0, maxNetUsage=0,
            is_verbose=False 
            )

    def accounts(self, account=""):
        if account == "":
            account = self.name
        else:
            try:
                account = account.name
            except:
                account = account                        
        GetTable(account, self.name, "accounts") 


class EosioAccount(Account):
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
    def __init__(
            self, owner, contractDir, 
            wast_file="", abi_file="", 
            permission="", expirationSec=30, 
            skipSignature=0, dontBroadcast=0, forceUnique=0,
            maxCpuUsage=0, maxNetUsage=0,
            is_verbose=True):
        try:
            self.owner_name = owner.name
        except:
            self.owner_name = owner
   
        super().__init__(
            self.owner_name, contractDir, 
            wast_file, abi_file,
            permission, expirationSec, 
            skipSignature, dontBroadcast, forceUnique,
            maxCpuUsage, maxNetUsage,
            is_verbose)

    def __str__(self):
        return self._out
        
    def action(self, action, data):
        PushAction(
            self.owner_name, action, data,
            permission=self.owner_name+"@active", 
            expirationSec=30, 
            skipSignature=0, dontBroadcast=0, forceUnique=0,
            maxCpuUsage=0, maxNetUsage=0
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
