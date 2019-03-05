# The Arbitration Contract

## Scenario

There are two parities, `ALICE` and `CAROL`, both having their accounts with an `ARBITRATOR`. The `ARBITRATOR` provides the service of `ESCROW`. Hence, the parties can enter a deal that involves a temporary deposit of payment with the `ARBITRATOR`, which will be released when the deal is concluded and no party objects to it or if the `ARBITRATOR` issues a ruling.

```python
import time, os, sys
import eosfactory.core.config as config
from eosfactory.eosf import *

EOSIO = MasterAccount()
ESCROW = Account()
ARBITRATOR = Account()
ALICE = Account()
CAROL = Account()
```

## Set up a local testnet

We start by some housekeeping definitions aimed at initializing a local testnet and getting reference to the master account called `EOSIO`:

```python
verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])
CONTRACT_WORKSPACE = sys.path[0] + "/../"
reset() # reset the local testnet
create_master_account("EOSIO")
```

## Set up the contracts

There are two contracts involved.

The `ARBITRATOR` account holds a contract facilitating transfers of payments:

```python
# EOSIO.token name is hard-codded in the source of the contract:
create_account("ARBITRATOR", EOSIO, "eosio.token")
contract_arbitrator = Contract(
    ARBITRATOR, os.path.join(config.eosf_dir(), "contracts/eosio_token"))
contract_arbitrator.build(force=False)
contract_arbitrator.deploy()
```

While the `ESCROW` account holds a contract implementing the actual arbitration:
```python
create_account("ESCROW", EOSIO)
contract_escrow = Contract(ESCROW, CONTRACT_WORKSPACE)
contract_escrow.build(force=False)
contract_escrow.deploy()
```

## Set up the permissions

The `ESCROW` account needs to be related to the `ARBITRATOR` account with a system permission named `eosio.code`. This allows it to execute actions of the `EOSIO.token` contract:

```python
COMMENT('''
ESCROW.set_account_permission()
''')
ESCROW.set_account_permission(Permission.ACTIVE,
    {
        "threshold": 1,
        "accounts": 
            [
                {
                    "permission": 
                        {
                            "actor": ESCROW,
                            "permission": "eosio.code"
                        },
                    "weight":1
                }
            ]
    },
    Permission.OWNER
)
```

In the real world, the `ARBITRATOR` is funded with its creator's money. But in this simplified example , on a local it is funded at the expense of the `EOSIO` account:

```python
ARBITRATOR.push_action(
    "create", 
    {
        "issuer": EOSIO, 
        "maximum_supply": "1000000000.0000 SYS"
    }, [EOSIO, ARBITRATOR])
```

## Create actors

We create two actors`ALICE` and `CAROL`:

```python
create_account("ALICE", EOSIO)
create_account("CAROL", EOSIO)
```

Again, what is impossible in the real world, but here is practical, for simplicity purposes the `ARBITRATOR` issues money to `ALICE`:

```python
ARBITRATOR.push_action(
    "issue", 
    {
        "to": ALICE, 
        "quantity": "100.0000 SYS", 
        "memo": ""
    }, EOSIO)
```

We can inspect the `ARBITRATOR` accounts.

`ALICE` has some `SYS` tokens, while`CAROL` has none:

```python
ARBITRATOR.table("accounts", ALICE)
ARBITRATOR.table("accounts", CAROL)
```

## Initiate the escrow process

`ALICE` has agreed to pay `CAROL` for the purchased merchandise, but she is not sure of its quality. Thus, `ALICE` instructs the `ARBITRATOR` to initiate an escrow process by opening a deposit:

```python
COMMENT('''
ESCROW.push_action("opendeposit")
''')
ESCROW.push_action(
    "opendeposit", {"buyer": ALICE, "seller": CAROL}, ALICE)
```

## Apply the escrow

`ALICE` transfers the payment amount to an account of the `ARBITRATOR`. Technically, the `ESCROW` smart contract taps to the transfer action of the `ARBITRATOR` contract (with `ESCROW`'s `transfer` action), and performs bookkeeping.

```python
COMMENT('''
ARBITRATOR.push_action("transfer")
''')
ARBITRATOR.push_action(
    "transfer", 
    {
        "from": ALICE, 
        "to": ESCROW, 
        "quantity": "10.0000 SYS", 
        "memo": str(CAROL)
    }, ALICE)
```

Let us inspect the accounts. `CAROL`'s account is still empty:

```python
COMMENT('''
After transfer:
''')
ARBITRATOR.table("accounts", ALICE)
ARBITRATOR.table("accounts", CAROL)
```

`CAROL` fulfils the deal and claims the payment:

```python
COMMENT('''
ESCROW.push_action("claim")
''')
ESCROW.push_action(
    "claim", 
    {"buyer": ALICE, "seller": CAROL}, 
    CAROL)
```

`CAROL` waits for her money.

```python
COMMENT('''
After CAROL's claim:
''')
ARBITRATOR.table("accounts", ALICE)
ARBITRATOR.table("accounts", CAROL)
```

The `ESCROW` contract takes time to verify the deal:

```python
COMMENT('''
The ``ESCROW`` contract need a time delay to arrange verify the deal:
''')
time.sleep(5)
```

## Finalize the escrow

`CAROL` signs the `refund` order. If there is no objection raised by `ALICE`, the `ARBITRATOR` assumes she is satisfied and allows the refund to go through:

```python
COMMENT('''
ESCROW.push_action("refund")
''')
ESCROW.push_action(
    "refund", {"buyer": ALICE, "seller": CAROL}, CAROL)
```

Now, after the `refund` action is complete, `CAROL` has received the payment:
```python
COMMENT('''
After refund:
''')
ARBITRATOR.table("accounts", ALICE)
ARBITRATOR.table("accounts", CAROL)
```

## Clean-up the local testnet

```python
stop()
```

## Test run

The python blocks in the current Markdown document can be executed with a provided bash tool. While the working directory is the root of the `EOSFactory` installation, do:

```bash
eosfactory/pythonmd.sh archive/arbitration/tests/test1.md
```