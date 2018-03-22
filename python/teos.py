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
    _error = False      

    def __init__(self, first, second, options = []):
        V = ""
        if _is_verbose:
            V = "-V"         
        command_line = [
            setup.teos_exe, first, second, V,
            "--json", str(self._args).replace("'", '"'), "--both"]
        command_line.extend(options)

        process = subprocess.run(command_line,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)  

        if _is_verbose:
            print(process.stdout.decode("utf-8"))
        
        rcv = process.stderr.decode("utf-8")
        if re.match(r'^ERROR', rcv):
            self._error = True
            print(textwrap.fill(process.stderr.decode("utf-8"), 80))
            return    
        self._json = json.loads(rcv)


"""Fetch a blockchain account
"""
class GetAccount(_Command):
    def __init__(self, accountName):
        self._args["account_name"] = accountName
        _Command.__init__(self, "get", "account")
        if not self._error:
            self.account_name = self._json["account_name"]
            self.eos_balance = self._json["eos_balance"]
            self.staked_balance = self._json["staked_balance"]
            self.eos_balance = self._json["eos_balance"]
            self.unsteostaking_balance = self._json["unstaking_balance"]
            self.last_unstaking_time = self._json["last_unstaking_time"]


""" Create a new wallet locally.
"""
class WalletCreate(_Command):
    def __init__(self, walletName="default"):
        self._args["name"] = walletName
        _Command.__init__(self, "wallet", "create")
        if not self._error:       
            self.password = self._json["password"]


""" Get current blockchain information.
"""
class GetInfo(_Command):
    def __init__(self):
        _Command.__init__(self, "get", "info")
        if not self._error:    
            self.head_block = self._json["head_block_num"]
            self.head_block_time = self._json["head_block_time"]
            self.last_irreversible_block_num \
                = self._json["last_irreversible_block_num"]


""" Retrieve a full block from the blockchain.
"""
class GetBlock(_Command):
    def __init__(self, blockNumber):
        self._args["block_num_or_id"] = blockNumber
        _Command.__init__(self, "get", "block")
        if not self._error:   
            self.block_num = self._json["block_num"]
            self.ref_block_prefix = self._json["ref_block_prefix"]
            self.timestamp = self._json["timestamp"]


""" Create a pair of cryptographic keys.
"""
class CreateKey(_Command):
    def __init__(self, keyPairName):
        self._args["name"] = keyPairName
        _Command.__init__(self, "create", "key")
        if not self._error:  
            self.private_key = self._json["privateKey"]
            self.public_key = self._json["publicKey"]


""" Start test EOSIO Daemon.
"""
class DaemonStart(_Command):
    def __init__(self):
        _Command.__init__(self, "daemon", "start")


""" Start clean test EOSIO Daemon.
"""
class DaemonClear(_Command):
    def __init__(self):
        _Command.__init__(self, "daemon", "start", ["-c"])        


""" Stop test EOSIO Daemon.
"""
class DaemonStop(_Command):
    def __init__(self):
        _Command.__init__(self, "daemon", "stop")


""" Delete local wallets.
"""
class DaemonDeleteWallets(_Command):
    def __init__(self):
        _Command.__init__(self, "daemon", "delete_wallets")


