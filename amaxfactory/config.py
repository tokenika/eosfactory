import amaxfactory.core.checklist
import configparser
import os
conf = configparser.RawConfigParser()
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf.read(root_path + '/config/config.ini','utf8')

def readconf(section,option):
    return conf.get(section=section,option=option)

FACTORY_DIR = os.getenv("FACTORY_DIR")
if FACTORY_DIR == None:
    FACTORY_DIR = readconf("config","FACTORY_DIR")
print("FACTORY_DIR:"+FACTORY_DIR)

WALLET_DIR = os.getenv("WALLET_DIR")
if WALLET_DIR == None:
    WALLET_DIR = readconf("config","WALLET_DIR")
print("WALLET_DIR:"+WALLET_DIR)

AMAX_DIR = os.getenv("AMAX_DIR")
if AMAX_DIR == None:
    AMAX_DIR = readconf("config","AMAX_DIR")
print("AMAX_DIR:"+AMAX_DIR)

CONTRACT_WORKSPACE = readconf("config","CONTRACT_WORKSPACE")
if CONTRACT_WORKSPACE == None:
    CONTRACT_WORKSPACE = readconf("config","CONTRACT_WORKSPACE")
print("CONTRACT_WORKSPACE:"+CONTRACT_WORKSPACE)

CONTRACT_WASM_PATH = FACTORY_DIR + "/templates/wasm/"

if __name__ == '__main__':
    amaxfactory.core.checklist.main()
