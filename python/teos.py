## @package teos

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

    """ Deletes the setup file.
    If there is no 'teos.json' file, new setup is proposed upon importing the
    module, and a new copy of the setup file is created. 
    """
    def delete(self):
        os.remove(self.__setupFile)


setup = Setup()


##############################################################################
# teos commands
##############################################################################

class _Command:
    global _is_verbose 
    global setup    
   
    _args = json.loads("{}")
    error = False      

    def __init__(self, first, second, is_verbose=True):
        V = ""
        if _is_verbose and is_verbose:
            V = "-V"       

        process = subprocess.run([setup.teos_exe, first, second, V,
            "--json", str(self._args).replace("'", '"'), "--both"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)  

        if _is_verbose and is_verbose:
            print(process.stdout.decode("utf-8"))
        
        working_resp = process.stderr.decode("utf-8")
        if re.match(r'^ERROR', working_resp):
            self.error = True
            print(textwrap.fill(process.stderr.decode("utf-8"), 80))
            return    
        self._this = json.loads(working_resp)

    def __str__(self):
        return pprint.pformat(self._this)
    
    def __repr__(self):
        return repr(self._this)


"""Fetch a blockchain account
"""
class GetAccount(_Command):
    def __init__(self, accountName, is_verbose=True):
        self._args["account_name"] = accountName
        _Command.__init__(self, "get", "account", is_verbose)
        if not self.error:
            self.account_name = self._this["account_name"]
            self.eos_balance = self._this["eos_balance"]
            self.staked_balance = self._this["staked_balance"]
            self.eos_balance = self._this["eos_balance"]
            self.unsteostaking_balance = self._this["unstaking_balance"]
            self.last_unstaking_time = self._this["last_unstaking_time"]


""" Create a new wallet locally.
"""
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

""" Get current blockchain information.
"""
class GetInfo(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "get", "info", is_verbose)
        if not self.error:    
            self.head_block = self._this["head_block_num"]
            self.head_block_time = self._this["head_block_time"]
            self.last_irreversible_block_num \
                = self._this["last_irreversible_block_num"]


""" Retrieve a full block from the blockchain.
"""
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
            self.abi = self._this["abi"]


""" Create a pair of cryptographic keys.
"""
class CreateKey(_Command):
    def __init__(self, keyPairName, is_verbose=True):
        self._args["name"] = keyPairName
        _Command.__init__(self, "create", "key", is_verbose)
        if not self.error:  
            self.private_key = self._this["privateKey"]
            self.public_key = self._this["publicKey"]
            self.name = keyPairName


class InitaKey(_Command):
    def __init__(self, is_verbose=True):
        self._this = json.loads("{}")
        self._this["privateKey"] = \
            "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self._this["publicKey"] = \
            "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
        self.private_key = self._this["privateKey"]
        self.public_key = self._this["publicKey"]
        self.account_name = "inita"
        self.name = "inita_account"        


class CreateAccount(_Command):
    def __init__(
            self, creator, account_name
            , owner_key, active_key
            , deposit_eos=1, skip=0, expirationSec=30, is_verbose=True
            ):
        self._args["creator"] = creator
        self._args["name"] = account_name
        self._args["ownerKey"] = owner_key.public_key
        self._args["activeKey"] = active_key.public_key
        self._args["deposit"] = deposit_eos
        self._args["skip"] = skip
        self._args["expiration"] = expirationSec
        _Command.__init__(self, "create", "account", is_verbose)
        if not self.error:
            self.name = account_name


class SetContract(_Command):
    def __init__(
            self, account_name
            , wast_file, abi_file
            , skip=0, expirationSec=30, is_verbose=True
            ):
        self._args["account"] = account_name
        self._args["wast"] = wast_file
        self._args["abi"] = abi_file
        self._args["skip"] = skip
        self._args["expiration"] = expirationSec
        _Command.__init__(self, "set", "contract", is_verbose)
        if not self.error:
            self.name = account_name      


""" Start test EOSIO Daemon.
"""
class DaemonStart(_Command):
    def __init__(self, is_verbose=True):
        self._args["resync-blockchain"] = 0
        _Command.__init__(self, "daemon", "start", is_verbose)


""" Start clean test EOSIO Daemon.
"""
class DaemonClear(_Command):
    def __init__(self, is_verbose=True):
        self._args["resync-blockchain"] = 1
        _Command.__init__(self, "daemon", "start", is_verbose)        


""" Stop test EOSIO Daemon.
"""
class DaemonStop(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "daemon", "stop", is_verbose)



""" Delete local wallets.
"""
class DaemonDeleteWallets(_Command):
    def __init__(self, name="", data_dir="", is_verbose=True):
        self._args["name"] = name
        self._args["data-dir"] = data_dir
        _Command.__init__(self, "daemon", "delete_wallets", is_verbose)


class _Commands:
    _this = json.loads("{}")
    def __repr__(self):
        return repr(self._this)

    def __str__(self):
        return pprint.pformat(self._this) 


class Wallet(_Commands):

    def __init__(self, name="default"):
        wallet = WalletCreate(name, is_verbose=False)
        wallet._this["keys"] = []
        self._this = wallet._this  

    def list(self):
        WalletList()

    def lock(self):
        WalletLock(self._this["name"], is_verbose=False)

    def unlock(self):
        WalletUnlock(self._this["name"], self._this["password"]
                    , is_verbose=False)

    def import_key(self, key_pair):
        WalletImport(self._this["name"], key_pair.private_key
                    , is_verbose=False)
        self._this["keys"].append([key_pair.name, key_pair.private_key])
        
    def delete(self):
        DaemonDeleteWallets(self._this["name"], is_verbose=False)

    def open(self):
        WalletOpen(self._this["name"], is_verbose=False)


class Account(_Commands):
    def __init__(
            self, creator, account_name, owner_key, active_key
            , deposit_eos=1, skip=0, expirationSec=30
            ):
        self.name = account_name
        create = CreateAccount(
            creator, self.name
            , owner_key, active_key, deposit_eos, skip, expirationSec
            , is_verbose=False
            )

        if not create.error:
            account = GetAccount(self.name, is_verbose=False)
            self._this = account._this

    def update(self):
        account = GetAccount(self.name, is_verbose=False)
        self._this = account._this

    def code(self, wast_file="", abi_file=""):
        code = GetCode(self.name, wast_file, abi_file, is_verbose=False)
        return code

    def set_contract(self, wast_file, abi_file, skip=0, expirationSec=30):
        set_contract = SetContract(
            self.name, wast_file, abi_file
            , skip, expirationSec, is_verbose=False
            )


class Daemon(_Commands):
    def start(self):
        DaemonStart()

    def clear(self):
        DaemonClear()

    def stop(self):
        DaemonStop()
    
    def delete_wallets(self):
       DaemonDeleteWallets()



