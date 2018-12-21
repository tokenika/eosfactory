'''
.. module:: eosfactory.core.interface
    :platform: Unix, Darwin
    :synopsis: basic interfaces.

.. moduleauthor:: Tokenika
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

    :param str key_public: The public key of a key pair.
    :param str key_private: The private key of a key pair.

    :var str key_public: The public key of a key pair.
    :var str key_private: The private key of a key pair.
    '''    
    def __init__(self, key_public, key_private):
        self.key_public = key_public
        self.key_private = key_private
        Omittable.__init__(self)


class Account(Omittable):
    '''Having the *name* and *key_public* and *key_private* attributes.

    :param str name: EOSIO contract name
    :param owner_key: The owner key of the account.
    :type owner_key: str or .Key
    :param active_key: The account key of the account.
    :type active_key: str or .Key
    
    :var str name: EOSIO contract name
    :var owner_key: The owner key of the account.
    :vartype owner_key: str or .Key
    :var active_key: The account key of the account.
    :vartype active_key: str or .Key
    '''    
    def __init__(self, name, owner_key=None, active_key=None):
        self.name = name
        self.owner_key = owner_key
        self.active_key = active_key
        Omittable.__init__(self)
    
    def owner(self):
        '''Get the public owner key

        :return: public owner key
        :rtype: str
        '''
        if isinstance(self.owner_key, Key):
            return self.owner_key.key_public
        else:
            return self.owner_key

    def active(self):
        '''Get the public active key

        :return: public active key
        :rtype: str
        '''        
        if isinstance(self.active_key, Key):
            return self.active_key.key_public
        else:
            return self.active_key    


class Wallet(Omittable):
    '''Having the *name* and *password* attributes.

    :param str name: The wallet name.
    :param str password: The password to the wallet.

    :var str name: The wallet name.
    :var str password: The password to the wallet.    
    '''    
    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        Omittable.__init__(self)


def wallet_arg(wallet):
    '''Accepts any *wallet* argument.

    :param wallet: *wallet* argument.
    :type wallet: str or interface.Wallet
    :return: name of the *wallet* argument.
    :rtype: str
    '''
    if isinstance(wallet, Wallet):
        return wallet.name
    if isinstance(wallet, str):
        return wallet


def key_arg(key, is_owner_key=True, is_private_key=True):
    '''Accepts any key argument.

    :param key: The *key* argument.
    :type key: str or .Key or .interface.Account
    :param bool is_owner_key: Solves ambivalence of the *key* parameter if
            the key argument is an .interface.Account object.
    :param bool is_private_key: Solves ambivalence of the *key* parameter if
            the the key argument is a .Key or .interface.Account object
    :return: The value of the *key* argument.
    :rtype: str
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

    :param account: *account* argument.
    :type account: str or .interface.Account
    :return: The EOSIO name of the *account* argument.
    :rtype: str 
    '''
    if isinstance(account, str):
        return account
    if isinstance(account, Account):
        return account.name


def permission_arg(permission):
    '''Accepts any permission argument.

    :param permission: The *permission* argument.
    :type permission: .interface.Account or str or (str, str) or \
        (.interface.Account, str) or any list of the previous items.
        
    Exemplary values of the argument *permission*::

        eosio # eosio is an interface.Account object

        "eosio@owner"

        ("eosio", "owner")

        (eosio, interface.Permission.ACTIVE)
        
        ["eosio@owner", (eosio, .Permission.ACTIVE)]

    :return: A list of tuples.
    :rtype: [(str, str)]
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

