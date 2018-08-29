# Wallet Object

This file can be executed as a python script:
```
cd docs/sphinx/source/cases
python3 03_wallet/case.py
```

## Set-up

The set-up statements are explained at [cases/00_setup](../cases/00_setup/case.html).

```
from eosfactory import *
```

## Case

The `Wallet` class wraps EOSIO wallets. The `Wallet` object keeps account objects, as desribed in [cases/00_account](../cases/00_account/case.html).

There has to be exactly one `Wallet` object in the namespace. After the `Wallet` singleton is created, it remains transparent to the script, yet usually, there is no need to access to it directly.

Although EOSFactory manages only one `Wallet` object at a time, it produces numerous wallet files in the wallet directory, i.e. in the location where the `keosd` wallet manager keeps wallets. The wallet files are marked with prefixes, which are either arbitrary (set by a particular test script)or encoding the URL of the testnet which was active during the creation time.

* Arbitrary prefixes mark wallets used for one-time tests; they are erased before repeating their tests.
* Testnode prefixes are consequently used in context of their nodes; they keep Factory state between sessions.
* Empty prefix (not implemented yet) marks wallets used with real EOSIO nodes.

For example, let us try with the local testnet:
```
reset()
create_wallet()
get_wallet().keys()

create_master_account("master")
create_account("alice", master)
create_account("carol", master)
get_wallet().keys()
get_wallet().lock_all()

stop()
```

![local_wallet](./img/local_wallet.png)

What has happened?

* The local node has restarted. Prior to the restart, the specifically marked wallet is deleted, together with other files hawing the same prefix: password file and account mapping file.
* The wallet object has been created.
* Its password has been stored to a file.
* An account object named `account_master` has been created and placed in the wallet.

If we close the session, then open it again, and recreate the wallet, we can expect that it opens without calling for password, having the same keys.

```
restart()
run()

create_wallet()
get_wallet().keys()

stop()
```

![local_wallet_reopen](./img/local_wallet_reopen.png)

### Methods of the `Wallet` class

We plan the Factory so that the singular wallet object is never referred to, in usual scripts. However, the `Wallet` class has several methods that are used internally. Some of them are obvious:

* Open wallet.
* Unlock wallet.
* Keys in all open wallets.
* etc.
