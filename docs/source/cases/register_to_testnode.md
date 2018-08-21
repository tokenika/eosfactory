'''
# Registering to a remote testnode

This file can be executed as a python script: 
'python3 registering_to_testnode.md'.

Registering to a public testnet involves three steps:

* `setup.set_nodeos_address(testnode.url)` # set the url of the testnode;
* `wallet = Wallet(file=True)` # create the wallet singleton (`file=True` means password to file);
* `account_master_create("account_master")` # create an account object, named as the argument of the factory function.

The last step prints data to be entered into the registration form of the testnet.

The procedure results are following:

* the wallet file named like `88_99_97_30_38888_default.wallet` (exactly, if the testnet url is `https://88.99.97.30:38888`) in the directory manager by the KOSD Wallet Manager;
* an entry in the Factory's account maping file (named like `88_99_97_30_38888_accounts.json`) that cause that the account object is available between sessions;
* an entry in the Factory's password maping file (named like `88_99_97_30_38888_password.json`) that cause that the wallet object is opened automatically between sessions.

The registration can be simply done with the command issued in a bash terminal:
```md
python3 registering_to_testnode.py <test node url> <account object name>
```
 
for example
```md
$ python3 register_to_testnode.py https://88.99.97.30:38888 account_master
```

The current article tests this registration procedure.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

### The header of the test

```md
'''
import setup
import logger
import eosf
import eosf_account
import testnet_data

from logger import Verbosity
from eosf_wallet import Wallet
from eosf_account import account_master_create

_ = logger.Logger([Verbosity.INFO, Verbosity.OUT])
logger.set_is_testing_errors(False)
logger.set_throw_error(True)
'''
```

### The testnode

There is many public testnodes: all we know are volatile: the one that you are 
prepared to use is stopped just when you need it. Therefore we have provision 
for easy change of the used testnode. 

In the `testnet_data` module, there is a pair of prefabricated testnode objects: `cryptolion` and `kylin`. Here we set one:

```md
'''
testnode = testnet_data.kylin
setup.set_nodeos_address(testnode.url)
'''
```
The second line statement makes the following arrangements:

* sets the url of the testnode as the working endpoint;
* sets a prefix differentiating system files used in currently, for example, the default name of the wallet is `88_99_97_30_38888_default.wallet`;

We do not want to use this default naming system for the current test, 
therefore we use an option of the function `setup.set_nodeos_address(...)` --

```md
'''
setup.set_nodeos_address(testnode.url, "registering_to_testnode")
'''
```
-- now the default name of the wallet is `registering_to_testnode_default.wallet`.

### Stop if the testnode is off

Make sure that the chosen testnode is operative:

```md
'''
if not eosf.is_running():
    print(
        "This test needs the testnode {} running, but it does not answer." \
            .format(testnode.url))
    exit()
'''
```

### Remove results of a possible previous use of the current script.

```md
'''
eosf.remove_files()
'''
```

## Case

At the beginning, the 'Wallet` singleton has to be created:

```md
'''
logger.Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT]
wallet = Wallet(file=True)
'''
```

### Register to the testnode

We usually name `account_master` any, yet single in the namespace, object that has resources necessary for creation of child accounts. 

The factory function `account_master_create` executed with a single argument meaning the name of the created account object (or with a second one, fixing the name of the physical account), conducts a registration process.

Just testing the system we do not want to polute the public testnet with dummy accounts, therefore, we expect you to responce `q` to the query of the script.

The script will then continue with the prefabricated account in the object `testnet`.
```md
'''
account_master_create("account_master")
'''
```
```md
'''
account_master_create(
    "account_master",
    testnode.account_name, 
    testnode.owner_key,
    testnode.active_key)
'''
```

### Test run

With a linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:

```md
$ python3 register_to_testnode.md
```

We hope that you get something similar to this one shown in the image below.

<img src="register.png" 
    onerror="this.src='../../../source/cases/registering.png'" width="640px"/>
    
'''