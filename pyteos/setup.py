#!/usr/bin/python3

import os
import json

_is_verbose = 1
_is_json = 0
_is_command_line_mode = False
_print_request = False
_print_response = False
_nodeos_address = None
_is_local_address = False
_is_use_keosd = False
account_map = "accounts.json"
password_map = "passwords.json"

def restart():
    global _nodeos_address
    _nodeos_address = None

def set_is_local_address(status):
    global _is_local_address
    _is_local_address = status


def is_local_address():
    global _is_local_address
    return _is_local_address


def set_nodeos_address(url):
    global _nodeos_address
    _nodeos_address = "http://" + url


def nodeos_address_arg():
    global _nodeos_address
    if _nodeos_address is None:
        return None
    return ["--url", _nodeos_address]


def use_keosd(status=False):
    """ Do use `keosd` Wallet Manager.

    Or use `nodeos`. See https://github.com/EOSIO/eos/wiki/CLI-Wallet
    for explanations.

    If wallets are not managed by `keosd`, they can be reset with the
    `eosf.reset([eosf.Verbosity.TRACE])` function, what is desired when testing smart contracts
    locally.
    """    
    global _is_use_keosd
    _is_use_keosd = status


def is_use_keosd():
    global _is_use_keosd
    return _is_use_keosd
    

def set_verbose(status=1):
    """ If set `False`, print error messages only.
    """
    global _is_verbose
    _is_verbose = status
    if status:
        print("##### verbose mode is set!")

def is_verbose():
    """ If `False`, print error messages only.
    """
    global _is_verbose
    return _is_verbose


def set_json(status=1):
    global _is_json
    _is_json = status
    if status:
        print("##### json mode is set!")

def is_json():
    """ If `True`, output json.
    """
    global _is_json
    return _is_json


def set_print_request(status=True):
    """If set `True`, print html request sent to the node.
    """
    global _print_request
    _print_request = status
    if status:
        print("##### print request mode is set!")
        set_json()

def is_print_request():
    """If `True`, print html request sent to the node.
    """
    global _print_request
    return _print_request


def set_print_response(status=True):
    """If set `True`, print html response of the node.
    """
    global _print_response
    _print_response = status
    if status:
        print("##### print response mode is set!")
        set_json()

def is_print_response():
    """If `True`, print html response of the node.
    """
    global _print_response
    return _print_response


def set_command_line_mode(status=True):
    """If set `True`, print html communication with the node.
    Also, be super-verbose.
    """
    global _is_command_line_mode
    _is_command_line_mode = status
    if status:
        print("##### command line mode is set!")

def is_print_command_line():
    """If `True`, print html communication with the node.
    Also, be super-verbose.
    """
    global _is_command_line_mode
    return _is_command_line_mode    


# def output(msg):
#     if _is_verbose:
#         print("#  " + msg.replace("\n", "\n#  "))

class Setup:
    """ Interface to the json configuration file.

    The configuration file is expected in the same folder as the current file.
    """
    __setupFile = os.path.dirname(os.path.abspath(__file__)) + "/../teos/config.json"
    __CLEOS_EXE = "cleos_executable"    
    __TEOS_EXE = "teos_executable"
    __EOSIO_SOURCE_DIR = "EOSIO_SOURCE_DIR"
    __TEOS_ENV = "eosf"

    __review = False
    cleos_exe = ""
    teos_exe = ""

    def __init__(self):

        with open(self.__setupFile) as json_data:
            setup_json = json.load(json_data)

        if not self.cleos_exe:
            try:
                path_to_cleos = os.environ[self.__EOSIO_SOURCE_DIR] \
                    + "/build/programs/cleos/cleos"
                if os.path.isfile(path_to_cleos):
                    self.cleos_exe = os.path.realpath(path_to_cleos)
            except:
                pass

        if not self.teos_exe:
            try:
                path_to_teos = os.environ[self.__TEOS_ENV]
                if os.path.isfile(path_to_teos):
                    self.teos_exe = os.path.realpath(path_to_teos)
            except:
                pass            

        if not self.teos_exe:
            path_to_teos =  os.path.abspath(__file__) \
                + "/../teos/build/teos/teos"
            if os.path.isfile(path_to_teos):
                self.teos_exe = os.path.realpath(path_to_teos)

        if not self.teos_exe:
            try:
                if os.path.isfile(self.__setupFile):
                    path_to_teos = os.path.dirname(os.path.abspath(__file__)) \
                            + setup_json[self.__TEOS_EXE]
                    if os.path.isfile(path_to_teos):
                        self.teos_exe = os.path.realpath(path_to_teos)
            except:
                pass

        if not self.cleos_exe:
            print('''ERROR in setup.py!
Do not know the cleos executable!
It is expected to be derived from the environment variable:
{0}
or
it is expected to be in the config file named
{1}
as {{"{2}":"absolute-path-to-eos-repository"}}
            '''.format(
                    self.__EOSIO_SOURCE_DIR,                 
                    os.path.realpath(self.__setupFile),
                    self.__CLEOS_EXE,
                    )
            
            )

        if not self.teos_exe:
            print('''ERROR in pyteos.py!
Do not know the teos executable!
It is expected to be the environment variable:
{0}
it is expected to be in the config file named
{1}
as {{"{2}":"absolute-path-to-teos-executable"}}
                '''.format(
                    self.__TEOS_ENV,                 
                    os.path.realpath(self.__setupFile),
                    self.__TEOS_EXE,
                    )
                )

