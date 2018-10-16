import os
import subprocess
import json
from cryptography.fernet import Fernet
from threading import Timer

from eosfactory.core.interface import *
import eosfactory.core.config as config
import eosfactory.core.errors as errors
import eosfactory.core.logger as logger
import eosfactory.core.utils as utils
import eosfactory.core.setup as setup


class OpenWallet:
    def __init__(self, name, cipher_suite=None):
        self.name = name
        self.cipher_suite = cipher_suite

_manager_id = "5JfjYNzKTDoU35RSn6BpXei8Uqs1B6EGNwkEFHaN8SPHwhjUzcX"
_file_ext = ".eosfwallet"
_timeout = 3000
_timer = None
_open_wallets = {}


class Create(Wallet):
    def __init__(self, name="default", password=None, is_verbose=True):
        Wallet.__init__(self, name, password)
        file = wallet_file(name)
        cipher_suite = None
        self.is_created = False

        if self.password:
            if not os.path.exists(file):
                raise errors.Error('''
                    Password is set, but the wallet file does not exist:
                        {}
                '''.format(file))
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
            if os.path.exists(file):
                raise errors.Error('''
                    Cannot overwrite existing wallet file:
                        {}
                '''.format(file))
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            self.password = key.decode("utf-8")

            try:
                with open(file, "w+")  as out:
                    out.write(encrypt(_manager_id, cipher_suite) + "\n")
            except Exception as e:
                raise errors.Error(str(e))
            
            self.is_creted = True

            if is_verbose:
                logger.OUT('''
                Created wallet: {}
                Save password to use in the future to unlock this wallet.
                Without password imported keys will not be retrievable.
                "{}"
                '''.format(name, self.password))

        _open_wallets[name] = OpenWallet(name, cipher_suite)
        global _timer
        _timer = Timer(_timeout, lock_all)
        _timer.start()


def setTimeout(time):
    global _timeout
    _timeout = time


def wallet_file(name):
    return config.keosd_wallet_dir() + name + _file_ext


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
    name = wallet_arg(wallet)
    file = wallet_file(name)
    if os.path.isfile(file):
        try:
            os.remove(file)
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
    name = wallet_arg(wallet)
    wallets_ = wallets()
    if name + _file_ext in wallets_:
        _open_wallets[name] = OpenWallet(name)
    else:
        raise errors.Error('''
        There is not any wallet file named
            {}
        '''.format((wallet_file(name))))

    if is_verbose:
        logger.OUT("Opened: {}".format(name))


def lock(wallet, is_verbose=True):
    name = wallet_arg(wallet)
    if _open_wallets[name]:
        _open_wallets[name].cipher_suite = None
    else:
        raise errors.Error('''
        The wallet '{}' is not open.
        '''.format(name))

    if is_verbose:
        logger.OUT("Locked: {}".format(name))


def lock_all(is_verbose=True):
    
    locked = []
    for name, open_wallet in _open_wallets.items():
        _open_wallets[name].cipher_suite = None
        locked.append(name)
    
    if is_verbose:
        if locked:
            logger.OUT("Locked: \n" + ", ".join(locked))
        else:
            logger.OUT("Nothing to lock.")


def unlock(wallet, password=None, is_verbose=True):
    name = wallet_arg(wallet)
    if not password and isinstance(wallet, Wallet):
        password = wallet.password

    if not is_open(name):
        raise errors.Error('''
            The wallet '{}' is not open.
            '''.format(name))

    _manager_id = None
    if not is_unlocked(name):
        try:
            _open_wallets[name].cipher_suite = Fernet(str.encode(password))
            with open(wallet_file(name), "r")  as input:
                keys_ciphered = [key.rstrip('\n') for key in input]

            _manager_id = decrypt(
                    keys_ciphered[0], _open_wallets[name].cipher_suite)
        except Exception as e:
            raise errors.Error('''
                Wrong password.
                ''')
        
    if is_verbose:
        logger.OUT("Unlocked: {}".format(name))    
    
    global _timer
    if _timer:
        _timer.cancel()
    _timer = Timer(_timeout, lock_all)
    _timer.start()
    return _manager_id


def list(is_verbose=True):
    wallets = []
    for name, open_wallet in _open_wallets.items():
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

    name = wallet_arg(wallet)
    key_private = key_arg(key, is_owner_key=True, is_private_key=True)

    with open(wallet_file(name), "a")  as out:
        out.write(encrypt(key_private, _open_wallets[name].cipher_suite) + "\n")

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

    for name, open_wallet in _open_wallets.items():
        if not open_wallet.cipher_suite:
            continue

        owner_key_public = key_arg(
            key, is_owner_key=True, is_private_key=False)
        active_key_public = key_arg(
            key, is_owner_key=False, is_private_key=False)

    
        private_keys_ = private_keys(name, False)

        keys = Node('''
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

        for pair in keys:
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
            logger.OUT("Removed keys from wallet '{}':\n".format(
                name
            ) + "\n".join(trash))
    

def keys(wallet=None, is_verbose=True, is_lock_checked=True):
    name = wallet_arg(wallet)
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
        logger.OUT("keys in all unlocked wallets: \n".format(
            name
        ) + "\n".join(public_keys))

    return public_keys


def private_keys(wallet=None, is_verbose=True):
    keys = []    
    for name, open_wallet in _open_wallets.items():
        if wallet:
            if name != wallet_arg(wallet):
                continue
        is_open_and_unlocked(name)
        
        with open(wallet_file(name), "r")  as input:
            keys_ciphered = [key.rstrip('\n') for key in input]

        for key in keys_ciphered:
            keys.append(decrypt(key, _open_wallets[name].cipher_suite))

    if is_verbose:
        logger.OUT("Private keys in all unlocked wallets: \n".format(
            name
        ) + "\n".join(keys))

    return keys
    

def stop(is_verbose=True):
    lock_all()
    _open_wallets = {}
    global _timer
    if _timer:
        _timer.cancel()

    if is_verbose:
        logger.OUT('''
    All the wallet objects locked and removed from the list of open wallets.''')


class Node():
    def __init__(self, js):
        self.json = None
        cl = ["node", "-e"]
        js = utils.heredoc(js)
        cl.append(js)

        if setup.is_print_command_line:
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
    name = wallet_arg(wallet)
    return name in _open_wallets


def is_unlocked(wallet):
    name = wallet_arg(wallet)
    return is_open(name) and _open_wallets[name].cipher_suite


def is_open_and_unlocked(wallet):
    name = wallet_arg(wallet)
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
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(_file_ext): 
            retval.append(filename)
    return retval


def unlocked():
    retval = []
    for name, open_wallet in _open_wallets.items():
        if is_unlocked(name):
            retval.append(name)
    return retval

