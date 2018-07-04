# python3 ./tests/test1.py

import setup
import teos
import cleos
import eosf
import unittest
from termcolor import colored, cprint
import time

setup.set_json(False)        
setup.set_verbose(True)
setup.use_keosd(False)

cprint("""
Testing `eosf.account()`.

`eosf.account()` is a factory: depending on parameters, it returns the same 
object, representing an EOSIO account functionality, yet build in many ways:

    -- with the `cleos create account` command;
    -- with the `cleos system newaccount` command;
    -- it can be one restored from the blockchain.
""", 'magenta')


def test():
    global account_alice
    global account_carol
    global account_master
    global account_bill
    global account_test

    cprint("""
Start session: reset the local EOSIO node, create a wallet object, put the
master account into it.
    """, 'magenta')

    account_master = eosf.AccountMaster()
    reset = eosf.reset()
    wallet = eosf.Wallet()
    wallet.import_key(account_master)

    cprint("""
Create an account object, named `account_alice`, with the `eosf.account()`, 
with default parameters: 

    -- using the `account_master` as the creator;
    -- using a random 12 character long name;
    -- using internally created `owner` and `active` keys.
    """, 'magenta')

    account_alice = eosf.account()
    wallet.import_key(account_alice)

    account_carol = eosf.account()
    wallet.import_key(account_carol)

    cprint("""
The following `account_bill` object represents the account of the name `bill`
    """, 'magenta')

    account_bill = eosf.account(name="bill")
    wallet.import_key(account_bill)

    account_test = eosf.account()
    wallet.import_key(account_test)

    cprint("""
The last account `account_test` is going to take a contract. Now, it does not have
any:
    """, 'magenta')

    account_test.code()

    cprint("""
Define a contract, with its code specified in the EOS repository 
(build/contracts/eosio.token), and deploy it:
    """, 'magenta')

    contract_test = eosf.Contract(account_test, "eosio.token")
    deploy = contract_test.deploy()
    account_test.code()

    time.sleep(1)

    action = account_test.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_master) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    action = contract_test.push_action(
        "issue", 
        '{"to":"' + str(account_alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            account_master)
    
    cprint("""
Experiments with the `eosio.token` contract are shown elsewere. 
Here, we show how the session accounts recover after restarting 
the session.
    """, 'magenta')

    account_alice = None
    account_bill = None
    account_carol = None
    account_test = None
    contract_test = None
    wallet = None

    wallet = eosf.Wallet()

    cprint("""
The old wallet is restored. It is possible, because there is a password map 
in the wallet directory. 

Note that this provision is available only if the `keosd` Wallet Manager is not 
used and wallets are managed by the local node - this condition is set with the
`setup.use_keosd(False)` statement above.
    """, 'magenta')

    wallet.restore_accounts(globals())
    print(account_alice.info())

    cprint("""
Continue operations on the restored account objects:
    """, 'magenta')

    action = account_test.push_action(
        "transfer", 
        '{"from":"' 
            + str(account_alice)
            + '", "to":"' + str(account_carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        account_alice)

    cprint("""
Note that the accounts have to be declared global, in order to be 
restorable with the current means.
    """, 'magenta')


if __name__ == "__main__":
    test()