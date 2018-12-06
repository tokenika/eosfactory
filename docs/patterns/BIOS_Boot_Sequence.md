# BIOS Boot Sequence

This article follows a [document](https://developers.eos.io/eosio-nodeos/docs/bios-boot-sequence) from eosio archives.

## Steps 1 - 2 Setup

Start `nodeos`, create a wallet.

```python

import os
from eosfactory.eosf import *
import eosfactory.core.cleos as cleos
import eosfactory.core.setup as setup
import eosfactory.core.config as config

eosio_contracts_dir = os.path.join(
    config.eosio_repository_dir(), "build/contracts")

reset()

create_master_account("eosio")
```
## Step 3: Create important system accounts

There are several system accounts that are needed. They are created with a third argument of the `create_account` factory function, in order to force the names of the new accounts.

```python
COMMENT('''Create important system accounts''')

create_account("eosio_bpay", eosio, "eosio.bpay")
create_account("eosio_msig", eosio, "eosio.msig")
create_account("eosio_names", eosio, "eosio.names")
create_account("eosio_ram", eosio, "eosio.ram")
create_account("eosio_ramfee", eosio, "eosio.ramfee")
create_account("eosio_saving", eosio, "eosio.saving")
create_account("eosio_stake", eosio, "eosio.stake")
create_account("eosio_token", eosio, "eosio.token")
create_account("eosio_vpay", eosio, "eosio.vpay")
```

## Step 4: Install the eosio.token contract

`eosio.token` contract enables you to create, issue, transfer, and get information about tokens.

```python
COMMENT('''Install the eosio.token contract''')

contract = "eosio.token"
Contract(
    contract, 
    os.path.join(eosio_contracts_dir, contract),
    abi_file = contract + ".abi",
    wasm_file = contract + ".wasm"
    ).deploy()
```

## Step 5: Set the eosio.msig contract

`eosio.msig` contract enables and simplifies defining and managing permission levels and performing multi-signature actions.

```python
COMMENT('''Set the eosio.msig contract''')

contract = "eosio.msig"
Contract(
    contract, 
    os.path.join(eosio_contracts_dir, contract),
    abi_file = contract + ".abi",
    wasm_file = contract + ".wasm"
    ).deploy()
```

## Step 6: Create and allocate the SYS currency

```python
COMMENT('''Create and allocate the SYS currency''')

eosio_token.push_action(
    "create",
    [eosio, "10000000000.0000 SYS"],
    (eosio_token, Permission.ACTIVE))

eosio_token.push_action(
    "issue",
    [eosio, "1000000000.0000 SYS", "memo"],
    (eosio, Permission.ACTIVE))
```

In the first step above, the create action from the eosio.token contract, authorized by the eosio.token account, creates 10B SYS tokens in the eosio account. This effectively creates the maximum supply of tokens, but does not put any tokens into circulation. Tokens not in circulation can be considered to be held in reserve.

In the second step, the eosio.token contract's issue action takes 1B SYS tokens out of reserve and puts them into circulation. At the time of issue, the tokens are held within the eosio account. Since the eosio account owns the reserve of uncirculated tokens, its authority is required to do the action.

As a point of interest, from an economic point of view, moving token from reserve into circulation, such as by issuing tokens, is an inflationary action. Issuing tokens is just one way that inflation can occur.

## Step 7: Set the eosio.system contract

`eosio.system` contract provides the actions for pretty much all token-based operational behavior. Prior to installing the system contract, actions are done independent of accounting. Once the system contract is enabled, **actions now have an economic element to them**. Resources (cpu, network, memory) must be paid for. Likewise, new accounts must be paid for. The system contract enables tokens to be staked and unstaked, resources to be purchased, potential producers to be registered and subsequently voted on, producer rewards to be claimed, privileges and limits to be set, and more.

Therefore, with the `eosio.system` contract, all the simple tests, using the simple signature of the `create_account` contract factory function, will fail.


```python
COMMENT('''Set the eosio.system contract''')

contract = "eosio.system"
Contract(
    eosio, 
    os.path.join(eosio_contracts_dir, contract),
    abi_file = contract + ".abi",
    wasm_file = contract + ".wasm"
    ).deploy()


```