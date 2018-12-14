# The Arbitration Contract

## Scenario

There are two persons, `Alice` and `Carol`, both having their accounts in a `Bank`. The `Bank` provides the service of `LC` (Letter of Credit). Hence, the parties can enter a deal that involves a temporal deposition of resources in the `Bank`, released when the deal is concluded in an agreed way.

## Setup EOSFactory

### Definitions

```python
import time
import os
import sys
import eosfactory.core.config as config
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])
CONTRACT_WORKSPACE = sys.path[0] + "/../"
reset() # clean local node started
create_master_account("eosio")
```

### Arrange the Bank

The `Bank` is made of two smart contracts. One belongs to the set of the eosio system contracts: it is `eosio.token`. It implements money transfers.

The other contract is the issue of the current project. This one implements the idea of the Letter of Credit.

Both contracts are, in fact, eosio accounts, `Bank` and `LC`, accordingly. Each of them is equipped with relevant actions. The `LC` account is to be related to the `Bank` account with a system permission named `eosio.code`.

```python
# eosio.token name is hard-codded in the source of the contract:
create_account("Bank", eosio, "eosio.token")
contract_bank = Contract(
    Bank, os.path.join(config.eosf_dir(), "contracts/02_eosio_token"))
# contract_bank.build(force=False)
contract_bank.deploy()

create_account("LC", eosio)
contract_lc = Contract(LC, CONTRACT_WORKSPACE)
# contract_lc.build(force=False)
contract_lc.deploy()
```

The `LC` Letter of Credit eosio smart contract requires the `eosio.code` permission to be able to execute actions of the `eosio.token` contract:

```python
COMMENT('''
LC.set_account_permission
''')
LC.set_account_permission(Permission.ACTIVE,
    {
        "threshold": 1,
        "accounts": 
            [
                {
                    "permission": 
                        {
                            "actor": LC,
                            "permission": "eosio.code"
                        },
                    "weight":1
                }
            ]
    },
    Permission.OWNER
)
```

In the real world, the Bank is funded with its founder's money, here, in a local 
testnet, it is funded at the expense of `eosio`:

```python
Bank.push_action(
    "create", 
    {
        "issuer": eosio, 
        "maximum_supply": "1000000000.0000 SYS"
    }, [eosio, Bank])
```

### Create actors: `Alice` and `Carol`

```python
create_account("Alice", eosio)
create_account("Carol", eosio)
```

Again, what is impossible in the real world, but here is practical, for simplicity purposes: the `Bank` issues money to `Alice`:

```python
Bank.push_action(
    "issue", 
    {
        "to": Alice, 
        "quantity": "100.0000 SYS", 
        "memo": ""
    }, eosio)
```

We can inspect the Bank accounts. `Alice` has money, and `Carol` has not.

```python
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)
```

## Let `Alice` instruct the `Bank` to issue a Letter of Credit on behalf of `Carol`

`Alice` accepts an offer from Carol who sells foos, but she is not sure of the quality of the goods. The parties agreed that `Alice` pays if, and only if, she is satisfied.

`Alice` opens a deposit in the Bank:
```python
COMMENT('''
LC.push_action("opendeposit"
''')
LC.push_action(
    "opendeposit", {"buyer": Alice, "seller": Carol}, Alice)
```

`Alice` transfers the deposit to a credit account of the `Bank`. Technically, the `LC` smart contract taps to the transfer action of the `Bank` contract (with `LC`'s `transfer` action), and makes bookkeeping.

```python
COMMENT('''
Bank.push_action("transfer"
''')
Bank.push_action(
    "transfer", 
    {
        "from": Alice, 
        "to": LC, 
        "quantity": "10.0000 SYS", 
        "memo": str(Carol)
    }, Alice)
```

Let us inspect the bank accounts: `Carol`'s account is still empty:

```python
COMMENT('''
After transfer:
''')
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)
```

`Carol` fulfils the deal and claims the payment:

```python
COMMENT('''
LC.push_action("claim"
''')
LC.push_action(
    "claim", 
    {"buyer": Alice, "seller": Carol}, 
    Carol)
```

`Carol` waits for her money.

```python
COMMENT('''
After Carol's claim:
''')
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)
```

The `LC` contract takes time to verify the deal:

```python
COMMENT('''
The ``LC`` contract need a time delay to arrange verify the deal:
''')
time.sleep(5)
```

`Carol` signs the `refund` order. But how the bank knows that `Alice` is satisfied?

```python
COMMENT('''
LC.push_action("refund"
''')
LC.push_action(
    "refund", {"buyer": Alice, "seller": Carol}, Carol)
```

Now, after the `refund` action, `Carol` has her money:
```python
COMMENT('''
After refund:
''')
Bank.table("accounts", Alice)
Bank.table("accounts", Carol)
```

## Clean-up

```python
stop()
```