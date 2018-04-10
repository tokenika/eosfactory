
"""
## Example "Currency" Contract Walkthrough

EOS comes with example contracts that can be uploaded and run for testing 
purposes. We will validate our single node setup using the sample contract 
'currency'.

### Start EOS node
"""
```
import teos
teos.set_verbose(False)

daemon = teos.Daemon()
daemon.clear()
#       nodeos exe file: /mnt/e/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#    genesis state file: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/genesis.json
#        server address: 127.0.0.1:8888
#      config directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir
#      wallet directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/wallet
#     head block number: 2
#       head block time: 2018-04-10T17:20:54

# See a prove that the daemon is started:
print(daemon)
#            head block: 1047
#       head block time: 2018-04-10T16:57:27
#  last irreversible block: 1046
```
"""

Bay the way, with the object 'daemon', the following methods work:

"""
```                 
daemon.info() # An alias for print(daemon)
#            head block: 1047
#       head block time: 2018-04-10T16:57:27
#  last irreversible block: 1046

daemon.delete_wallets()
#  deleted wallet count: 1

daemon.stop()
#  Daemon is stopped.

daemon.start()
#       nodeos exe file: /mnt/e/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#    genesis state file: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/genesis.json
#        server address: 127.0.0.1:8888
#      config directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir
#      wallet directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/wallet
#     head block number: 1046
#       head block time: 2018-04-10T16:57:27
```
"""

### Create a wallet

Every contract requires an associated account, so first you need to create 
a wallet. To create a wallet, you need to have the wallet_api_plugin loaded 
into the nodeos process:
"""
wallet = teos.Wallet()
"""
The wallet name argument is not set: the default wallet name is 'default'.

With the object wallet, the following methods apply:
```
"""
key_one = teos.CreateKey("key one")
key_two = teos.CreateKey("key two")
wallet.import_key(key_one)
wallet.import_key(key_two)
print(wallet)
{'keys': [['key one', '5Kcf8D12wCVQLK8PLL5Bi6nCLjVzjtfrpQpuvLgjWuPL4s13GfK'],
          ['key two', '5J1iEfuvs8biBu7r6gQMvTr21MboXmymZypZd1sxe8vf5MxwHeq']],
'name': 'default',
'password': 'PW5KJrnNjw5gDwM4npTo9qscqxTCokqqfXVuyWkAZEeqiWnYVwwum'}

wallet.list()
#                wallet: default *

wallet.lock()
wallet.list()
#                wallet: default
wallet.unlock()
wallet.list()
#                wallet: default *
"""
```
### Load the Bios Contract

Set eosio.bios as the default system contract. This contract enables you to 
have direct control over the resource allocation of other accounts and to 
access other privileged API calls.
"""
eosio_bios_contract = teos.SetContract("eosio", "eosio.bios", permission="eosio")
#        transaction id: 7d5d9c7f56d46d6eab95f2dea6aaab667b5eb3d087737ada0cba5b82f26962c3
"""

### Create an account for the "currency" contract

The account named "currency" will be used for the "currency" contract. 
Generate two public/private key pairs that will be later assigned as the 
owner_key and the active_key:
"""
owner_key = teos.CreateKey("owner_key")
#              key name: owner_key
#           private key: 5J4bSiNprJzPYVHqoZdSDGTTd454LiDc89AVvKT4Miv2SyzZTDF
#            public key: EOS7vDtGf9cVxEChKN7YeDgqMGrgFgvcCdN5qAUEhMMufAnPHddTb
active_key = teos.CreateKey("active_key")
#              key name: active_key
#           private key: 5KRHeQ1S7pEtCw6TMeW6WKvupuR8cVGJjpNbAN5uviXTAtvhmDW
#            public key: EOS6FfNuYYKoSa7pjhoqqeymi6iwe6j9ukVHiQxPbMeAcHmcoxRwj
"""

Import the two private keys into the wallet:
"""
wallet.import_key(owner_key)
wallet.import_key(active_key)
"""

You can see the contents of the wallet:  
"""
print(wallet)
{'keys': [['owner_key', '5J4bSiNprJzPYVHqoZdSDGTTd454LiDc89AVvKT4Miv2SyzZTDF'],
          ['active_key',
           '5KRHeQ1S7pEtCw6TMeW6WKvupuR8cVGJjpNbAN5uviXTAtvhmDW']],
 'name': 'default',
 'password': 'PW5Kih88UxyFeVeYfWiuhbBRVhxmzr4nVvyTjsuNLgP6Ropxb9SJY'}
"""

Create the currency account using the cleos create account command. The 
create will be authorized by the eosio account. The two public keys generated 
above will be associated with the account, one as its OwnerKey and the other 
as its ActiveKey.
"""
account = teos.Account("eosio", "currency", owner_key, active_key)
#        transaction id: 0c4e0fb1163562909a83947b77aa3ee293b880cd61d4c6610fdcd3198e2d0eb7
"""

You can verify that the account was successfully created:
"""
print(account)
{'account_name': 'currency',
 'permissions': [{'parent': 'owner',
                  'perm_name': 'active',
                  'required_auth': {'accounts': '',
                                    'keys': [{'key': 'EOS88rqdDApfzRMcSCTuy3HmS2gBZSW8ZokjC8cQ4aeFL7zEQqmdx',
                                              'weight': '1'}],
                                    'threshold': '1'}},
                 {'parent': '',
                  'perm_name': 'owner',
                  'required_auth': {'accounts': '',
                                    'keys': [{'key': 'EOS5WULc9uFcaME5xJbHdrrbi5xr3AhCNCogaeMGoxRkPp8PATmtc',
                                              'weight': '1'}],
                                    'threshold': '1'}}]}
