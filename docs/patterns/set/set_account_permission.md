# set account permission

Creates or updates an account's permission.

```python

from eosfactory.eosf import *
import eosfactory.core.cleos as cleos
import eosfactory.core.setup as setup

reset()
create_master_account("master")
create_account("Alice", master)
create_account("Jim", master)
Alice.info()

```
`Alice.info()` reads, in the *permissions* section:
```md
permissions:
     owner     1:    1 Alice@owner
        active     1:    1 Alice@active
```

## Set new key to a permission
```python

COMMENT("Set new key to a permission:")
key = cleos.CreateKey(is_verbose=False)
setup.is_print_command_line = True
Alice.set_account_permission(
    Permission.ACTIVE, key.key_public, Permission.OWNER, 
    (Alice, Permission.OWNER))
setup.is_print_command_line = False
Alice.info()

```
Now, the *permissions* section of `Alice.info()` changes:
```md
permissions:
     owner     1:    1 Alice@owner
        active     1:    1 Alice@active
```

## Set an account (instead of a key) as authority for a permission
```python

COMMENT("Set an account (instead of a key) as authority for a permission:")
create_account("Bob", master)
setup.is_print_command_line = True
Alice.set_account_permission(
    Permission.ACTIVE, Bob, Permission.OWNER, 
    (Alice, Permission.OWNER))
setup.is_print_command_line = False
Alice.info()

```

The permissions section of `Alice.info()`:

```md
permissions:
     owner     1:    1 Alice@owner
        active     1:    1 Bob@active
```

## Weights and Threshold

Note that actors have to be sorted in the ``authority`` JSON. (Why ``cleos`` cannot sort them itself?)

```python

COMMENT("Weights and Threshold:")
create_account("Carol", master)
actors = [str(Bob), str(Carol)]
actors.sort()
Alice.set_account_permission(Permission.ACTIVE,
    {
        "threshold" : 100, 
        "keys" : [], 
        "accounts" : 
            [
                {
                    "permission":
                        {
                            "actor": actors[0],
                            "permission":"active"
                        },
                    "weight":25
                }, 
                {	
                    "permission":
                        {
                            "actor":actors[1],
                            "permission":"active"
                        },
                    "weight":75
                }
            ]
    },
    Permission.OWNER,
    (Alice, Permission.OWNER))
Alice.info()

```
The permissions section of `Alice.info()`:
```md
permissions:
     owner     1:    1 Alice@owner
        active   100:    25 Carol@active, 75 Bob@active
```

## Set two weighted keys

Note that keys have to be sorted in the ``authority`` JSON. (Why ``cleos`` cannot sort them itself?)
```python

COMMENT("Set two weighted keys:")
keys = [Bob.owner(), Carol.owner()]
keys.sort()

Alice.set_account_permission(Permission.ACTIVE,
    {
        "threshold" : 100, 
        "keys" : 
            [
                {
                    "key": keys[0],
                    "weight": 50
                },
                {
                    "key": keys[1],
                    "weight": 50
                }                    
            ]
    },
    Permission.OWNER,
    (Alice, Permission.OWNER)
)
Alice.info()

```
The permissions section of `Alice.info()`:

```md
permissions:
     owner     1:    1 Alice@owner
        active   100:    50 Alice@active, 50 Bob@owner
```

