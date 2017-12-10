# Testing whether the *currency* contract survives the changes proposed (tokenika-lab).

```
EOSIO_INSTALL_DIR="/mnt/hgfs/Workspaces/EOS/eos"
source /mnt/hgfs/Workspaces/EOS/eoscBash/eoscBash $EOSIO_INSTALL_DIR
eosc clean
source /mnt/hgfs/Workspaces/EOS/eoscBash/eoscBash $EOSIO_INSTALL_DIR

eosc wallet create
eosc wallet import ${initaPrivKey}
eosc create key owner
eosc create key active
eosc wallet import $activePrivKey
eosc create account inita currency $ownerPublKey $activePublKey

contractSrc=/mnt/hgfs/Workspaces/EOS/EosContracts/currency/currency.cpp
```
In types.hpp, (tokenika-lab) `static eosio::uint64_t string_to_name(` does not compile. 

Back to the original: `static constexpr eosio::uint64_t string_to_name(`
```
eosc buildContract $contractSrc
eosc set contract currency ${contractSrc/.cpp/.wast}  ${contractSrc/.cpp/.abi}

jq '.processed.messages' <<< "$contractSet"
```
```
[
  {
    "code": "eos",
    "type": "setcode",
    "authorization": [
      {
        "account": "currency",
        "permission": "active"
      }
    ],
    "data": {
      "account": "currency",
      "vm_type": 0,
      "vm_version": 0,
      "code": 
(...)

eosc push message currency transfer '{"from":"currency","to":"inita","amount":50}' --scope currency,inita --permission currency@active
##
## code: 5093418677655568384; name(code): currency name(code).value: 5093418677655568384 N(name(code).value): 11071149854176575926
## action: 14829575313431724032; name(action): transfer
## Transfer 50 currency from 5093418677655568384 to 8421048506461978624

jq '.processed.messages' <<< "$messagePushed"
```
```
[
  {
    "code": "currency",
    "type": "transfer",
    "authorization": [
      {
        "account": "currency",
        "permission": "active"
      }
    ],
    "data": {
      "from": "currency",
      "to": "inita",
      "amount": 50
    },
    "hex_data": "0000001e4d75af46000000000093dd743200000000000000"
  }
]
```
OK!
