# Tests with a remote node

## Getting testnet account

Go to the *python* interpreter:
```bash
$ python3
```
```python
>>> import setup
>>> import cleos
>>> import eosf

>>> setup.set_cryptolions()
```
The above will cause *EOSFactory* to use [*cryptolions*](http://dev.cryptolions.io/#home) (http://54.38.137.99:8888) testnet.

Create a wallet, if you do not any ...
```
>>> wallet_name = "tokenika"
>>> wallet = eosf.Wallet(wallet_name)
Creating wallet: tokenika
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5K1kaARAqjMgQ4vd4NtoDvkqbuz4tcQuSfWRL3bXLbrDPb2a8j7"

>>> tokenika_pass = "PW5J3NBesBhoepcn6gCpXSfbYZs7jFt7kqH5D1csErDwN3L9qHFs4"
```
... but if you have one, the `Wallet` object with a password that you have kept:
```
>>> wallet = eosf.Wallet(
                "tokenika", "PW5K1kaARAqjMgQ4vd4NtoDvkqbuz4tcQuSfWRL3bXLbrDPb2a8j7")
Restored wallet: tokenika
Password is
PW5K1kaARAqjMgQ4vd4NtoDvkqbuz4tcQuSfWRL3bXLbrDPb2a8j7
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
>>> setup.set_cryptolions()

>>> account_master = cleos.ManualAccount()

>>> print(account_master)
SAVE THE FOLLOWING DATA to use in the future to restore this account object.
Accout Name: vkgljdlpxuip
Owner Public Key: EOS7m5MaQPX6xWjqTm8EW1PJ1mXL6pV6nhotGsjK9woNS2wE723BL
Active Public Key: EOS5wgQCZATqBwhiatufUs3NyWbDX2TzgBvGa4TpXdDLGnQNUV31k
```
Use the above output data to feed the *Create Account* form. 

You can see the result:
```
>>> ok = cleos.GetAccount(account_master)
permissions:
     owner     1:    1 EOS7m5MaQPX6xWjqTm8EW1PJ1mXL6pV6nhotGsjK9woNS2wE723BL
        active     1:    1 EOS5wgQCZATqBwhiatufUs3NyWbDX2TzgBvGa4TpXdDLGnQNUV31k
memory:
     quota:     527.5 KiB    used:     3.365 KiB

net bandwidth:
     staked:        100.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:                 0 bytes
     available:         19.2 MiB
     limit:             19.2 MiB

cpu bandwidth:
     staked:        100.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:                 0 us
     available:        3.842 sec
     limit:            3.842 sec

producers:     <not voted>
```
```
>>> ok = wallet.unlock()
>>> ok = wallet.import_key(account_master)
```

## Using remote testnet

Restore both the wallet and the master account:
```
import setup
import teos
import cleos
import eosf

setup.set_cryptolions()

>>> wallet = eosf.Wallet(
                "tokenika", "PW5K1kaARAqjMgQ4vd4NtoDvkqbuz4tcQuSfWRL3bXLbrDPb2a8j7")
Restored wallet: tokenika
Password is
PW5K1kaARAqjMgQ4vd4NtoDvkqbuz4tcQuSfWRL3bXLbrDPb2a8j7

>>> ok = wallet.open()
Opened: tokenika
>>> ok = wallet.unlock()
Unlocked: tokenika

>>> account_master = cleos.ManualAccount(
        "vkgljdlpxuip",
        "EOS7m5MaQPX6xWjqTm8EW1PJ1mXL6pV6nhotGsjK9woNS2wE723BL",
        "EOS5wgQCZATqBwhiatufUs3NyWbDX2TzgBvGa4TpXdDLGnQNUV31k")


Create a new account:
```
>>> account_new = eosf.Account(account_master)

```












## ????????????????????????????????????????????????????????????????????????










> ## First session

### Get contact with the *Tokenika* node and have a *wallet*

Go to the *python* interpreter:
```bash
$ python3
```

Now, see that the remote node responses ... 
```python
>>> import setup
>>> import cleos
>>> import eosf

>>> setup.set_cryptolions()
>>> info = cleos.GetInfo()
{
  "server_version": "c9b7a247",
  "chain_id": "038f4b0fc8ff18a4f0842a8f0564611f6e96e8535901dd45e43ac8691a1c4dca",
  "head_block_num": 1935676,
  "last_irreversible_block_num": 1935348,
  "last_irreversible_block_id": "001d87f4062a221e7d285aaa2d5f8f822cae06717ca93f54566dfd2983220566",
  "head_block_id": "001d893c938097b292bf30562d56911732db27df26d891d7b11c71e74c30ab23",
  "head_block_time": "2018-06-22T14:34:07.500",
  "head_block_producer": "galapaguin22",
  "virtual_block_cpu_limit": 200000000,
  "virtual_block_net_limit": 1048576000,
  "block_cpu_limit": 193198,
  "block_net_limit": 1047856
}
```

... if it does, if you need a *wallet*, create it:
```
>>> wallet_name = "tokenika"
>>> wallet = eosf.Wallet(wallet_name)
Creating wallet: tokenika
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5J3NBesBhoepcn6gCpXSfbYZs7jFt7kqH5D1csErDwN3L9qHFs4"

>>> tokenika_pass = "PW5J3NBesBhoepcn6gCpXSfbYZs7jFt7kqH5D1csErDwN3L9qHFs4"
```
However, if you have the wallet already, you have to build the `Wallet` object with a password that you have kept:
```
>>> wallet = eosf.Wallet(
  "tokenika", "PW5J3NBesBhoepcn6gCpXSfbYZs7jFt7kqH5D1csErDwN3L9qHFs4")

>>> ok =  wallet.open()
Opened: tokenika
>>> ok = wallet.unlock()
Unlocked: tokenika
```

Register an account on the [*cryptolions*](http://dev.cryptolions.io/#home) testnet:
```
>>> setup.set_cryptolions()
>>> account_master = eosf.ManualAccount()
Accout Name: vkgljdlpxuip
Owner Public Key: EOS7m5MaQPX6xWjqTm8EW1PJ1mXL6pV6nhotGsjK9woNS2wE723BL
Active Public Key: EOS5wgQCZATqBwhiatufUs3NyWbDX2TzgBvGa4TpXdDLGnQNUV31k
```
Use the above output data to feed the *Create Account* form. You can see the result:
```
>>> ok = cleos.GetAccount(account_master)
permissions:
     owner     1:    1 EOS7m5MaQPX6xWjqTm8EW1PJ1mXL6pV6nhotGsjK9woNS2wE723BL
        active     1:    1 EOS5wgQCZATqBwhiatufUs3NyWbDX2TzgBvGa4TpXdDLGnQNUV31k
memory:
     quota:     527.5 KiB    used:     3.365 KiB

net bandwidth:
     staked:        100.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:                 0 bytes
     available:         19.2 MiB
     limit:             19.2 MiB

cpu bandwidth:
     staked:        100.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:                 0 us
     available:        3.842 sec
     limit:            3.842 sec

producers:     <not voted>
```


Add the account to your wallet:
```
>>> ok = wallet.unlock()
ERROR:
Error 3120007: Already unlocked
Error Details:
Wallet is already unlocked: tokenika

>>> wallet.import_key(account_master)
'imported private key for: EOS8fKnPAWfmjBSsD2Fq37kzBWfwRFQUke8oGUSZ2tDkVH7ehv8D8\n'
```

### Try the `eosf.Account` class
```

>>> ok = wallet.unlock()
Unlocked: tokenika

>>> account_second = eosf.Account(account_master)
ERROR:
Error 3080001: account using more than allotted RAM usage

>>> wallet.keys()()
[
  "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
]
```

Cross-check with the plain EOSIO `cleos`

```bash
./cleos wallet unlock -n tokenika --password=PW5J3NBesBhoepcn6gCpXSfbYZs7jFt7kqH5D1csErDwN3L9qHFs4
Unlocked: tokenika

$ ./cleos --url http://54.38.137.99:8888 create account wdn2wmo3fkga account1test EOS7Xrkd6niuNBTDS1EzMRNEDisknTR7xoXgwSwE1LrvXfBViCXZF EOS4yPuQd7jTEqaCkn1DEqsU9DPG7jyh6JoCrAweqHGeS3st36mDx
Error 3080001: account using more than allotted RAM usage
```





