# Introduction to the `session` module

```python
from session import *

# import importlib
# importlib.reload(s)

run()
```
## session.init()

```
init()
dir()
```
... outputs names that `s` (session module, in general) defines:
```
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'account_eosio', 'alice', 'bob', 'carol', 'init', 'teos', 'wallet']
```
Try the python help facility...
```
help(init)
```
... outputs
```
Help on function init in module session:

init()
    Initialise a test session.

    - **global variables**

        account_eosio: Primary owned account.
        wallet: The wallet.
        allice, bob, carol: Prefabricated accounts.
(END)
```
You have to input `q`, in order to escape the help view.

See the wallet ...
```
print(wallet)
```
... result is:
```
{'keys': [['key_owner', '5JeYw9fHPnZbYn34W4kRuTrX7uy66MAHHS5KWQCZCYRyptViKkY'],
          ['key_active',
           '5KQ7w24iVoufQBUoryn4NFLGCi9PRu4FASyDtqLcSeVMixftoSE']],
 'name': 'default',
 'password': 'PW5JFisSF9VwYbPKZxV6B7iEQMNjNoinU1TsFsXdKXVVnjUnC2JYN'}
```
```
print(bob)
#     account name: bob
```

## session.Contract

```
help(Contract)
```
```
Help on class Contract in module session:

class Contract(teos.Contract)
 |  Given a contract directory defining WAST and ABA, creates a contract.
 |
 |  This class extends the teos.Contract: it goes without the `account`
 |  parameter, instead it uses an account created internally.
 |
 |  - **parameters**
 |      contract_dir: A contract directory, structures according to the
 |          `contract template', that means, including the `build' directory
 |          that contains WAST and ABI.
 |      wast_file: The file containing the contract WAST, relative
 |          to contract-dir, defaults to "".
:
```
Any key to scroll up, `q` to escape.

```
contract_currency = Contract("currency")
#         key name: key_owner
#      private key: 5K6Qh97Z1bMm5b4iX7ewpWK2eNu4fo4Hs65ZhKBokrVNG8uca8U
#       public key: EOS7UeB2WFkT1CK3cxzPh8aUXTJryw8NsXY2PEdcRQHjAbRBtL4xc

#         key name: key_active
#      private key: 5JRaXkwhYw3axXPTFRk8jJ5R4D5fB9XAXBUFamfHTR2hdyCQojM
#       public key: EOS5NWBHzhJbmPuQzJPHGG2Tq8gttMkUTA4k1nrt4VpGiJfcyXjg7

#   transaction id: acdd8ac4c28f6aa4efdb9d5996cd890441773b55c0fc746657228f0c93f6f8d0

#   transaction id: cc71cb88d70f742426fc207a20cca15527e621ba7d8d10c1e00087896648c0a3
```