#!/usr/bin/python3

"""
Python front-end for `EOSIO cleos`.

.. module:: pyteos
    :platform: Unix, Windows
    :synopsis: Python front-end for `EOSIO cleos`.

.. moduleauthor:: Tokenika

"""

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
from termcolor import cprint, colored

import setup
import teos
import cleos
import cleos_system

def restart():
    cleos.restart()

class AccountNotExist:
    msg_template = """
Account ``{}`` does not exist in the blockchain. It may be created.
"""
    def __init__(self, msg):
        self.msg = cleos.heredoc(msg)

class WalletExists:
    msg_template = """
Account ``{}`` does not exist in the blockchain. It may be created.
"""
    def __init__(self, msg):
        self.msg = cleos.heredoc(msg)

class WalletNotExist:
    msg_template = """
Wallet ``{}`` does not exist.
"""
    def __init__(self, msg):
        self.msg = cleos.heredoc(msg)

class InvalidPassword:
    msg_template = """
Invalid password for wallet {}.
"""
    def __init__(self, msg):
        self.msg = cleos.heredoc(msg)

class LowRam:
    msg_template = """
Ram needed is {}kB, deficiency is {}kB.
"""
    def __init__(self, needs, deficiency):
        self.needs = needs
        self.deficiency = deficiency
        self.msg = cleos.heredoc(msg_template.format(needs, deficiency))    

class Error:
    def __init__(self, msg):
        self.msg = cleos.heredoc(msg)

class Verbosity(enum.Enum):
    COMMENT = ['green', None, []]
    TRACE = ['blue', None, ['bold']]
    EOSF = ['blue', None, []]
    ERROR = ['red', None, []]
    ERROR_TESTING = ['magenta', None, []]
    OUT = ['']
    OUT_INFO = ['magenta', 'on_green', []]
    DEBUG = ['yellow', None, []]

_is_throw_error = False
def set_throw_error(status=False):
    global _is_throw_error
    _is_throw_error = status

_is_testing_error = False
def set_is_testing_errors(status=True):
    """Changes the color of the ``ERROR`` logger printout.

    Makes it less alarming.
    """
    global _is_testing_error
    _is_testing_error = status

