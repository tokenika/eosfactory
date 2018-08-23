'''
# Setting-up EOSFactory tests

This file can be executed as a python script: 'python3 setup.md'.

## Set-up part

### Throw exceptions status

The set-up part of a test does not involve test specific assumptions.
Instead, the EOSFactory is set there to throw fatal exceptions: the set-up
block is enclosed within the following statements:

```md
logger.set_throw_error(True)
logger.set_throw_error(False)
```

### Verbosity status

You can determine the amount of the verbosity of the tested processes.
The output of the commands is made with objects of the `logger.Logger` class.

The verbosity can assume the following values:

* logger.Verbosity.INFO      # only main tasks are marked
* logger.Verbosity.TRACE       # subtasks are noted
* logger.Verbosity.OUT        # command output is printed
* logger.Verbosity.DEBUG      # debugging info is printed

Default is [logger.Verbosity.TRACE, logger.Verbosity.OUT]

### Code excerpt

The following script demonstrates steering statements:

```md
'''
import setup
import eosf
from eosf_wallet import Wallet
from eosf_account import create_account, create_master_account

logger.Logger.verbosity = [logger.Verbosity.TRACE, logger.Verbosity.OUT]
setup.set_command_line_mode(False) # print message sent to the cleos
logger.set_is_testing_errors(False) # make the error mesages alarming

logger.set_throw_error(True) # throw exception rather then print message
eosf.restart()
eosf.reset([logger.Verbosity.INFO]) # start local testnode
create_wallet() # create the singleton `Wallet` object
create_master_account("account_master") # create local testnode `eosio` account
logger.set_throw_error(False) # print message rather then throw exception

logger.set_is_testing_errors() # make the error mesages less alarming
'''
```
'''