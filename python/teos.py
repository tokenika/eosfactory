## @package teos

# import importlib
# importlib.reload(teos)

import os
import subprocess
import json
import re
import pprint
import textwrap
import time

setupFile__ = "teos.json"
isVerbose__ = True

if os.path.isfile(setupFile__) and os.path.getsize(setupFile__) > 0 :
  with open(setupFile__) as json_data:
    print("Reading setup from file:\n   {}".format(setupFile__))
    setupJson = json.load(json_data)
else:
  setupJson = json.loads("{}")
  with open(setupFile__, 'w') as outfile:
    json.dump(setupJson, outfile)

def setParam(label, value):
  if label in setupJson:
    return setupJson[label]
  else:
    while True:
      print("{} is \n   {}".format(label, value))
      newValue = input("Enter an empty line to confirm, or a value:\n")
      if newValue in ['', '\n', '\r\n']:
        setupJson[label] = value
        return value
      value = newValue

""" Deletes the setup file.
If there is no 'teos.json' file, new setup is proposed upon importing the
module, and a new copy of the setup file is created. 
"""
def deleteSetup():
  os.remove(setupFile__)

## Prints the setup file.
def printSetup():
  pprint.pprint(setupJson)

## If set False, teos commands print error messages only. 
def setVerbose(isVerbose):
  global isVerbose__
  isVerbose__ = isVerbose

def output__(msg):
  if isVerbose__:
    print("#  " + msg.replace("\n", "\n#  "))

teosExe = os.environ['LOGOS_DIR'] + "/teos/build/teos"
teosExe = setParam("TEOS executable", teosExe)
nodeAddress = ""
nodeAddress = setParam("EOS node http address", nodeAddress)
EOSIO_SOURCE_DIR = os.environ['EOSIO_SOURCE_DIR']
EOSIO_SOURCE_DIR = setParam("EOSIO_SOURCE_DIR", EOSIO_SOURCE_DIR)

with open(setupFile__, 'w') as outfile:
    json.dump(setupJson, outfile)

###############################################################################
# teos commands
###############################################################################

class Command__:
  def __init__(self, first, second, args):
    self.error = False
    if nodeAddress in ['', '\n', '\r\n']:
      completedProcess = subprocess.run([teosExe, first, second
        , "--json", args.replace("'", '"'), "--both"]
        , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      completedProcess = subprocess.run([teosExe, nodeAddress, first, second
        , "--json", args.replace("'", '"'), "--both"]
        , stdout=subprocess.PIPE, stderr=subprocess.PIPE)     

    if isVerbose__:
      print(completedProcess.stdout.decode("utf-8"))
    
    rcv = completedProcess.stderr.decode("utf-8")
    if re.match(r'^ERROR', rcv):
      self.error = True
      print(textwrap.fill(completedProcess.stderr.decode("utf-8"), 80))
      return    
    self.json = json.loads(rcv)

""" Create a new wallet locally.
"""
class WalletCreate:
  def __init__(self, walletName="default"):
    args = json.loads("{}")
    args["name"] = name
    command = Command__("wallet", "create", str(args))
    if(command.error):
      return
    
    self.json = command.json
    self.password = command.json["password"]

""" Get current blockchain information.
"""
class GetInfo:
  def __init__(self):
    command = Command__("get", "info", "{}")
    if(command.error):
      return
    
    self.json = command.json
    self.head_block = command.json["head_block_num"]
    self.head_block_time = command.json["head_block_time"]
    self.last_irreversible_block_num = command.json["last_irreversible_block_num"]

""" Retrieve a full block from the blockchain.
"""
class GetBlock:
  def __init__(self, blockNumber):
    args = json.loads("{}")
    args["block_num_or_id"] = blockNumber
    command = Command__("get", "block", str(args))
    if(command.error):
      return  
    
    self.json = command.json
    self.block_num = command.json["block_num"]
    self.ref_block_prefix = command.json["ref_block_prefix"]
    self.timestamp = command.json["timestamp"]

""" Create a new pair of cryptographic keys.
"""
class CreateKey:
  def __init__(self, keyPairName):
    args = json.loads("{}")
    args["name"] = keyPairName
    command = Command__("create", "key", str(args))
    if(command.error):
      return    
    
    self.json = command.json
    self.private_key = command.json["privateKey"]
    self.public_key = command.json["publicKey"]


""" Kill locally running EOSIO daemon.
"""
class KillChainNode:
  def getPid(self):
    pidof = subprocess.run(["pidof", "eosiod"]
      , stdout=subprocess.PIPE)
    pid = str(pidof.stdout.decode("utf-8")).strip()
    return pid

  def __init__(self, isVerbose=True):
    pid = self.getPid()
    if not pid:
      if isVerbose:
        output__("Is EOSIO chain node running?")
      return
    kill = subprocess.run(["kill", pid], stdout=subprocess.PIPE)

    count = 10
    while True:
      time.sleep(0.5)
      pid = self.getPid()
      if not pid or count:
        if not pid:
          if isVerbose:
            output__("EOSIO chain node has been killed.")
        return
      count -= 1

    eprint("Process id is {}, Do not know why cannot kill it!".format(pid))

""" Starts a test EOSIO daemon
"""
class StartChainNode:
  def __init__(self, clean = False):
    KillChainNode(False)
    commandLine = "{} --genesis-json {} --http-server-address {} --data-dir {}".format(
      EOSIO_SOURCE_DIR + "/build/programs/eosiod/eosiod", 
      EOSIO_SOURCE_DIR + "/genesis.json",
      nodeAddress,
      EOSIO_SOURCE_DIR + "/build/programs/eosiod/eosiod/data-dir"
      )
    if clean:
      commandLine += " --resync-blockchain"
    print(commandLine)
    # eosiod = subprocess.Popen('mvn clean install'
    #   , stdout=subprocess.PIPE, stderr=subprocess.PIPE)


