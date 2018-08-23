'''
# Eosio Token Contract

This file can be executed as a python script: 'python3 eosio_token_contract.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

```md
'''
from  eosfactory import *
Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]
CONTRACT_DIR = "02_eosio_token"
'''
```

### The `Wallet` object

Create the singleton wallet object. The object represents a physical wallet,
managedby  the KEOSD:

```md
'''
#reset([Verbosity.INFO])
create_wallet()

account_master_create("account_master")
print(account_master.info())
exit()
'''
```

## Case

With the master account, create four accounts: 'alice', 'bob', 'carol' and 'eosio_token'. Add the 'eosio.token' contract to the last account.

### The `account_create` factory

Note that the account-creation command places in the global namespace the
account object named with the first argument. The object represent a physical
account in the blockchain and in the wallet.

```md
'''

account_create("eosio_token", account_master)
contract = Contract(eosio_token, CONTRACT_DIR).deploy()

account_create("alice", account_master)
account_create("bob", account_master)
account_create("carol", account_master)
'''
```

Execute actions on the contract account:

* let eosio deposit an amount of 1000000000.0000 EOS there;
* transfer some EOS to the 'alice' account.

Use the 'push_action' method of the contract account:

```md
'''
eosio_token.push_action(
    "create", 
    {
        "issuer": account_master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0",
        "can_recall": "0",
        "can_whitelist": "0"
    }, [account_master, eosio_token])

eosio_token.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    },
    account_master)
'''
```

Execute a series of transfers between the accounts. Use the 'push_action' 
method of the contract account:

```md
'''
eosio_token.push_action(
    "transfer",
    {
        "from": alice, "to": carol,
        "quantity": "25.0000 EOS", "memo":""
    },
    alice)

eosio_token.push_action(
    "transfer",
    {
        "from": carol, "to": bob, 
        "quantity": "11.0000 EOS", "memo": ""
    },
    carol)

eosio_token.push_action(
    "transfer",
    {
        "from": carol, "to": bob, 
        "quantity": "2.0000 EOS", "memo": ""
    },
    carol)

eosio_token.push_action(
    "transfer",
    {
        "from": bob, "to": alice, \
        "quantity": "2.0000 EOS", "memo":""
    },
    bob)

'''
```

To see the records of the accounts, use the 'table' method of the contract
account:

```md
'''
table_alice = eosio_token.table("accounts", alice)
table_bob = eosio_token.table("accounts", bob)
table_carol = eosio_token.table("accounts", carol)
'''
```

### Test run

In an linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter this command:

```md
$ python3 eosio_token_contract.md
```

We expect that you get something similar to this one shown in the image below.

<img src="eosio_token.png" 
    onerror="this.src='../../../source/cases/eosio_token.png'" width="640px"/>
'''