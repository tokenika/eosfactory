import enum

class Omittable:
    def __init__(self):
        self.err_msg = None

class Permission(enum.Enum):
    OWNER = '@owner'
    ACTIVE = '@active'


class Key(Omittable):
    '''Having the ``name`` and 'Key' attributes.
    '''    
    def __init__(self, name, key_public, key_private):
        self.name = name
        self.key_public = key_public
        self.key_private = key_private
        Omittable.__init__(self)


class Account(Omittable):
    '''Having the ``name`` and 'Key' attributes.
    '''    
    def __init__(self, name, owner_key=None, active_key=None):
        self.name = name
        self.owner_key = owner_key
        self.active_key = active_key
        Omittable.__init__(self)


class Wallet(Omittable):
    '''Having the ``name`` attribute.
    '''    
    def __init__(self, name, password=None):
        self.name = name
        self.password = password
        Omittable.__init__(self)


def wallet_arg(wallet):
    if isinstance(wallet, Wallet):
        return wallet.name
    if isinstance(wallet, str):
        return wallet


def key_arg(key, is_owner_key=True, is_private_key=True):
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
    if isinstance(account, str):
        return account
    if isinstance(account, Account):
        return account.name


def permission_arg(permission):
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
        permission_value = None
        if isinstance(permission[1], Permission):
            permission_value = permission[1].value
        if isinstance(permission[1], str):
            permission_value = permission[1]

        if not permission_value is None:
            if permission_value[0] == "@":
                retval = retval + permission_value
            else:
                retval = retval + "@" + permission_value
            return [retval]
        else:
            return None

    if isinstance(permission, list):
        retval = []
        while len(permission) > 0:
            p = permission_arg(permission.pop())
            retval.append(p[0])
        return retval

