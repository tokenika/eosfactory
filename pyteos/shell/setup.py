#!/usr/bin/python3

import re
import os
# import sys
import json
# from textwrap import dedent

LOCALHOST_HTTP_ADDRESS = "127.0.0.1:8888"
CONTRACTS_DIR = "contracts/"
CONFIG_JSON = "config.json"
EOSIO_CONTRACT_DIR = "build/contracts/"

__nodeos_address = None


is_print_command_line = False
is_print_request = False
is_print_response = False


def nodeos_address():
    global __nodeos_address
    return __nodeos_address

is_translating = True

account_map = "accounts.json"
password_map = "passwords.json"
wallet_default_name = "default"

is_local_address = False

_file_prefix = None


def url_prefix(address):
    p = re.sub("\.|\:|-|https|http|\/", "_", __nodeos_address)
    return re.sub("_+", "_", p) + "_"


def set_nodeos_address(address, prefix=None):
    global __nodeos_address
    if address:
        __nodeos_address = address

    if not __nodeos_address:
        print('''
ERROR in setup.set_nodeos_address(...)!
nodeos address is not set.
        ''')
        return

    p = url_prefix(address)

    if prefix:
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


def reboot():
    global is_local_address
    is_local_address = False
    global __nodeos_address
    __nodeos_address = None
    global _file_prefix
    _file_prefix = None







def heredoc(message):
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    return message


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