'''
# Contract object

This file can be executed as a python script: 'python3 contract.md'.


## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

```md
'''
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
CONTRACT_DIR = "02_eosio_token"
reset([Verbosity.INFO])
'''
```

### Exactly one 'Wallet' object has to exist in the namespace

```md
'''
create_wallet()   
account_master_create("account_master")
set_throw_error(False)
'''
```

## Case

None 'Contract' object can exist without an account object that keeps this
contract. The account object is presented at <a href="account.html">cases/account</a>.

Create an account objects: 'eosio_token'. Provide it with a contract 
of the class 'eosio.token'. The code for the 'eosio.token' class comes with 
the EOSIO repository, and it is copied, slightly modified to the Factory's. 
We use the later copy.

Make three other account objects, and execute actions of the contract on them.

### Accounts

```md
'''
account_create("eosio_token", account_master)
account_create("alice", account_master)
account_create("bob", account_master)
account_create("carol", account_master)
'''
```

### Create a Contract object

Create an instance of the 'Contract' class, appending it to the account 
'eosio_token':

```md
'''
contract = Contract(eosio_token, CONTRACT_DIR)
'''
```

The second argument of the creator of the 'Contract' class identifies the 
code source. The Factory tries to be smart, and searches the repository of the 
Factory. If it fails, put the right path there, 
'/mnt/c/Workspaces/EOS/eosfactory/contracts/eosio.token/',
for example.

Note that the 'Contract' creator takes several default arguments that 
sometimes have to be adjusted.

### Methods of a contract objects

Any 'Contract' object can:

* Build itself.
    * Build abi alone.
    * Build wast alone.
* Deploy itself.
* Push an action.
* Show an action pushing it without broadcasting.
* Show entry (a table) in the blockchain database of its account.

### Deploy and build the contract

```md
'''
contract.build()
contract.deploy()
'''
```

### Try the contract

Execute actions of the contract:

```md
'''
contract.push_action(
    "create", 
    {
        "issuer": account_master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0",
        "can_recall": "0",
        "can_whitelist": "0"
    }, [account_master, eosio_token])
    
contract.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    },
    account_master)

contract.push_action(
    "transfer",
    {
        "from": alice, "to": carol,
        "quantity": "25.0000 EOS", "memo":""
    },
    alice)

contract.push_action(
    "transfer",
    {
        "from": carol, "to": bob, 
        "quantity": "11.0000 EOS", "memo": ""
    },
    carol)

contract.push_action(
    "transfer",
    {
        "from": carol, "to": bob, 
        "quantity": "2.0000 EOS", "memo": ""
    },
    carol)

contract.push_action(
    "transfer",
    {
        "from": bob, "to": alice, \
        "quantity": "2.0000 EOS", "memo":""
    },
    bob)            
'''
```
Inspect the database of the blockchain:

```md
'''
table_alice = eosio_token.table("accounts", alice)
table_bob = eosio_token.table("accounts", bob)
table_carol = eosio_token.table("accounts", carol)
'''
```

```md
You can see the result of a logging facility, printed in yellow, starting with 
'INFO'.
```

### Test run

With a linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:

```md
$ python3 contract.md
```
```md
We hope that you get something similar to this one shown in the image below.
```
<img src="contract.png" 
    onerror="this.src='../../../source/cases/contract.png'" width="720px"/>
'''