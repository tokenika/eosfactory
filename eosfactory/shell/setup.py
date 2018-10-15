#!/usr/bin/python3

import re
import os
import json
import eosfactory.core.config as config


is_print_command_line = False
is_print_request = False
is_print_response = False
is_translating = True
account_map = "accounts.json"
password_map = "passwords.json"
wallet_default_name = "default"
is_local_address = False
node_api = config.node_api()

__nodeos_address = None
__file_prefix = None


def nodeos_address():
    global __nodeos_address
    return __nodeos_address


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

    global __file_prefix
    __file_prefix = p

    global account_map
    account_map = __file_prefix + "accounts.json"
    global password_map
    password_map = __file_prefix + "passwords.json"
    global wallet_default_name
    wallet_default_name = __file_prefix + "default"


def file_prefix():
    global __file_prefix
    return __file_prefix


# def reboot():
#     global is_local_address
#     is_local_address = False
#     global __nodeos_address
#     __nodeos_address = None
#     global __file_prefix
#     __file_prefix = None


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