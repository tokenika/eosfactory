# The Arbitration Contract

## Scenario

There are two parities, `Alice` and `Carol`, both having their accounts with an `Arbitrator`. The `Arbitrator` provides the service of `Escrow`. Hence, the parties can enter a deal that involves a temporary deposit of payment with the `Arbitrator`, which will be released when the deal is concluded and no party objects to it or if the `Arbitrator` issues a ruling.

## Set up a local testnet

We start by some housekeeping definitions aimed at initializing a local testnet and getting reference to the master account called `eosio`:

```python
import time, os, sys
import eosfactory.core.config as config
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])
CONTRACT_WORKSPACE = sys.path[0] + "/../"
reset() # reset the local testnet
create_master_account("eosio")
```

## Set up the contracts

There are two contracts involved.

The `Arbitrator` account holds a contract facilitating transfers of payments:

```python
# eosio.token name is hard-codded in the source of the contract:
create_account("Arbitrator", eosio, "eosio.token")
contract_arbitrator = Contract(
    Arbitrator, os.path.join(config.eosf_dir(), "contracts/02_eosio_token"))
contract_arbitrator.build(force=False)
contract_arbitrator.deploy()
```

While the `Escrow` account holds a contract implementing the actual arbitration:
```python
create_account("Escrow", eosio)
contract_escrow = Contract(Escrow, CONTRACT_WORKSPACE)
contract_escrow.build(force=False)
contract_escrow.deploy()
```

## Set up the permissions

The `Escrow` account needs to be related to the `Arbitrator` account with a system permission named `eosio.code`. This allows it to execute actions of the `eosio.token` contract:

```python
COMMENT('''
Escrow.set_account_permission()
''')
Escrow.set_account_permission(Permission.ACTIVE,
    {
        "threshold": 1,
        "accounts": 
            [
                {
                    "permission": 
                        {
                            "actor": Escrow,
                            "permission": "eosio.code"
                        },
                    "weight":1
                }
            ]
    },
    Permission.OWNER
)
```

In the real world, the `Arbitrator` is funded with its creator's money. But in this simplified example , on a local it is funded at the expense of the `eosio` account:

```python
Arbitrator.push_action(
    "create", 
    {
        "issuer": eosio, 
        "maximum_supply": "1000000000.0000 SYS"
    }, [eosio, Arbitrator])
```

## Create actors

We create two actors`Alice` and `Carol`:

```python
create_account("Alice", eosio)
create_account("Carol", eosio)
```

Again, what is impossible in the real world, but here is practical, for simplicity purposes the `Arbitrator` issues money to `Alice`:

```python
Arbitrator.push_action(
    "issue", 
    {
        "to": Alice, 
        "quantity": "100.0000 SYS", 
        "memo": ""
    }, eosio)
```

We can inspect the `Arbitrator` accounts.

`Alice` has some `SYS` tokens, while`Carol` has none:

```python
Arbitrator.table("accounts", Alice)
Arbitrator.table("accounts", Carol)
```

## Initiate the escrow process

`Alice` has agreed to pay `Carol` for the purchased merchandise, but she is not sure of its quality. Thus, `Alice` instructs the `Arbitrator` to initiate an escrow process by opening a deposit:

```python
COMMENT('''
Escrow.push_action("opendeposit")
''')
Escrow.push_action(
    "opendeposit", {"buyer": Alice, "seller": Carol}, Alice)
```

## Apply the escrow

`Alice` transfers the payment amount to an account of the `Arbitrator`. Technically, the `Escrow` smart contract taps to the transfer action of the `Arbitrator` contract (with `Escrow`'s `transfer` action), and performs bookkeeping.

```python
COMMENT('''
Arbitrator.push_action("transfer")
''')
Arbitrator.push_action(
    "transfer", 
    {
        "from": Alice, 
        "to": Escrow, 
        "quantity": "10.0000 SYS", 
        "memo": str(Carol)
    }, Alice)
```

Let us inspect the accounts. `Carol`'s account is still empty:

```python
COMMENT('''
After transfer:
''')
Arbitrator.table("accounts", Alice)
Arbitrator.table("accounts", Carol)
```

`Carol` fulfils the deal and claims the payment:

```python
COMMENT('''
Escrow.push_action("claim")
''')
Escrow.push_action(
    "claim", 
    {"buyer": Alice, "seller": Carol}, 
    Carol)
```

`Carol` waits for her money.

```python
COMMENT('''
After Carol's claim:
''')
Arbitrator.table("accounts", Alice)
Arbitrator.table("accounts", Carol)
```

The `Escrow` contract takes time to verify the deal:

```python
COMMENT('''
The ``Escrow`` contract need a time delay to arrange verify the deal:
''')
time.sleep(5)
```

## Finalize the escrow

`Carol` signs the `refund` order. If there is no objection raised by `Alice`, the `Arbitrator` assumes she is satisfied and allows the refund to go through:

```python
COMMENT('''
Escrow.push_action("refund")
''')
Escrow.push_action(
    "refund", {"buyer": Alice, "seller": Carol}, Carol)
```

Now, after the `refund` action is complete, `Carol` has received the payment:
```python
COMMENT('''
After refund:
''')
Arbitrator.table("accounts", Alice)
Arbitrator.table("accounts", Carol)
```

## Clean-up the local testnet

```python
stop()
```