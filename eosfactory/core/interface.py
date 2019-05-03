'''
'''
import enum

class Omittable:
    '''Having the *err_msg* attribute.
    '''
    def __init__(self):
        self.err_msg = None

class Permission(enum.Enum):
    '''Enumeration {OWNER, ACTIVE}
    '''
    OWNER = 'owner'
    ACTIVE = 'active'


class Key(Omittable):
    '''Having the *key_public* and *key_private* attributes.

    Args:
        key_public (str): The public key of a key pair.
        key_private (str): The private key of a key pair.

    Attributes:
        key_public (str): The public key of a key pair.
        key_private (str): The private key of a key pair.
    '''    
    def __init__(self, key_public, key_private):
        self.key_public = key_public
        self.key_private = key_private
        Omittable.__init__(self)

    def __str__(self):
        if not self.key_private:
            return "public:  {}".format(self.key_public)
        return "public: {}\nprivate: {}".format(
                                            self.key_public, self.key_private)


class Account(Omittable):
    '''Having the *name* and *key_public* and *key_private* attributes.

    Args:
        name (str): EOSIO contract name
        owner_key (str or .Key): The owner key of the account.
        active_key (str or .Key): The account key of the account.
    
    Attributes:
        name (str): EOSIO contract name
        owner_key (str or .Key): The owner key of the account.
        active_key (str or .Key): The account key of the account.
    '''
    def __init__(self, name, owner_key=None, active_key=None):
        self.name = name
        self.owner_key = owner_key
        self.active_key = active_key if active_key else owner_key
        Omittable.__init__(self)
    
    def owner(self):
        '''Get the public owner key

        Returns:
            str: public owner key
        '''
        if isinstance(self.owner_key, Key):
            return self.owner_key.key_public
        else:
            return self.owner_key

    def active(self):
        '''Get the public active key

        Returns:
            str: public active key
        '''        
        if isinstance(self.active_key, Key):
            return self.active_key.key_public
        else:
            return self.active_key    


class Wallet(Omittable):
    '''Having the *name* and *password* attributes.

    Args:
        name (str): The wallet name.
        password (str): The password to the wallet.

    Attributes:
        name (str): The wallet name.
        password (str): The password to the wallet.    
    '''    
    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        Omittable.__init__(self)


def wallet_arg(wallet):
    '''Accepts any *wallet* argument.

    Args:
        wallet (str or interface.Wallet): *wallet* argument.

    Returns:
        str: name of the *wallet* argument.
    '''
    if isinstance(wallet, Wallet):
        return wallet.name
    if isinstance(wallet, str):
        return wallet


def key_arg(key, is_owner_key=True, is_private_key=True):
    '''Accepts any key argument.

    Args:
        key (str or .Key or .interface.Account): The *key* argument. 
        is_owner_key (bool): Solves ambivalence of the *key* parameter if
            the key argument is an .interface.Account object.
        is_private_key (bool): Solves ambivalence of the *key* parameter if
            the the key argument is a .Key or .interface.Account object

    Returns:
        str: The value of the *key* argument.
    '''
    if isinstance(key, Account):
        if is_owner_key:
            key = key.owner_key
        else:
            key = key.active_key
        if is_private_key:
            key = key.key_private
        else:
            key = key.key_public

        if not key:
            return None
        return key

    if isinstance(key, Key):
        if is_private_key:
            key = key.key_private
        else:
            key = key.key_public
        if not key:
            return None
        return key
    if isinstance(key, str):
        return key


def account_arg(account):
    '''Accepts any account argument.

    Args:
        account (str or .interface.Account): *account* argument.

    Returns:
        str: The EOSIO name of the *account* argument.
    '''
    if isinstance(account, str):
        return account
    if isinstance(account, Account):
        return account.name


def permission_arg(permission):
    '''Accepts any permission argument.

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
    '''
    if isinstance(permission, str):
        return [permission]
    if isinstance(permission, Account):
        return [permission.name]
    if isinstance(permission, tuple):
        retval = None
        if isinstance(permission[0], str):
            retval = permission[0]
        if isinstance(permission[0], Account):
            retval = permission[0].name
        if retval is None:
            return None
        permission_name = None
        if isinstance(permission[1], Permission):
            permission_name = permission[1].value
        if isinstance(permission[1], str):
            permission_name = permission[1]

        if not permission_name is None:
            if permission_name[0] == "@":
                retval = retval + permission_name
            else:
                retval = retval + "@" + permission_name
            return [retval]
        else:
            return None

    if isinstance(permission, list):
        retval = []
        while len(permission) > 0:
            p = permission_arg(permission.pop())
            retval.append(p[0])
        return retval