"""

### Upload the sample "currency" contract to the blockchain

Before uploading a contract, verify that there is no current contract:
"""
code = account.code()
print(code)
"""

Upload the sample currency contract using the currency account:
"""
account.set_contract("currency")
"""

You can also verify that the code has been set:
"""
account.code()
"""

Before using the currency contract, you must first create, then issue the 
currency:
"""
teos.PushAction(
  "currency", "create", 
  '{"issuer":"currency","maximum_supply":"1000000.0000 CUR", \
    "can_freeze":"0","can_recall":"0","can_whitelist":"0"}',
  permission="currency@active")

teos.PushAction(
  "currency", "issue", 
  '{"to":"currency","quantity":"1000.0000 CUR","memo":""}',
  permission="currency@active")
"""











"""
daemon = teos.Daemon()
daemon.clear()
print(daemon)
wallet = teos.Wallet()
eosio_bios_contract = teos.SetContract("eosio", "eosio.bios", permission="eosio")

owner_key = teos.CreateKey("owner_key")
active_key = teos.CreateKey("active_key")
wallet.import_key(owner_key)
wallet.import_key(active_key)

account = teos.Account("eosio", "currency", owner_key, active_key)

code = account.code()
print(code)

"""

For the purpose of this walkthrough, import the private key of the 'eosio' 
account, a test account included within genesis.json, so that you're able to 
issue API commands under authority of an existing account. The private key 
referenced below is found within your config.ini and is provided to you for 
testing purposes.
"""
eosio_key = teos.EosioKey()
wallet.import_key(eosio_key)
"""

#### Creating accounts for sample "currency" contract

First, generate some public/private key pairs that will be later assigned as 
owner_key and active_key.
"""
owner_key = teos.CreateKey("owner_key")
active_key = teos.CreateKey("active_key")

"""
Run the create command where 'eosio' is the account authorizing the creation of 
the currency account and PUBLIC_KEY_1 and PUBLIC_KEY_2 are the values 
generated by the create key command
"""
account = teos.Account(
    eosio_key.account_name, "currency", owner_key, active_key
    )

"""
You should then get a JSON response back with a transaction ID confirming it 
was executed successfully.

Go ahead and check that the account was successfully created:
"""
print(account)

"""
Import the active private key generated previously in the wallet:
"""
wallet.import_key(active_key)
print(wallet)

"""
You will upload sample "currency" contract to blockchain. Before uploading a 
contract, verify that there is no current contract:
"""
code = wallet.code()
print(code)

"""
Code hash is null, there is no contract.

With an account for a contract created, upload a sample contract:
"""
account.set_contract("currency.wast", "currency.abi")

"""
As a response you should get a JSON with a transaction_id field. Your contract 
was successfully uploaded!

You can also verify that the code has been set with the following command:
"""
code = account.code()
print(code.code_hash)

"""
Now, code hash is not null anymore.

Before using the currency contract, you must issue the currency.
"""
teos.PushAction(
  "currency", "issue", 
  '{"to":"currency","quantity":"1000.0000 CUR","memo":""}', 
  permission="currency@active")
"""

./eosioc push action currency issue '{"to":"currency","quantity":"1000.0000 CUR"}' --permission currency@active
Next verify the currency contract has the proper initial balance:

./eosioc get table currency currency account
{
  "rows": [{
     "currency": 1381319428,
     "balance": 10000000
     }
  ],
  "more": false

}

"""
daemon = teos.Daemon()
daemon.clear()
wallet = teos.Wallet("default")
eosio_key = teos.EosioKey()
wallet.import_key(eosio_key)
owner_key = teos.CreateKey("owner_key")
active_key = teos.CreateKey("active_key")

account = teos.Account(
    eosio_key.account_name, "currency", owner_key, active_key
    )
print(account)
wallet.import_key(active_key)
print(wallet)
code = account.code()
print(code.code_hash)
account.set_contract("currency.wast", "currency.abi")
code = account.code()
print(code.code_hash)
"""

Transfering funds with the sample "currency" contract

Anyone can send any message to any contract at any time, but the contracts may reject messages which are not given necessary permission. Messages are not sent "from" anyone, they are sent "with permission of" one or more accounts and permission levels. The following commands show a "transfer" message being sent to the "currency" contra ct.

The content of the message is '{"from":"currency","to":"eosio","quantity":"20.0000 CUR","memo":"any string"}'. In this case we are asking the currency contract to transfer funds from itself to someone else. This requires the permission of the currency contract.

./eosioc push action currency transfer '{"from":"currency","to":"eosio","quantity":"20.0000 CUR","memo":"my first transfer"}' --permission currency@active
Below is a generalization that shows the currency account is only referenced once, to specify which contract to deliver the transfer message to.

./eosioc push action currency transfer '{"from":"${usera}","to":"${userb}","quantity":"20.0000 CUR","memo":""}' --permission ${usera}@active
As confirmation of a successfully submitted transaction, you will receive JSON output that includes a transaction_id field.


Reading sample "currency" contract balance

So now check the state of both of the accounts involved in the previous transaction.

./eosioc get table eosio currency account
{
  "rows": [{
      "currency": 1381319428,
      "balance": 200000
       }
    ],
  "more": false

}
./eosioc get table currency currency account
{
  "rows": [{
      "currency": 1381319428,
      "balance": 9800000
    }
  ],
  "more": false
}
As expected, the receiving account eosio now has a balance of 20 tokens, and the sending account now has 20 less tokens than its initial supply.



"""



