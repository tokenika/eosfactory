import os
import subprocess
import json
from cryptography.fernet import Fernet
from threading import Timer

import eosfactory.core.interface as interface
import eosfactory.core.config as config
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup

# The first key in any eosf wallet: identification of the system.

_WALLET_FILE_EXT = ".eosfwallet"
_TIMEOUT = 3000
_TIMER = None
_OPEN_WALLETS = {}


class OpenWallet:
    def __init__(self, name, cipher_suite=None):
        self.name = name
        self.cipher_suite = cipher_suite


class Wallet(interface.Wallet):
    '''
    If the *password* argument is set, try to open a wallet. Otherwise, create
    a new wallet.

    Args:
        name (str): The name of the wallet, defaults to *default*.
        password (str): The password to the wallet, if the wallet exists. 
        is_verbose (bool): If *False* do not print. Default is *True*.

    Attributes:
        name (str): The name of the wallet.
        password (str): The password returned by the *wallet create* 
            EOSIO cleos command.
        is_created (bool): True, if the wallet created.
    '''

    def __init__(self, name=None, password=None, is_verbose=True):

        setup.set_local_nodeos_address_if_none()
        if name is None:
            name = setup.wallet_default_name

        interface.Wallet.__init__(self, name, password)
        _file = wallet_file(name)
        cipher_suite = None
        self.is_created = False

        if self.password:
            if not os.path.exists(_file):
                raise errors.Error('''
                    Password is set, but the wallet file does not exist:
                        {}
                '''.format(_file))
            cipher_suite = Fernet(str.encode(password))
            keys_ciphered = None
            try:
                with open(wallet_file(name), "r")  as input:
                    keys_ciphered = [key.rstrip('\n') for key in input]
            except Exception as e:
                raise errors.Error(str(e))
            try:
                decrypt(keys_ciphered[0], cipher_suite)
            except:
                raise errors.Error('''
                Wrong password.
                ''')
            if is_verbose:
                logger.OUT('''
                Opened existing wallet: {}
                '''.format(name))
        else:
            if os.path.exists(_file):
                raise errors.Error('''
                    Cannot overwrite existing wallet file:
                        {}
                '''.format(_file))
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            self.password = key.decode("utf-8")
            
            self.is_created = True

            if is_verbose:
                logger.OUT('''
                Created wallet: {}
                Save password to use in the future to unlock this wallet.
                Without password imported keys will not be retrievable.
                "{}"
                '''.format(name, self.password))

        _OPEN_WALLETS[name] = OpenWallet(name, cipher_suite)
        global _TIMER
        _TIMER = Timer(_TIMEOUT, lock_all)
        _TIMER.start()


def setTimeout(time):
    global _TIMEOUT
    _TIMEOUT = time


def wallet_file(name):
    return config.keosd_wallet_dir() + name + _WALLET_FILE_EXT


def encrypt(key, cipher_suite):
    return cipher_suite.encrypt(str.encode(key)).decode("utf-8")


def public_key(private_key):
    return Node('''
    const ecc = require('eosjs-ecc');
    
    ((private_key) => {
        public_key = {key_public: ecc.privateToPublic(private_key)}
        console.log(JSON.stringify(public_key))   
    })('%s')
        ''' % (private_key)).json["key_public"]


def decrypt(ciphered_key, cipher_suite):
    return cipher_suite.decrypt(str.encode(ciphered_key)).decode("utf-8")


def delete(wallet, is_verbose=True):
    name = interface.wallet_arg(wallet)
    _file = wallet_file(name)
    if os.path.isfile(_file):
        try:
            os.remove(_file)
        except Exception as e:
            raise errors.Error(str(e))

        if is_verbose:
            logger.OUT("Deleted wallet: '{}'".format(name))
        return True

    if is_verbose:
        logger.OUT('''
            There is not any wallet file named
                '{}'
            '''.format(name))
    return False


