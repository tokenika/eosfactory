import os
import subprocess
import json
from cryptography.fernet import Fernet

from shell.interface import *
import shell.setup as setup
import core.config as config
import core.errors as errors
import core.logger as logger
import core.utils as utils

class OpenWallet:
    def __init__(self, name, cipher_suite=None):
        self.name = name
        self.cipher_suite = cipher_suite

manager_id = "5JfjYNzKTDoU35RSn6BpXei8Uqs1B6EGNwkEFHaN8SPHwhjUzcX"
file_ext = ".eosfwallet"
open_wallets = {}


def wallet_file(name):
    return config.getKeosdWalletDir() + name + file_ext


def encrypt(name, password, append):
        # plaintext = manager_id + "\n"
        # ciphertext = encrypt(password, plaintext)
        # plaintext = decrypt('password', ciphertext) 
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
# encoded_text = cipher_suite.encrypt(str.encode(x))
# decoded_text = cipher_suite.decrypt(encoded_text).decode("utf-8").splitlines()

    pass


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


# def decrypt(name, password):
#     with open((wallet_file(name), "r")  as input:
#         data = input.read()
#     plaintext = decrypt('password', data)
#     keys = plaintext.splitlines()
#     cipher_suite = Fernet(key)


class Create:
    def __init__(self, name="default", is_verbose=True):
        self.name = name
        file = wallet_file(name)
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
                out.write(
                    cipher_suite.encrypt(
                        str.encode(manager_id)).decode("utf-8") + "\n")
        except Exception as e:
            raise errors.Error(str(e))
        
        open_wallets[name] = OpenWallet(name, cipher_suite)

        if is_verbose:
            logger.OUT('''
            Created wallet: {}
            Save password to use in the future to unlock this wallet.
            Without password imported keys will not be retrievable.
            "{}"
            '''.format(name, self.password))


def open_wallet(wallet, is_verbose=True):
    name = wallet_arg(wallet)
    wallets_ = wallets()
    if name + file_ext in wallets_:
        open_wallets[name] = OpenWallet(name)
    else:
        raise errors.Error('''
        There is not any wallet file named
            {}
        '''.format((wallet_file(name))))

    if is_verbose:
        logger.OUT("Opened: {}".format(name))


def lock(wallet):
    name = wallet_arg(wallet)
    if open_wallets[name]:
        open_wallets[name].cipher_suite = None
    else:
        raise errors.Error('''
        The wallet '{}' is not open.
        '''.format(name))

    if is_verbose:
        logger.OUT("Locked: {}".format(name))


def lock_all(is_verbose=True):
    locked = []
    for name, cipher_suite in open_wallets.items():
        open_wallets[name] = None
        locked.append(name)
    
    if is_verbose:
        if locked:
            logger.OUT("Locked: \n" + ", ".join(locked))
        else:
            logger.OUT("Nothing to lock.")


def unlock(wallet, password, is_verbose=True):
    name = wallet_arg(wallet)
    manager_id = None
    if open_wallets[name]:
        keys_ = private_keys(name, False)
        cipher_suite = Fernet(str.encode(password))
        try:
            manager_id = cipher_suite.decrypt(
                str.encode(keys_[0])).decode("utf-8")
        except:
            raise errors.Error('''
                Wrong password.
                ''')
    else:
        raise errors.Error('''
        The wallet '{}' is not opened.
        '''.format(name))

    open_wallets[name].cipher_suite = cipher_suite
    if is_verbose:
        logger.OUT("Unlocked: {}".format(name))    

    return manager_id


def list(is_verbose=True):
    wallets = []
    for name, cipher_suite in open_wallets.items():
        if cipher_suite:
            wallets.append("* " + name)
        else:
            wallets.append(name)

    if is_verbose:
        if wallets:
            logger.OUT('''
        Opened wallets. Starlet, if any, means 'unlocked':\n''' 
            + "\n".join(wallets))
        else:
            logger.OUT("There is not any wallet open.")            


