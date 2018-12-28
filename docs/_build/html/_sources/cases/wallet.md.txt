# Wallet Class


This document demonstrates how the `Wallet` class works. We present how account objects can be preserved across separate Python sessions. Also, we discuss the `Wallet` class methods.

## Context

The `Wallet` class wraps an *EOSIO* wallet. An instance of the class, i.e. a `Wallet` object keeps track of `Account` objects.

The `Wallet` class is a singleton, so there needs to be exactly one `Wallet` object in the namespace. After the `Wallet` is created with the `create_wallet()` command, it remains transparent to the script, yet usually there is no need to access it directly.

Although *EOSFactory* manages only one `Wallet` object at a time, it produces numerous wallet files in `~/eosio-wallet`, i.e. in the location where the `keosd` wallet manager stores its wallets.

The wallet files are marked with prefixes which are encoding the URL of the active testnet (i.e. the one which is active when the `create_wallet()` command is executed), for example: `_127_0_0_1_8888_default.wallet` or `_88_99_97_30_38888_default.wallet`.


## Use Case

The python blocks in the current Markdown document can be executed with a provided bash tool. While the working directory is the root of the `EOSFactory` installation, do:

```bash
eosfactory/utils/pythonmd.sh docs/cases/wallet.md
```

#### Create a new wallet

Create a new Python session and import *EOSFactory* API:

```bash
python3
```

```python
from eosfactory.eosf import *
```

First, lets's start a local testnet:

```python
reset()
```

Next, create a wallet, then create a couple of accounts and finally let the `Wallet` object list the private keys associated with those accounts:

```python
create_wallet()
create_master_account("master")
create_account("alice", master)
create_account("carol", master)
get_wallet().keys()
```

Here is the expected outcome:

![create wallet and put two accounts](../images/create_wallet_put_two_accounts.png)

What has happened?

* The wallet object is created, with its password is stored locally in a file.
* An account object named `master` is created and its keys are stored in the wallet.
* Similarly, account objects named `alice` and `carol` are created and their keys are stored in the wallet.

Finally, stop the local testnet and exit Python CLI:

```python
stop()
```

Note that the command `create_wallet()` is not necessary: it is issued internally with the first call to the `create_master_account` and `create_account` account factory functions.

#### Resume the testnet

Create a new Python session and import *EOSFactory* API:

```bash
python3
```

```python
from eosfactory.eosf import *
```

Resume the testnet:

```python
resume()
```

When you run the `create_wallet()` command, *EOSFactory* will recreate the existing wallet, including the private keys we created in the previous session:

```python
create_wallet()
get_wallet().keys()
```

Here is the expected outcome:

![resume wallet](../images/resume_wallet.png)

Finally, stop the local testnet and exit Python CLI:

```python
stop()
```

#### Reset the testnet

Create a new Python session and import *EOSFactory* API:

```bash
python3
```

```python
from eosfactory.eosf import *
```

And this time we reset the testnet:

```python
reset()
```

When you run the `create_wallet()` command, *EOSFactory* will lose track of the private keys, as the wallet is created from scratch. This is because the local testnet was reset, not resumed.

```python
create_wallet()
get_wallet().keys()
```
You should get output similar to this:

![reset wallet](../images/reset_wallet.png)

Finally, stop the local testnet and exit Python CLI:

```python
stop()
```

#### Methods of the Wallet class

As we mentioned before, when working with unit tests you should never need to access the `Wallet` object directedly. 

However, if you do, below there is a list of methods available in the `Wallet` class.

Create a new Python session and import *EOSFactory* API:

```bash
python3
```

```python
from eosfactory.eosf import *
```

Then reset the local testnode and create an account. The singleton `Wallet` object is created automatically:

```python
reset()
create_master_account("master")
create_account("alice", master)
```

And execute the following methods of the `Wallet` class:

```python
get_wallet().index()
get_wallet().open()
get_wallet().unlock()
get_wallet().keys()
get_wallet().lock()
```

You should get output similar to this:

![wallet methods](../images/wallet_methods.png)

Finally, exit Python CLI:

```python
exit()
```

## Test Run

The python blocks in the current Markdown document can be executed with a provided bash tool. While the working directory is the root of the `EOSFactory` installation, do:

```bash
eosfactory/utils/pythonmd.sh docs/cases/wallet.md
```
