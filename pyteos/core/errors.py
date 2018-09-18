import re

import core.logger as logger
import shell.interface as interface


def validate(omittable):
    '''Throw exception if validation fails.
    '''
    err_msg = omittable.err_msg
    if not err_msg:
        return

    if "unknown key" in err_msg:
        raise AccountDoesNotExistError(omittable)
    elif "Error 3080001: Account using more than allotted RAM" in err_msg:
        needs = int(re.search('needs\s(.*)\sbytes\shas', err_msg).group(1))
        has = int(re.search('bytes\shas\s(.*)\sbytes', err_msg).group(1))
        raise LowRamError(needs, needs - has)
    elif "transaction executed locally, but may not be" in err_msg:
        pass
    elif "Wallet already exists" in err_msg:
        raise WalletAlreadyExistsError(omittable)
    elif "Error 3120002: Nonexistent wallet" in err_msg:
        raise WalletDoesNotExistError(
            WalletDoesNotExistError.msg_template.format(self.name))
    elif "Invalid wallet password" in err_msg:
        raise InvalidPasswordError(omittable)
    elif "Contract is already running this version of code" in err_msg:
        raise ContractRunningError()
    elif "Missing required authority" in err_msg:
        raise MissingRequiredAuthorityError(err_msg)
    elif "Duplicate transaction" in err_msg:
        raise DuplicateTransactionError(err_msg)
    
    #######################################################################
    # NOT ERRORS
    #######################################################################
    
    elif "Error 3120008: Key already exists" in err_msg:
        pass                
    else:
        raise Error(err_msg)
        

class Error(Exception):
    '''Base class for exceptions in EOSFactory.
    '''
    def __init__(self, message, translate=True):
        self.message = logger.error(message, translate)
        Exception.__init__(self, self.message)


class AccountDoesNotExistError(Error):
    '''Account does not exist.

    Attributes:
        account: account argument: an ``Account`` object or account name.
    '''
    def __init__(self, account):
        self.account = account
        Error.__init__(
            self, 
            "Account ``{}`` does not exist in the blockchain."
            .format(interface.account_arg(account)), 
            True)


class WalletDoesNotExistError(Error):
    def __init__(self, wallet):
        self.wallet = wallet
        Error.__init__(
            self, 
            "Wallet ``{}`` does not exist."
            .format(interface.wallet_arg(wallet)), 
            True)


class WalletAlreadyExistsError(Error):
    def __init__(self, wallet):
        self.wallet = wallet
        Error.__init__(
            self, 
            "Wallet ``{}`` already exists."
            .format(interface.wallet_arg(wallet)), 
            True)


class InvalidPasswordError(Error):
    def __init__(self, wallet):
        self.wallet = wallet
        Error.__init__(
            self, 
            "Invalid password for wallet {}"
            .format(interface.wallet_arg(wallet)), 
            True)


class ContractRunningError(Error):
    def __init__(self):
        Error.__init__(
            self, 
            "Contract is already running this version of code", 
            True)


class LowRamError(Error):
    def __init__(self, needs_byte, deficiency_byte):
        self.needs_kbyte =  needs_byte// 1024 + 1
        self.deficiency_kbyte = deficiency_byte // 1024 + 1
        Error.__init__(
            self, 
            "RAM needed is {}kB, deficiency is {}kB."
            .format(self.needs_kbyte, self.deficiency_kbyte), 
            True)   


class MissingRequiredAuthorityError(Error):
    def __init__(self, message):
        Error.__init__(
            self, message, True)


class DuplicateTransactionError(Error):
    def __init__(self, message):
        Error.__init__(
            self, message, True)