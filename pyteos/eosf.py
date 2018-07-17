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


def reload():
    import importlib
    importlib.reload(eosf)


class Verbosity(enum.Enum):
    COMMENT = 'green'
    TRACE = 'magenta'
    EOSF = 'cyan'
    ERROR = 'red'
    ERROR_TESTING = 'blue'
    OUT = ''
    DEBUG = 'yellow'

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
    if status:
        global _is_testing_error
        _is_testing_error = status

class Logger():

    verbosity = []
    err_msg = ""
    error = False

    def __init__(self, verbosity=None):
        if verbosity is None:
            global _verbosity
            verbosity = _verbosity

        self.verbosity = verbosity

    def COMMENT(self, msg):
        cprint(
            cleos.heredoc(msg) + "\n",
            Verbosity.COMMENT.value)

    def EOSF(self, msg):
        if msg and (Verbosity.EOSF in self.verbosity \
                or Verbosity.EOSF in _verbosity_plus):
            cprint(
                cleos.heredoc(msg),
                Verbosity.EOSF.value)

    def TRACE(self, msg):
        if msg and (Verbosity.TRACE in self.verbosity \
                or Verbosity.TRACE in _verbosity_plus):
            cprint(
                cleos.heredoc(msg),
                Verbosity.TRACE.value)

    def EOSF_TRACE(self, msg):
        if msg and Verbosity.EOSF in self.verbosity \
                or Verbosity.EOSF in _verbosity_plus:
            self.EOSF(msg)
        else:
            self.TRACE(msg)

    def OUT(self, msg):
        if msg and (Verbosity.OUT in self.verbosity \
                or Verbosity.OUT in _verbosity_plus):
            self.out_msg = msg
            print(cleos.heredoc(msg) + "\n")


    def DEBUG(self, msg):
        if msg and (Verbosity.DEBUG in self.verbosity \
                or Verbosity.DEBUG in _verbosity_plus):
            cprint(
                cleos.heredoc(msg),
                Verbosity.DEBUG.value)

    def ERROR(self, err_msg):
        """Print an error message or throw 'Exception'.

        The 'err_msg' argument may be a string error message or any object having
        the string attribute `err_msg`.

        If 'set_throw_error(True)', an `Exception object is thrown, otherwise the
        message is printed.

        arguments:
        err_msg -- error message string or object having the attribute err_msg
        """
        error = False
        if not self.error:
            try:
                self.err_msg = msg.err_msg
                self.error = msg.error
            except:
                if err_msg:
                    self.error = True
                    self.err_msg = err_msg

        if not self.error:
            return False

        if _is_testing_error:
            color = Verbosity.ERROR_TESTING.value
        else:
            color = Verbosity.ERROR.value

        self.err_msg = colored(
            "ERROR:\n{}".format(cleos.heredoc(self.err_msg)), 
            color)  + "\n"

        global _is_throw_error
        if _is_throw_error:
            raise Exception(self.err_msg)
        else:
            print(self.err_msg)

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


def kill_keosd():
    cleos.WalletStop(is_verbose=-1)


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


class ContractBuilder():
    def __init__(
            self, contract_dir,
            wast_file="", abi_file="",
            is_mutable = True,
            is_verbose=1):

        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.is_mutable = is_mutable
        self.is_verbose = is_verbose

    def path(self):
        return self.contract_dir

    def build_wast(self):
        if self.is_mutable:
            wast = teos.WAST(
                self.contract_dir, "",
                is_verbose=self.is_verbose)
        else:
            if self.is_verbose > 0:
                print("ERROR!")
                print("Cannot modify system contracts.")
        return wast

    def build_abi(self):
        if self.is_mutable:
            abi = teos.ABI(
                self.contract_dir, "",
                is_verbose=self.is_verbose)
        else:
            if self.is_verbose > 0:
                print("ERROR!")
                print("Cannot modify system contracts.")
        return abi

    def build(self):
        return not self.build_abi().error and not self.build_wast().error


class ContractBuilderFromTemplate(ContractBuilder):
    def __init__(self, name, template="", remove_existing=False, visual_studio_code=False, is_verbose=True):
        t = teos.Template(name, template, remove_existing, visual_studio_code, is_verbose)
        super().__init__(t.contract_path_absolute)