class Logger():
    verbosity = [Verbosity.EOSF, Verbosity.OUT, Verbosity.DEBUG]

    def __init__(self, verbosity=None):
        if verbosity is None:
            self._verbosity = Logger.verbosity
        else:
            self._verbosity = verbosity

        self.cleos_object = None
        self.eosf_buffer = ""
        self.out_buffer = ""
        self.out_info_buffer = ""
        self.error_buffer = ""
        self.debug_buffer = ""

    def COMMENT(self, msg):
        frame = inspect.stack()[1][0]
        test_name = inspect.getframeinfo(frame).function
        color = Verbosity.COMMENT.value
        cprint(
            "\n###  " + test_name + ":\n" + cleos.heredoc(msg) + "\n",
            color[0], color[1], attrs=color[2])

    def SCENARIO(self, msg):
        self.COMMENT(msg)

    def EOSF(self, msg, do=False):
        msg = cleos.heredoc(msg)
        self.eosf_buffer = msg
        if msg and (Verbosity.EOSF in self._verbosity or do):
            color = Verbosity.EOSF.value
            cprint(msg, color[0], color[1], attrs=color[2])

    def TRACE(self, msg, do=False):
        if msg and (Verbosity.TRACE in self._verbosity or do):
            color = Verbosity.TRACE.value
            cprint(cleos.heredoc(msg), color[0], color[1], attrs=color[2])

    def EOSF_TRACE(self, msg, do=False):
        if msg and Verbosity.EOSF in self._verbosity:
            self.EOSF(msg, do)
        else:
            self.TRACE(msg, do)

    def OUT_INFO(self, msg, do=False):
        msg = cleos.heredoc(msg)
        self.out_info_buffer = msg

        error = False
        try:
            error = msg.error
        except:
            pass

        try:
            msg = err_msg.err_msg
        except:
            pass

        if msg and (Verbosity.OUT_INFO in self._verbosity or do):
            color = Verbosity.OUT_INFO.value
            cprint(msg, color[0], color[1], attrs=color[2])            

    def OUT(self, msg, do=False):
        msg = cleos.heredoc(msg)
        self.out_buffer = msg

        if msg and (Verbosity.OUT in self._verbosity or do):
            print(msg + "\n")

        self.OUT_INFO(msg, do)

    def DEBUG(self, msg, do=False):
        msg = cleos.heredoc(msg)
        self.debug_buffer = msg

        if msg and (Verbosity.DEBUG in self._verbosity or do):
            color = Verbosity.DEBUG.value
            cprint(msg, color[0], color[1], attrs=color[2])

    def error_map(self, err_msg):
        if "main.cpp:2888" in err_msg:
            return AccountNotExist(
                AccountNotExist.msg_template.format(self.name))

        if "Error 3080001: Account using more than allotted RAM" in err_msg:
            needs = int(re.search('needs\s(.*)\sbytes\shas', err_msg).group(1))
            has = int(re.search('bytes\shas\s(.*)\sbytes', err_msg).group(1))
            return LowRam(needs//1024, (needs - has) // 1024)

        if "transaction executed locally, but may not be" in err_msg:
            return None

        if not err_msg:
            return None
        return Error(err_msg)

    def switch(self, cleos_object_or_str):
        try:
            cleos_object_or_str.error_object = \
                self.error_map(cleos_object_or_str.err_msg)
        except:
            pass

        return cleos_object_or_str   
                     
    def ERROR_OBJECT(self, err_msg):
        try:
            cleos_object = self.switch(err_msg)
            return cleos_object.error_object
        except:
            return None

    def ERROR(self, cleos_or_str=None):
        """Print an error message or throw 'Exception'.

            The 'cleos_or_str' argument may be a string error message or any object having
            the string attribute `err_msg`.

            If 'set_throw_error(True)', an `Exception object is thrown, otherwise the
            message is printed.

            arguments:
            cleos_or_str -- error message string or object having the attribute err_msg
        """
        if cleos_or_str is None:
            cleos_or_str = self

        cleos_object = None
        if not isinstance(cleos_or_str, str):
            if not cleos_or_str.error:
                return False
                            
            cleos_object = self.switch(cleos_or_str)
            if cleos_object.error_object is None:
                return False

            msg = cleos_object.err_msg
        else:
            msg = cleos_or_str

        if not msg:
            return False

        if _is_testing_error:
            color = Verbosity.ERROR_TESTING.value
        else:
            color = Verbosity.ERROR.value

        

        msg = colored(
            "ERROR:\n{}".format(cleos.heredoc(msg)), 
            color[0], color[1], attrs=color[2])  + "\n"
        if not cleos_object is None:
            cleos_object.error_object.msg = msg

        self.error_buffer = msg
        global _is_throw_error
        if _is_throw_error:
            raise Exception(msg)
        else:
            print(msg)

        return True

def wallet_dir():
    if setup.is_use_keosd():
        wallet_dir_ = os.path.expandvars(teos.get_keosd_wallet_dir())
    else:
        wallet_dir_ = teos.get_node_wallet_dir()
    return wallet_dir_

"""Return json account map
"""
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
                    logger.ERROR("""
                The account mapping file is misformed. The error message is:
                {}
                
                Do you want to edit the file?
                """.format(str(e)))
                        
                    answer = input("y/n <<< ")
                    if answer == "y":
                        edit_account_map()
                        continue
                    else:
                        logger.ERROR("""
            Use the function 'eosf.edit_account_map(text_editor="nano")'
            or the corresponding method of any object of the 'eosf_wallet.Wallet` 
            class to edit the file.
                        """)                    
                        return None

def edit_account_map(text_editor="nano"):
    import subprocess
    subprocess.run([text_editor, wallet_dir() + setup.account_map])

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

def use_keosd(status):
    restart()
    if status:
        setup.use_keosd(True)
    else:
        kill_keosd()
        time.sleep(3)
        setup.use_keosd(False)

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

def reset(verbosity=None):
    """ Start clean the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    """
    node = teos.NodeStart(1, is_verbose=0)
    cleos.set_wallet_url_arg(node, node.json["EOSIO_DAEMON_ADDRESS"], False)
    probe = teos.NodeProbe(is_verbose=-1)
    logger = Logger(verbosity)
    if not logger.ERROR(probe):
        logger.EOSF_TRACE("""
        ######### Local test node is reset and is running.
        """)
        logger.OUT(str(node))

def run(verbosity=None):
    """ Restart the EOSIO local node.

    Return: `True` if `GeiInfo()` call is successful, otherwise `False`.
    """
    node = teos.NodeStart(0, is_verbose=0)
    cleos.set_wallet_url_arg(node, node.json["EOSIO_DAEMON_ADDRESS"], False)
    probe = teos.NodeProbe(is_verbose=-1)
    logger = Logger(verbosity)
    if not logger.ERROR(probe):
        logger.EOSF_TRACE("""
        ######### Local test node is started and is running.
        """)
        logger.OUT(str(node))

def stop(verbosity=None):
    """ Stops all running EOSIO nodes and empties the local `nodeos` wallet 
    directory.

    Return: True if no running nodes and the local `nodeos` wallet directory 
    is empty, otherwise `False`.
    """
    stop = teos.NodeStop(is_verbose=0)
    logger = Logger(verbosity)
    if not logger.ERROR(stop):
        logger.EOSF_TRACE("""
        ######### Local test node is stopped.
        """)
        logger.OUT(str(stop))

def info():
    """
    Display EOS node status.
    """
    get_info = cleos.GetInfo(is_verbose=-1)
    logger = Logger(None)
    get_info.err_msg = """
    {}
    THE NODE {} IS NOT OPERATIVE.
    """.format(get_info.err_msg, setup.nodeos_address())
    if not logger.ERROR(get_info):
        logger.EOSF_TRACE("""
        ######### Node ``{}``, head block number ``{}``.
        """.format(
            setup.nodeos_address(),
            get_info.json["head_block_num"]))

def is_running():
    """
    Check if testnet is running.
    """
    try: # if running, produces json
        head_block_num = int(cleos.GetInfo(0).json["head_block_num"])
    except:
        head_block_num = -1
    return head_block_num > 0

if __name__ == "__main__":
    template = ""
    if len(sys.argv) > 2:
        template = str(sys.argv[2])

    teos.TemplateCreate(str(sys.argv[1]), template, visual_studio_code=True)

