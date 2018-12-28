# Set Action Permission

The `set_account_permission` command sets authorization for a contract's specific action. You might want to see the plain `cleos` approach [here](https://developers.eos.io/eosio-cleos/v1.2.0/reference#cleos-set-action-permission).

**NOTE**: The Python code listed below is executable, as explained [here](../README.html).

```python
from eosfactory.eosf import *
```

```python
reset()
create_master_account("master")
create_account("producer", master)
producer.info()
```

The `permissions` section of `producer.info()`:

```md
permissions:
     owner     1:    1 producer@owner
        active     1:    1 producer@active
```

```python
COMMENT('''producer.set_account_permission("claimer"''')
producer.set_account_permission("claimer",
    {
        "threshold" : 1, 
        "keys" : 
            [
                {
                    "key": producer.active(),
                    "weight": 1
                }
            ]

    },
    Permission.ACTIVE)

producer.info()
```

The `permissions` section of `producer.info()`:

```md
permissions:
     owner     1:    1 producer@owner
        active     1:    1 producer@active
           claimer     1:    1 producer@active
```

```python
COMMENT('''producer.set_action_permission("eosio"''')
producer.set_action_permission(
    "eosio", "claimrewards", "claimer", permission=(producer, "active"))
```

```python
stop()
```