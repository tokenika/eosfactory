"""
## Logos And Teos

### Logos

### Teos

#### Daemon class
```
"""
import teos
import pprint

teos.set_verbose(True)

daemon = teos.Daemon()
daemon.clear()
#       nodeos exe file: /mnt/e/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#    genesis state file: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/genesis.json
#        server address: 127.0.0.1:8888
#      config directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir
#      wallet directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/wallet
#     head block number: 1
#       head block time: 2018-04-11T17:12:26

print(daemon)
#            head block: 162
#       head block time: 2018-04-11T17:13:47
#  last irreversible block: 161

daemon.stop()
#  Daemon is stopped.

daemon.start()
#       nodeos exe file: /mnt/e/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#    genesis state file: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/genesis.json
#        server address: 127.0.0.1:8888
#      config directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir
#      wallet directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/wallet
#     head block number: 280
#       head block time: 2018-04-11T17:14:46

"""
```

#### Wallet class
```
"""
wallet1 = teos.Wallet("1")
#              password: PW5HxHqShzDF1q7gUdeL39NJz6c8bRZWQ6FkM8pHFdrMWWaNv4YcP
#  You need to save this password to be able to lock/unlock the wallet!

wallet2 = teos.Wallet("2")
#              password: PW5J1SbKyVvpkWCyHaLrTdhMmc1B3tDqbaJ7HugUvkepgFYry8eqD
#  You need to save this password to be able to lock/unlock the wallet!

wallet1.list()                   ## Lists all wallets, starlet marks unlocked:
#                wallet: 1 *
#                wallet: 2 *

wallet1.lock()
wallet1.list()
#                wallet: 1
#                wallet: 2 *

wallet1.unlock()
wallet1.list()
#                wallet: 1 *
#                wallet: 2 *

wallet1.import_key(key)          ## See in CreateKey section.
pprint.pprint(repr(wallet1))     ## See in CreateKey section.

print(wallet1)
#              password: PW5J9tbUbJTpdKBzCoyDmBb2BMin3wQ86kM7R3DN6i7kEhQfgG9zy
#  You need to save this password to be able to lock/unlock the wallet!

"""
```
#### CreateKey class
```
"""
key_first = teos.CreateKey("first")
#              key name: first
#           private key: 5KSnHTTdcdeE1bJWeRRguN9NG8fdv2ASphtHQWRb5kU9fXg3utL
#            public key: EOS7EHHBJfeSv7szqZg42S7AA7Ype8nMjXqxK9eQS3pALr8ydjce1

key_second = teos.CreateKey("second")
#              key name: second
#           private key: 5KUg1E7bKucgBNJrfHywvH6YF2LtkaXdo6yKz6qA4nRAfy66Sov
#            public key: EOS5CxqGXaMuSSrZMiQ8xVewmmDT1hA3s8TSH7NLktLdni7HkiR5d

wallet1.import_key(key_first)
wallet1.import_key(key_second)

print(wallet1)
{'keys': [['first', '5J5xP2sWs9ZfLB49aW4jxAitEahWGJDcWVbjazQg9Xp7dhA8KZr'],
          ['second', '5HzbJ9MCyB4AGdti6AtpydwkkTFjHZ6SfyLv35ZENkQ7LMRegTP']],
 'name': '1',
 'password': 'PW5K7Vririm7iSpnf3TGUWPYixoJKEJr2cZMMxtcqNGcuVi3dYpGg'}
"""
```
#### Account class
A special 'SetContract' object has to be defined before any action on an 
account. See [Contract class] section.

```
"""
account_eosio = teos.EosioAccount()
contract_eosio_bios = teos.Contract(account_eosio, "eosio.bios")
"""
```

```
"""
account_alice = teos.Account("eosio", "alice", key_first, key_second)
#        transaction id: 99f00b5eaa48bbe697aa54451eb0ea263d057aa9feba44f332021ad4c8e99d0c
"""
```
"""

