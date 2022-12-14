import json
import os
from time import sleep
from string import digits
from amaxfactory.beans.base import config

env = config.readconf("global","evn")
url = config.readconf(env,"url")

def runaction(body):

    body = f"amcli  -u {url} push action " + body
    print(body)
    res = os.popen(body).read()
    print(res)
    return res


def gettable(body):
    body = f"amcli  -u {url} get table " + body
    print(body)
    res = os.popen(body).read()
    print(res)
    return res


def newaccount(creator):
    res = os.popen("amcli create key --to-console").read()
    print(res)
    values = res.split(" ")
    privateKey = values[2].split("\n")[0]
    publicKey = values[4].split("\n")[0]
    
    table = str.maketrans('', '', digits)
    name = publicKey.translate(table)[0:12].lower()
    os.popen(f" amcli wallet import --private-key {privateKey}").read()

    body = f"amcli  -u {url} system newaccount {creator} {name} {publicKey} --stake-net '1.10 AMAX' --stake-cpu '1.10 AMAX' --buy-ram-kbytes 400 "
    print(body)
    res = os.popen(body).read()
    print(res)
    
    transfer = f'''amax.token transfer '["amax","{name}","100.00000000 AMAX",""]' -p amax'''
    runaction(transfer)
    
    return name
def newaccount(name,publickey):
 
    body = f"amcli  -u {url} system newaccount amax {name} {publickey} --stake-net '1.10 AMAX' --stake-cpu '1.10 AMAX' --buy-ram-kbytes 400 "
    print(body)
    res = os.popen(body).read()
    print(res)
    
    transfer = f'''amax.token transfer '["amax","{name}","100.00000000 AMAX",""]' -p amax'''
    runaction(transfer)
    transfer = f'''amax.mtoken transfer '["ad","{name}","10000.000000 MUSDT",""]' -p ad'''
    runaction(transfer)
    
    return name


def newContract(name):
    res = os.popen("amcli create key --to-console").read()
    print(res)
    values = res.split(" ")
    privateKey = values[2].split("\n")[0]
    publicKey = values[4].split("\n")[0]

    os.popen(f" amcli wallet import --private-key {privateKey}").read()

    body = f"amcli  -u {url} system newaccount amax {name} {publicKey} --stake-net '1.10 AMAX' --stake-cpu '1.10 AMAX' --buy-ram-kbytes 4000 "
    print(body)
    res = os.popen(body).read()
    print(res)
    return name

def setContract(path,contract_name,name):
    body = f"amcli  -u {url}  set contract {name} /opt/amax/contracts{path}/build/contracts/{contract_name} -p {name}"
    print(body)
    res = os.popen(body).read()
    print(res)

    code = f"amcli  -u {url}  set account permission {name} active --add-code "
    print(code)
    coderes = os.popen(code).read()
    print(coderes)

def convert(body):
    body = "amcli  -u {url} convert pack_action_data " + body
    print(body)
    res = os.popen(body).read()
    res = str(res)[0:-1]
    print(res)
    return res
