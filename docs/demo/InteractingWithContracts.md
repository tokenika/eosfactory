# Getting Started with Contracts 

The purpose of this tutorial is to demonstrate how *EOSFactory* and its Python syntax can be used to make interacting with EOS easy & intuitive.

## Prerequisites

This tutorial assumes that you have successfully installed *EOSIO* and *EOSFactory*.

## Run Python CLI

In *Visual Studio Code* start a Bash console and type `python3` to run the Python CLI. 
Next, import the predefined *EOSFactory* Python classes:

```
import pyteos
```

## Manage a Local Testnet

To start your own single-node local testnet:

```
$ pyteos.run()
```

Assuming everything worked properly, you should see a block generation message every 0.5 seconds.  

```
eosio generated block 046b9984... #101527 @ 2018-04-01T14:24:58.000 with 0 trxs
```

To stop and then continue running the testnet:

```
$ pyteos.stop()
$ pyteos.run()
```

And to stop and reset the testnet:

```
$ pyteos.reset()
```

To get information about the testnet:

```
$ pyteos.info()
```

## Initialize the Workspace

To initialize the workspace:

```
$ pyteos.init()
```

The initialization process does the following things:

* deploys the *Bios* contract
* creates a wallet and imports the default `eosio` account into it 
* creates several test accounts `alice`, `bob` &`carol` and imports their keys into the wallet

If you need additional test accounts, you can easily create them:

```
$ charlie = pyteos.Account("charlie", eosio)
```

**NOTE:** The first argument indicates the new account's name, whereas the second indicates the master account, in this case the default `eosio` account.

## Deploy the Contract

To deploy the pre-compiled `eosio.token` contract:

```
$ contract = pyteos.Contract("eosio.token")
```

## Create the EOS Token

To create a new token we call the `create` action with the proper arguments:

```
$ contract.push_action("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}', contract.owner)
```

**NOTE:** The `push_action` method takes three arguments: the action name, its arguments in JSON format, and the account whose permission is needed. In this case the permission is assigned to the account holding the contract.

## Issue Tokens

Now that we have created the token, the issuer can issue new tokens to `alice`:

```
$ contract.push_action("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', eosio)
```

**NOTE:** In this case the permission is assigned to the default `eosio` account.

If you want to see the actual transaction that was broadcast, you can use the `show_action` method:

```
$ contract.show_action("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', eosio)
```

## Transfer Tokens

Now that account `alice` has tokens, we will transfer some to account `carol`.  

```
$ contract.push_action("transfer", '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"}', alice)
```

**NOTE:** As the third argument we pass the reference to the account `alice` to indicate that she is the one who authorized this action.

## Check the Contract Table

From the contract's ABI we know that the table keeping track of the token balances is called `accounts`. Let's check the state of both accounts involved in the previous transaction:

```
$ contract.get_table("accounts", alice)
$ contract.get_table("accounts", carol)
```

**NOTE:** The `get_table` method takes two arguments: the name of the table as specified by the contract ABI and the scope within the contract in which the table is found.