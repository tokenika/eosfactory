# Getting Started with Contracts

The purpose of this tutorial is to demonstrate how EOSFactory and its Python syntax can be used to make interacting with EOS easier & more intuitive.

## Prerequisites

This tutorial assumes that you have installed EOSIO and EOSFactory.

##  Running Python

In Visual Studio Code start a Bash console and type `python3` to run a Python CLI. 
Next, import the predefined EOSFactory Python classes:

```
import pyteos
```

And initialize y 

```
pyteos.set_verbose(true)
```

## Managing a Local Testnet

You can start your own single-node local testnet using this command:

```
$ pyteos.run()
```

Assuming everything worked properly, you should see a block generation message every 0.5 seconds.  

```
eosio generated block 046b9984... #101527 @ 2018-04-01T14:24:58.000 with 0 trxs
```

To stop and then continue running the testnet use these commands:

```
$ pyteos.stop()
$ pyteos.run()
```

And to stop and reset use this:

```
$ pyteos.reset()
```

To get information about the testnet:

```
$ pyteos.Info()
```

**NOTE:** To be consistent with Python conventions, we use lower case for invoking an object's methods and upper case when calling a constructor of class. Here is a list of classes defined in `pyteos`: `Info`, `Wallet`, `Key`, `Account`,  `AccountEosio`, `Contract`.

## Creating a Wallet

To create a wallet and set a reference to it named `wallet` run this command:

```
$ wallet = pyteos.Wallet()
```

To lock and unlock it use these commands:

```
$ wallet.lock()
$ wallet.unlock()
```

You will need your wallet unlocked for the rest of this tutorial.

## The EOSIO account

To interact with the blockchain you will need to create a reference to the initial account called `eosio` and import its private key into your wallet:

```
$ eosio = pyteos.AccountEosio()
$ wallet.import(eosio)
```

To make sure `eosio` keys have been successfully imported, run this command:

```
wallet.keys()
```

## Loading the Bios Contract

Now that we have a wallet with the key for the `eosio` account loaded, we can set a default system contract:

```
$ eosio.set_contract("eosio.bios")
```

## Creating Accounts

We will create two accounts, `account1` and `account2`, and we will need to associate a key with each account.  In this example, the same key will be used for both accounts.

To do this we first generate keys for the accounts:

```
$ key1 = pyteos.Key("key1")
$ key2 = pyteos.Key("key2")
```

Then we import this key into our wallet:

```
$ wallet.import(key1)
$ wallet.import(key2)
```

## Create Two User Accounts

Next we will create two accounts, `account1` and `account2`, using the key we created and imported above.

```
$ account1 = pyteos.Account(eosio, "account1", key1, key1)
$ account2 = pyteos.Account(eosio, "account2", key2, key2)
```

**NOTE:** In this tutorial example we use the same key for *owner key* and *active key*.

We can query all accounts that are controlled by our key:

```
$ key1.accounts()
$ key2.accounts()
```

## Deploy the Contract

Before we can deploy the token contract we must create an account to deploy it to:

```
$ key = pyteos.Key("key")
$ account = pyteos.Account(eosio, "eosio.token", key, key)
```

Then we can deploy the contract to this account:

```
$ contract = pyteos.Contract(account, "eosio.token")
```

## Create the EOS Token

To create a new token we call the `create` action with the proper arguments:

```
$ contract.push_action("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}', account)
```

**NOTE:** The `push_action` method takes three arguments: the action name, its arguments in JSON format, and the account whose permission is needed.

## Issue Tokens

Now that we have created the token, the issuer can issue new tokens to the account `account1` we created earlier.

```
$ contract.push_action("issue", '{"to":"account1", "quantity":"100.0000 EOS", "memo":"memo"}', eosio)
```

If you want to see the actual transaction that was broadcast, you can use the `show_action` method.

```
$ contract.show_action("issue", '{"to":"account1", "quantity":"100.0000 EOS", "memo":"memo"}', eosio)
```

## Transfer Tokens

Now that account `account1` has tokens, we will transfer some to account `account2`.  We indicate that `account1` authorized this action using the permission argument `permission=account1`.

```
$ contract.push_action("transfer", '{"from":"account1", "to":"account2", "quantity":"25.0000 EOS", "memo":"memo"}', account1)
```

## Check the Contract Table

Let's check the state of both accounts involved in the previous transaction:

```
$ contract.get_table("accounts", account1);
$ contract.get_table("accounts", account2);
```

**NOTE:** The `get_table` method takes two arguments: the name of the table as specified by the contract ABI and the scope within the contract in which the table is found.