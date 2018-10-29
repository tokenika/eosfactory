#!/usr/bin/python3

'''
'''

import sys
import os
import json

import eosfactory.core.logger as logger
import eosfactory.core.errors as errors
import eosfactory.core.setup as setup
import eosfactory.core.teos as teos
if setup.node_api == "cleos":
    import eosfactory.core.cleos as cleos
elif setup.node_api == "eosjs":
    import eosfactory.core.eosjs as cleos


def reboot():
    logger.INFO('''
    ######### Reboot EOSFactory session.
    ''')
    stop([])
    import eosfactory.shell.account as account
    account.reboot()


def clear_testnet_cache(verbosity=None):
    ''' Remove wallet files associated with the current testnet.
    '''

    if not setup.file_prefix():
        return
    logger.TRACE('''
    Removing testnet cache for prefix `{}`
    '''.format(setup.file_prefix()))

    kill_keosd() # otherwise the manager may protects the wallet files
    dir = wallet_dir()
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


def wallet_dir():
    return os.path.expandvars(teos.get_keosd_wallet_dir())


def accout_names_2_object_names(sentence):
    if not setup.is_translating:
        return sentence
        
    exceptions = ["eosio"]
    map = account_map()
    for name in map:
        account_object_name = map[name]
        if name in exceptions:
            continue
        sentence = sentence.replace(name, account_object_name)

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


def reset(verbosity=None):
    ''' Start clean the EOSIO local node.
    '''
    if not cleos.set_local_nodeos_address_if_none():
        logger.INFO('''
        No local nodeos is set: {}
        '''.format(setup.nodeos_address()), verbosity)

    import eosfactory.shell.account as account
    account.reboot()
    clear_testnet_cache()
    teos.node_start(clear=True, verbosity=verbosity)


def resume(verbosity=None):
    ''' Resume the EOSIO local node.
    ''' 
    if not cleos.set_local_nodeos_address_if_none():   
        logger.INFO('''
            Not local nodeos is set: {}
        '''.format(setup.nodeos_address()), verbosity)

    teos.node_start(verbosity=verbosity)


def stop(verbosity=None):
    ''' Stops all running EOSIO nodes.
    '''
    teos.node_stop(verbosity)


def status():
    '''
    Display EOS node status.
    '''
    get_info = cleos.GetInfo(is_verbose=0)

    logger.INFO('''
    ######### Node ``{}``, head block number ``{}``.
    '''.format(
        setup.nodeos_address(),
        get_info.json["head_block_num"]))


def info():
    '''
    Display EOS node info.
    '''
    get_info = cleos.GetInfo(is_verbose=False)
    logger.INFO(str(get_info))


def is_head_block_num():
    '''
    Check if testnet is running.
    '''
    get_info = cleos.GetInfo(is_verbose=False)
    try: # if running, json is produced
        head_block_num = int(get_info.json["head_block_num"])
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
in the wallet directory ``wallet_dir()``, to return its json contents. If the 
file does not exist, return an empty json.

If the file is corrupted, offer editing the file with the ``nano`` linux 
editor. Return ``None`` if the the offer is rejected.
    '''
    wallet_dir_ = wallet_dir()
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
    with open(os.path.join(wallet_dir(), file_name), "w") as out:
        out.write(map)            


def edit_map(file_name, text_editor="nano"):
    import subprocess
    subprocess.run([text_editor, os.path.join(wallet_dir(), file_name)])
    read_map(file_name, text_editor)


def read_map(file_name, text_editor="nano"):
    '''Return json account map

Attempt to open the account map file named ``setup.account_map``, located 
in the wallet directory ``wallet_dir()``, to return its json contents. If the 
file does not exist, return an empty json.

If the file is corrupted, offer editing the file with the ``nano`` linux 
editor. Return ``None`` if the the offer is rejected.
    '''
    wallet_dir_ = wallet_dir()
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