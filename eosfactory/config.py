import eosfactory.core.config

if __name__ == '__main__':
    eosfactory.core.config.main()



The code is wrong. Thank you for your remark. We will correct the error in the next edition of EOSFactory.

#####################################
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
#    elif "Error 3120002: Nonexistent wallet" in err_msg:
#        raise WalletDoesNotExistError(
#            WalletDoesNotExistError.msg_template.format(self.name))
    elif "Error 3120002: Nonexistent wallet" in err_msg: # correction
        raise WalletDoesNotExistError(omittable) # correction
    elif "Invalid wallet password" in err_msg:
        raise InvalidPasswordError(omittable)
    elif "Contract is already running this version of code" in err_msg:
        raise ContractRunningError()
    elif "Missing required authority" in err_msg:
#####################################