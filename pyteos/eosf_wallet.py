import os
import json

import setup
import teos
import cleos
import eosf

wallet = None

class Wallet(eosf.Logger, cleos.WalletCreate):
    """ Create a new wallet locally and operate it.

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
    """

    def error_map(self, err_msg):

        if "Wallet already exists" in err_msg:
            return"""
                Wallet `{}` already exists.
                """.format(self.name)

        if "Error 3120002: Nonexistent wallet" in err_msg:
            return """
                Wallet ``{}`` does not exist.
                """.format(self.name)
 
        if "Invalid wallet password" in err_msg:
            return "Invalid password."

        return err_msg

    wallet_keys = None
    
    def __init__(self, name="default", password="", verbosity=None):
        eosf.Logger.__init__(self, verbosity)

        global wallet
        if not wallet is None:
            self.ERROR("""
            It can be only one ``Wallet`` object in the script; there is one
            named ``{}``.
            """.format(wallet.name))
            return

        wallet = self
        self.wallet_dir = eosf.wallet_dir()
        
        if setup.is_use_keosd():
            self.EOSF_TRACE("""
                ######### Create a `Wallet` object with the KEOSD Wallet Manager.
                """)
        else:
            self.EOSF_TRACE("""
                ######### Create a `Wallet` object with the NODEOS wallet plugin.
                """)

        self.EOSF("""
                * Wallet directory is
                    {}.
                """.format(self.wallet_dir))

        if self.ERROR(cleos.is_notrunningnotkeosd_error()):
            return

        if not password and not setup.is_use_keosd(): # look for password:
            try:
                with open(self.wallet_dir + setup.password_map, "r") \
                        as input:    
                    password_map = json.load(input)
                    password = password_map[name]

                self.loggerelf.EOSF("""
                    The pasword is restored from the file:
                    {}
                    """.format(self.wallet_dir + setup.password_map))
            except:
                pass

        cleos.WalletCreate.__init__(self, name, password, is_verbose=-1)
            
        if not self.error:
            if not setup.is_use_keosd(): 
                try:
                    with open(self.wallet_dir + setup.password_map, "r") \
                            as input:
                        password_map = json.load(input)
                except:
                    password_map = {}
                password_map[name] = self.password

                with open(self.wallet_dir + setup.password_map, "w+") \
                        as out:
                    json.dump(password_map, out)

                if not password: # new password
                    self.EOSF_TRACE("""
                        * Created wallet ``{}`` with the local testnet.
                        * Password is saved to the file ``{}`` in the wallet directory.
                        """.format(self.name, setup.password_map)
                    )

                else: # password taken from file
                    self.EOSF_TRACE("Opened wallet `{}`.".format(self.name))

            else: # KEOSD Wallet Manager
                self.EOSF_TRACE("""
                        Opened wallet ``{}``
                        """.format(self.name))
                if not password: # new password
                    self.OUT(self.out_msg)

        else: # wallet.error:
            self.ERROR(self)

    def index(self):
        """ Lists opened wallets, * marks unlocked.
        Returns `cleos.WalletList` object
        """ 
        result = cleos.WalletList(is_verbose=0)
        self.OUT(result.out_msg)
    
    def open(self):
        """ Opens the wallet.
        Returns `WalletOpen` object
        """
        result = cleos.WalletOpen(self.name, is_verbose=-1)
        if not self.ERROR(result):
            self.EOSF("""
            * Wallet ``{}`` opened.
            """.format(self.name))

    def lock(self):
        """ Lock the wallet.
        Returns `cleos.WalletLock` object.
        """
        result = cleos.WalletLock(self.name, is_verbose=-1)
        if not self.ERROR(result):
            self.EOSF("Wallet `{}` locked.".format(self.name))

    def lock_all(self):
        """ Lock the wallet.
        Returns `cleos.WalletLock` object.
        """
        result = cleos.WalletLock(is_verbose=-1)
        if not self.ERROR(self.error_map(result)):
            self.EOSF("All wallet locked.")                        

    def unlock(self):
        """ Unlock the wallet.
        Returns `WalletUnlock` object.
        """
        result = cleos.WalletUnlock(
            self.name, self.json["password"], is_verbose=-1)
        if not self.ERROR(result):
            self.EOSF("""
            * Wallet ``{}`` unlocked.
            """.format(self.name))

    def remove_key(self, account_or_key):
        """
        """
        removed_keys = []
        account_name = None
        try: # whether account_or_key is an account:
            account_name = account_or_key.name
            key = account_or_key.owner_key
            removed_keys.append(key.key_public)

            remove_key = cleos.WalletRemove_key(
                key, self.name, self.password, is_verbose=-1)
            removed_keys.append(key.key_public)

            try: # the account may have active key, as well:
                key = account_or_key.active_key
                remove_key = cleos.WalletRemove_key(
                    key, self.name, self.password, is_verbose=-1)
                removed_keys.append(key.key_public)
            except:
                pass                    
        except:
            try:
                cleos.WalletRemove_key(
                    account_or_key, self.name, self.password, is_verbose=-1)
                removed_keys.append(account_or_key.key_public)
            except: # account_or_key is string
                remove_key = cleos.WalletRemove_key(
                    account_or_key, self.name, self.password, is_verbose=-1)
                removed_keys.append(account_or_key)

        if account_name is None:
            if len(removed_keys) > 0:
                self.EOSF_TRACE("""
                    Removing key '{}' 
                    from the wallet '{}'
                    """.format(removed_keys[0], self.name)
                            )
        else:            
            self.EOSF_TRACE("""
                Removing keys of the account '{}' from the wallet '{}'
                """.format(account_name, self.name)
                        )        

        wallet_keys = cleos.WalletKeys(is_verbose=-1)

        ok = True
        for key in removed_keys:
            if key in wallet_keys.json[""]:
                ok = False
                err_msg = """
                Failed to remove key '{}' from the wallet '{}'
                """.format(key, self.name)

                self.ERROR(self.err_msg)
                return False
        if ok:
            self.EOSF("""
            * Cross-checked: all listed keys removed from the wallet.
            """)
        return True


    def import_key(self, account_or_key):
        """ Imports private keys of an account into wallet.
        Returns list of `cleos.WalletImport` objects
        """
        imported_keys = []
        account_name = None
        try: # whether account_or_key is an account:
            account_name = account_or_key.name  
            key = account_or_key.owner_key
            imported_keys.append(key.key_public)

            wallet_import = cleos.WalletImport(
                key, self.name, is_verbose=-1)
            imported_keys.append(key.key_public)

            try:
                key = account_or_key.active_key
                imported_keys.append(key.key_public)

                wallet_import = cleos.WalletImport(
                    key, self.name, is_verbose=-1)
                
            except:
                pass                    
        except:
            cleos.WalletImport(account_or_key, self.name, is_verbose=-1)
            imported_keys.append(account_or_key.key_public)            

        self.EOSF_TRACE("""
            * Importing keys of the account ``{}`` into the wallet '{}'
            """.format(account_name, self.name)
                    )
        wallet_keys = cleos.WalletKeys(is_verbose=-1)

        if len(imported_keys) == 0:
            err_msg = """
                The list of imported keys is empty.
                """
            self.ERROR(err_msg)
            return False

        ok = True
        for key in imported_keys:
            if not key in wallet_keys.json[""]:
                ok = False
                err_msg = """
                Failed to import keys of the account '{}' into the wallet '{}'
                """.format(account_name, self.name)

                self.ERROR(err_msg)
                return False
        if ok:
            self.EOSF("""
            * Cross-checked: all account keys are in the wallet.
            """)
        return True

    def keys_in_wallets(self, keys):
        result = cleos.WalletKeys(is_verbose=-1)
        for key in keys:
            if not key in result.json[""]:
                return False
        return True

    def restore_accounts(self, namespace):
        """
        """
        account_names = set() # accounts in wallets
        keys = cleos.WalletKeys(is_verbose=0).json

        for key in keys[""]:
            accounts = cleos.GetAccounts(key, is_verbose=0)
            for acc in accounts.json["account_names"]:
                account_names.add(acc)

        self.EOSF("""
                Restored accounts as global variables:
                """)

        restored = dict()
        if len(account_names) > 0:
            try:
                with open(self.wallet_dir + setup.account_map, "r") as input:    
                    account_map = json.load(input)
            except:
                account_map = {}
            
            object_names = set()

            for name in account_names:
                try:
                    object_name = account_map[name]
                    if object_name in object_names:
                        object_name = object_name + "_" + name
                except:
                    object_name = name
                object_names.add(object_name)

                if object_name:
                    self.EOSF("""
                         {} ({})
                    """.format(object_name, name))
                    restored[object_name] = account(name, restore=True)
        else:
            self.EOSF("""
                 empty list
            """)

        namespace.update(restored)
        return restored

    def keys(self):
        """ Lists public keys from all unlocked wallets.
        Returns `cleos.WalletKeys` object.
        """
        self.wallet_keys = cleos.WalletKeys(is_verbose=-1)
        self.EOSF("""
            Keys in all open walets:
            {}
            """.format(self.wallet_keys.out_msg))

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
                        self.ERROR("""
                The given account object name
                `{}`({})
                points to an existing account, of the name {},
                mapped in a file in directory:
                `{}`
                Cannot overwrite it.

                However, you can free the name by changing the mapping. 
                Do you want to edit the file?
                """.format(
                    account_object_name, account_name, name, self.wallet_dir))
                        is_taken = True
                        break

            if is_taken:
                answer = input("y/n <<< ")
                if answer == "y":
                    eosf.edit_account_map()
                    continue
                else:
                    self.ERROR("""
            Use the function 'eosf.edit_account_map(text_editor="nano")'
            or the corresponding method of any object of the 'eosf_wallet.Wallet` 
            class to edit the file.
                    """)
                    return True
            else:
                break

        return False
            

    def map_account(self, account_object_name, account_object):
        if not self.is_name_taken(account_object_name, account_object.name):
            account_map_json = eosf.account_map(self)
            if account_map_json is None:
                return

            account_map_json[account_object.name] = account_object_name

            with open(self.wallet_dir + setup.account_map, "w") as out:
                out.write(eosf.account_mapp_to_string(account_map_json))

            self.EOSF_TRACE("""
                * Account ``{}`` mapped as '{}', stored in the file ``{}`` 
                    in the wallet directory:
                    {}
                """.format(
                    account_object.name,
                    account_object_name,
                    setup.account_map,
                    self.wallet_dir + setup.account_map))


    def info(self):
        retval = json.dumps(self.json, indent=4) + "\n"
        retval = retval + json.dumps(self.keys().json, indent=4) + "\n"
        print(retval + json.dumps(self.list().json, indent=4) + "\n")

