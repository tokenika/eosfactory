'''Issue set by Patric-Shih

I follow https://eosfactory.io/build/html/patterns/set/set_account_permission.html#weights-and-threshold and try to add eosio.code permission to account as follow

```
ALICE.set_account_permission(
    Permission.ACTIVE, {
        "threshold":
            1,
        "keys": [],
        "accounts": [{
            "permission": {
                "actor": str(ALICE),
                "permission": "active"
            },
            "weight": 1
        }, {
            "permission": {
                "actor": str(ALICE),
                "permission": "eosio.code"
            },
            "weight": 1
        }]
    }, Permission.OWNER, (ALICE, Permission.OWNER))
```
The eosio.code permission is working but original ALICE@active is not working anymore. For example when doing a push action like

```
host.push_action("hi", {"player": ALICE}, permission=(ALICE, Permission.ACTIVE))
```
it shows

```
eosfactory.core.errors.Error: ERROR:
Error 3090003: Provided keys, permissions, and delays do not satisfy declared authorizations
Ensure that you have the related private keys inside your wallet and your wallet is unlocked.
Error Details:
transaction declares authority '{"actor":"ALICE","permission":"active"}', but does not have signatures for it.
```
'''
import sys, os
import eosfactory.core.config as config
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

#CONTRACT_WORKSPACE = os.path.join(config.eosf_dir(), "contracts/hello_world")
CONTRACT_WORKSPACE = os.path.join(config.eosf_dir(), "contracts/eosio_token")

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

ALICE.set_account_permission(
    Permission.ACTIVE, {
        "threshold":
            1,
        "keys": [],
        "accounts": [
            {
                "permission": 
                    {
                        "actor": ALICE,
                        "permission": "active"
                    },
                "weight": 1
            },
            {
                "permission": 
                    {
                        "actor": ALICE,
                        "permission": "eosio.code"
                    },
                "weight": 1
            }
        ]
    }, Permission.OWNER, (ALICE, Permission.OWNER)) 

HOST = new_account(MASTER)
smart = Contract(HOST, CONTRACT_WORKSPACE)
smart.build(force=False)
smart.deploy()

# HOST.push_action(
#     "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))

HOST.push_action(
    "create",
    {
        "issuer": MASTER,
        "maximum_supply": "1000000000.0000 EOS"
    },
    permission=[(MASTER, Permission.OWNER), (HOST, Permission.ACTIVE)])

HOST.push_action(
    "issue",
    {
        "to": ALICE, "quantity": "100.0000 EOS", "memo": ""
    },
    permission=(MASTER, Permission.ACTIVE))


stop()

