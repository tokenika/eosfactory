"""
# Setting-up cases
```md
The structure of the most of the ``Cases`` files is explained in this file.

Note, that all case files are both ``Markdown`` and ``Python` scripts. 
Therefore, you can execute them with `python3 <file name>` bash command, or 
you can view them, (RIGHT MOUSE -> Open Preview if you use the ``Visual Studio 
Code``).

Any test has two parts. At first, test staging goes. If a local testnode is 
used, is set-up to meet conditions of the scenario of the test. Otherwise, 
with a remote node, test staging involves probing the state of the node 
whether it fulfils the assumptions of the scenario of the test.

In this article, we show facilities the the `EOSFactory` provids for staging
the tests.
```

## Set-up part

### Throw exceptions status

```md
The set-up part of a test does not involve testing specific assumptions.
Instead, the `EOSFactory` is set then to throw fatal exceptions: the set-up
block is enclosed within the following statements:
```

```md
eosf.set_throw_error(True)
#
# set-up statements
#
eosf.set_throw_error(False)
```
### Verbosity status

```md
You can determine the amount of the verbosity of the tested processes.
The output of the commands is made with objects of the `eosf.Logger` class.

The verbosity can assume the following values:

    * eosf.Verbosity.TRACE      # only main tasks are marked
    * eosf.Verbosity.EOSF       # subtasks are noted
    * eosf.Verbosity.OUT        # command output is printed
    * eosf.Verbosity.DEBUG      # debugging info is printed

Default is [eosf.Verbosity.EOSF, eosf.Verbosity.OUT]
```
### Code excerpt

```md
It follows a script that demonstates all the (almost) steering statements:
```

```md
"""
import setup
import eosf
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT])
setup.set_command_line_mode(False) # print message sent to the cleos
eosf.set_is_testing_errors(False) # make the error mesages alarming

eosf.set_throw_error(True) # throw exception rather then print message
eosf.restart()
eosf.use_keosd(False) # nodeos vs keosd wallet management
eosf.reset([eosf.Verbosity.TRACE]) # start local testnode
wallet = Wallet() # create the singleton `Wallet` object
account_master_create("account_master") # create local testnode `eosio` account
eosf.set_throw_error(False) # print message rather then throw exception

eosf.set_is_testing_errors() # make the error mesages less alarming
"""
```
"""