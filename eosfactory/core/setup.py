import os
import re
import json

import eosfactory.core.utils as utils
import eosfactory.core.config as config
import eosfactory.core.logger as logger
import eosfactory.core.errors as errors


wallet_default_name = "default"
is_print_command_lines = False
is_save_command_lines = False
is_show_private_keys = False
command_line_file = "command_lines.txt"
is_print_request = False
is_print_response = False
is_translating = True
ACCOUNT_MAP = "accounts.json"
password_map = "passwords.json"
is_local_address = False
cleos_package = "eosfactory.core.cleos"
eosiojs_package = "eosfactory.core.eosjs"
light_full = cleos_package

__nodeos_address = None
__file_prefix = None


def set_local_nodeos_address_if_none():
    if not nodeos_address():
        set_nodeos_address("http://" + config.http_server_address())
        global is_local_address
        is_local_address = True

    return is_local_address


def set_is_lt(is_lt=True):
    global light_full
    if is_lt:
        light_full = eosiojs_package
    else:
        light_full = cleos_package


def save_command_lines():
    global is_save_command_lines
    is_save_command_lines = True
    with open(command_line_file, "w+") as f:
        f.write("")


def add_to__command_line_file(command_line):
    if is_save_command_lines:
        with open(command_line_file, "a+") as f:
            f.write("{}\n\n".format(command_line))


def nodeos_address():
    global __nodeos_address
    return __nodeos_address


def url_prefix(address):
    p = re.sub(r"\.|\:|-|https|http|\/", "_", address)
    return re.sub("_+", "_", p) + "_"


def set_nodeos_address(address, prefix=None):
    """Set testnet properties.

    :param str address: testnet url, for example `http://faucet.cryptokylin.io`.
    :param str prefix: A prefix prepended to names of system files like the
        wallet file and password map file and account map file, in order to 
        relate them to the given testnet.
    """
    global __nodeos_address
    if address:
        __nodeos_address = address

    if not __nodeos_address:
        print("""
ERROR in setup.set_nodeos_address(...)!
nodeos address is not set.
        """)
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


def read_map(file_name, text_editor="nano"):
    """Return json account map

Attempt to open the account map file named ``setup.account_map``, located 
in the wallet directory ``config.keosd_wallet_dir()``, to return its json 
contents. If the file does not exist, return an empty json.

If the file is corrupted, offer editing the file with the ``nano`` linux 
editor. Return ``None`` if the the offer is rejected.
    """
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
                logger.ERROR("""
            The json file 
            {}
            is misformed. The error message is:
            {}
            
            Do you want to edit the file?
            """.format(str(path), str(e)), translate=False)
                    
                answer = input("y/n <<< ")
                if answer == "y":
                    utils.spawn([text_editor, path])
                    continue
                else:
                    raise errors.Error("""
                    Use the function 'manager.edit_account_map()' to edit the file.
                    """, translate=False)                    

def save_account_map(map_):
    save_map(map_, account_map)


def edit_account_map():
    edit_map(account_map)


def save_map(map_, file_name):
    map_ = json.dumps(map_, indent=3, sort_keys=True)
    with open(os.path.join(config.keosd_wallet_dir(), file_name), "w") as out:
        out.write(map_)


def edit_map(file_name, text_editor="nano"):
    utils.spawn([text_editor, os.path.join(
                                    config.keosd_wallet_dir(), file_name)])
    read_map(file_name, text_editor)