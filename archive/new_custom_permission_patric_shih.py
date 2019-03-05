'''Issue set by Patric-Shih

I follow https://eosfactory.io/build/html/patterns/set/set_account_permission.html#weights-and-threshold and try to add eosio.code permission to account as follow

```
alice.set_account_permission(
    Permission.ACTIVE, {
        "threshold":
            1,
        "keys": [],
        "accounts": [{
            "permission": {
                "actor": str(alice),
                "permission": "active"
            },
            "weight": 1
        }, {
            "permission": {
                "actor": str(alice),
                "permission": "eosio.code"
            },
            "weight": 1
        }]
    }, Permission.OWNER, (alice, Permission.OWNER))
```
The eosio.code permission is working but original alice@active is not working anymore. For example when doing a push action like

```
host.push_action("hi", {"player": alice}, permission=(alice, Permission.ACTIVE))
```
it shows

```
eosfactory.core.errors.Error: ERROR:
Error 3090003: Provided keys, permissions, and delays do not satisfy declared authorizations
Ensure that you have the related private keys inside your wallet and your wallet is unlocked.
Error Details:
transaction declares authority '{"actor":"alice","permission":"active"}', but does not have signatures for it.
```
'''
import sys, os
import eosfactory.core.config as config
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = os.path.join(config.eosf_dir(), "contracts/hello_world")

reset()
MASTER = new_master_account()

COMMENT('''
Build and deploy the contract:
''')

COMMENT('''
Create test accounts:
''')
ALICE = new_account(MASTER)
print(ALICE.active_key); 
print(get_wallet().keys())
CAROL = new_account(MASTER)
COMMENT('''
Evidently, EOSIO does not like giving permissins to itself. Change `str(alice)` 
to `carol`.
You do not need to convert account object to string in the `actor` field. The conversion is needed if there is many actors: EOSIO has them sorted lexicographically. Therefore, in the tutorial actors physical names are sorted, being converted to strings.
''')
ALICE.set_account_permission(
    Permission.ACTIVE, {
        "threshold":
            1,
        "keys": [],
        "accounts": [
            {
                "permission": 
                {
                    "actor": CAROL,
                    "permission": "active"
                },
                "weight": 1
            },
            {
                "permission": 
                {
                    "actor": CAROL,
                    "permission": "eosio.code"
                },
                "weight": 1
            }
        ]
    }, Permission.OWNER, (ALICE, Permission.OWNER)) 

HOST = new_account(MASTER)
contract = Contract(HOST, CONTRACT_WORKSPACE)
contract.build(force=False)
contract.deploy()

COMMENT('''
Test an action for Alice:
''')
HOST.push_action(
    "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))
assert("ALICE" in DEBUG())

COMMENT('''
Test an action for Carol:
''')
HOST.push_action(
    "hi", {"user":CAROL}, permission=(CAROL, Permission.ACTIVE))
assert("CAROL" in DEBUG())

stop()

