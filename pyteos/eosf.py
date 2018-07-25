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


class Verbosity(enum.Enum):
    COMMENT = ['green']
    TRACE = ['magenta']
    EOSF = ['cyan']
    ERROR = ['red']
    ERROR_TESTING = ['blue']
    OUT = ['']
    OUT_INFO = ['magenta', 'on_green']
    DEBUG = ['yellow']

_verbosity = [Verbosity.EOSF, Verbosity.OUT]
def set_verbosity(value=_verbosity):
    global _verbosity
    _verbosity = value

_verbosity_plus = []
def set_verbosity_plus(value=[]):
    global _verbosity_plus
    _verbosity_plus = value

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

    verbosity = []
    out_buffer = ""
    out_info_buffer = ""
    error_buffer = ""
    debug_buffer = ""

    def __init__(self, verbosity=None):
        if verbosity is None:
            global _verbosity
            verbosity = _verbosity

        self.verbosity = verbosity

    def COMMENT(self, msg):
        frame = inspect.stack()[1][0]
        test_name = inspect.getframeinfo(frame).function
        cprint(
            "\n###  " + test_name + ":\n" + cleos.heredoc(msg) + "\n",
            ", ".join(Verbosity.COMMENT.value))

    def SCENARIO(self, msg):
        self.COMMENT(msg)

    def EOSF(self, msg, do=False):
        if msg and (Verbosity.EOSF in self.verbosity \
                or Verbosity.EOSF in _verbosity_plus) \
                or do:
            cprint(
                cleos.heredoc(msg),
                ", ".join(Verbosity.EOSF.value))

    def TRACE(self, msg, do=False):
        if msg and (Verbosity.TRACE in self.verbosity \
                or Verbosity.TRACE in _verbosity_plus) \
                or do:
            cprint(
                cleos.heredoc(msg),
                ", ".join(Verbosity.TRACE.value))

    def EOSF_TRACE(self, msg, do=False):
        if msg and Verbosity.EOSF in self.verbosity \
                or Verbosity.EOSF in _verbosity_plus:
            self.EOSF(msg, do)
        else:
            self.TRACE(msg, do)

    def OUT_INFO(self, msg, do=False):
        error = False
        try:
            error = msg.error
        except:
            pass

        try:
            msg = err_msg.err_msg
        except:
            pass

        if msg and (Verbosity.OUT_INFO in self.verbosity \
                or Verbosity.OUT_INFO in _verbosity_plus) \
                or do:
            msg = cleos.heredoc(msg)
            self.out_info_buffer = msg
            cprint(
                msg,
                ", ".join(Verbosity.OUT_INFO.value))

    def OUT(self, msg, do=False):
        if msg and (Verbosity.OUT in self.verbosity \
                or Verbosity.OUT in _verbosity_plus) \
                or do:
            msg = cleos.heredoc(msg)
            self.out_buffer = msg
            print(msg + "\n")

        self.OUT_INFO(msg, do)

    def DEBUG(self, msg, do=False):
        if msg and (Verbosity.DEBUG in self.verbosity \
                or Verbosity.DEBUG in _verbosity_plus) \
                or do:
            msg = cleos.heredoc(msg)
            self.debug_buffer = msg
            cprint(
                msg,
                ", ".join(Verbosity.DEBUG.value))

    def ERROR(self, err_msg=None):
        """Print an error message or throw 'Exception'.

        The 'err_msg' argument may be a string error message or any object having
        the string attribute `err_msg`.

        If 'set_throw_error(True)', an `Exception object is thrown, otherwise the
        message is printed.

        arguments:
        err_msg -- error message string or object having the attribute err_msg
        """
        if not err_msg is None:
            error = True
            try:
                error = err_msg.error
            except:
                pass

            try:
                err_msg = err_msg.error_map()
            except:
                try:
                    err_msg = err_msg.err_msg
                except:
                    pass
        else:
            return False

        if not error or not err_msg:
            return False

        if _is_testing_error:
            color = Verbosity.ERROR_TESTING.value
        else:
            color = Verbosity.ERROR.value

        err_msg = colored(
            "ERROR:\n{}".format(cleos.heredoc(err_msg)), 
            color)  + "\n"

        self.error_buffer = err_msg
        global _is_throw_error
        if _is_throw_error:
            raise Exception(err_msg)
        else:
            print(err_msg)

        return True

def wallet_dir():
    if setup.is_use_keosd():
        wallet_dir_ = os.path.expandvars(teos.get_keosd_wallet_dir())
    else:
        wallet_dir_ = teos.get_node_wallet_dir()
    return wallet_dir_

def account_map(logger):

    wallet_dir_ = wallet_dir()
    while True:
        try: # whether the setup map file exists:
            with open(wallet_dir_ + setup.account_map, "r") as input_file:
                return json.load(input_file)

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                return {}
            else: 
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
    cleos.set_wallet_url_arg(stop, "")
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
    get_info = cleos.GetInfo()
    logger = Logger(verbosity)
    if not logger.ERROR(get_info):
        logger.OUT(str(logger))

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

    teos.Template(str(sys.argv[1]), template, visual_studio_code=True)
