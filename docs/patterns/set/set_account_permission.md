# Set Account Permission

The `set_account_permission` command creates or updates an account's permission. You might want to see the plain `cleos` approach [here](https://developers.eos.io/eosio-cleos/v1.2.0/reference#cleos-set-account).

**NOTE**: The Python code listed below is executable, as explained [here](../README.html).

```python
import os
import eosfactory.core.setup as setup
# Set the interface configuration (CLEOS or EOSJS):
# setup.set_is_eosjs()

from eosfactory.eosf import *
```

```python
reset()
create_master_account("MASTER")
create_account("ALICE", MASTER)
ALICE.info()
```

The permissions section of ALICE.info():

```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=1
                       wght=1 key=ALICE@active
```

## Let ALICE set `eosio.code` permission to herself

```python
COMMENT("""
ALICE sets `eosio.code` permission to herself:
""")

ALICE.set_account_permission(
    Permission.ACTIVE, ALICE, add_code=True)
ALICE.info()
```
The permissions section of ALICE.info():
```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=1
                       wght=1 key=ALICE@active
                       wght=1 perm=ALICE@eosio.code
```

## Let ALICE remove her `eosio.code` permission

```python
COMMENT("""
ALICE removes her `eosio.code` permission:
""")

ALICE.set_account_permission(
    Permission.ACTIVE, ALICE, remove_code=True)
ALICE.info()
```
The permissions section of ALICE.info():
```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=1
                       wght=1 key=ALICE@active
### memory:
                   quota: unlimited, used: 2.7 KiB
```

## Set new key to a permission
```python
COMMENT("""
Create a key and save it to the wallet, then set it to the ALICE's ``active1`` permissions.
""")

key = CreateKey(is_verbose=False)
get_wallet().import_key(key)

ALICE.set_account_permission(
    "active1", key.key_public, Permission.OWNER,
    permission=(ALICE, Permission.OWNER))
ALICE.info()
```

The `permissions` section of `ALICE.info()`:
```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=1
                       wght=1 key=ALICE@active
    |--> active1 thrd=1
                       wght=1 key=EOS7NPEUv5jodCsDDFmeRiWVjL4v1jfddHsM1xsz3EVB4wLbupqwE
```

## Remove a permission.
```python
COMMENT("""
Remove the previously set permission ``active1``:
""")

ALICE.set_account_permission(
    "active1", "remove", Permission.OWNER,
    permission=(ALICE, Permission.OWNER))
ALICE.info()
```
The `permissions` section of `ALICE.info()`:
```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=1
                       wght=1 key=ALICE@active
```

## Weights and Threshold

```python
COMMENT("""
Create two new accounts and use them as weighted permissions for ALICE:
""")

create_account("BOB", MASTER)
create_account("CAROL", MASTER)
ALICE.set_account_permission(Permission.ACTIVE,
    {
        "threshold" : 100, 
        "keys" : [], 
        "accounts" : 
            [
                {
                    "permission":
                        {
                            "actor": BOB,
                            "permission":"active"
                        },
                    "weight":25
                }, 
                {	
                    "permission":
                        {
                            "actor": CAROL,
                            "permission":"active"
                        },
                    "weight":75
                }
            ]
    },
    Permission.OWNER,
    (ALICE, Permission.OWNER))
ALICE.info()
```

> **NOTE**: `cleos` eosio CLI demands that the lists in the `authority` JSON are specifically sorted. EOSFactory sorts them itself.

The permissions section of `ALICE.info()`:
```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=100
                       wght=75 perm=CAROL@active
                       wght=25 perm=BOB@active
    |--> active1 thrd=1
                       wght=1 key=EOS6GeD7tNy8iqa7DdncAz7qGi4PG3agDE37jmdzUKLdLYaTUogzm
```

## Set permission from a file

The argument ``authority`` can be set from a file, for example, the file `set_account_permission.json`:
```
{
    "threshold" : 100, 
    "keys" : [], 
    "accounts" : 
        [
            {
                "permission":
                    {
                        "actor": BOB,
                        "permission":"active"
                    },
                "weight":15
            }, 
            {	
                "permission":
                    {
                        "actor": CAROL,
                        "permission":"active"
                    },
                "weight":85
            }
        ]
}
```
Note, that the account names can be symbolic (without quatation marks).

```python
COMMENT("""
Set permission from the file ``set_account_permission.json``:
""")

ALICE.set_account_permission(
    Permission.ACTIVE,
    os.path.join(os.path.dirname(__file__), "set_account_permission.json"),
    Permission.OWNER,
    permission=(ALICE, Permission.OWNER))
ALICE.info()
```

The permissions section of `ALICE.info()`:
```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=100
                       wght=15 perm=BOB@active
                       wght=85 perm=CAROL@active
```

## Set two weighted keys

```python
COMMENT("""
Set two weighted keys:
""")

ALICE.set_account_permission(Permission.ACTIVE,
    {
        "threshold" : 100, 
        "keys" : 
            [
                {
                    "key": BOB.owner_public(),
                    "weight": 50
                },
                {
                    "key": CAROL.owner_public(),
                    "weight": 50
                }                    
            ]
    },
    Permission.OWNER,
    (ALICE, Permission.OWNER)
)
ALICE.info()
```
The permissions section of `ALICE.info()`:

```
### permissions:
    owner thrd=1
                  wght=1 key=ALICE@owner
    |--> active thrd=100
                       wght=50 key=ALICE@active
                       wght=50 key=CAROL@owner
    |--> active1 thrd=1
                       wght=1 key=EOS6GeD7tNy8iqa7DdncAz7qGi4PG3agDE37jmdzUKLdLYaTUogzm
```

```python
stop()
```

