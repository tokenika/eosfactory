# set action permission

Set's authorization for a contract's specific action.

The python code involved can be executed, as it is explained [here](../README.html).

```python

from eosfactory.eosf import *
import eosfactory.core.cleos as cleos
import eosfactory.core.setup as setup

reset()
create_master_account("master")
create_account("PRODUCERACCT", master)
```

```python

PRODUCERACCT.info()
```

The `permissions` section of `PRODUCERACCT.info()`:

```md
permissions:
     owner     1:    1 PRODUCERACCT@owner
        active     1:    1 PRODUCERACCT@active
```

```python

COMMENT('''PRODUCERACCT.set_account_permission("claimer"''')
PRODUCERACCT.set_account_permission("claimer",
    {
        "threshold" : 1, 
        "keys" : 
            [
                {
                    "key": PRODUCERACCT.active(),
                    "weight": 1
                }
            ]

    },
    Permission.ACTIVE)

PRODUCERACCT.info()
```

The `permissions` section of `PRODUCERACCT.info()`:

```md
permissions:
     owner     1:    1 PRODUCERACCT@owner
        active     1:    1 PRODUCERACCT@active
           claimer     1:    1 PRODUCERACCT@active
```

```python

COMMENT('''PRODUCERACCT.set_action_permission("eosio"''')
PRODUCERACCT.set_action_permission(
    "eosio", "claimrewards", "claimer", permission=(PRODUCERACCT, "active"))

```

```python
stop()
```