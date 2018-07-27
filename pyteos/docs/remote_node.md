# Tests with a remote node

## Getting testnet account

Go to the *python* interpreter:
```bash
$ python3
```
```
>>> import setup
>>> import cleos
>>> import eosf

>>> setup.set_nodeos_address("88.99.97.30:38888")
```
The above setting will cause *EOSFactory* to use [*cryptolions*](http://dev.cryptolions.io/#home) testnet (http://54.38.137.99:8888).  


Create a wallet, if you do not any ...
```
>>> wallet_name = "tokenika"
>>> wallet = eosf.Wallet(wallet_name)
Creating wallet: tokenika
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ"

>>> tokenika_pass = "PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ"
```
... but if you have one, the `Wallet` object with a password that you have kept:
```
>>> wallet = eosf.Wallet(
                "tokenika", "PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ")
Restored wallet: tokenika
Password is
PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ
```

```
>>> ok =  wallet.open()
Opened: tokenika
>>> ok = wallet.unlock()
Unlocked: tokenika
```

Register an account on the [*cryptolions*](http://dev.cryptolions.io/#home) testnet:
```
>>> import setup
>>> import cleos
>>> import eosf
>>> setup.set_nodeos_address("88.99.97.30:38888")

>>> account_master = eosf.AccountMaster()
SAVE THE FOLLOWING DATA to use in the future to restore thisaccount object.
Accout Name: upe1ahhgb3xq
Owner Public Key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
Active Public Key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP

>>> print(account_master.owner_key)
Private key: 5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp
Public key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP

>>> print(account_master.active_key)
Private key: 5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp
Public key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
```

Use the above output data to feed the *Create Account* form. 

You can see the result:
```
>>> print(account_master.account())

name: upe1ahhgb3xq
permissions:
     owner     1:    1 EOS5Hf9xk8S15fqznskXVFFeZQW53VjZiFXSDpCMLmovtoPP8NzBK
        active     1:    1 EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
memory:
     quota:     513.1 KiB    used:     3.365 KiB

net bandwidth:
     staked:        100.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:                 0 bytes
     available:        19.19 MiB
     limit:            19.19 MiB

cpu bandwidth:
     staked:        100.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:                 0 us
     available:        3.841 sec
     limit:            3.841 sec

producers:     <not voted>

```
```
>>> ok = wallet.unlock()
>>> ok = wallet.import_key(account_master)
imported private key for: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
>>> ok = wallet.import_key("5JkcycNLgJHsawz5Sw4cFjjWEs5rSEAYaPR3GwwgPnYGC2rS213")
imported private key for: EOS5Hf9xk8S15fqznskXVFFeZQW53VjZiFXSDpCMLmovtoPP8NzBK
```

## Using remote testnet

Restore both the wallet and the master account:
```
import setup
import teos
import cleos
import eosf
import 

setup.set_nodeos_address("88.99.97.30:38888")

>>> wallet = eosf.Wallet(
                "tokenika"
                "PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ"
                )
Restored wallet: tokenika
Password is
"PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ"


>>> ok = wallet.open()
Opened: tokenika
>>> ok = wallet.unlock()
Unlocked: tokenika

>>> account_master = eosf.AccountMaster(
        "vkgljdlpxuip",
        "EOS5Hf9xk8S15fqznskXVFFeZQW53VjZiFXSDpCMLmovtoPP8NzBK",
        "EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP")

>>> print(account_master.account())


Create a new account:
```
>>> account_new = eosf.NewAccount(
      "upe1ahhgb3xq", 
      stake_net='100 EOS', stake_cpu='100 EOS', 
      buy_ram_kbytes=8, transfer=True
      )
ERROR:
Error 3080001: account using more than allotted RAM usage
```

