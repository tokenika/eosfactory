# BIOS Boot Sequence

This article follows a [document](https://developers.eos.io/eosio-nodeos/docs/bios-boot-sequence) from eosio archives.

The python code involved can be executed, as it is explained [here](./README.html).

## Steps 0 System contracts

Execution of the presented code depends on definitions given in [eosio.contracts repository](https://github.com/EOSIO/eosio.contracts), hence, if running the code, as it is explained [here](./README.html), for the first time, you will be asked for the root directory of the repository (build).

The following chunk of code serves the prompt.

```python

import os

import eosfactory.core.utils as utils
from eosfactory.eosf import *
```

```python
import pathlib
from termcolor import colored

import eosfactory.core.config as config

contract_dir = None

while True:
    map = config.config_map()
    eosio_contracts_dir = None
    EOSIO_CONTRACTS = "EOSIO_CONTRACTS"
    prompt_color = "green"
    error_path_color = "red"
    eosio_bios = "build/eosio.bios"

    def ok():
        is_ok = eosio_contracts_dir and os.path.exists(
                    os.path.join(eosio_contracts_dir, eosio_bios))
        if is_ok:
            global contract_dir
            contract_dir = os.path.join(eosio_contracts_dir, "build")
        return is_ok

    if EOSIO_CONTRACTS in map:
        eosio_contracts_dir = map[EOSIO_CONTRACTS]
        if ok():
            break

    eosio_contracts_dir = input(colored(utils.heredoc('''
        Where is 'eosio.contracts` repository located on your machine?
        Input an existing directory path:
        ''') + "\n", prompt_color))

    eosio_contracts_dir.replace("~", str(pathlib.Path.home()))

    if ok():
        map[EOSIO_CONTRACTS] = eosio_contracts_dir
        config.write_config_map(map)
        print()
        break

    print("\n" + utils.heredoc('''
    The path you entered:
    {}
    doesn't seem to be correct!
    directory --
    {} 
    -- does not exist.
    ''').format(
        colored(eosio_contracts_dir, error_path_color),
        colored(os.path.join(eosio_contracts_dir, eosio_bios), error_path_color)
        ) + "\n")
```
## Steps 1 - 2 Setup

Start nodeos, create a wallet.

```python
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
    os.path.join(contract_dir, contract),
    contract + ".abi",
    contract + ".wasm"    
    ).deploy()
```

## Step 5: Set the eosio.msig contract

`eosio.msig` contract enables and simplifies defining and managing permission levels and performing multi-signature actions.

```python
COMMENT('''Set the eosio.msig contract''')

contract = "eosio.msig"
Contract(
    contract, 
    os.path.join(contract_dir, contract),
    contract + ".abi",
    contract + ".wasm"
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

Therefore, with the `eosio.system` contract, all the simple tests in the EOSFactory distribution, using the simple signature of the `create_account` account factory function, will fail.


```python
COMMENT('''Set the eosio.system contract''')

contract = "eosio.system"
Contract(
    eosio, 
    os.path.join(contract_dir, contract),
    contract + ".abi",
    contract + ".wasm"
    ).deploy()
```

```python
stop()
```