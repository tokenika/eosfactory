import os
import json
import inspect

import setup
import teos
import front_end
import cleos
import eosf

def wallet_json_read():
    try:
        with open(eosf.wallet_dir() + setup.password_map, "r") as input:    
            return json.load(input)
    except:
        return {}

def wallet_json_write(wallet_json):
    with open(eosf.wallet_dir() + setup.password_map, "w+")  as out:
        json.dump(wallet_json, out)

def create_wallet(
        name=None, password="", verbosity=None, file=False,
        globals=None):
    if globals:
        Wallet.globals = globals
    else:
        Wallet.globals = inspect.stack()[1][0].f_globals

    Wallet.wallet = Wallet(name, password, verbosity, file)
    Wallet.wallet.restore_accounts()

def get_wallet():
    return Wallet.wallet


class Wallet(cleos.WalletCreate):
    ''' Create a new wallet locally and operate it.

    - **parameters**::

        name: The name of the new wallet, defaults to `default`.
        is_verbose: If `0`, do not print unless on error, 
            default is `1`.

    - **attributes**::

        name: The name of the wallet.
        password: The password returned by wallet create.
        error: Whether any error ocurred.
        json: The json representation of the object.
        is_verbose: Verbosity at the constraction time.  
    '''
    wallet_keys = None
    wallet = None
    globals = None
  
    def __init__(self, name=None, password="", verbosity=None, file=False):

        cleos.set_local_nodeos_address_if_none()
        if name is None:
            name = setup.wallet_default_name
        else:
            name = setup.file_prefix() + name

        logger = front_end.Logger(verbosity)
        if not self.wallet is None:
            logger.ERROR('''
            It can be only one ``Wallet`` object in the script; there is one
            named ``{}``.
            '''.format(wallet.name))
            return

        self.wallet_dir = eosf.wallet_dir()

        logger.INFO('''
                * Wallet name is ``{}``, wallet directory is
                    {}.
                '''.format(name, self.wallet_dir))

        if not password: # look for password:
            passwords = wallet_json_read()
            if name in passwords:
                password = passwords[name]
                logger.INFO('''
                    The pasword is restored from the file:
                    {}
                    '''.format(
                        os.path.join(self.wallet_dir, setup.password_map)))

        cleos.WalletCreate.__init__(self, name, password, is_verbose=-1)

        if self.is_created: # new password
            self.INFO('''
                * Created wallet ``{}``.
                '''.format(self.name)
            )            
            if setup.is_local_address or file:           
                password_map = wallet_json_read()
                password_map[name] = self.password
                wallet_json_write(password_map)
                self.INFO('''
                    * Password is saved to the file ``{}`` in the wallet directory.
                    '''.format(setup.password_map)
                )
            else:
                self.OUT(self.out_msg)
        else:
            self.TRACE('''
                    Opened wallet ``{}``
                    '''.format(self.name))            

    def index(self):
        ''' Lists opened wallets, * marks unlocked.
        Returns `cleos.WalletList` object
        ''' 
        result = cleos.WalletList(is_verbose=0)
        self.OUT(result.out_msg)
    
    def open(self):
        ''' Opens the wallet.
        Returns `WalletOpen` object
        '''
        result = cleos.WalletOpen(self.name, is_verbose=-1)
        if not self.ERROR(result):
            self.TRACE('''
            * Wallet ``{}`` opened.
            '''.format(self.name))

    def lock(self):
        ''' Lock the wallet.
        Returns `cleos.WalletLock` object.
        '''
        result = cleos.WalletLock(self.name, is_verbose=-1)
        if not self.ERROR(result):
            self.TRACE("Wallet `{}` locked.".format(self.name))

    def lock_all(self):
        ''' Lock the wallet.
        Returns `cleos.WalletLock` object.
        '''
        result = cleos.WalletLockAll(is_verbose=-1)
        if not self.ERROR(result):
            self.TRACE("All wallets locked.")

    def unlock(self):
        ''' Unlock the wallet.
        Returns `WalletUnlock` object.
        '''
        result = cleos.WalletUnlock(
            self.name, self.password, is_verbose=-1)
        if not self.ERROR(result):
            self.TRACE('''
            * Wallet ``{}`` unlocked.
            '''.format(self.name))

    def open_unlock(self):
        ''' Open&Unlock automatics.
        '''
        result = cleos.WalletOpen(self.name, is_verbose=-1)
        if not result.error:
            result = cleos.WalletUnlock(
                self.name, self.password, is_verbose=-1)
            if not result.error:
                return
        self.ERROR(result)

    def remove_key(self, account_or_key):
        '''
        '''
        self.open_unlock()

        removed_keys = []
        account_name = None
        if isinstance(account_or_key, cleos.Account):
            cleos.WalletRemove_key(
                self._key_arg(
                    account_or_key, is_owner_key=True, is_private_key=True), 
                self.name, is_verbose=-1)
            removed_keys.append(self._key_arg(
                    account_or_key, is_owner_key=True, is_private_key=False))

            cleos.WalletRemove_key(
                self._key_arg(
                    account_or_key, is_owner_key=False, is_private_key=True), 
                self.name, is_verbose=-1)
            removed_keys.append(self._key_arg(
                    account_or_key, is_owner_key=False, is_private_key=False))
        else:
            cleos.WalletRemove_key(
                self._key_arg(
                    account_or_key, is_private_key=True), 
                self.name, is_verbose=-1)
            removed_keys.append(self._key_arg(
                    account_or_key, is_private_key=False))

        if account_name is None:
            if len(removed_keys) > 0:
                self.TRACE('''
                    Removing key '{}' 
                    from the wallet '{}'
                    '''.format(removed_keys[0], self.name)
                            )
        else:            
            self.TRACE('''
                Removing keys of the account '{}' from the wallet '{}'
                '''.format(account_name, self.name)
                        )        

        wallet_keys = cleos.WalletKeys(is_verbose=-1)

        ok = True
        for key in removed_keys:
            if key in wallet_keys.json[""]:
                ok = False
                err_msg = '''
                Failed to remove key '{}' from the wallet '{}'
                '''.format(key, self.name)

                self.ERROR(self.err_msg)
                return False
        if ok:
            self.TRACE('''
            * Cross-checked: all listed keys removed from the wallet.
            ''')
        return True


    def import_key(self, account_or_key):
        ''' Imports private keys of an account into wallet.
        Returns list of `cleos.WalletImport` objects
        '''
        self.open_unlock()

        imported_keys = []
        account_name = None
        if isinstance(account_or_key, cleos.Account):
            account_name = account_or_key.name
            wallet_import = cleos.WalletImport(
                self._key_arg(
                    account_or_key, is_owner_key=True, is_private_key=True), 
                self.name, is_verbose=-1)
            imported_keys.append(self._key_arg(
                    account_or_key, is_owner_key=True, is_private_key=False))

            wallet_import = cleos.WalletImport(
                self._key_arg(
                    account_or_key, is_owner_key=False, is_private_key=True), 
                self.name, is_verbose=-1)
            imported_keys.append(self._key_arg(
                    account_or_key, is_owner_key=False, is_private_key=False))
            self.TRACE('''
                * Importing keys of the account ``{}`` into the wallet ``{}``
                '''.format(account_name, self.name)
                )
        else:           
            wallet_import = cleos.WalletImport(
                self._key_arg(account_or_key, is_private_key=True), 
                self.name, is_verbose=-1)
            if self.ERROR(wallet_import):
                return False
            else:
                self.TRACE('''
                    * Importing keys into the wallet ``{}``
                    '''.format(self.name)
                            )
                return True
        
        wallet_keys = cleos.WalletKeys(is_verbose=-1)

        if len(imported_keys) == 0:
            err_msg = '''
                The list of imported keys is empty.
                '''
            self.ERROR(err_msg)
            return False

        ok = True
        for key in imported_keys:
            if not key in wallet_keys.json[""]:
                ok = False
                err_msg = '''
                Failed to import keys of the account '{}' into the wallet '{}'
                '''.format(
                    account_name if account_name else "n/a", self.name)

                self.ERROR(err_msg)
                return False
        if ok:
            self.TRACE('''
            * Cross-checked: all account keys are in the wallet.
            ''')
        return True

    def keys_in_wallets(self, keys):
        self.open_unlock()

        result = cleos.WalletKeys(is_verbose=-1)
        for key in keys:
            if not key in result.json[""]:
                return False
        return True

    def restore_accounts(self):
        '''
        '''
        self.open_unlock()

        account_map = eosf.account_map()
        new_map = {}
        wallet_keys = cleos.WalletKeys(is_verbose=0)
        if len(account_map) > 0:
            self.INFO('''
                    ######### Restored accounts as global variables:
                    ''') 

            for name, object_name in account_map.items():
                account_ = cleos.GetAccount(name, json=True, is_verbose=-1)
                if not account_.error:
                    if account_.owner_key in wallet_keys.json[""] and \
                            account_.active_key in wallet_keys.json[""]:
                        new_map[name] = object_name
                        from eosf_account import create_account
                        create_account(
                            object_name, name, restore=True, verbosity=None)

                    self.INFO('''
                         {}
                    '''.format(object_name))

            eosf.save_account_map(new_map)
        else:
            self.INFO('''
                 * The wallet is empty.
            ''')

    def keys(self):
        ''' Lists public keys from all unlocked wallets.
        Returns `cleos.WalletKeys` object.
        '''
        self.open_unlock()

        self.wallet_keys = cleos.WalletKeys(is_verbose=-1)
        self.TRACE('''
            Keys in all open walets:
            {}
            '''.format(self.wallet_keys.out_msg))

    def edit_account_map(self, text_editor="nano"):
        eosf.edit_account_map(text_editor)

    def is_name_taken(self, account_object_name, account_name):
        while True:
            account_map_json = eosf.account_map(self)
            if account_map_json is None:
                return False

            is_taken = False
            for name, object_name in account_map_json.items():
                if object_name == account_object_name:
                    if not name == account_name:                    
                        self.ERROR('''
                The given account object name
                ``{}``
                points to an existing account, of the name {},
                mapped in a file in directory:
                {}
                Cannot overwrite it.

                However, you can free the name by changing the mapping. 
                Do you want to edit the file?
                '''.format(
                    account_object_name, name, self.wallet_dir), is_fatal=False)
                        is_taken = True
                        break

            if is_taken:
                answer = input("y/n <<< ")
                if answer == "y":
                    eosf.edit_account_map()
                    continue
                else:
                    self.ERROR('''
            Use the function 'eosf.edit_account_map(text_editor="nano")'
            or the corresponding method of any object of the 'eosf_wallet.Wallet` 
            class to edit the file.
                    ''')
                    return True
            else:
                break

        return False
            

    def map_account(self, account_object_name, account_object):
        '''
        '''
        if not self.is_name_taken(account_object_name, account_object.name):
            account_map_json = eosf.account_map(self)
            if account_map_json is None:
                return

            account_map_json[account_object.name] = account_object_name

            with open(self.wallet_dir + setup.account_map, "w") as out:
                out.write(json.dumps(
                    account_map_json, indent=3, sort_keys=True))

            self.TRACE('''
                * Account ``{}`` stored in the file 
                    ``{}`` in the wallet directory:
                    {}
                '''.format(
                    account_object_name,
                    setup.account_map,
                    self.wallet_dir + setup.account_map))


