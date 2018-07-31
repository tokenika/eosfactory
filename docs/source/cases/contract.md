"""
# Contract object

```md
This file can be executed as a python script: 
``python3 contract.md``.

The set-up statements are explained in the ``setup.md`` case file.
```

## Set-up
```md
"""
import setup
import eosf
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

eosf.restart()
eosf.set_throw_error(True)
eosf.reset([eosf.Verbosity.TRACE])
"""
```
### Exactly one 'Wallet' object has to exist in the namespace:
```md
"""
wallet = Wallet()   
account_master_create("account_master")
eosf.set_throw_error(False)
"""
```
## Case
```md
``Contract`` objects cannot exist without an account object that keeps this
contract. The account object is presented elsewhere (``account.md`` case).

Create an account objects: ``account_hello``. Add a contract of the class
``hello`` to it. The code for the ``hello`` class comes with the EOSIO 
repository.

Next add two other account objects and execute the action of the account on 
them.
```
### Accounts
```md
"""
account_create("account_hello", account_master)
account_create("account_alice", account_master)
account_create("account_carol", account_master)
"""
```

### Create a Contract object
```md
Now, you have to create a smart contract object instance, appending it to the 
account ``account_hello``.
```
```md
"""
contract_hello = Contract(account_hello, "hello")
"""
```
```md
The second argument of the creator of the ``Contract`` class identifies the 
code source. The EOSFactort tries to be smart and search the repository of the 
Factory. If it fails, put the right path there, 
``/mnt/c/Workspaces/EOS/eosfactory/contracts/hello/``,
for example.
```

### Methods of an account objects

```md
Any ``Contract`` object can:

    * Build itself.
    * Deploy itself.
    * Push an action.
    * Show an action pushing it without broadcasting.
    * Show entry (a table) in the blockchain database of its account.
```
### Deploy and build the contract

```md
"""
contract_hello.build()
contract_hello.deploy()
"""
```

### Try the contract

```md
Execute the action of the contract ``hello``:
```
```md
"""
account_hello.push_action(
    "hi", '{"user":"' + str(account_alice) + '"}', account_alice)

account_hello.push_action(
    "hi", '{"user":"' + str(account_carol) + '"}', account_carol)
"""
```
```md
Besides the usual ``Hello`` message, you can see the result of a logging 
facility, starting with ``INFO``.
```

### Test run
```md
In an linux bash, change directory to where this file exists, it is the 
directory ``docs/source/cases`` in the repository, and enter the following 
command:
```
```md
$ python3 account.md
```
```md
We hope that you get anything similar to this shown in the image below.
```
<img src="account.png" 
    onerror="this.src='../../../source/cases/account.png'"   
    alt="account name conflict" width="720px"/>

"""