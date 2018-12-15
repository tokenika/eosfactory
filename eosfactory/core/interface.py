import enum

class Omittable:
    '''Having the ``err_msg`` attribute.
    '''
    def __init__(self):
        self.err_msg = None

class Permission(enum.Enum):
    '''Enumeration {OWNER, ACTIVE}
    '''
    OWNER = 'owner'
    ACTIVE = 'active'


class Key(Omittable):
    '''Having the ``key_public`` and ``key_private`` attributes.
    '''    
    def __init__(self, key_public, key_private):
        self.key_public = key_public
        self.key_private = key_private
        Omittable.__init__(self)


class Account(Omittable):
    '''Having the ``name`` and ``key_public`` and ``key_private`` attributes.
    '''    
    def __init__(self, name, owner_key=None, active_key=None):
        self.name = name
        self.owner_key = owner_key
        self.active_key = active_key
        Omittable.__init__(self)
    
    def owner(self):
        if isinstance(self.owner_key, Key):
            return self.owner_key.key_public
        else:
            return self.owner_key

    def active(self):
        if isinstance(self.active_key, Key):
            return self.active_key.key_public
        else:
            return self.active_key    


class Wallet(Omittable):
    '''Having the ``name`` and ``password`` attributes.
    '''    
    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        Omittable.__init__(self)


def wallet_arg(wallet):
    '''Accepts any ``wallet`` argument.

    Args:
        wallet: ``wallet`` argument. May be a string or :class:`.Wallet` object.
    
    Returns:
        The string name of the ``wallet`` argument.
    '''
    if isinstance(wallet, Wallet):
        return wallet.name
    if isinstance(wallet, str):
        return wallet


def key_arg(key, is_owner_key=True, is_private_key=True):
    '''Accepts any key argument.

    Args:
        key: ``key`` argument. May be a string, or :class:`.Account` object, or 
            :class:`.Key` object.
        is_owner_key (bool): Solves ambivalence of the ``key`` parameter if
            the key argument is an :class:`.Account` object.
        is_private_key (bool): Solves ambivalence of the ``key`` parameter if
            the the key argument is a :class:`.Key` or :class:`.Account` object.
    
    Returns:
        The string value of the ``key`` argument.
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
        account: ``account`` argument. May be a string EOSIO name, 
            or :class:`.Account` object.

    Returns:
        The string EOSIO name of the ``account`` argument. 
    '''
    if isinstance(account, str):
        return account
    if isinstance(account, Account):
        return account.name


def permission_arg(permission):
    '''Accepts any permission argument.

    Args:
        permission: Permission argument. May be a one of the following:

        - string like ``"eosio"`` or ``"eosio@owner"``;
        - Account object, like ``eosio``;
        - tuple like ``("eosio", "owner")`` or ``(eosio, Permission.OWNER)``;
        - list of the above elements as 
            ``["eosio", (eosio, Permission.OWNER)]``.
    
    Returns:
        A list of ``(<account name>, <permission>)`` tuples.
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

