'''
# Registering to a remote testnet

This file can be executed as a python script: 
'python3 register_to_testnode.md'.

Registering to a public testnet involves three steps:

* `set_nodeos_address(testnet.url)` # set the url of the testnet;
* `create_wallet(file=True)` # create the wallet singleton (`file=True` means password to file);
* `create_master_account("account_master")` # create an account object, named as the argument of the factory function.

The last step prints data to be entered into the registration form of the testnet.

The procedure results are following:

* the wallet file named like `88_99_97_30_38888_default.wallet` (exactly, if the testnet url is `https://88.99.97.30:38888`) in the directory manager by the KOSD Wallet Manager;
* an entry in the Factory's account maping file (named like `88_99_97_30_38888_accounts.json`) that cause that the account object is available between sessions;
* an entry in the Factory's password maping file (named like `88_99_97_30_38888_password.json`) that cause that the wallet object is opened automatically between sessions.

The registration can be simply done with the command issued in a bash terminal:
```md
python3 utlis/register_account.py <test node url> <testnet pseudo>
```
 
for example
```md
$ python3 utlis/register_account.py https://88.99.97.30:38888 jungle
```

The current article tests this registration procedure.

## Set-up

The set-up statements are explained at <a href="html">cases/setup</a>.

### The header of the test

```md
'''
from  eosfactory import *
import testnode_data

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
'''
```

### The testnet

There is many public testnodes: all we know are volatile: the one that you are 
prepared to use is stopped just when you need it. Therefore we have provision 
for easy change of the used testnet. 

In the `testnode_data` module, there is a pair of prefabricated testnet objects: `cryptolion` and `kylin`. Here we set one:

```md
'''
testnet = testnode_data.cryptolion
set_nodeos_address(testnet.url)
'''
```
The second line statement makes the following arrangements:

* sets the url of the testnet as the working endpoint;
* sets a prefix differentiating system files currently used, for example, the default name of the wallet is `88_99_97_30_38888_default.wallet`;

We do not want to use this default naming system for the current test, 
therefore we use an option of the function `set_nodeos_address(...)` --

```md
'''
set_nodeos_address(testnet.url, "registering_to_testnode")
'''
```
-- now the default name of the wallet is `registering_to_testnode_default.wallet`.

### Stop if the testnet is off

Make sure that the chosen testnet is operative:

```md
'''
verify_testnet()
'''
```

### Remove results of a possible previous use of the current script.

```md
'''
remove_testnet_files()
'''
```

## Case

At the beginning, the 'Wallet` singleton has to be created:

```md
'''
Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT]
create_wallet(file=True)
'''
```

### Register to the testnet

We usually name `account_master` any, yet single in the namespace, object that has resources necessary for creation of child accounts. 

The factory function `create_master_account` executed with a single argument meaning the name of the created account object (or with a second one, fixing the name of the physical account), conducts a registration process.

Just testing the system we do not want to polute the public testnet with dummy accounts, therefore, we expect you to responce `q` to the query of the script.

The script will then continue with the prefabricated account in the object `testnet`.
```md
'''
create_master_account("account_master")
'''
```
```md
'''
create_master_account("account_master", testnet)
import pdb; pdb.set_trace()
testnet_data.add_to_map(
    testnode_url, account_master.name, 
    account_master.owner_key.key_private,
    account_master.active_key.key_private, alias="jungle")
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