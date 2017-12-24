## benchmark

## wallet

### setup

### transfer

## version

## client

```
./eosc version client
Build version: 70fd94c3

```

### create: Create a new wallet locally
```
./eosc wallet create -n third_wallet
REQUEST httc.cpp [66]
POST /v1/wallet/create HTTP/1.0
Host: localhost
content-length: 14
Accept: */*
Connection: close

"third_wallet"
/REQUEST
RESPONSE  httc.cpp [111]
```
```
./eosc wallet create
REQUEST httc.cpp [66]
POST /v1/wallet/create HTTP/1.0
"PW5J4SC8bwbDyuRePyeeSBJ7Sosgck2ymnxjYQBKK3Q7kZVVHraMB"/RESPONSE
153398ms            main.cpp:1195                 main                 ] Failed with error: End Of File (11)
unexpected end of file
Host: localhost
content-length: 9
Accept: */*
Connection: close

"default"
/REQUEST
RESPONSE  httc.cpp [111]
```

### open: Open an existing wallet
```
./eosc wallet open -n second_wallet
REQUEST httc.cpp [66]
POST /v1/wallet/open HTTP/1.0
Host: localhost
content-length: 15
Accept: */*
Connection: close

"second_wallet"
/REQUEST
RESPONSE  httc.cpp [111]
{}/RESPONSE
```

### lock: Lock wallet
```
./eosc wallet lock -n third_wallet
REQUEST httc.cpp [66]
POST /v1/wallet/lock HTTP/1.0
Host: localhost
content-length: 14
Accept: */*
Connection: close                        

"third_wallet"
/REQUEST
RESPONSE  httc.cpp [111]
{}/RESPONSE
```

### lock_all: Lock all unlocked wallets
```
./eosc wallet lock_all
REQUEST httc.cpp [66]
POST /v1/wallet/lock_all HTTP/1.0
Host: localhost
content-length: 0
Accept: */*
Connection: close


/REQUEST
RESPONSE  httc.cpp [111]
{}/RESPONSE
```
### unlock: Unlock wallet
```
./eosc wallet unlock -n third_wallet --password PW5KYupdww61FE3xo891GfSdMHLvvVW96ETWxVFDSeRtojY82iGmh
Failed to connect to eosd at localhost:8888; is eosd running?
```
```
./eosc wallet unlock -n third_wallet --password "PW5KYupdww61FE3xo891GfSdMHLvvVW96ETWxVFDSeRtojY82iGmh"
REQUEST httc.cpp [66]
POST /v1/wallet/unlock HTTP/1.0
Host: localhost
content-length: 72
Accept: */*
Connection: close

["third_wallet","PW5KYupdww61FE3xo891GfSdMHLvvVW96ETWxVFDSeRtojY82iGmh"]
/REQUEST
RESPONSE  httc.cpp [111]
{}/RESPONSE
```

### import: Import private key into wallet
```
./eosc wallet import -n third_wallet 5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3
REQUEST httc.cpp [66]
POST /v1/wallet/import_key HTTP/1.0
Host: localhost
content-length: 70
Accept: */*
Connection: close

["third_wallet","5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"]
/REQUEST
RESPONSE  httc.cpp [111]
{}/RESPONSE
```

### list: List opened wallets, * = unlocked
```
./eosc wallet list
Wallets:
REQUEST httc.cpp [66]
POST /v1/wallet/list_wallets HTTP/1.0
Host: localhost
content-length: 0
Accept: */*
Connection: close


/REQUEST
RESPONSE  httc.cpp [111]
["second_wallet","third_wallet *"]/RESPONSE
```

### keys: List of private keys from all unlocked wallets in wif format.
```
./eosc wallet keys
REQUEST httc.cpp [66]
POST /v1/wallet/list_keys HTTP/1.0
Host: localhost
content-length: 0
Accept: */*
Connection: close

## get

```
  info                        Get current blockchain information
  block                       Retrieve a full block from the blockchain
  account                     Retrieve an account from the blockchain
  code                        Retrieve the code and ABI for an account
  table                       Retrieve the contents of a database table
  accounts                    Retrieve accounts associated with a public key
  servants                    Retrieve accounts which are servants of a given account 
  transaction                 Retrieve a transaction from the blockchain
  transactions                Retrieve all transactions with specific account name referenced in their scope

```
### info
```
./eosc get info
REQUEST httc.cpp [66]
POST /v1/chain/get_info HTTP/1.0
Host: localhost
content-length: 0
Accept: */*
Connection: close


/REQUEST
RESPONSE  httc.cpp [123]
{"server_version":"70fd94c3","head_block_num":33,"last_irreversible_block_num":16,"head_block_id":"00000021d998470e3502c4df411ea75b556116b27711120574abf3df4531c157","head_block_time":"2017-12-22T12:06:42","head_block_producer":"initk","recent_slots":"1111111111111111111111111111111111111111111111111111111111111111","participation_rate":"1.00000000000000000"}/RESPONSE
```
### block
```
./eosc get block 12
REQUEST httc.cpp [66]
POST /v1/chain/get_block HTTP/1.0
Host: localhost
content-length: 24
Accept: */*
Connection: close

