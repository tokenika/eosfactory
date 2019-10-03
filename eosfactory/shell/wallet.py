"""Wallet object singleton"""

import os
import json
import inspect
import importlib

import eosfactory.core.setup as setup
import eosfactory.core.manager as manager
import eosfactory.core.errors as errors
import eosfactory.core.config as config
import eosfactory.core.logger as logger
import eosfactory.core.interface as interface
BASE_COMMANDS = importlib.import_module(".base", setup.interface_package())


class Wallet(BASE_COMMANDS.WalletCreate):
    """ Create a new wallet locally and operate it.

    Args:

        name (str): The name of the new wallet, defaults to `default`.
        password (str): The password to the wallet, if the wallet exists. 
    """
    wallet_singleton = None
    wallet_globals = {}

    def __init__(self, name=None, password="", save_password=False):
        setup.set_local_nodeos_address_if_none()
        if not name:
            name = setup.WALLET_DEFAULT_NAME
        else:
            name = setup.file_prefix() + name

        if Wallet.wallet_singleton:
            raise errors.Error("""
            It can be only one ``Wallet`` object in the script; there is one
            named ``{}``.
            """.format(Wallet.wallet_singleton.name))

        self.wallet_dir = config.keosd_wallet_dir()

        logger.INFO("""
                * Wallet name is ``{}``, wallet directory is
                    {}.
                """.format(name, self.wallet_dir))

        if not password: # look for password:
            password = read_password(name)
            if password:
                if BASE_COMMANDS.WalletCreate.exists(name):
                    logger.INFO("""
                        The password is restored from the file:
                        {}
                        """.format(os.path.join(password_file(name))))
                else:
                    password = None
                    
        BASE_COMMANDS.WalletCreate.__init__(
                                        self, name, password, is_verbose=False)
        if self.is_created: # new password
            logger.INFO("""
                * Created wallet ``{}``.
                """.format(self.name)
            )

            if save_password or setup.WALLET_SAVE_PASSWORD:
                with open(password_file(self.name), "w+")  as _:
                    _.write(self.password)
                
                # Cross-check:
                password = read_password(self.name)
                if not password == self.password:
                    raise errors.Error("""
The password to the newly created wallet {} is lost, perhaps, accidentally.
Retry. 
                """.format(self.name))
                try:
                    BASE_COMMANDS.WalletLock(self.name, is_verbose=False)
                    BASE_COMMANDS.WalletUnlock(
                                    self.name, password, is_verbose=False)
                except:
                    raise errors.Error("""
The password to the newly created wallet {} is lost, perhaps, accidentally.
Retry. 
                """.format(self.name))

                logger.INFO("""
                    * Password is saved to the file ``{}`` 
                    in the wallet directory.
                    """.format(password_file(self.name))
                )
            else:
                logger.OUT(self.out_msg)
        else:
            logger.TRACE("""
                    Opened wallet ``{}``
                    """.format(self.name))            

    def index(self):
        """ Lists opened wallets, * marks unlocked.
        Returns `BASE_COMMANDS.WalletList` object
        """ 
        result = BASE_COMMANDS.WalletList(is_verbose=0)
        logger.OUT(result.out_msg)
    
    def open(self):
        """ Opens the wallet.
        Returns `WalletOpen` object
        """
        BASE_COMMANDS.WalletOpen(self.name, is_verbose=False)
        logger.TRACE("""
        * Wallet ``{}`` opened.
        """.format(self.name))

    def lock(self):
        """ Lock the wallet.
        Returns `BASE_COMMANDS.WalletLock` object.
        """
        BASE_COMMANDS.WalletLock(self.name, is_verbose=False)
        logger.TRACE("Wallet `{}` locked.".format(self.name))

    def lock_all(self):
        """ Lock the wallet.
        Returns `BASE_COMMANDS.WalletLock` object.
        """
        BASE_COMMANDS.WalletLockAll(is_verbose=False)
        logger.TRACE("All wallets locked.")

    def unlock(self):
        """ Unlock the wallet.
        Returns `WalletUnlock` object.
        """
        BASE_COMMANDS.WalletUnlock(
            self.name, self.password, is_verbose=False)
        logger.TRACE("""
        * Wallet ``{}`` unlocked.
        """.format(self.name))

    def open_unlock(self):
        """ Open & Unlock.
        """
        BASE_COMMANDS.WalletOpen(self.name, is_verbose=False)
        BASE_COMMANDS.WalletUnlock(self.name, self.password, is_verbose=False)

    def remove_key(self, account_or_key):
        """Remove key from wallet.

        Args:
            account_or_key (str or .interface.Key or .interface.Account):
                A public key to remove. If ``account_or_key`` is an 
                .interface.Account object, both owner and active keys are 
                removed.
        """
        self.open_unlock()

        removed_keys = []
        account_name = None
        if isinstance(account_or_key, interface.Account):
            BASE_COMMANDS.WalletRemove_key(
                interface.key_arg(
                    account_or_key, is_owner_key=True, is_private_key=True), 
                self.name, self.password, is_verbose=False)
            removed_keys.append(interface.key_arg(
                    account_or_key, is_owner_key=True, is_private_key=False))

            BASE_COMMANDS.WalletRemove_key(
                interface.key_arg(
                    account_or_key, is_owner_key=False, is_private_key=True), 
                self.name, self.password, is_verbose=False)
            removed_keys.append(interface.key_arg(
                    account_or_key, is_owner_key=False, is_private_key=False))
        else:
            BASE_COMMANDS.WalletRemove_key(
                interface.key_arg(
                    account_or_key, is_private_key=True), 
                self.name, self.password, is_verbose=False)
            removed_keys.append(interface.key_arg(
                    account_or_key, is_private_key=False))

        if not account_name:
            if len(removed_keys) > 0:
                logger.TRACE("""
                    Removing key '{}' 
                    from the wallet '{}'
                    """.format(removed_keys[0], self.name)
                            )
        else:            
            logger.TRACE("""
                Removing keys of the account '{}' from the wallet '{}'
                """.format(account_name, self.name)
                        )        

        wallet_keys = BASE_COMMANDS.WalletKeys(is_verbose=False)

        for key in removed_keys:
            if key in wallet_keys.json:
                raise errors.Error("""
                Failed to remove key '{}' from the wallet '{}'
                """.format(key, self.name))

        logger.TRACE("""
        * Cross-checked: all listed keys removed from the wallet.
        """)
        return True

    def import_key(self, account_or_key):
        """ Imports private keys into wallet.

        Return list of `BASE_COMMANDS.WalletImport` objects

        Args:
            account_or_key (str or .interface.Key or .interface.Account):
                A private key to import. If ``account_or_key`` is an 
                .interface.Account object, both owner and active keys are 
                imported.
        """
        self.open_unlock()
        imported_keys = []
        account_name = None
        if isinstance(account_or_key, interface.Account):
            account_name = account_or_key.name
            BASE_COMMANDS.WalletImport(
                interface.key_arg(
                    account_or_key, is_owner_key=True, is_private_key=True), 
                self.name, is_verbose=False)
            imported_keys.append(interface.key_arg(
                    account_or_key, is_owner_key=True, is_private_key=False))

            BASE_COMMANDS.WalletImport(
                interface.key_arg(
                    account_or_key, is_owner_key=False, is_private_key=True), 
                self.name, is_verbose=False)
            imported_keys.append(interface.key_arg(
                    account_or_key, is_owner_key=False, is_private_key=False))
            logger.TRACE("""
                * Importing keys of the account ``{}`` 
                    into the wallet ``{}``
                """.format(account_name, self.name)
                )
        else:
            BASE_COMMANDS.WalletImport(
                interface.key_arg(account_or_key, is_private_key=True), 
                self.name, is_verbose=False)

            logger.TRACE("""
                * Importing key into the wallet ``{}``
                """.format(self.name)
                        )
            return True
        
        wallet_keys = BASE_COMMANDS.WalletKeys(is_verbose=False)

        if len(imported_keys) == 0:
            raise errors.Error("""
                The list of imported keys is empty.
                """)

        ok = True
        for key in imported_keys:
            if not key in wallet_keys.json:
                ok = False
                raise errors.Error("""
                Failed to import keys of the account '{}' into the wallet '{}'
                """.format(
                    account_name if account_name else "n/a", self.name))

        if ok:
            logger.TRACE("""
            * Cross-checked: all account keys are in the wallet.
            """)
        return True

    def keys_in_wallets(self, keys):
        """Check whether all listed keys are in the wallet.

        Args:
            keys ([str]): List of public keys to be verified.

        Returns: 
            bool: Whether all listed keys are in the wallet.
        """
        self.open_unlock()
        result = BASE_COMMANDS.WalletKeys(is_verbose=False)
        for key in keys:
            if not key in result.json:
                return False
        return True

    def restore_accounts(self):
        """Restore into the global namespace all the account objects 
        represented in the wallet.
        """

        self.open_unlock()
        account_map = manager.account_map()
        new_map = {}
        wallet_keys = BASE_COMMANDS.WalletKeys(is_verbose=0)

        import eosfactory.core.account as ca
        import eosfactory.shell.account as sh
        class GetAccountAccount(ca.GetAccount, sh.Account):
            pass

        logger.INFO("""
                ######### Restore cached account objects:
                """)
        if len(account_map) > 0:
            for name, object_name in account_map.items():
                account_object = ca.GetAccount(object_name, name)
                if account_object.exists:
                    if account_object.owner_public() in wallet_keys.json and \
                        account_object.active_public() in wallet_keys.json:

                        new_map[name] = object_name
                        account_object.__class__ = GetAccountAccount
                        sh.set_is_account(account_object)

                        Wallet.wallet_globals[object_name] = account_object

            setup.save_account_map(new_map)

    def delete_globals(self):
        """Delete from the global namespace all the account objects restored
        with the function :func:`restore_accounts`.

        """
        account_map = manager.account_map()
        for _, object_name in account_map.items():
            del Wallet.wallet_globals[object_name]

    def stop(self):
        """Stop keosd, the EOSIO wallet manager.
        """
        BASE_COMMANDS.WalletStop()

    def keys(self):
        """ Lists public keys in the open unlocked wallet.
        """
        self.open_unlock()
        wallet_keys = BASE_COMMANDS.WalletKeys(is_verbose=False)
        logger.TRACE("""
            Keys in the open walet '{}':
            {}
            """.format(self.name, wallet_keys.out_msg))
        return wallet_keys.json

    def private_keys(self):
        """ Lists public keys from all unlocked wallets.
        Returns `BASE_COMMANDS.WalletKeys` object.
        """
        self.open_unlock()
        
        wallet_private_keys = BASE_COMMANDS.WalletPrivateKeys(
                self.name, self.password, is_verbose=False)
        logger.TRACE(str(wallet_private_keys))
        return wallet_private_keys

    def edit_account_map(self):
        """Edit the mapping between native account names and account object names."""
        setup.edit_account_map()
            
    def map_account(self, account_object):
        """Save a new account object.

        Args:
            account_object (.shell.account.Account): The account to be saved.
        """
        account_object_name = account_object.account_object_name
        account_map_json = manager.account_map()
        account_map_json[account_object.name] = account_object_name

        with open(self.wallet_dir + setup.ACCOUNT_MAP, "w") as out:
            out.write(json.dumps(
                account_map_json, indent=3, sort_keys=True))

        logger.TRACE("""
            * Account object ``{}`` stored in the file 
                ``{}`` in the wallet directory:
                {}
            """.format(
                account_object_name,
                setup.ACCOUNT_MAP,
                self.wallet_dir + setup.ACCOUNT_MAP))


def password_file(wallet_name):
    return os.path.join(
                        config.keosd_wallet_dir(),
                        wallet_name + setup.WALLET_PSWD_FILE_EXT)


def read_password(wallet_name):
    try:
        with open(password_file(wallet_name), "r") as _:
            return _.read()
    except: # pylint: disable=bare-except
            return ""


def create_wallet(
        name=None, password=None, save_password=False,
        wallet_globals=None, restore=False):
    """Create a singleton :class:`.Wallet` object.

    It is not usual to use this function. Instead, it is called automatically
    on the first use of either :func:`.shell.account.create_master_account`
    or :func:`.shell.account.create_account` functions.
    """
    if Wallet.wallet_singleton:
        return Wallet.wallet_singleton

    if wallet_globals:
        Wallet.wallet_globals = wallet_globals
    else:
        Wallet.wallet_globals = inspect.stack()[1][0].f_globals

    Wallet.wallet_singleton = Wallet(name, password, save_password)
    if restore:
        Wallet.wallet_singleton.restore_accounts()

    return Wallet.wallet_singleton


def get_wallet():
    """Get a singleton :class:`.Wallet` object."""
    return Wallet.wallet_singleton
