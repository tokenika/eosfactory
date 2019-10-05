"""
"""
import re
import enum

class Omittable:
    """Having the *err_msg* attribute.
    """
    def __init__(self):
        self.err_msg = None


class Permission(enum.Enum):
    """Enumeration {OWNER, ACTIVE}
    """
    OWNER = 'owner'
    ACTIVE = 'active'

    @staticmethod
    def name(permission):
        if isinstance(permission, Permission):
            return permission.value
        return permission


class Key(Omittable):
    """Having the ``key_public`` and ``key_private`` attributes.

    Args:
        key_public (str): The public key of a key pair.
        key_private (str): The private key of a key pair.

    Attributes:
        key_public (str): The public key of a key pair.
        key_private (str): The private key of a key pair.
    """
    @staticmethod
    def create_key(key):
        if not key:
            return Key()
        
        if isinstance(key, str):
            if not is_public_key(key):
                import eosfactory.core.errors as errors
                raise errors.InterfaceError("""
        The argument ``key`` is not a valid public key.
        """)
            return Key(key, None)
        elif isinstance(key, Key):
            return key
        else:
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        The argument ``key`` which is 
        ``{}`` 
        have to be either ``str`` or ``interface.Key``.
        """.format(key))

    @staticmethod
    def get_key_private(key):
        if isinstance(key, str):
            if not is_private_key(key):
                import eosfactory.core.errors as errors
                raise errors.InterfaceError("""
        The argument ``key`` is not a valid private key.
        """)
            return key
        elif isinstance(key, Key):
            return key.key_private
        else:
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        The argument ``key`` have to be either ``str`` or ``interface.Key``.
        """)
            
    @staticmethod
    def get_key_public(key):
        if isinstance(key, str):
            if not is_public_key(key):
                import eosfactory.core.errors as errors
                raise errors.InterfaceError("""
        The argument ``key`` is not a valid public key.
        """)
            return key
        elif isinstance(key, Key):
            return key.key_public
        else:
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        The argument ``key`` have to be either ``str`` or ``interface.Key``.
        """)

    def __init__(self, key_public=None, key_private=None):

        if key_public and not is_public_key(key_public):
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        The argument ``key_public`` is not a valid public key.
        """)
        self.key_public = key_public

        if key_private and not is_private_key(key_private):
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        The argument ``key_private`` is not a valid private key.
        """)        
        self.key_private = key_private

        Omittable.__init__(self)

    def is_complete(self):
        return self.key_public and self.key_private

    def __str__(self):
        return "public: {}\nprivate: {}".format(
                                            self.key_public, self.key_private)


class Account(Omittable):
    """Having the ``name`` and ``owner_key`` and ``active_key`` attributes.

    Args:
        name (str or Account): EOSIO contract name or Account object, then
            copies this object.
        owner_key (str or .Key): The owner key of the account.
        active_key (str or .Key): The account key of the account.
    
    Attributes:
        name (str): EOSIO contract name
    """
    def __init__(self, name, owner_key=None, active_key=None):
        self.name = account_arg(name) # Verifies name.

        if isinstance(name, Account):
            self.owner_key = name.owner_key
            self.active_key = name.active_key
        elif isinstance(name, str):
            if not active_key:
                active_key = owner_key
            self.owner_key = Key.create_key(owner_key)
            self.active_key = Key.create_key(owner_key)

        Omittable.__init__(self)
    
    def owner_public(self):
        """Get the public owner key

        Returns:
            str: public owner key
        """
        if isinstance(self.owner_key, Key):
            return self.owner_key.key_public
        else:
            return self.owner_key

    def active_public(self):
        """Get the public active key

        Returns:
            str: public active key
        """
        if isinstance(self.active_key, Key):
            return self.active_key.key_public
        else:
            return self.active_key


class Wallet(Omittable):
    """Having the *name* and *password* attributes.

    Args:
        name (str): The wallet name.
        password (str): The password to the wallet.

    Attributes:
        name (str): The wallet name.
        password (str): The password to the wallet.    
    """    
    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        Omittable.__init__(self)


def wallet_arg(wallet):
    """Accepts any *wallet* argument.

    Args:
        wallet (str or interface.Wallet): *wallet* argument.

    Returns:
        str: name of the *wallet* argument.
    """
    if isinstance(wallet, Wallet):
        return wallet.name
    if isinstance(wallet, str):
        return wallet


def is_public_key(key):
    return isinstance(key, str) and re.match(r"^[A-Za-z0-9]*$", key) \
                                    and "EOS" == key[0:3] and len(key) == 53


def is_private_key(key):
    return isinstance(key, str) and re.match(r"^[A-Za-z0-9]*$", key) \
                                    and key[0] == "5" and len(key) == 51


def is_key(key):
    return isinstance(key, Key) \
        or isinstance(key, str) \
                    and (re.match(r"^[A-Za-z0-9]*$", key) \
                        and ("EOS" == key[0:3] and len(key) == 53) \
                                            or key[0] == "5" and len(key) == 51)


def is_account(account):
    return isinstance(account, Account) or isinstance(account, str) \
        and(re.match(r"^[A-Za-z0-9]*$", account) and len(account) <= 12)


def key_arg(key, is_owner_key=True, is_private_key=True):
    """Accepts any key argument.

    Args:
        key (str or .Key or .interface.Account): The *key* argument. 
        is_owner_key (bool): Solves ambivalence of the *key* parameter if
            the key argument is an .interface.Account object.
        is_private_key (bool): Solves ambivalence of the *key* parameter if
            the the key argument is a .Key or .interface.Account object

    Returns:
        str: The value of the *key* argument.
    """
    if not key:
        import eosfactory.core.errors as errors
        raise errors.ArgumentNotSet(
                    "key",
                    "key string or Key object or Account object")

    if isinstance(key, Account):
        if is_owner_key:
            key = key.owner_key
        else:
            key = key.active_key

        if is_private_key:
            key = key.key_private
        else:
            key = key.key_public

        return key

    if isinstance(key, Key):
        if is_private_key:
            key = key.key_private
        else:
            key = key.key_public

        return key
    
    if isinstance(key, str):
        if not is_key(key):
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        ``{}`` is not a valid eosio public key.
        """.format(key))
        return key