class Contract():

    def __init__(
            self, account, contract_dir,
            wast_file="", abi_file="",
            permission="",
            expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=1):

        self.account = account
        self.contract_dir = contract_dir
        self.wast_file = wast_file
        self.abi_file = abi_file
        self.expiration_sec = expiration_sec
        self.skip_signature = skip_signature
        self.dont_broadcast = dont_broadcast
        self.forceUnique = forceUnique
        self.max_cpu_usage = max_cpu_usage
        self.max_net_usage = max_net_usage
        self.ref_block = ref_block
        self.is_mutable = True

        self.contract = None
        self._console = None
        self.is_verbose = is_verbose
        self.error = self.account.error


    def deploy(self, permission="", is_verbose=1):
        self.contract = cleos.SetContract(
            self.account, self.contract_dir, 
            self.wast_file, self.abi_file, 
            permission, self.expiration_sec, 
            self.skip_signature, self.dont_broadcast, self.forceUnique,
            self.max_cpu_usage, self.max_net_usage,
            self.ref_block,
            self.is_verbose > 0 and is_verbose > 0
        )
        if not self.contract.error:
            try:
                self.contract.json = json.loads(self.contract.err_msg)
                for action in self.contract.json["actions"]:
                    action["data"] = "contract code data, deleted for readability ..................."
            except:
                pass

            return self.contract


    def is_deployed(self):
        if not self.contract:
            return False
        return not self.contract.error


    def build_wast(self):
        return ContractBuilder(
            self.contract_dir, "", "",
            self.is_mutable, self.is_verbose).build_wast()


    def build_abi(self):
        return ContractBuilder(
            self.contract_dir, "", "", 
            self.is_mutable, self.is_verbose).build_abi()

    
    def build(self):
        return ContractBuilder(
            self.contract_dir, "", "", 
            self.is_mutable, self.is_verbose).build()


    def push_action(
            self, action, data,
            permission="", expiration_sec=30,
            skip_signature=0, dont_broadcast=0, forceUnique=0,
            max_cpu_usage=0, max_net_usage=0,
            ref_block="",
            is_verbose=1,
            json=False,
            output=False
        ):
        if not permission:
            permission = self.account.name
        else:
            try: # permission is an account:
                permission = permission.name
            except: # permission is the name of an account:
                permission = permission

        if output:
            is_verbose = 0
            json = True
    
        self.action = cleos.PushAction(
            self.account.name, action, data,
            permission, expiration_sec, 
            skip_signature, dont_broadcast, forceUnique,
            max_cpu_usage, max_net_usage,
            ref_block,
            self.is_verbose > 0 and is_verbose > 0, json)

        if not self.action.error:
            try:
                self._console = self.action.console
                if self.is_verbose:
                    print(self._console + "\n") 
            except:
                pass

        return self.action


    def show_action(self, action, data, permission=""):
        """ Implements the `push action` command without broadcasting. 

        """
        return self.push_action(action, data, permission, dont_broadcast=1)


    def table(
            self, table_name, scope="",
            binary=False, 
            limit=10, key="", lower="", upper=""):
        """ Return a contract's table object.
        """
        self._table = cleos.GetTable(
                    self.account.name, table_name, scope,
                    binary=False, 
                    limit=10, key="", lower="", upper="", 
                    is_verbose=self.is_verbose)

        return self._table


    def code(self, code="", abi="", wasm=False):
        return cleos.GetCode(
            self.account.name, code, abi, wasm, is_verbose=self.is_verbose)


    def console(self):
        return self._console


    def path(self):
        """ Return contract directory path.
        """
        if self.contract:
            return str(self.contract.contract_path_absolute)
        else:
            return str(self.contract_dir)


    def delete(self):
        try:
            if self.contract:
                shutil.rmtree(str(self.contract.contract_path_absolute))
            else:
                shutil.rmtree(str(self.contract_dir))
            return True
        except:
            return False


    def __str__(self):
        if self.is_deployed():
            return str(self.contract)
        else:
            return str(self.account)


def reset(is_verbose=1):
    return node.reset(is_verbose)


def run(is_verbose=1):
    return node.run(is_verbose)


def stop(is_verbose=1):
    return node.stop(is_verbose)


if __name__ == "__main__":
    template = ""
    if len(sys.argv) > 2:
        template = str(sys.argv[2])

    teos.Template(str(sys.argv[1]), template, visual_studio_code=True)
