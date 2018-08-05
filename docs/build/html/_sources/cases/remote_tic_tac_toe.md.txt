"""
# Tic-tac-toe contract on a remote testnet

<pre>
This file can be executed as a python script: 'python3 account_master.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre>

## Set-up

<pre>
"""
import os
import setup
import eosf
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

cryptolions = "88.99.97.30:38888"
_ = eosf.Logger()
"""
</pre>

<pre>
The following account exists in the blockchain of the testnode. It is used, in
this article, for testing. It is referred to as the 'testing account'.
</pre>

<pre>
Account Name: dgxo1uyhoytn
Owner Public Key: EOS8AipFftYjovw8xpuqCxsjid57XqNstDyeTVmLtfFYNmFrgY959
Active Public Key: EOS6HDfGKbR79Gcs74LcQfvL6x8eVhZNXMGZ48Ti7u84nDnyq87rv

Owner Private Key: 5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY
Active Private Key: 5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA 
</pre>

<pre>
For the sake of this tutorial, to make it reproducible without the need of 
keeping the password of the system wallet, we delete the test wallet 
(if exists) and recreate it.
</pre>

<pre>
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
</pre>

<pre>
"""
eosf_account.restart()    # reset the Factory
eosf.use_keosd(True)
setup.set_nodeos_address(cryptolions)

wallet = Wallet(wallet_name)
account_master_create(
    "account_master",
    "dgxo1uyhoytn",
    "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY",
    "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA"
    )
account_master.info()

"""
"""