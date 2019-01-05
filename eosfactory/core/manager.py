#!/usr/bin/python3
import sys
import os
import json
import re

import eosfactory.core. config as config
import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.interface as interface
import eosfactory.core.setup as setup
import eosfactory.core.teos as teos
import eosfactory.core.cleos as cleos
import eosfactory.core.cleos_get as cleos_get


def reboot():
    logger.INFO('''
    ######### Reboot EOSFactory session.
    ''')
    stop([])
    import eosfactory.shell.account as account
    account.reboot()


def clear_testnet_cache():
    ''' Remove wallet files associated with the current testnet.
    '''

    if not setup.file_prefix():
        return
    logger.TRACE('''
    Removing testnet cache for prefix `{}`
    '''.format(setup.file_prefix()))

    kill_keosd() # otherwise the manager may protects the wallet files
    dir = config.keosd_wallet_dir()
    files = os.listdir(dir)
    try:
        for file in files:
            if file.startswith(setup.file_prefix()):
                os.remove(os.path.join(dir, file))
    except Exception as e:
        raise errors.Error('''
        Cannot remove testnet cache. The error message is:
        {}
        '''.format(str(e)))
    logger.TRACE('''
    Testnet cache successfully removed.
    ''')


def accout_names_2_object_names(sentence, keys=False):
    if not setup.is_translating:
        return sentence
        
    exceptions = ["eosio"]
    map = account_map()
    for name in map:
        account_object_name = map[name]
        if name in exceptions:
            continue
        sentence = sentence.replace(name, account_object_name)
        
        if keys:
            account = cleos.GetAccount(
                        name, is_info=False, is_verbose=False)
            owner_key = account.owner()
            if owner_key:
                sentence = sentence.replace(
                    owner_key, account_object_name + "@owner")

            active_key = account.active()
            if active_key:
                sentence = sentence.replace(
                    active_key, account_object_name + "@active")        

    return sentence


def object_names_2_accout_names(sentence):
    map = account_map()
    for name in map:
        account_object_name = map[name]
        sentence = sentence.replace(account_object_name, name)

    return sentence


def stop_keosd():
    cleos.WalletStop(is_verbose=False)


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


def is_local_testnet():
    cleos.set_local_nodeos_address_if_none()
    return setup.is_local_address


def node_start(clear=False, nodeos_stdout=None):
    try:
        teos.node_start(clear, nodeos_stdout)
        teos.node_probe()
    except:
        try:
            teos.node_start(clear, nodeos_stdout)
            teos.node_probe()
        except:
            teos.on_nodeos_error(clear)


def reset(nodeos_stdout=None):
    ''' Start clean the EOSIO local node.
    '''
    if not cleos.set_local_nodeos_address_if_none():
        logger.INFO('''
        No local nodeos is set: {}
        '''.format(setup.nodeos_address()))

    import eosfactory.shell.account as account
    teos.keosd_start()
    account.reboot()
    clear_testnet_cache()
    node_start(clear=True, nodeos_stdout=nodeos_stdout)
    


def resume(nodeos_stdout=None):
    ''' Resume the EOSIO local node.
    ''' 
    if not cleos.set_local_nodeos_address_if_none():   
        logger.INFO('''
            Not local nodeos is set: {}
        '''.format(setup.nodeos_address()))

    node_start(nodeos_stdout=nodeos_stdout)
    


def stop():
    ''' Stops all running EOSIO nodes.
    '''
    teos.node_stop()


def status():
    '''
    Display EOS node status.
    '''

    logger.INFO('''
    ######### Node ``{}``, head block number ``{}``.
    '''.format(
        setup.nodeos_address(),
        cleos_get.GetInfo(is_verbose=0).head_block))


def info():
    '''
    Display EOS node info.
    '''
    logger.INFO(str(cleos_get.GetInfo(is_verbose=False)))


