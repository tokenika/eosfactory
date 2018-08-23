'''
# Account object

This file can be executed as a python script: 'python3 account.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

```md
'''
from  eosfactory import *
CONTRACT_DIR = "01_hello_world"
reset([Verbosity.INFO])
'''
```

### Exactly one 'Wallet' object has to exist in the namespace

```md
'''
create_wallet()   
account_master_create("account_master")
'''
```

## Case

The EOSFactory wraps EOSIO accounts with objects. Accounts can hold smart
contracts. 

Create an account objects: 'account_hello'. Add a contract of the class
'hello' to it. The code for the 'hello' class is in the EOSIO repository.

Add two other account objects, and execute the action of the contract on them 
subsequently.

### The 'account_create' factory function

```md
'''
account_create("account_hello", account_master)
'''
```

The first argument is the name of the account object to be created, the second
one points to the account master, authorizing the creation.

Only this two arguments are necessary, however there is several default 
arguments that sometimes have to be adjusted.

The 'account_create' does many tasks:

* Checks whether a 'Wallet' object exist in the namespace.
* Checks whether its first argument is not the same as the name of any other
    account objects in the Factory's statistics. If it is so, a correction
    action is proposed - see the 'account_name_conflict.md' case.
* Creates a global object named as the first argument, representing 
    a physical account of a random name (however, the name cen be fixed).
* Opens the wallet, unlock it, put the physical account into it.
* Updates the statistics of the accounts.

All the actions are logged to the terminal, if the verbosity is set default. 

### Methods of an account objects

Any account object can:

* Load a smart contract.
* Push an action on its contract.
* Show its entry (a table) in the blockchain database.

### Create a Contract object

Create a smart contract object instance, appending it to the account 
'account_hello'. The 'Contract' class is presented at <a href="contract.html">cases/contract</a>.

```md
'''
contract_hello = Contract(account_hello, CONTRACT_DIR)
contract_hello.build()
contract_hello.deploy()
'''
```

The second argument of the creator of the 'Contract' class identifies the 
code source. The Factory tries to be smart therefore searches the repository. 
If it fails, put the right path there, 
'/mnt/c/Workspaces/EOS/eosfactory/contracts/hello/',
for example.

If the deployment succeeds, the contract can be executed.

### Try the contract

Create two contracts 'account_alice' and 'account_carol'...

```md
'''
account_create("account_alice", account_master)
account_create("account_carol", account_master)
'''
```

... and execute the action of the contract 'hello':

```md
'''
account_hello.push_action(
    "hi", '{"user":"' + str(account_alice) + '"}', account_alice)

account_hello.push_action(
    "hi", '{"user":"' + str(account_carol) + '"}', account_carol)
'''
```

Besides the usual 'Hello' message, you can see the result of a logging 
facility, starting with 'INFO'.

### Test run

```md
In an linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:
```
```md
$ python3 account.md
```

We expect that you get something similar to this one shown in the image:

<img src="account.png" 
    onerror="this.src='../../../source/cases/account.png'"   
    width="720px"/>
'''