def import_key(wallet, key, is_verbose=True):
    name = wallet_arg(wallet)
    key_private = key_arg(key, is_owner_key=True, is_private_key=True)

    with open(wallet_file(name), "a")  as out:
        out.write(key_private + "\n")

    key_public = Node('''
        const ecc = require('eosjs-ecc')
        print_result('%s', null)
        function process_result(private_key) {
            return {key_public: ecc.privateToPublic(private_key)}
        }
    ''' % (key_private)).json["key_public"]

    if is_verbose:
        logger.OUT("Imported key to wallet '{}':\n{}".format(
            name, key_public))
    
    return key_public
    

def remove_key(wallet, key, is_verbose=True):
    name = wallet_arg(wallet)
    owner_key_public = key_arg(
        key, is_owner_key=True, is_private_key=False)
    active_key_public = key_arg(
        key, is_owner_key=False, is_private_key=False)
    private_keys = private_keys(wallet, False)

    keys = Node('''
    const ecc = require('eosjs-ecc')
    keys = %s
    print_result(keys)

    function process_result(keys) {
        public_keys = []
        for (i = 0; i < keys.length; i++) {
            pair = []
            pair[0] = keys[i]
            pair[1] = ecc.privateToPublic(keys[i])
            public_keys[i] = pair
        }

        return public_keys
    }
    ''' % private_keys).json

    trash = []
    for pair in keys:
        if pair[1] == owner_key_public or pair[1] == active_key_public:
            trash.append(pair[0])

    if trash:
        remaining = []
        for private_key in private_keys:
            if not private_key in trash:
                remaining.append(private_key)

        with open(wallet_file(name), "w")  as out:
            out.write("\n".join(remaining))
    
    if is_verbose:
        if trash:
            logger.OUT("Removed keys from wallet '{}':\n".format(
                name
            ) + "\n".join(trash))
    

def keys(wallet, is_verbose=True):
    name = wallet_arg(wallet)
    private_keys_ = private_keys(wallet, False)
    public_keys = Node('''
    const ecc = require('eosjs-ecc')
    keys = %s
    print_result(keys)

    function process_result(keys) {
        var public_keys = []
        for (i = 0; i < keys.length; i++) {
            public_keys[i] = ecc.privateToPublic(keys[i])
        }

        return public_keys
    }
    ''' % private_keys_).json
    if is_verbose:
        logger.OUT("keys in wallet '{}': \n".format(
            name
        ) + "\n".join(public_keys))


def private_keys(wallet, is_verbose=True):
    name = wallet_arg(wallet)
    with open(wallet_file(name), "r")  as input:
        keys = [key.rstrip('\n') for key in input]
    if is_verbose:
        logger.OUT("private keys in wallet '{}': \n".format(
            name
        ) + "\n".join(keys))

    return keys
    

def stop(is_verbose=True):
    pass

def wallets():
    directory = os.fsencode(config.getKeosdWalletDir())
    retval = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(file_ext): 
            retval.append(filename)
    return retval


class Node():
    def __init__(js):
        self.out_msg = None
        self.err_msg = None
        self.json = None
        cl = ["node", "-e"]
        header = '''
            no_error_tag = 'OK'

            function print_result(result, err) {
                if (err) {
                    console.error(err)
                }
                else {
                    result = process_result(result)
                    console.error(no_error_tag)
                    console.log(JSON.stringify(result))
                }
            }

            function process_result(result) {
                return result
            }
        '''
        js = utils.heredoc(header + js)
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
        self.err_msg = process.stderr.decode("utf-8")
        if self.err_msg.strip() != "OK":
            raise errors.Error(self.err_msg)

        self.out_msg = process.stdout.decode("utf-8")
        self.json = json.loads(self.out_msg)

    def __str__(self):
        return json.dumps(self.json, sort_keys=True, indent=4)

    def __repr__(self):
        return ""