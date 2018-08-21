'''
# Wallet object

This file can be executed as a python script: 'python3 wallet.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

```md
'''
import os
import setup
import eosf
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

logger.set_throw_error(False)
'''
```

## Case

The 'Wallet` class wraps EOSIO wallets. The 'Wallet' object keep account 
objects, presented at <a href="account.html">cases/account</a>.

It can be exactly one 'Wallet' object in the namespace. After the 'Wallet' 
singleton is created, it remains transparent to the script: usually, there 
is no need to refer to it.

If the 'Wallet' object is of the local testnet, its password is kept between 
sessions, and used automatically.

Let us consider two cases: 'NODEOS` and 'KEOSD' subsequently.

### NODEOS managed wallet

```md
'''
eosf.reset([logger.Verbosity.INFO])          # reset the local testnet
wallet = Wallet()
wallet.keys()
account_master_create("account_master")     # account object is put to wallet
wallet.keys()
wallet.lock_all()

eosf.stop()                                 # stop the local testnet
'''
```

<img src="wallet_images/reset_nodeos_wallet.png" 
    onerror="this.src='../../../source/cases/wallet_images/reset_nodeos_wallet.png'"   
    alt="nodeos wallet reset" width="720px"/>

What has happened?

* The local node has restarted, that is the local wallet file was deleted.
* The wallet object has been created.
* Its password has been stored to a file.
* An account object named 'account_master' has been created and placed in
    the wallet.

If we close the session, then open it again, and recreate the wallet, we can
expect that it opens without calling for password, having the same keys.

```md
'''
eosf_account.restart()                      # reset the Factory
eosf.run([logger.Verbosity.INFO])    # restart the local testnet
wallet = Wallet()
wallet.keys()   
eosf.stop()                         # stop the local testnet
'''
```

<img src="wallet_images/run_nodeos_wallet.png" 
    onerror="this.src='../../../source/cases/wallet_images/run_nodeos_wallet.png'"   
    alt="nodeos wallet reset" width="720px"/>

### KEOSD managed wallet

For the sake of this tutorial, we dare to treat a system wallet so rudely:
we delete it.

```md
'''
eosf.kill_keosd()       # otherwise, the manager protects the wallet file

wallet_name = "jungle_wallet"
try:
    wallet_file = eosf.wallet_dir() + wallet_name + ".wallet"
    os.remove(wallet_file)
    print("The deleted wallet file:\n{}\n".format(wallet_file))
except Exception as e:
    print("Cannot delete the wallet file:\n{}\n".format(str(e)))
'''
```

Create a 'KEOSD' wallet named 'wallet_name':

```md
'''
eosf_account.restart()                      # reset the Factory

wallet = Wallet(wallet_name)
'''
```

<img src="wallet_images/keosd_wallet_create.png" 
    onerror="this.src='../../../source/cases/wallet_images/keosd_wallet_create.png'"   
    alt="nodeos wallet reset" width="720px"/>

### Methods of the 'Wallet' class

We plan the Factory so that the singular wallet object is never referred to, in
usual scripts. However, the 'Wallet` class has several methods that are used
internally. Some of them are obvious:

* Open wallet.
* Unlock wallet.
* Keys in all open wallets.
* etc.

'''

