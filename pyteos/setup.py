#!/usr/bin/python3

import re
import os
import sys
import json
from textwrap import dedent

is_verbose = 1
is_json = 0
is_print_command_line = False
is_print_request = False
is_print_response = False
is_translating = True

account_map = "accounts.json"
password_map = "passwords.json"
wallet_default_name = "default"

is_local_address = False
_nodeos_address = None
_file_prefix = None


def url_prefix(address):
    p = re.sub("\.|\:|-|https|http|\/", "_", _nodeos_address)
    return re.sub("_+", "_", p) + "_"


def set_nodeos_address(address, prefix=None):
    global _nodeos_address
    if address:
        _nodeos_address = address

    if not _nodeos_address:
        print('''
ERROR in setup.set_nodeos_address(...)!
nodeos address is not set.
        ''')
        return

    p = url_prefix(address)

    if not prefix is None:
        p = prefix + "_" + p

    global _file_prefix
    _file_prefix = p

    global account_map
    account_map = _file_prefix + "accounts.json"
    global password_map
    password_map = _file_prefix + "passwords.json"
    global wallet_default_name
    wallet_default_name = _file_prefix + "default"


def file_prefix():
    global _file_prefix
    return _file_prefix


def restart():
    global is_local_address
    is_local_address = False
    global _nodeos_address
    _nodeos_address = None
    global _file_prefix
    _file_prefix = None


def nodeos_address():
    global _nodeos_address
    return _nodeos_address


class Setup:
    ''' Interface to the json configuration file.

    The configuration file is expected in the same folder as the current file.
    '''
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


def heredoc(msg):
    msg = dedent(msg).strip()
    msg.replace("<br>", "\n")
    return msg


def save_code():
    '''Copy the current file without heredoc comments.
    '''
    if len(sys.argv) < 2 or sys.argv[1] != "-s" and sys.argv[1] != "--save":
        return

    original = os.path.abspath(sys.argv[0])
    converted = os.path.splitext(original)[0] + ".py"

    try:
        with open(original, "r") as r:
            text = r.read()

        search = re.compile(r'\'\'\'.*?\'\'\'', flags=re.DOTALL)
        with open(converted, "w") as w:
            w.write(re.sub(search, '', text))
    except Exception as e: 
        print(e)

    exit()