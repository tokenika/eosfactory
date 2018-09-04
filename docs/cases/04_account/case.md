# Account Class

This case demonstrates how the `Account` class works. We present how to create an account object, associate it with a contract and then execute some actions of this contract.

## Context

*EOSFactory* wraps *EOSIO* accounts using Python objects, i.e. instances of the `Account` class. The mapping between actual accounts and their *EOSFactory* representations is cached locally in a file. As a result, what we achieve is consistent testing environment across separate Python sessions.

## Use Case

#### Create a new account

Create a new Python session and import *EOSFactory* API:

```
$ python3
```

```
from eosf import *
```

Start a local testnet, create a wallet and then create a special master account referenced by a global variable called `master`:

```
reset()
create_wallet()   
create_master_account("master")
```

Next, use the `master` account to create another account referenced by a global variable called `host`:

```
create_account("host", master)
```

The first argument is the name of variable to be created, the second one points to the `master` account, which we created in the previous step.

You can verify that the variable exists and its methods can be invoked, for example:

```
host.info()
```

The `create_account` command performs several tasks:

* verifies that a `Wallet` object exist in the namespace,
* verifies that the proposed variable name is not already taken,
* registers a new account on the testnet - this account has its own name generated randomly,
* using the proposed name, creates a global variable referencing the actual account on the testnet,
* opens the wallet, unlocks it and stores the account's private keys into it,
* and finally, updates its internal statistics tracking all accounts created in a similar way.

All the above actions are logged to the terminal, which can be visible, provided the verbosity is set to its default value.

#### Methods of the Account class

An instance of the `Account` class has the following methods:

* `info()` - list the account's information,
* `push_action()` - push an action to the smart-contract,
* `show_action()` - display a `JSON` file of a transaction without sending it to the blockchain,
* `table()` - list the content of the local database associated with the smart-contract.

**NOTE:** the `master` account is an instance of a different class (i.e. the `AccountMaster` class) which does not implement the above methods. As a consequence, you cannot associate a smart-contract with an instance of the `AccountMaster` class.

#### Create a contract object

Create an instance of the `Contract` class and associate it with the `host` account:

```
contract = Contract(host, "01_hello_world")
```

The second argument of the creator of the `Contract` class identifies the location of the contract's source code (you can supply the entire path, but in case of standard locations, e.g. *EOSFactory* demo contracts or your predefined workspace, you can just specify the folder name).

Next, let's build and deploy the contract:

```
contract.build()
contract.deploy()
```

#### Execute the contract

If the deployment succeeds, the contract can be executed.

First, create two accounts - `alice` and `carol`:

```
create_account("alice", master)
create_account("carol", master)
```

And then you can push actions of the contract stored at the `host` account, using those two other accounts as arguments:

```
host.push_action("hi", {"user":alice}, alice)
host.push_action("hi", {"user":carol}, carol)
```

You can also try the `show_action` method:

```
host.show_action("hi", {"user":alice}, alice)
```

**NOTE:** As the `01_hello_world` does not define any tables, in this case the `table` method will not work.

Finally, stop the local testnet and exit Python CLI:

```
stop()
exit()
```

#### Test run

The examples presented in this document can be executed as a Python script:

```
python3 docs/sphinx/source/cases/04_account/case.py
```

You should get output similar to this:

![](./case.png)