# set action permission

Set's authorization for a contract's specific action

```python

from eosfactory.eosf import *
import eosfactory.core.cleos as cleos
import eosfactory.core.setup as setup

reset()
create_master_account("master")

create_account("host", master)
contract = Contract(host, "02_eosio_token")
# contract.build(force=False)
contract.deploy()

create_account("PRODUCERACCT", master)
create_account("Bob", master)
```

```python

PRODUCERACCT.info()

COMMENT('''PRODUCERACCT.set_account_permission("create"''')
PRODUCERACCT.set_account_permission("create",
    {
        "threshold" : 1, 
        "keys" : 
            [], 
        "accounts" : 
            [
                {
                    "permission":
                        {
                            "actor": host,
                            "permission":"active"
                        },
                    "weight":1
                }
            ]

    },
    Permission.ACTIVE)

PRODUCERACCT.info()

COMMENT('''PRODUCERACCT.set_action_permission(host''')
PRODUCERACCT.set_action_permission(
    host, "create", "create", 
    permission=(PRODUCERACCT, "create"))

host.push_action(
    "create",
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0",
        "can_recall": "0",
        "can_whitelist": "0"
    },
    permission=(PRODUCERACCT, "create")
)

#cleos set action permission @ACCOUNT @CONTRACT ACTION_NAME PERMISSION_NAME

#Link a `voteproducer` action to the 'vote' permissions
# PRODUCERACCT.set_action_permission(
#     "eosio.system", "voteproducer", "voting", (PRODUCERACCT, "voting")
# )

# ) sandwichfarm eosio.system voteproducer voting -p sandwichfarm@voting

# #Now can execute the transaction with the previously set permissions. 
# cleos system voteproducer approve sandwichfarm someproducer -p sandwichfarm@voting
```