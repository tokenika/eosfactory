# Set Account Permission

The `set_account_permission` command creates or updates an account's permission. You might want to see the plain `cleos` approach [here](https://developers.eos.io/eosio-cleos/v1.2.0/reference#cleos-set-account).

**NOTE**: The Python code listed below is executable, as explained [here](../README.html).

```python
from eosfactory.eosf import *
import eosfactory.core.setup as setup
```

```python
reset()
create_master_account("master")
create_account("alice", master)
alice.info()
```

The permissions section of `alice.info()`:

```md
permissions:
     owner     1:    1 alice@owner
        active     1:    1 alice@active
```

## Set new key to a permission
```python
COMMENT("Set new key to a permission:")
key = CreateKey(is_verbose=False)
setup.is_print_command_lines = True
alice.set_account_permission(
    Permission.ACTIVE, key.key_public, Permission.OWNER, 
    (alice, Permission.OWNER))
setup.is_print_command_lines = False
alice.info()
```

The `permissions` section of `alice.info()`:

```md
permissions:
     owner     1:    1 alice@owner
        active     1:    1 alice@active
```

## Set an account (instead of a key) as authority for a permission
```python
COMMENT("Set an account (instead of a key) as authority for a permission:")
create_account("bob", master)
setup.is_print_command_lines = True
alice.set_account_permission(
    Permission.ACTIVE, bob, Permission.OWNER, 
    (alice, Permission.OWNER))
setup.is_print_command_lines = False
alice.info()
```

The permissions section of `alice.info()`:

```md
permissions:
     owner     1:    1 alice@owner
        active     1:    1 bob@active
```

## Weights and Threshold

Note that actors have to be sorted in the ``authority`` JSON.

```python
COMMENT("Weights and Threshold:")
create_account("carol", master)
actors = [str(bob), str(carol)]
actors.sort()
alice.set_account_permission(Permission.ACTIVE,
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
    (alice, Permission.OWNER))
alice.info()
```
The permissions section of `alice.info()`:
```md
permissions:
     owner     1:    1 alice@owner
        active   100:    25 carol@active, 75 bob@active
```

## Set two-weighted keys

Note that keys have to be sorted in the ``authority`` JSON.
```python
COMMENT("Set two weighted keys:")
keys = [bob.owner_public(), carol.owner_public()]
keys.sort()
alice.set_account_permission(Permission.ACTIVE,
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
    (alice, Permission.OWNER)
)
alice.info()
```
The permissions section of `alice.info()`:

```md
permissions:
     owner     1:    1 alice@owner
        active   100:    50 alice@active, 50 bob@owner
```

```python
stop()
```

