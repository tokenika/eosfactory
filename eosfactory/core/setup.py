"""Configure the current session.

The module defines the following global constants:
    - ``WALLET_DEFAULT_NAME`` (str): Default wallet, defaults to ``"default"``
    - ``IS_PRINT_COMMAND_LINES`` (bool): If set, print data sent to external processes such as ``nodeos`` and ``cleos`` or ``node``. Defaults to ``False``.
    - ``IS_SAVE_COMMAND_LINES`` (bool): If set, save to the ``COMMAND_LINE_FILE``, data sent to external processes such as ``nodeos`` and ``cleos`` or ``node``. Defaults to ``False``.
    - ``COMMAND_LINE_FILE`` (str): Use this path if ``IS_SAVE_COMMAND_LINES`` is set. Defaults to ``"command_lines.txt"``.
    - ``IS_SHOW_PRIVATE_KEYS`` (bool): If set, do not hide private keys. Defaults to ``False``.
    - ``IS_PRINT_REQUEST`` (bool): If set, print requests sent to the node. Defaults to ``False``.
    - ``IS_PRINT_RESPONSE`` (bool): If set, print responses of the node. Defaults to ``False``.
    - ``IS_TRANSLATING`` (bool): If set, translate responces from the node replacing native account names and keys with object names. Defaults to ``True``. 
"""

import os
import re
import json

import eosfactory.core.utils as utils
import eosfactory.core.config as config
import eosfactory.core.logger as logger
import eosfactory.core.errors as errors


WALLET_DEFAULT_NAME = "default"
IS_PRINT_COMMAND_LINES = False
IS_SAVE_COMMAND_LINES = False
COMMAND_LINE_FILE = "command_lines.txt"
IS_SHOW_PRIVATE_KEYS = False
IS_PRINT_REQUEST = False
IS_PRINT_RESPONSE = False
IS_TRANSLATING = True
IS_LOCAL_ADDRESS = False

ACCOUNT_MAP = None
PASSWORD_MAP = None

__NODEOS_ADDRESS = None
__FILE_PREFIX = None
__INTERFACE_PACKAGE = None


def set_local_nodeos_address_if_none():
    """Set address of the local testnet.

    It is called just before a request is to be send to a testnet. The address of the testnet can be then set or not; if not, the locall testnet address is assumed.
    """
    if not nodeos_address():
        set_nodeos_address("http://" + config.http_server_address())
        global IS_LOCAL_ADDRESS
        IS_LOCAL_ADDRESS = True

    return IS_LOCAL_ADDRESS


def set_is_eosjs(is_lt=True):
    """Determine whether to use ``eosjs`` interface rathert than ``cleos`` one."""

    global __INTERFACE_PACKAGE
    if is_lt:
        __INTERFACE_PACKAGE = config.EOSJS_PACKAGE
    else:
        __INTERFACE_PACKAGE = config.CLEOS_PACKAGE


def interface_package():
    """This function is used internally."""
    if __INTERFACE_PACKAGE:
        return __INTERFACE_PACKAGE

    return config.interface_package()


def save_command_lines():
    """Set the mode of saving to a file the data sent to the testnet.
    
    The file is set with the global constant ``COMMAND_LINE_FILE``.
    """
    global IS_SAVE_COMMAND_LINES
    IS_SAVE_COMMAND_LINES = True
    with open(COMMAND_LINE_FILE, "w+") as f:
        f.write("")


def add_to__COMMAND_LINE_FILE(command_line):
    """This function is used internally."""

    if IS_SAVE_COMMAND_LINES:
        with open(COMMAND_LINE_FILE, "a+") as f:
            f.write("{}\n\n".format(command_line))


def nodeos_address():
    """Return the address of the testnet."""

    global __NODEOS_ADDRESS
    return __NODEOS_ADDRESS


def url_prefix(address):
    """This function is used internally."""

    p = re.sub(r"\.|\:|-|https|http|\/", "_", address)
    return re.sub("_+", "_", p) + "_"


def set_nodeos_address(address, prefix=None):
    """Set testnet properties.

    Args:
        address (str): testnet url, for example `http://faucet.cryptokylin.io`.
        prefix (str): A prefix prepended to names of system files like the
        wallet file and password map file and account map file, in order to 
        relate them to the given testnet.
    """

    global __NODEOS_ADDRESS
    if address:
        __NODEOS_ADDRESS = address

    if not __NODEOS_ADDRESS:
        print("""
ERROR in setup.set_nodeos_address(...)!
nodeos address is not set.
        """)
        return

    address = __NODEOS_ADDRESS
    p = url_prefix(address)

    if prefix:
        p = prefix + "_" + p

    global __FILE_PREFIX
    __FILE_PREFIX = p

    global ACCOUNT_MAP
    ACCOUNT_MAP = __FILE_PREFIX + "accounts.json"
    global PASSWORD_MAP
    PASSWORD_MAP = __FILE_PREFIX + "passwords.json"
    global WALLET_DEFAULT_NAME
    WALLET_DEFAULT_NAME = __FILE_PREFIX + "default"


def file_prefix():
    """Return the current prefix used to identify the current wallet and account mapping"""

    global __FILE_PREFIX
    return __FILE_PREFIX


def reboot():
    """Reset EOSFactory to its startup conditions."""

    global IS_LOCAL_ADDRESS
    IS_LOCAL_ADDRESS = False
    global __NODEOS_ADDRESS
    __NODEOS_ADDRESS = None
    global __FILE_PREFIX
    __FILE_PREFIX = None


def read_map(file_name, text_editor="nano"):
    """Return json account map

    Attempt to open the account map file named ``setup.ACCOUNT_MAP``, located 
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
                    Use the function 'manager.edit___ACCOUNT_MAP()' to edit the file.
                    """, translate=False)                    

def save_account_map(map_):
    """Save a file with the mapping between native account names and account object names.
    
    This function is used internally.
    """

    save_map(map_, ACCOUNT_MAP)


def edit_account_map():
    """Edit the mapping between native account names and account object names.
    
    This function is used internally.
    """

    edit_map(ACCOUNT_MAP)


def save_map(map_, file_name):
    """This function is used internally."""
    
    map_ = json.dumps(map_, indent=3, sort_keys=True)
    with open(os.path.join(config.keosd_wallet_dir(), file_name), "w") as out:
        out.write(map_)


def edit_map(file_name, text_editor="nano"):
    """This function is used internally."""

    utils.spawn([text_editor, os.path.join(
                                    config.keosd_wallet_dir(), file_name)])
    read_map(file_name, text_editor)