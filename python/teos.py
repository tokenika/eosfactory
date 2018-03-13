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
import tempfile
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
            "EOS node http address", os.environ['HTTP_SERVER_ADDRESS'])

        self.daemon_name = "eosiod"
        self.daemon_exe = self.EOSIO_SOURCE_DIR \
                            + "/build/programs/eosiod/eosiod"
        self.genesis_json = self.EOSIO_SOURCE_DIR + "genesis.json"
        self.data_dir = self.EOSIO_SOURCE_DIR \
                            + "/build/programs/eosiod/data-dir"        

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
    __args = json.loads("{}")
    global _is_verbose 

    def __init__(self, first, second, is_verbose=True):
        self._error = False
        global setup
        if not setup.http_server_address:
            process = subprocess.run([setup.teos_exe, first, second
                , "--json", args.replace("'", '"'), "--both"]
                , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.run([
                setup.teos_exe, setup.http_server_address, first, second,
                "--json", str(self.__args).replace("'", '"'), "--both"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

        if _is_verbose and is_verbose:
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
        self.__args["account_name"] = accountName
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
        self.__args["name"] = walletName
        _Command.__init__(self, "wallet", "create")
        if not self._error:       
            self.password = self._json["password"]


""" Get current blockchain information.
"""
class GetInfo(_Command):
    def __init__(self, is_verbose=True):
        _Command.__init__(self, "get", "info", is_verbose=is_verbose)
        if not self._error:    
            self.head_block = self._json["head_block_num"]
            self.head_block_time = self._json["head_block_time"]
            self.last_irreversible_block_num \
                = self._json["last_irreversible_block_num"]


""" Retrieve a full block from the blockchain.
"""
class GetBlock(_Command):
    def __init__(self, blockNumber):
        self.__args["block_num_or_id"] = blockNumber
        _Command.__init__(self, "get", "block")
        if not self._error:   
            self.block_num = self._json["block_num"]
            self.ref_block_prefix = self._json["ref_block_prefix"]
            self.timestamp = self._json["timestamp"]


""" Create a new pair of cryptographic keys.
"""
class CreateKey(_Command):
    def __init__(self, keyPairName):
        self.__args["name"] = keyPairName
        _Command.__init__(self, "create", "key")
        if not self._error:  
            self.private_key = self._json["privateKey"]
            self.public_key = self._json["publicKey"]



""" Operates a test EOSIO daemon
"""
class EosDaemon:
    def __init__(self):
        global setup
        self.genesis_json = setup.genesis_json
        self.http_server_address = setup.http_server_address
        self.data_dir = setup.data_dir
        self.daemon_exe = setup.daemon_exe

    def pid(self):
        global setup
        pidof = subprocess.run(["pidof", setup.daemon_name] \
            , stdout=subprocess.PIPE)
        pid = str(pidof.stdout.decode("utf-8")).strip()
        return pid

    def kill(self, is_verbose=True):
        pid = self.pid()
        if not pid:
            if is_verbose:
                output__("Is EOSIO chain node running?")
            return
        kill = subprocess.run(["kill", pid], stdout=subprocess.PIPE)

        count = 10
        while True:
            time.sleep(0.5)
            pid = self.pid()
            if not pid or count:
                if not pid:
                    if is_verbose:
                        output__("EOSIO chain node has been killed.")
                return
            count -= 1
        eprint("Running EOSIO daemon process id is {}. "
            "Do not know why cannot kill it!".format(pid))

    def _start(self, clean=False):
        command_line = ["gnome-terminal"
            , "--"
            , self.daemon_exe
            , "--genesis-json", self.genesis_json
            , "--http-server-address", self.http_server_address
            , "--data-dir", self.data_dir]

        if clean:
            command_line.append("--resync-blockchain")
        subprocess.Popen(command_line)

        count = 10
        while True: 
            time.sleep(1)
            getInfo = GetInfo(is_verbose=False)
            if not getInfo._error or count < 0:
                if count < 0:
                    eprint("Cannot start any EOSIO daemon!")
                break
            count -= 1           

    def clean(self):
        self.kill(is_verbose=False)
        self._start(clean=True)         

    def start(self):
        if not self.pid():
            self._start()

    def delete_wallets(self):
        global setup
        for f in glob.glob(self.data_dir + "/*.wallet"):
            os.remove(f)


class BuildContract:
    def __init__(self, target_wast_file, 
            src_files=[
                "/mnt/hgfs/Workspaces/EOS/Logos/teos/teoslib/control/config.cpp",
                "/mnt/hgfs/Workspaces/EOS/Logos/teos/teoslib/control/xonfig.cpp"
            ], 
            include_dir=[]):
        workdir = tempfile.mkdtemp()
        build = workdir + "/build/"
        pathlib.Path(build)

        object_file_list = ""
        for file in src_files:
            object_file_list += build + pathlib.Path(file).resolve().stem + ".o "
        
        print(object_file_list)

        # "/mnt/hgfs/Workspaces/EOS/Logos/teos/teoslib/control/config.cpp", 
