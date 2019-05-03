#!/usr/bin/python3

import re

is_print_command_line = False
is_raise_error = False
is_print_request = False
is_print_response = False
is_translating = True
account_map = "accounts.json"
password_map = "passwords.json"
wallet_default_name = "default"
is_local_address = False

__nodeos_address = None
__file_prefix = None


def nodeos_address():
    global __nodeos_address
    return __nodeos_address


def url_prefix(address):
    p = re.sub(r"\.|\:|-|https|http|\/", "_", address)
    return re.sub("_+", "_", p) + "_"


def set_nodeos_address(address, prefix=None):
    '''Set testnet properties.

    :param str address: testnet url, for example `http://faucet.cryptokylin.io`.
    :param str prefix: A prefix prepended to names of system files like the
        wallet file and password map file and account map file, in order to 
        relate them to the given testnet.
    '''
    global __nodeos_address
    if address:
        __nodeos_address = address

    if not __nodeos_address:
        print('''
ERROR in setup.set_nodeos_address(...)!
nodeos address is not set.
        ''')
        return

    address = __nodeos_address
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


def reboot():
    global is_local_address
    is_local_address = False
    global __nodeos_address
    __nodeos_address = None
    global __file_prefix
    __file_prefix = None

