import os
import json

import setup
import teos
import cleos
import eosf


class Wallet(cleos.WalletCreate):
    """ Create a new wallet locally and operate it.
    Usage: WalletCreate(name="default", is_verbose=1)

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
    def __init__(self, name="default", password="", verbosity=None):

        self.logger = eosf._Eosf(verbosity)
        self.wallet_dir = eosf.wallet_dir()
        
        if setup.is_use_keosd():
            self.logger.EOSF_TRACE("""
                ######### 
                Create a `Wallet` object with the KEOSD Wallet Manager.
                """)
        else:
            self.logger.EOSF_TRACE("""
                ######### 
                Create a `Wallet` object with the NODEOS wallet plugin.
                """)

        self.logger.EOSF("""
                The wallet directory is
                {}.
                """.format(self.wallet_dir))

        if cleos.is_notrunningnotkeosd_error(self):
            self.logger.ERROR(self.err_msg)
            return self.logger

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

        self.logger.DEBUG("""
            Local node is running: {}
            """.format(cleos.node_is_running()))

        cleos.WalletCreate.__init__(self, name, password, is_verbose=-1)
            
        if not self.error:
            self.logger.OUT(
                self.out_msg
            )

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
                    self.logger.EOSF_TRACE("""
                        Created wallet `{}` with the local testnet.
                        Password is saved to the file {} in the wallet directory.
                        """.format(self.name, setup.password_map)
                    )

                else: # password taken from file
                    self.logger.EOSF_TRACE("Opened wallet `{}`.".format(self.name))

            else: # KEOSD Wallet Manager
                if not password: # new password
                    self.logger.EOSF_TRACE("""
                        Created wallet `{}` with the `keosd` Wallet Manager.
                        Save password to use in the future to unlock this wallet.
                        Without password imported keys will not be retrievable.
                        {}
                        """.format(self.name, self.password)
                    )

                else: # password introduced
                    self.logger.EOSF_TRACE("""
                        Opened wallet {}
                        """.format(self.name))

        else: # wallet.error:
            if "Wallet already exists" in self.err_msg:
                self.logger.ERROR("Wallet `{}` already exists.".format(self.name))
                return
            if "Invalid wallet password" in self.err_msg:
                self.logger.ERROR("Invalid password.")
                return

            self.logger.ERROR(self.err_msg)


    def index(self):
        """ Lists opened wallets, * marks unlocked.
        Returns `cleos.WalletList` object
        """ 
        cleos.WalletList(is_verbose=self.is_verbose)
    

    def open(self):
        """ Opens the wallet.
        Returns `WalletOpen` object
        """
        self.wallet_open = cleos.WalletOpen(
            self.name, is_verbose=self.is_verbose)
        if self.wallet_open.error:
            self.logger.ERROR(self.wallet_open.err_msg)
        else:
            self.logger.EOSF("Wallet `{}` opened.".format(self.name))


    def lock(self):
        """ Locks the wallet.
        Returns `cleos.WalletLock` object.
        """
        self.wallet_lock = cleos.WalletLock(
            self.name, is_verbose=self.is_verbose)


    def unlock(self):
        """ Unlocks the wallet.
        Returns `WalletUnlock` object.
        """
        self.wallet_unlock = cleos.WalletUnlock(
            self.name, self.json["password"], is_verbose=self.is_verbose)


    def import_key(self, account_or_key):
        """ Imports private keys of an account into wallet.
        Returns list of `cleos.WalletImport` objects
        """
        imported_keys = []
        account_name = None
        try: # whether account_or_key is an account:
            account_name = account_or_key.name
            key = account_or_key.owner_key
            if key:
                imported_keys.append(key.key_public)
                cleos.WalletImport(key, self.name, is_verbose=-1)
                imported_keys.append(key.key_public)
            try:
                key = account_or_key.active_key
                if key:
                    imported_keys.append(key.key_public)
                    cleos.WalletImport(key, self.name, is_verbose=-1)
            except:
                pass                    
        except:
            imported_keys.append(account_or_key.key_public)
            cleos.WalletImport(account_or_key, self.name, is_verbose=-1)

        self.logger.EOSF_TRACE("""
            Importing keys of the account '{}' into the wallet '{}'
            """.format(account_name, self.name)
                    )
                    
        wallet_keys = cleos.WalletKeys(is_verbose=-1)
        for key in imported_keys:
            if not key in wallet_keys.json[""]:
                self.logger.ERROR("""
                Failed to import keys of the account '{}' into the wallet '{}'
                """.format(account_name, self.name))


    def restore_accounts(self, namespace):
        account_names = set() # accounts in wallets
        keys = cleos.WalletKeys(is_verbose=0).json

        for key in keys[""]:
            accounts = cleos.GetAccounts(key, is_verbose=0)
            for acc in accounts.json["account_names"]:
                account_names.add(acc)

        if self.is_verbose:
            print("Restored accounts as global variables:")

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
                    if self.is_verbose:
                        print("     {0} ({1})".format(object_name, name))
                    restored[object_name] = account(name, restore=True)
        else:
            if self.is_verbose:
                print("     empty list")

        namespace.update(restored)
        return restored


    def keys(self):
        """ Lists public keys from all unlocked wallets.
        Returns `cleos.WalletKeys` object.
        """
        cleos.WalletKeys(is_verbose=self.is_verbose)


    def edit_account_map(self, text_editor="nano"):
        eosf.edit_account_map(text_editor)


    def is_name_taken(self, account_object_name):

        while True:
            account_map_json = eosf.account_map(self.logger)
            if account_map_json is None:
                return False

            is_taken = False
            for name, object_name in account_map_json.items():
                if object_name == account_object_name:

                    self.logger.ERROR("""
                        The given account object name
                        `{}`({})
                        points to an existing account, mapped in a file in directory:
                        `{}`
                        Cannot overwrite it.

                        However, you can free the name by changing the mapping. 
                        Do you want to edit the file?
                        """.format(object_name, name, self.wallet_dir))

                    is_taken = True
                    break

            if is_taken:
                answer = input("y/n <<< ")
                if answer == "y":
                    eosf.edit_account_map()
                    continue
                else:
                    logger.ERROR("""
            Use the function 'eosf.edit_account_map(text_editor="nano")'
            or the corresponding method of any object of the 'eosf_wallet.Wallet` 
            class to edit the file.
                    """)
                    return False
            else:
                break

        return True
            

    def map_account(self, account_object_name, account_object):

        if not self.is_name_taken(account_object_name):
            account_map_json = eosf.account_map(self.logger)
            if account_map_json is None:
                return

            account_map_json[account_object.name] = account_object_name
            # account_map_json = sorted(
            #     account_map_json.items(), key=lambda x: x[1])
            with open(self.wallet_dir + setup.account_map, "w") as out:
                out.write(json.dumps(account_map_json, sort_keys=False, indent=4))

            self.logger.EOSF_TRACE("""
                Account '{}' mapped as '{}', stored in the file '{}' 
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
        return retval + json.dumps(self.list().json, indent=4) + "\n"