{"block_num_or_id":"12"}
/REQUEST
RESPONSE  httc.cpp [123]
{"previous":"0000000b3589eb5bfaa020f6717311f8052bcb6cb7e81b53e979708b78e347a2","timestamp":"2017-12-22T12:06:21","transaction_merkle_root":"0000000000000000000000000000000000000000000000000000000000000000","producer":"initm","producer_changes":[],"producer_signature":"1f3a8825400231d1fb89bbf0fc9e22c6386b97beb1f5cc11ab5a19f9d275f62a7e74cf36b7a5350390ffa3f626aa60d7c59e764007477ff89b880ccc694506f920","cycles":[],"id":"0000000c9b1412714beca27a275d7359bd845e7c71f515d643d09a05f94e5a9a","block_num":12,"ref_block_prefix":2057497675}/RESPONSE
```
### account
```
./eosc get account inita
REQUEST httc.cpp [66]
POST /v1/chain/get_account HTTP/1.0
Host: localhost
content-length: 24
Accept: */*
Connection: close

{"account_name":"inita"}
/REQUEST
RESPONSE  htt{
  "required_keys": [
    "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
  ]
}c.cpp [123]
{"account_name":"inita","eos_balance":"1000000.0000 EOS","staked_balance":"0.0000 EOS","unstaking_balance":"0.0000 EOS","last_unstaking_time":"1969-12-31T23:59:59","permissions":[{"perm_name":"active","parent":"owner","required_auth":{"threshold":1,"keys":[{"key":"EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV","weight":1}],"accounts":[]}},{"perm_name":"owner","parent":"","required_auth":{"threshold":1,"keys":[{"key":"EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV","weight":1}],"accounts":[]}}]}/RESPONSE
```

### code
```
./eosc get code inita
REQUEST httc.cpp [66]
POST /v1/chain/get_code HTTP/1.0
Host: localhost
content-length: 24
Accept: */*
Connection: close

{"account_name":"inita"}
/REQUEST
RESPONSE  httc.cpp [123]
{"account_name":"inita","code_hash":"0000000000000000000000000000000000000000000000000000000000000000","wast":""}/RESPONSE
```

### table
```
$ curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d 
'{"scope":"inita", "code":"currency", "table":"account", "json": true}'

$ curl  http://127.0.0.1:8888/v1/chain/get_table_rows -X POST -d 
'{"scope":"inita", "code":"currency", "table":"account", "json": true, "lower_bound":0, "upper_bound":-1, "limit":10}'
```
```
./eosc get table inita currency account
REQUEST httc.cpp [66]
POST /v1/chain/get_table_rows HTTP/1.0
Host: localhost
content-length: 65
Accept: */*
Connection: close

{"json":true,"scope":"inita","code":"currency","table":"account"}
/REQUEST
RESPONSE  httc.cpp [123]
{"code":500,"message":"Internal Service Error","details":"unknown key"}/RESPONSE
```
### accounts

### servants

### transaction

### transactions
```
./eosc get transactions inita
REQUEST httc.cpp [66]
POST /v1/account_history/get_transactions HTTP/1.0
Host: localhost
content-length: 24
Accept: */*
Connection: close

{"account_name":"inita"}
/REQUEST
RESPONSE  httc.cpp [123]
{"code":404,"message":"Not Found","details":"Unknown Endpoint"}/RESPONSE
```
### required_keys
```
$ curl  http://127.0.0.1:8888/v1/chain/get_required_keys -X POST -d 

'{"transaction": {"ref_block_num":"100","ref_block_prefix":"137469861","expiration":"2017-09-25T06:28:49","scope":["initb","initc"],"messages":[{"code":"currency","type":"transfer","recipients":["initb","initc"],"authorization":[{"account":"initb","permission":"active"}],"data":"000000000041934b000000008041934be803000000000000"}],"signatures":[],"authorizations":[]}, "available_keys":["EOS4toFS3YXEQCkuuw1aqDLrtHim86Gz9u3hBdcBw5KNPZcursVHq","EOS7d9A3uLe6As66jzN8j44TXJUqJSK3bFjjEEqR4oTvNAB3iM9SA","EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"]}'

## create

### key

### account

### producer


RESULT
{
  "required_keys": [
    "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
  ]
}
```


## other

### abi_json_to_bin
```

```


## Notes

/REQUEST
RESPONSE  httc.cpp [111]
[["EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV","5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"]]/RESPONSE
```
yyyccc PW5JWcwceRf89aVSNW1fhoPH46TbWqR62WZTkjHZprxCvk4rxQmi9

xxxccc PW5K18ya55udfNSfnWRnxvFLEgUNb4mxeY9frXofyCH1mxqBdKmND