def open_wallet(wallet, is_verbose=True):
    name = interface.wallet_arg(wallet)
    wallets_ = wallets()
    if name + _WALLET_FILE_EXT in wallets_:
        _OPEN_WALLETS[name] = OpenWallet(name)
    else:
        raise errors.Error('''
        There is not any wallet file named
            {}
        '''.format((wallet_file(name))))

    if is_verbose:
        logger.OUT("Opened: {}".format(name))


def lock(wallet, is_verbose=True):
    name = interface.wallet_arg(wallet)
    if _OPEN_WALLETS[name]:
        _OPEN_WALLETS[name].cipher_suite = None
    else:
        raise errors.Error('''
        The wallet '{}' is not open.
        '''.format(name))

    if is_verbose:
        logger.OUT("Locked: {}".format(name))


def lock_all(is_verbose=True):
    
    locked = []
    for name, interface.open_wallet in _OPEN_WALLETS.items():
        _OPEN_WALLETS[name].cipher_suite = None
        locked.append(name)
    
    if is_verbose:
        if locked:
            logger.OUT("Locked: \n" + ", ".join(locked))
        else:
            logger.OUT("Nothing to lock.")


def unlock(wallet, password=None, is_verbose=True):
    name = interface.wallet_arg(wallet)
    if not password and isinstance(wallet, interface.Wallet):
        password = wallet.password

    if not is_open(name):
        raise errors.Error('''
            The wallet '{}' is not open.
            '''.format(name))

    if not is_unlocked(name):
        try:
            _OPEN_WALLETS[name].cipher_suite = Fernet(str.encode(password))
            with open(wallet_file(name), "r")  as input:
                keys_ciphered = [key.rstrip('\n') for key in input]

            wallet_manager_id = decrypt(
                    keys_ciphered[0], _OPEN_WALLETS[name].cipher_suite)
        except Exception as e:
            raise errors.Error('''
                Wrong password.
                ''')
        
    if is_verbose:
        logger.OUT("Unlocked: {}".format(name))    
    
    global _TIMER
    if _TIMER:
        _TIMER.cancel()
    _TIMER = Timer(_TIMEOUT, lock_all)
    _TIMER.start()
    return wallet_manager_id


def list(is_verbose=True):
    wallets = []
    for name, open_wallet in _OPEN_WALLETS.items():
        if open_wallet:
            wallets.append("* " + name)
        else:
            wallets.append(name)

    if is_verbose:
        if wallets:
            logger.OUT('''
        Open wallets. Starlet, if any, means 'unlocked':\n''' 
            + "\n".join(wallets))
        else:
            logger.OUT("There is not any wallet open.")            


def import_key(wallet, key, is_verbose=True):
    is_open_and_unlocked(wallet)

    name = interface.wallet_arg(wallet)
    key_private = interface.key_arg(key, is_owner_key=True, is_private_key=True)

    with open(wallet_file(name), "a")  as out:
        out.write(encrypt(key_private, _OPEN_WALLETS[name].cipher_suite) + "\n")

    key_public = Node('''
    const ecc = require('eosjs-ecc');

    ((private_key) => {
        public_key = {key_public: ecc.privateToPublic(private_key)}
        console.log(JSON.stringify(public_key))   
    })('%s')
        ''' % (key_private)).json["key_public"]

    if is_verbose:
        logger.OUT("Imported key to wallet '{}':\n{}".format(
            name, key_public))
    
    return key_public
    

def remove_key(key, is_verbose=True):
    trash = []

    for name, _open_wallet in _OPEN_WALLETS.items():
        if not _open_wallet.cipher_suite:
            continue

        owner_key_public = interface.key_arg(
            key, is_owner_key=True, is_private_key=False)
        active_key_public = interface.key_arg(
            key, is_owner_key=False, is_private_key=False)

    
        private_keys_ = private_keys(name, False)

        _keys = Node('''
        const ecc = require('eosjs-ecc');

        ((keys) => {
            public_keys = []
            for (i = 0; i < keys.length; i++) {
                pair = []
                pair[0] = keys[i]
                pair[1] = ecc.privateToPublic(keys[i])
                public_keys[i] = pair
            }

            console.log(JSON.stringify(public_keys))   
        })(%s)
        ''' % private_keys_).json

        for pair in _keys:
            if pair[1] == owner_key_public or pair[1] == active_key_public:
                trash.append(pair[0])

        if trash:
            remaining = []
            for private_key in private_keys_:
                if not private_key in trash:
                    remaining.append(private_key)

            with open(wallet_file(name), "w")  as out:
                out.write("\n".join(remaining))
    
    if is_verbose:
        if trash:
            logger.OUT("Removed keys:\n{}".format("\n".join(trash)))
    

