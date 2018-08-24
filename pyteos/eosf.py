#!/usr/bin/python3

'''
Python front-end for `EOSIO cleos`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for `EOSIO cleos`.

.. moduleauthor:: Tokenika

'''

import sys
import os
import time
import json
import inspect
import types
import node
import shutil
import pprint
import enum

import setup
import front_end
import teos
import cleos
import cleos_system

def restart():
    cleos.restart()

def remove_files():
    if not setup.file_prefix():
        return
    kill_keosd()   # otherwise, the manager may protects the wallet files
    dir = wallet_dir()
    files = os.listdir(dir)
    try:
        for file in files:
            if file.startswith(setup.file_prefix()):
                os.remove(os.path.join(dir,file)) 
    except Exception as e:
        logger = front_end.Logger()
        logger.ERROR('''
        Cannot remove nodeos address files. The error message is
        {}
        '''.format(str(e)))   

def wallet_dir():
    return os.path.expandvars(teos.get_keosd_wallet_dir())

'''Return json account map
'''
def account_map(logger=None):

    wallet_dir_ = wallet_dir()
    while True:
        try: # whether the setup map file exists:
            with open(wallet_dir_ + setup.account_map, "r") as input_file:
                return json.load(input_file)

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                return {}
            else: 
                if not logger is None:
                    logger.ERROR('''
                The account mapping file is misformed. The error message is:
                {}
                
                Do you want to edit the file?
                '''.format(str(e)))
                        
                    answer = input("y/n <<< ")
                    if answer == "y":
                        edit_account_map()
                        continue
                    else:
                        logger.ERROR('''
            Use the function 'eosf.edit_account_map(text_editor="nano")'
            or the corresponding method of any object of the 'eosf_wallet.Wallet` 
            class to edit the file.
                        ''')                    
                        return None

def accout_names_2_object_names(sentence, keys=False):
    global _is_translating
    if not _is_translating:
        return sentence

    map = account_map()
    global wallet_globals
    for name in map:
        account_object_name = map[name]
        sentence = sentence.replace(name, account_object_name)
        if keys:
            account_object = wallet_globals[account_object_name]
            try:
                key = account_object.owner_key.key_public
                sentence = sentence.replace(key, account_object_name + "_owner")
            except:
                pass

            try:
                key = account_object.active_key.key_public
                sentence = \
                    sentence.replace(owner_key, account_object_name + "_active")
            except:
                pass

    return sentence

def object_names_2_accout_names(sentence, keys=False):
    map = account_map()
    global wallet_globals
    for name in map:
        account_object_name = map[name]
        sentence = sentence.replace(account_object_name, name)

    return sentence

def edit_account_map(text_editor="nano"):
    import subprocess
    subprocess.run([text_editor, wallet_dir() + setup.account_map])

_is_translating = True
def set_is_translating(status=True):
    global _is_translating
    _is_translating = status

def account_mapp_to_string(account_map):
    sort = sorted(account_map, key=account_map.get, reverse=False)
    retval = "{\n"
    next = False
    for k in sort:
        if next:
            retval = retval + ",\n"
        next = True
        retval = retval + '    "{}": "{}"'.format(k, account_map[k])
    retval = retval + "\n}\n"

    return retval

def clear_account_mapp(exclude=["account_master"]):
    wallet_dir_ = wallet_dir()
    account_map = {}

    try: # whether the setup map file exists:
        with open(wallet_dir_ + setup.account_map, "r") as input:
            account_map = json.load(input)
    except:
        pass
        
    clear_map = {}
    for account_name in account_map:
        if account_map[account_name] in exclude:
            clear_map[account_name] = account_map[account_name]
        
    with open(wallet_dir_ + setup.account_map, "w") as out:
        out.write(account_mapp_to_string(account_map))

def stop_keosd():
    cleos.WalletStop(is_verbose=-1)

def kill_keosd():
    os.system("pkill keosd")

class Transaction():
    def __init__(self, msg):
        self.transaction_id = ""
        msg_keyword = "executed transaction: "
        if msg_keyword in msg:
            beg = msg.find(msg_keyword, 0)
            end = msg.find(" ", beg + 1)
            self.transaction_id = msg[beg : end]
        else:
            try:
                self.transaction_id = msg.json["transaction_id"]
            except:
                pass

    def get_transaction(self):
        pass

def is_local_address():
    cleos.set_local_nodeos_address_if_none()
    return setup.is_local_address

def reset(verbosity=None):
    ''' Start clean the EOSIO local node.
    '''
    logger = front_end.Logger(verbosity) 
    if not cleos.set_local_nodeos_address_if_none():   
        logger.TRACE_INFO('''
            Not local nodeos is set: {}
        '''.format(setup.nodeos_address()))

    remove_files()

    node = teos.NodeStart(1, is_verbose=0)
    probe = teos.NodeProbe(is_verbose=-1)
    if not logger.ERROR(probe):
        logger.TRACE_INFO('''
        ######### Local test node is reset and is running.
        ''')
        logger.OUT(str(node))

def run(verbosity=None):
    ''' Restart the EOSIO local node.
    ''' 
    logger = front_end.Logger(verbosity)
    if not cleos.set_local_nodeos_address_if_none():   
        logger.TRACE_INFO('''
            Not local nodeos is set: {}
        '''.format(setup.nodeos_address()))

    node = teos.NodeStart(0, is_verbose=0)
    probe = teos.NodeProbe(is_verbose=-1)
    logger = front_end.Logger(verbosity)
    if not logger.ERROR(probe):
        logger.TRACE_INFO('''
        ######### Local test node is started and is running.
        ''')
        logger.OUT(str(node))

def stop(verbosity=None):
    ''' Stops all running EOSIO nodes and empties the local `nodeos` wallet 
    directory.

    Return: True if no running nodes and the local `nodeos` wallet directory 
    is empty, otherwise `False`.
    '''
    stop = teos.NodeStop(is_verbose=0)
    logger = front_end.Logger(verbosity)
    if not logger.ERROR(stop):
        logger.TRACE_INFO('''
        ######### Local test node is stopped.
        ''')

def status():
    '''
    Display EOS node status.
    '''
    get_info = cleos.GetInfo(is_verbose=-1)
    logger = front_end.Logger(None)
    get_info.err_msg = '''
    {}
    THE NODE {} IS NOT OPERATIVE.
    '''.format(get_info.err_msg, setup.nodeos_address())
    if not logger.ERROR(get_info):
        logger.TRACE_INFO('''
        ######### Node ``{}``, head block number ``{}``.
        '''.format(
            setup.nodeos_address(),
            get_info.json["head_block_num"]))

def info():
    '''
    Display EOS node info.
    '''
    get_info = cleos.GetInfo(is_verbose=-1)
    logger = front_end.Logger(None)
    logger.TRACE_INFO(str(get_info))

def node_is_operative():
    '''
    Check if testnet is running.
    '''
    get_info = cleos.GetInfo(is_verbose=-1)
    try: # if running, produces json
        head_block_num = int(get_info.json["head_block_num"])
    except:
        head_block_num = -1
    return head_block_num > 0

if __name__ == "__main__":
    template = ""
    if len(sys.argv) > 2:
        template = str(sys.argv[2])

    teos.TemplateCreate(str(sys.argv[1]), template, visual_studio_code=True)

