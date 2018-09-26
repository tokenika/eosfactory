import os
import subprocess
import json

from shell.interface import *
import shell.setup as setup
import core.config as config
import core.errors as errors
import core.logger as logger
import core.utils as utils

class Node():
    def __init__(self, js):
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

class WalletManager:

    manager_id = "5JfjYNzKTDoU35RSn6BpXei8Uqs1B6EGNwkEFHaN8SPHwhjUzcX"
    file_ext = ".walletjs"

    def wallet_file(self, name):
        return config.getKeosdWalletDir() + name + WalletManager.file_ext

    def create(self, name, is_verbose=True):        
        password_key = Node('''
            const ecc = require('eosjs-ecc')
            ecc.randomKey().then(print_result)

            function process_result(private_key) {
                return {key_private: private_key, 
                        key_public: ecc.privateToPublic(private_key)}
            }
        ''').json
        password = password_key["key_public"]

        file = self.wallet_file(name)
        if os.path.exists(file):
            raise errors.Error('''
                Cannot overwrite existing wallet file:
                    {}
            '''.format(file))

        with open(file, "w+")  as out:
            out.write(WalletManager.manager_id + "\n")

        if is_verbose:
            logger.OUT('''
        With 'eosjs' interface, wallets are not password-protected, currently.
            ''')

    def open(self, wallet, is_verbose=True):
        name = wallet_arg(wallet)
        if is_verbose:
            logger.OUT("Opened: {}".format(name))

    def lock(self, wallet):
        name = wallet_arg(wallet)
        if is_verbose:
            logger.OUT("Locked: {}".format(name))

    def wallets(self):
        directory = os.fsencode(config.getKeosdWalletDir())
        retval = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(WalletManager.file_ext): 
                retval.append(filename)
        return retval

    def lock_all(self, is_verbose=True):
        if is_verbose:
            logger.OUT("Locked: \n" + ", ".join(self.wallets()))

    def unlock(self, wallet, is_verbose=True):
        name = wallet_arg(wallet)
        if is_verbose:
            logger.OUT("Unlocked: {}".format(name))

    def list(self, is_verbose=True):
        pass

    def import_key(self, key, is_verbose=True):
        key_private = key_arg(key, is_owner_key=True, is_private_key=True)

        with open(self.wallet_file(name), "w")  as out:
            out.write(key_private + "\n")

        key_public = Node('''
            const ecc = require('eosjs-ecc')
            print_result('%s', null)
            function process_result(private_key) {
                return {key_public: ecc.privateToPublic(private_key)}
            }
        ''' % (key_private)).json["key_public"]
        
        import pdb; pdb.set_trace()
        if is_verbose:
            logger.OUT("Imported key: {}".format(name))
        

    def remove_key(self, key, is_verbose=True):
        pass

    def keys(self):
        pass

    def private_keys(self, is_verbose=True):
        pass

    def stop(self, is_verbose=True):
        pass

__wallet_manager = WalletManager()
def wallet_manager():
    return __wallet_manager