"""
# Tic-tac-toe contract on a remote testnet

<pre>
This file can be executed as a python script: 'python3 account_master.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre>

## Set-up

```md
"""
import os
import setup
import eosf
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

cryptolions = "88.99.97.30:38888"

"""
```

```md
Throw an exception if the testnode is off:
```

```md
"""
eosf.use_keosd(True)
setup.set_nodeos_address(cryptolions)
eosf.set_throw_error(True)
eosf.info()
eosf.set_throw_error(False)
"""
```

```md
The following account exists in the blockchain of the testnode. It is used, in
this article, for testing. It is referred to as the 'testing account'.
```

```md
Account Name: dgxo1uyhoytn
Owner Public Key: EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959
Active Public Key: EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv

Owner Private Key: 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY
Active Private Key: 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA 
```

```md
For the sake of this tutorial, to make it reproducible without the need of 
keeping the password of the system wallet, we delete the test wallet 
(if exists) and recreate it.
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
eosf_account.restart()    # reset the Factory
eosf.use_keosd(True)
setup.set_nodeos_address(cryptolions)

ACCOUNT_MASTER = "account_master"
ACCOUNT_TTT = ACCOUNT_MASTER

wallet = Wallet(wallet_name)
account_master_create(
    ACCOUNT_MASTER,
    "dgxo1uyhoytn",
    "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
    "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
    )
account_master.info()
"""
```

```md
"""
contract_tic_tac_toe = Contract(account_master, "tic_tac_toe_jungle")
contract_tic_tac_toe.build_abi()
contract_tic_tac_toe.deploy()
"""
```

```md
"""
import unittest
import setup
import eosf

from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

eosf.set_verbosity([eosf.Verbosity.EOSF, eosf.Verbosity.OUT, \
    eosf.Verbosity.DEBUG])
eosf.set_throw_error(False)

class Test1(unittest.TestCase):
    def test_tic_tac_toe(self):
        
        account_master = globals()[ACCOUNT_MASTER]
        account_tic_tac_toe = globals()[ACCOUNT_TTT]

        account_create("account_alice", account_master)
        account_create("account_carol", account_master)

        eosf.set_throw_error(False)
        eosf.set_is_testing_errors()

        ######################################################################  

        account_tic_tac_toe.push_action(
            "create", 
            '{"challenger":"' + str(account_alice) 
                +'", "host":"' + str(account_carol) + '"}',
            account_carol)

        t = account_tic_tac_toe.table("games", account_carol)
        self.assertFalse(t.error)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)

        account_tic_tac_toe.push_action(
            "move", 
            '{"challenger":"' + str(account_alice) 
                + '", "host":"' + str(account_carol) 
                + '", "by":"' + str(account_carol) 
                + '", "row":0, "column":0 }', 
            account_carol)

        account_tic_tac_toe.push_action(
            "move", 
            '{"challenger":"' + str(account_alice) 
                + '", "host":"' + str(account_carol) 
                + '", "by":"' + str(account_alice) 
                + '", "row":1, "column":1 }', 
            account_alice)

        t = account_tic_tac_toe.table("games", account_carol)

        self.assertEqual(t.json["rows"][0]["board"][0], 1)

        account_tic_tac_toe.push_action(
                "restart", 
                '{"challenger":"' + str(account_alice) 
                    + '", "host":"' + str(account_carol) 
                    + '", "by":"' + str(account_carol) + '"}', 
                account_carol)

        t = account_tic_tac_toe.table("games", account_carol)
        self.assertFalse(t.error)

        self.assertEqual(t.json["rows"][0]["board"][0], 0)

        account_tic_tac_toe.push_action(
                "close", 
                '{"challenger":"' + str(account_alice) 
                    + '", "host":"' + str(account_carol) + '"}', 
                account_carol)
"""
```

```
"""
unittest.main()
"""
```
"""