def keys(wallet=None, is_verbose=True):
    private_keys_ = private_keys(wallet, False)
    public_keys = Node('''
    const ecc = require('eosjs-ecc');

    ((keys) => {
        var public_keys = []
        for (i = 0; i < keys.length; i++) {
            public_keys[i] = ecc.privateToPublic(keys[i])
        }

        console.log(JSON.stringify(public_keys))   
    })(%s)
    ''' % (private_keys_)).json

    if is_verbose:
        if wallet:
            logger.OUT("Keys in the wallet '{}': \n{}".format(
                        interface.wallet_arg(wallet), "\n".join(public_keys)))
        else:
            logger.OUT("Keys in all unlocked wallets: \n{}".format(
                                                        "\n".join(public_keys)))

    return public_keys


def private_keys(wallet=None, is_verbose=True):
    _keys = []    
    for name, _ in _OPEN_WALLETS.items():
        if wallet:
            if name != interface.wallet_arg(wallet):
                continue
        is_open_and_unlocked(name)
        
        with open(wallet_file(name), "r")  as f:
            keys_ciphered = [key.rstrip('\n') for key in f]

        for key in keys_ciphered:
            _keys.append(decrypt(key, _OPEN_WALLETS[name].cipher_suite))

    if is_verbose:
        if wallet:
            logger.OUT("Private keys in the wallet '{}': \n{}".format(
                                interface.wallet_arg(wallet), "\n".join(_keys)))
        else:
            logger.OUT("Private keys in all unlocked wallets: \n{}".format(
                                                            "\n".join(_keys)))

    return _keys
    

def stop(is_verbose=True):
    lock_all()
    _OPEN_WALLETS = {}
    global _TIMER
    if _TIMER:
        _TIMER.cancel()

    if is_verbose:
        logger.OUT('''
    All the wallet objects locked and removed from the list of open wallets.''')


class Node():
    def __init__(self, js):
        self.json = None
        cl = ["node", "-e"]
        js = utils.heredoc(js)
        cl.append(js)

        if setup.is_print_command_lines:
            print("javascript:")
            print("___________")
            print("")
            print(js)
            print("")

        process = subprocess.run(
            cl,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE) 
        err_msg = process.stderr.decode("utf-8")
        if err_msg:
            raise errors.Error(err_msg)

        self.json = json.loads( process.stdout.decode("utf-8"))


def is_open(wallet):
    name = interface.wallet_arg(wallet)
    return name in _OPEN_WALLETS


def is_unlocked(wallet):
    name = interface.wallet_arg(wallet)
    return is_open(name) and _OPEN_WALLETS[name].cipher_suite


def is_open_and_unlocked(wallet):
    name = interface.wallet_arg(wallet)
    if not is_open(wallet):
        raise errors.Error('''
        Wallet '{}' is not open.
        '''.format(name))

    if not is_unlocked(wallet):
        raise errors.Error('''
        Wallet '{}' is locked.
        '''.format(name))


def wallets():
    directory = os.fsencode(config.keosd_wallet_dir())
    retval = []
    for _file in os.listdir(directory):
        filename = os.fsdecode(_file)
        if filename.endswith(_WALLET_FILE_EXT): 
            retval.append(filename)
    return retval


def unlocked():
    retval = []
    for name, open_wallet in _OPEN_WALLETS.items():
        if is_unlocked(name):
            retval.append(name)
    return retval