def account_arg(account):
    """Accepts any account argument.

    Args:
        account (str or .interface.Account): *account* argument.

    Returns:
        str: The EOSIO name of the *account* argument.
    """
    if isinstance(account, str):
        if not is_account(account):
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
        ``{}`` is not a valid eosio account name.
        """.format(account))
        return account
    if isinstance(account, Account):
        return account.name


def permission_arg(permission):
    """Accepts any permission argument.

    Args:
    :param permission (.interface.Account or str or (str, str) or \
        (.interface.Account, str) or any list of the previous items): The *permission* argument.
        
    Exemplary values of the argument *permission*::

        eosio # eosio is an interface.Account object

        perm_str = "eosio@owner"

        perm_tuple = ("eosio", "owner")

        perm_tuple = (eosio, interface.Permission.ACTIVE)
        
        perm_list = ["eosio@owner", (eosio, .Permission.ACTIVE)]

    Returns:
        [(str, str)]: A list of tuples (<account name>, <permission name>).
    """
    if isinstance(permission, str):
        return [permission]
    elif isinstance(permission, Account):
        return [permission.name]
    elif isinstance(permission, tuple):
        if isinstance(permission[0], str):
            retval = permission[0]
        elif isinstance(permission[0], Account):
            retval = permission[0].name
        else:
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
                ``{}`` is not a valid permission object.
                """.format(permission))
                
        if isinstance(permission[1], Permission):
            permission_name = permission[1].value
        elif isinstance(permission[1], str):
            permission_name = permission[1]
        else:
            import eosfactory.core.errors as errors
            raise errors.InterfaceError("""
                ``{}`` is not a valid permission object.
                """.format(permission))

        if permission_name[0] == "@":
            retval = retval + permission_name
        else:
            retval = retval + "@" + permission_name
        return [retval]

    elif isinstance(permission, list):
        retval = []
        while len(permission) > 0:
            p = permission_arg(permission.pop())
            retval.append(p[0])
        return retval

    else:
        import eosfactory.core.errors as errors
        raise errors.InterfaceError("""
            ``{}`` is not a valid permission object.
            """.format(permission))