def is_head_block_num():
    '''
    Check if testnet is running.
    '''
    try: # if running, json is produced
        head_block_num = cleos_get.GetInfo(is_verbose=False).head_block
    except:
        head_block_num = -1
    return head_block_num > 0

def verify_testnet_production():
    result = is_head_block_num()
    domain = "LOCAL" if is_local_testnet() else "REMOTE"
    if not result:
        raise errors.Error('''
        {} testnet is not running or is not responding @ {}.
        '''.format(domain, setup.nodeos_address()))
    else:
        logger.INFO('''
        {} testnet is active @ {}.
        '''.format(domain, setup.nodeos_address()))
    return result


def account_map(logger=None):
    '''Return json account map

Attempt to open the account map file named ``setup.account_map``, located 
in the wallet directory ``config.keosd_wallet_dir()``, to return its json 
contents. If the file does not exist, return an empty json.

If the file is corrupted, offer editing the file with the ``nano`` linux 
editor. Return ``None`` if the the offer is rejected.
    '''
    wallet_dir_ = config.keosd_wallet_dir(raise_error=False)
    if not wallet_dir_:
        return {}
    
    path = os.path.join(wallet_dir_, setup.account_map)
    while True:
        try: # whether the setup map file exists:
            with open(path, "r") as input_file:
                return json.load(input_file)

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                return {}
            else:
                logger.OUT('''
            The account mapping file is misformed. The error message is:
            {}
            
            Do you want to edit the file?
            '''.format(str(e)))
                    
                answer = input("y/n <<< ")
                if answer == "y":
                    edit_account_map()
                    continue
                else:
                    raise errors.Error('''
        Use the function 'efman.edit_account_map(text_editor="nano")'
        or the corresponding method of any object of the 'eosfactory.wallet.Wallet` 
        class to edit the file.
                    ''')                    
                    return None


def save_account_map(map):
    save_map(map, setup.account_map)


def edit_account_map():
    edit_map(setup.account_map)


def save_map(map, file_name):
    map = json.dumps(map, indent=3, sort_keys=True)
    with open(os.path.join(config.keosd_wallet_dir(), file_name), "w") as out:
        out.write(map)            


def edit_map(file_name, text_editor="nano"):
    import subprocess
    subprocess.run([text_editor, os.path.join(
                                    config.keosd_wallet_dir(), file_name)])
    read_map(file_name, text_editor)


def read_map(file_name, text_editor="nano"):
    '''Return json account map

Attempt to open the account map file named ``setup.account_map``, located 
in the wallet directory ``config.keosd_wallet_dir()``, to return its json 
contents. If the file does not exist, return an empty json.

If the file is corrupted, offer editing the file with the ``nano`` linux 
editor. Return ``None`` if the the offer is rejected.
    '''
    wallet_dir_ = config.keosd_wallet_dir()
    path = os.path.join(wallet_dir_, file_name)
    while True:
        try: # whether the setup map file exists:
            with open(path, "r") as input_file:
                return json.load(input_file)

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                return {}
            else:
                raise errors.Error('''
            The json file 
            {}
            is misformed. The error message is:
            {}
            
            Do you want to edit the file?
            '''.format(str(path), str(e)), is_fatal=False, translate=False)
                    
                answer = input("y/n <<< ")
                if answer == "y":
                    import subprocess
                    subprocess.run([text_editor, path])
                    continue
                else:
                    raise errors.Error('''
                    Use the function 'manager.edit_account_map(text_editor="nano")' to edit the file.
                    ''', translate=False)                    
                    return None


def data_json(data):
    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, interface.Account):
                return str(o)
            else:
                json.JSONEncoder.default(self, o) 
    if not data:
        return data

    data_json = data
    if isinstance(data, dict) or isinstance(data, list):
        data_json = json.dumps(data, cls=Encoder)
    else:
        if isinstance(data, str):
            data_json = re.sub("\s+|\n+|\t+", " ", data)
            data_json = object_names_2_accout_names(data_json)
    return data_json