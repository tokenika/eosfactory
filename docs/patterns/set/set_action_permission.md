# Set Action Permission

The `set_action_permission` command sets authorization for a contract's specific action. You might want to see the plain `cleos` approach [here](https://developers.eos.io/eosio-cleos/v1.2.0/reference#cleos-set-action-permission).

**NOTE**: The Python code listed below is executable, as explained [here](../README.html).

```python
import eosfactory.core.setup as setup
# Set the interface configuration (CLEOS or EOSJS):
setup.set_is_eosjs()
from eosfactory.eosf import *
```

```python
COMMENT("""
Reset the local testnet, create a master account -- having the authority to create
accounts -- and let it create a test account object named ``PRODUCER``:
""")
reset()
create_master_account("MASTER")
create_account("PRODUCER", MASTER)
PRODUCER.info()
```

The `permissions` section of `PRODUCER.info()`:
```
### permissions:
    owner thrd=1
                  wght=1 key=PRODUCER@owner
    |--> active thrd=1
                       wght=1 key=PRODUCER@active
         |--> claimer thrd=1
                            wght=1 key=PRODUCER@active
```

```python
COMMENT("""
Set an account permission named ``claimer`` to the account PRODUCER:
""")

PRODUCER.set_account_permission("claimer",
    {
        "threshold" : 1, 
        "keys" : 
            [
                {
                    "key": PRODUCER.active_public(),
                    "weight": 1
                }
            ]

    },
    Permission.ACTIVE)

PRODUCER.info()
```

The `permissions` section of `PRODUCER.info()`:
```
### permissions:
    owner thrd=1
                  wght=1 key=PRODUCER@owner
    |--> active thrd=1
                       wght=1 key=PRODUCER@active
         |--> claimer thrd=1
                            wght=1 key=PRODUCER@active
```

```python
COMMENT("""
Now, set permission to the account PRODUCER to execute an action named
``claimrewards``, owned by the MASTER with the permission ``claimer``.
""")
PRODUCER.set_action_permission(MASTER, "claimrewards", "claimer")

OUT(str(PRODUCER.set_action_permission_result))
```
See the following confirmation of the action permission setting:
```
>>>>>>>>>>                MASTER <= MASTER::linkauth:
    {'account': PRODUCER, 'code': MASTER, 'type': 'claimrewards', 'requirement': 'claimer'}
```

```python
stop()
```