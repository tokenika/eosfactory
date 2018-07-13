import os
import json

import setup
import teos
import cleos
import eosf


class Wallet(cleos.WalletCreate, eosf._Eosf):
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

        is_verbose = self.verify_is_verbose(verbosity)

        self.wallet_dir = eosf.wallet_dir()
        
        if setup.is_use_keosd():
            self.EOSF_TRACE("""
                ######### 
                Create a `Wallet` object with the KEOSD Wallet Manager.
                """)
        else:
            self.EOSF_TRACE("""
                ######### 
                Create a `Wallet` object with the NODEOS wallet plugin.
                """)

        if cleos.is_notrunningnotkeosd_error(self):
            self.ERROR(self.err_msg)
            return

        if not password and not setup.is_use_keosd(): # look for password:
            try:
                with open(self.wallet_dir + setup.password_map, "r") \
                        as input:    
                    password_map = json.load(input)
                    password = password_map[name]

                self.EOSF("""
                    Pasword is restored from the file:
                    {}
                    """.format(self.wallet_dir + setup.password_map))
            except:
                pass

        self.EOSF("""
            Wallet directory is {}
            """.format(self.wallet_dir))

        self.DEBUG("""
            Local node is running: {}
            """.format(cleos.node_is_running()))

        cleos.WalletCreate.__init__(self, name, password, is_verbose)

        self.DEBUG("""
            Name is `{}`
            Wallet URL is {}
            Use keosd status is {}
            self._out:
            {}
            self.err_msg:
            {}
            """.format(
                self.name,
                cleos.wallet_url(), setup.is_use_keosd(),
                self._out,
                self.err_msg
                ))
            
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
                        Created wallet `{}` with the local testnet.
                        Password is saved to the file {} in the wallet directory.
                        """.format(self.name, setup.password_map)
                    )

                else: # password taken from file
                    self.EOSF_TRACE("""Opened wallet `{}`.""".format(self.name))

            else: # KEOSD Wallet Manager
                if not password: # new password
                    self.EOSF_TRACE("""
                        Created wallet `{}` with the `keosd` Wallet Manager.
                        Save password to use in the future to unlock this wallet.
                        Without password imported keys will not be retrievable.
                        {}
                        """.format(self.name, self.password)
                    )

                else: # password introduced
                    self.EOSF_TRACE("""
                        Opened wallet {}
                        """.format(self.name))

        else: # wallet.error:
            if "Wallet already exists" in self.err_msg:
                self.ERROR("Wallet `{}` already exists.".format(self.name))
                return
            if "Invalid wallet password" in self.err_msg:
                self.ERROR("Invalid password.")
                return

            self.ERROR(self.err_msg)


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
            self.ERROR(self.wallet_open.err_msg)
        else:
            self.EOSF("Wallet `{}` opened.".format(self.name))


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
            key = account_or_key.owner_key
            account_name = account_or_key.name
            if key:
                imported_keys.append(key.key_public)
                cleos.WalletImport(key, self.name, is_verbose=-1)
                imported_keys.append(key.key_public)

            key = account_or_key.active_key
            if key:
                imported_keys.append(key.key_public)
                cleos.WalletImport(key, self.name, is_verbose=-1)                    
        except:
            imported_keys.append(account_or_key.key_public)
            cleos.WalletImport(account_or_key, self.name, is_verbose=-1)

        self.EOSF_TRACE("""
            Importing keys of the account '{}' into the wallet '{}'
            """.format(account_name, self.name)
                    )
                    
        wallet_keys = cleos.WalletKeys(is_verbose=-1)
        for key in imported_keys:
            if not key in wallet_keys.json[""]:
                self.ERROR("""
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
            if setup.is_use_keosd():
                wallet_dir_ = os.path.expandvars(teos.get_keosd_wallet_dir())
            else:
                wallet_dir_ = teos.get_node_wallet_dir()
            try:
                with open(wallet_dir_ + setup.account_map, "r") as input:    
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


    def __change_object_name(self):
        # self.OUT("""
        #     The given account object name
        #     `{}`({})
        #     points to an existing account, mapped in a file in directory:
        #     `{}`
        #     Cannot overwrite it, however, the existing name can be changed.
        #     Enter a new name to change, or nothing to escape.
        #     """.format(object_name, name, self.wallet_dir))
        # new_name = input("<<< ")
        # for name, object_name in account_map_.items():
        pass
        #????????????????????????????? TODO 


    def is_name_taken(self, account_object_name):
        account_map_json = eosf.account_map()
        for name, object_name in account_map_json.items():
            if object_name == account_object_name:
                self.__change_object_name()

                self.ERROR("""
                    The given account object name
                    `{}`({})
                    points to an existing account, mapped in a file in directory:
                    `{}`
                    Cannot overwrite it.
                    """.format(object_name, name, self.wallet_dir))
                return False
        return True
            

    def map_account(self, account_object_name, account_object):
        if self.is_name_taken(account_object_name):
            account_map_json = eosf.account_map()
            account_map_json[account_object.name] = account_object_name
            with open(self.wallet_dir + setup.account_map, "w") as out:
                out.write(json.dumps(account_map_json, sort_keys=True, indent=4))

            self.EOSF_TRACE("""
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

