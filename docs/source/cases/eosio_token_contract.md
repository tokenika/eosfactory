"""
# Eosio Token Contract

<pre>
This file can be executed as a python script: 'python3 eosio_token_contract.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre>

## Set-up

<pre>
"""
import unittest
import setup
import eosf
import time

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract
eosf.set_throw_error(True) # make the errors be thrown as exceptions

eosf.use_keosd(False)
eosf.reset([eosf.Verbosity.TRACE]) # start the local test node, reset
"""
</pre>

### The `Wallet` object

<pre>
Create the singleton wallet object. The object represents a physical wallet,
managed with either the KEOSD or NODEOS Wallet Manager:
</pre>
<pre>
"""
wallet = Wallet()
account_master_create("account_master")

eosf.set_throw_error(False) # make the errors be printed
"""
</pre>

## Case

<pre>
With the master account, create four accounts: 'account_alice', 
'account_bob', 'account_carrol' and 'account_test'. Add the 
'eosio.token' contract to the last account.
</pre>

### The `account_create` factory

<pre>
Note that the account-creation command places in the global namespace the
account object named with the first argument. The object represent a physical
account in the blockchain and in the wallet.
</pre>
<pre>
"""
account_create("account_alice", account_master)
account_create("account_bob", account_master)
account_create("account_carol", account_master)
account_create("account_test", account_master)
contract_test = Contract(account_test, "token")
deploy = contract_test.deploy()

time.sleep(1)
"""
</pre>
<pre>
Execute actions on the contract account:

* let eosio deposit an amount of 1000000000.0000 EOS there;
* transfer some EOS to the 'alice' account.

Use the 'push_action' method of the contract account:
</pre>
<pre>
"""
account_test.push_action(
    "create", 
    '{"issuer":"' 
        + str(account_master) 
        + '", "maximum_supply":"1000000000.0000 EOS", \
        "can_freeze":0, "can_recall":0, "can_whitelist":0}')

account_test.push_action(
    "issue",
    '{"to":"' + str(account_alice)
        + '", "quantity":"100.0000 EOS", '
        + '"memo":"issue 100.0000 EOS from eosio to alice"}',
    permission=account_master)
"""
</pre>
<pre>
Execute a series of transfers between the accounts. Use the 'push_action' 
method of the contract account:
</pre>

<pre>
"""
account_test.push_action(
    "transfer",
    '{"from":"' + str(account_alice)
        + '", "to":"' + str(account_carol)
        + '", "quantity":"25.0000 EOS", '
        + '"memo":"transfer 25.0000 EOS from alice to carol"}',
    permission=account_alice)

account_test.push_action(
    "transfer",
    '{"from":"' + str(account_carol)
        + '", "to":"' + str(account_bob)
        + '", "quantity":"11.0000 EOS", '
        + '"memo":"transfer 11.0000 EOS from carol to bob"}',
    permission=account_carol)

account_test.push_action(
    "transfer",
    '{"from":"' + str(account_carol)
        + '", "to":"' + str(account_bob)
        + '", "quantity":"2.0000 EOS", '
        + '"memo":"transfer 2.0000 EOS from carol to bob"}',
    permission=account_carol)

account_test.push_action(
    "transfer",
    '{"from":"' + str(account_bob)
        + '", "to":"' + str(account_alice)
        + '", "quantity":"2.0000 EOS", '
        + '"memo":"transfer 2.0000 EOS from bob to alice"}',
    permission=account_bob)

"""
</pre>
<pre>
To see the records of the accounts, use the 'table' method of the contract
account:
</pre>
<pre>
"""
table_alice = account_test.table("accounts", account_alice)
table_bob = account_test.table("accounts", account_bob)
table_carol = account_test.table("accounts", account_carol)
"""
</pre>

### Test run

<pre>
In an linux bash, change directory to where this file exists, it is the 
directory 'docs/source/cases' in the repository, and enter this command:
</pre>
<pre>
$ python3 eosio_token_contract.md
</pre>
<pre>
We hope that you get something similar to this one shown in the image below.
</pre>
<img src="eosio_token.png" 
    onerror="this.src='../../../source/cases/eosio_token.png'"   
    alt="eosio token contract" width="640px"/>

"""