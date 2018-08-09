"""
# Registering to a remote testnet

<pre>
This file can be executed as a python script: 'python3 
registering_to_testnode.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre>

## Set-up

```md
The following account exists in the blockchain of the testnode. It is used, in
this article, for testing. It is referred to as the 'testing account'.
```

```md
Owner Public Key: EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959
Active Public Key: EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv

Owner Private Key: OWNER_KEY
Active Private Key: ACTIVE_KEY 
```

```md
"""
import os
import unittest
import setup
import eosf
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_master_create
from user_data import *

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, \
    eosf.Verbosity.DEBUG])

remote_testnet = "88.99.97.30:38888"
_ = eosf.Logger()

"""
```

### Set a remote testnode

```md
"""
eosf.use_keosd(True)        # use KEOSD Wallet Manager
setup.set_nodeos_address(remote_testnet)
"""
```

```md
Throw an exception if the testnode is off:
```

```md
"""
eosf.set_throw_error(True)
eosf.info()
eosf.set_throw_error(False)
"""
```

### Clean the 'jungle wallet'

```md
For the sake of this tutorial, we dare to treat a system wallet so rudely:
we delete it.
```

```md
"""
eosf.use_keosd(True)    # to determine the directory of the wallet
eosf.kill_keosd()       # otherwise, the manager protects the wallet file

wallet_name = "jungle_wallet"
try:
    wallet_file = eosf.wallet_dir() + wallet_name + ".wallet"
    os.remove(wallet_file)
    print("The deleted wallet file:\n{}\n".format(wallet_file))
except Exception as e:
    print("Cannot delete the wallet file:\n{}\n".format(str(e)))
"""
```

```md
"""
wallet = Wallet(wallet_name)

eosf.set_is_testing_errors(False)
eosf.set_throw_error(True)

"""
```

### Introduce a test trick

```md
We use an active account, named 'account_master_test' to simulate the 
registration procedure: if set, this account substitutes one that would be
physically registered.

In the following definitions, we use real data obtained with a real registration
session executed with the procedure that is shown in this article.

The constants 'ACCOUNT_NAME', 'OWNER_KEY', 'ACTIVE_KEY' are defined in the 
script 'user_data.py`. We hope, that you will replace them with your own 
data, as they are used in other articles.
```

```md
"""
eosf_account.account_master_test = eosf_account.GetAccount(
    "account_master_test",
    ACCOUNT_NAME, 
    OWNER_KEY,
    ACTIVE_KEY
)
eosf_account.account_master_test.ERROR()
"""
```

### End the set-up part

```md
"""
eosf.set_throw_error(False)         # on error, do not throw exception
eosf.set_is_testing_errors()        # make error messages less alarming
"""
```

## Case

```md
In subsequent tests, you may have to change the account object name, here 
'account_master', or to resolve name conflicts, if you are prompted.
```

### Register to the testnode

```md
"""
account_master_create("account_master")
"""
```

### Test run

```md
In an linux bash, change directory to where this file exists, it is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:
```
```md
$ python3 registering_to_testnode.md
```
```md
We hope that you get something similar to this one shown in the image below.
```
<img src="registering.png" 
    onerror="this.src='../../../source/cases/registering.png'"   
    alt="registering" width="640px"/>
    
"""