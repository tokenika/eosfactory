'''
# Wallet object

This file can be executed as a python script: 'python3 wallet.md'.

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

```md
'''
from  eosfactory import *
'''
```

## Case

The 'Wallet` class wraps EOSIO wallets. The 'Wallet' object keep account 
objects, presented at <a href="account.html">cases/account</a>.

It can be exactly one 'Wallet' object in the namespace. After the 'Wallet' 
singleton is created, it remains transparent to the script: usually, there 
is no need to refer to it.

Although the Factory manages only one 'Wallet` object at a time, it produces numerous wallet files in the wallet directory, that is where the KEOSD Wallet Manager keeps wallets. The wallet files are marked with prefixes -- either arbitrary, set by a particular test script -- or encoding the URL of the testnet active at the creation time. For example, let us try with the local testnet.
```md
'''
reset([Verbosity.INFO])
wallet = Wallet()
wallet.keys()
account_master_create("account_master")
wallet.keys()
import pdb; pdb.set_trace()
wallet.lock_all()

stop()

exit()
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
run([Verbosity.INFO])    # restart the local testnet
wallet = Wallet()
wallet.keys()   
stop()                         # stop the local testnet
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
kill_keosd()       # otherwise, the manager protects the wallet file

wallet_name = "jungle_wallet"
try:
    wallet_file = wallet_dir() + wallet_name + ".wallet"
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

