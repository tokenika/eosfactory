import os
import json

import setup
import teos
import cleos
import eosf

wallet = None

def wallet_json_read():
    try:
        with open(eosf.wallet_dir() + setup.password_map, "r") as input:    
            return json.load(input)
    except:
        return {}

def wallet_json_write(wallet_json):
    with open(eosf.wallet_dir() + setup.password_map, "w+")  as out:
        json.dump(wallet_json, out)

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
            return eosf.WalletExists(
                eosf.WalletExists.msg_template.format(self.name))

        if "Error 3120002: Nonexistent wallet" in err_msg:
            return eosf.WalletNotExist(
                eosf.WalletNotExist.msg_template.format(self.name))
 
        if "Invalid wallet password" in err_msg:
            return eosf.InvalidPassword(
                eosf.InvalidPassword.msg_template.format(self.name))

        if not err_msg:
            return None
        return eosf.Error(err_msg)

    wallet_keys = None
  
    def __init__(self, name=None, password="", verbosity=None):
        eosf.Logger.__init__(self, verbosity)
        if name is None:
            name = setup.wallet_default_name

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
                * Wallet name is {}, wallet directory is
                    {}.
                """.format(name, self.wallet_dir))

        if self.ERROR(cleos.is_notrunningnotkeosd_error()):
            return

        if not password and not setup.is_use_keosd(): # look for password:
            password_map = wallet_json_read()
            try:
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
                password_map = wallet_json_read()
    
                password_map[name] = self.password
                wallet_json_write(password_map)

                if not password: # new password
                    self.EOSF("""
                        * Created wallet ``{}`` with the local testnet.
                        * Password is saved to the file ``{}`` in the wallet directory.
                        """.format(self.name, setup.password_map)
                    )

                else: # password taken from file
                    self.EOSF("Opened wallet `{}`.".format(self.name))

            else: # KEOSD Wallet Manager
                self.EOSF("""
                        Opened wallet ``{}``
                        """.format(self.name))
                if not password: # new password
                    self.OUT(self.out_msg)

                self.restore_accounts()

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
        if not self.ERROR(result):
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
                self.EOSF("""
                    Removing key '{}' 
                    from the wallet '{}'
                    """.format(removed_keys[0], self.name)
                            )
        else:            
            self.EOSF("""
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
        if isinstance(account_or_key, cleos.Account):
            cleos.WalletImport(
                self._key_arg(
                    account_or_key, is_owner_key=True, is_private_key=True), 
                self.name, is_verbose=-1)
            imported_keys.append(self._key_arg(
                    account_or_key, is_owner_key=True, is_private_key=False))

            cleos.WalletImport(
                self._key_arg(
                    account_or_key, is_owner_key=False, is_private_key=True), 
                self.name, is_verbose=-1)
            imported_keys.append(self._key_arg(
                    account_or_key, is_owner_key=False, is_private_key=False))
        else:
            cleos.WalletImport(
                self._key_arg(
                    account_or_key, is_private_key=True), 
                self.name, is_verbose=-1)
            imported_keys.append(self._key_arg(
                    account_or_key, is_private_key=False))

        self.EOSF("""
            * Importing keys of the account ``{}`` into the wallet ``{}``
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

    def restore_accounts(self):
        """
        """
        account_names = set() # accounts in wallets
        keys = cleos.WalletKeys(is_verbose=0).json

        for key in keys[""]:
            accounts = cleos.GetAccounts(key, is_verbose=0)
            for acc in accounts.json["account_names"]:
                account_names.add(acc)

        restored = dict()
        if len(account_names) > 0:
            self.EOSF("""
                    ######### Restored accounts as global variables:
                    """)
                        
            account_map = eosf.account_map()           
            object_names = set()

            # account_names: {'vqodjjlemsc5', 'cgecc2d4pgvm', 'tlb54yedjgzq'}
            for name in account_names: 
                try: 
                    object_name = account_map[name]
                    # one object name with the another account
                    if object_name in object_names: 
                        object_name = object_name + "_" + name
                except:
                    object_name = name
                object_names.add(object_name)

                if object_name:
                    self.EOSF("""
                         {} ({})
                    """.format(object_name, name))
                    from eosf_account import account_create
                    restored[object_name] = account_create(
                        object_name, name, restore=True, verbosity=[])
        else:
            self.EOSF("""
                 * The wallet is empty.
            """)

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

            self.EOSF("""
                * Account ``{}`` mapped as ``{}``, stored in the file 
                    ``{}`` in the wallet directory:
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

