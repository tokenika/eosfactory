"""
# Account name conflict

## Cases

The structure of the `Cases` files is explained in the file `cases`.

Note, that all case files are, in the same time, both `Markdown` and `Python`
scripts. Therefore, you can execute it with `python3 <file name>` or you can
preview it, `RIGHT MOUSE -> Open Preview` if you use the `Visual Studio Code`.
 
## Set-up
```
"""
import setup
import eosf
import time
import eosf_account
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
_ = eosf.Logger()

eosf.restart()
eosf.set_is_testing_errors(False)
eosf.set_throw_error(True)
eosf.reset([eosf.Verbosity.TRACE]) 
wallet = Wallet()
account_master_create("account_master")
eosf.set_throw_error(False)
eosf.set_is_testing_errors()
"""
```
## Case

The `EOSFactory` wraps the EOSIO accounts with objects. The symbolic names
of this account objects, for example `account_alice` have to be unique in 
program. Moreover, they have be unique in a collection of scripts, especially
if they represent real accounts.

The `EOSFactory` uses a mapping files that enforce the uniqueness.

However, it is possible that a user wants to ascribe a previously used name
to another physical account. Then, the only way to keep the previous physical
account within the system is to change its mapping name.

See the `SCENARIO` text below.
```
"""
_.SCENARIO("""
Create two account objects: ``account_alice`` and ``account_carrol``.

Then try to create another account object called ``account_alice``. Although
this object is going to refer to a new blockchain account, it cannot accept
the given name: error is issued.

You are prompted to change the blocking name. On acceptance, the ``nano``
editor opens. CTR+X, to save and exit. 
Change ``account_alice`` to ``account_alice_b``.
""")
account_create("account_alice", account_master)
account_create("account_carrol", account_master)
account_create("account_alice", account_master)
"""
```
"""