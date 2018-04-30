# EOSIO Smart Contract

We rephrase an [article](#https://github.com/EOSIO/eos/wiki/Smart%20Contract) from the EOSIO wiki.

- [Introduction to EOSIO Smart Contract](#introduction-to-eos-smart-contract)
  * [Required Background Knowledge](#required-background-knowledge)
  * [Basics of EOSIO Smart Contract](#basics-of-eos-smart-contract)
  * [Technical Limitation](#technical-limitation)
- [Smart Contract Files](#smart-contract-files)
  * [hpp](#hpp)
  * [cpp](#cpp)
  * [wast](#wast)
  * [abi](#abi)
- [Debugging Smart Contract](#debugging-smart-contract)
  * [Method](#method)
  * [Print](#print)
  * [Example](#example)

<!-- /MarkdownTOC -->

## Introduction to EOSIO Smart Contract

### Required Background Knowledge

**C / C++ Experience**

EOSIO based blockchains execute user-generated applications and code using [WebAssembly](http://webassembly.org/) (WASM). WASM is an emerging web standard with widespread support of Google, Microsoft, Apple, and others. At the moment the most mature toolchain for building applications that compile to WASM is [clang/llvm](https://clang.llvm.org/) with their C/C++ compiler.

Other toolchains in development by 3rd parties include: Rust, Python, and Solidity. While these other languages may appear simpler, their performance will likely impact the scale of application you can build. We expect that C++ will be the best language for developing high-performance and secure smart contracts and plan to use C++ for the foreseeable future.

**Python Knowledge**

We use Python scripts for steering the flow of data. Python is renowned for its intuitive simplicity. 

Let you start Python in the `eosfactory/teos_python` directory (issue `python3` UBUNTU bash command). Then launch the `teos`:
```python
import teos
teos.set_verbose(True)
```
The response is the path to the `teos` executable which drives functions of the `teos.py` module.
```
teos exe: /mnt/c/Workspaces/EOS/eosfactory/teos/build/teos
```

### Basics of EOSIO Smart Contract

**Communication Model**

EOSIO Smart Contracts communicate with each other in the form of actions and shared memory database access, e.g. a contract can read the state of another contract's database as long as it is included within the read scope of the transaction with an async vibe. The async communication may result in spam which the resource limiting algorithm will resolve.
There are two communication modes that can be defined within a contract:

- **Inline**. Inline is guaranteed to execute with the current transaction or unwind; no notification will be communicated regardless of success or failure. Inline operates with the same scopes and authorities the original transaction had.

- **Deferred**. Defer will get scheduled later at producer's discretion; it's possible to communicate the result of the communication or can simply timeout. Deferred can reach out to different scopes and carry the authority of the contract that sends them.

**Action vs Transaction**

A action represents a single operation, whereas a transaction is a collection of one or more actions. A contract and an account communicate in the form of actions. Actions can be sent individually, or in combined form if they are intended to be executed as a whole. 

*Transaction with 1 action*.

```base
{
  "expiration": "2018-04-01T15:20:44",
  "region": 0,
  "ref_block_num": 42580,
  "ref_block_prefix": 3987474256,
  "net_usage_words": 21,
  "kcpu_usage": 1000,
  "delay_sec": 0,
  "context_free_actions": [],
  "actions": [{
      "account": "eosio.token",
      "name": "issue",
      "authorization": [{
          "actor": "eosio",
          "permission": "active"
        }
      ],
      "data": "00000000007015d640420f000000000004454f5300000000046d656d6f"
    }
  ],
  "signatures": [
    ""
  ],
  "context_free_data": []
}
```

*Transaction with multiple actions*, these actions should either all be successed or all failed.
```base
{
  "expiration": "...",
  "region": 0,
  "ref_block_num": ...,
  "ref_block_prefix": ...,
  "net_usage_words": ..,
  "kcpu_usage": ..,
  "delay_sec": 0,
  "context_free_actions": [],
  "actions": [{
      "account": "...",
      "name": "...",
      "authorization": [{
          "actor": "...",
          "permission": "..."
        }
      ],
      "data": "..."
    }, {
      "account": "...",
      "name": "...",
      "authorization": [{
          "actor": "...",
          "permission": "..."
        }
      ],
      "data": "..."
    }
  ],
  "signatures": [
    ""
  ],
  "context_free_data": []
}
```

**Action Name Restrictions**

Action types are actually **base32 encoded 64-bit integers**. This means they are limited to the characters a-z, 1-5, and '.' for the first 12 characters. If there is a 13th character then it is restricted to the first 16 characters ('.' and a-p).

**Transaction Confirmation**

Receiving a transaction hash does not mean that the transaction has been confirmed, it only means that the node accepted it without error, which also means that there is a high probability other producers will accept it.

By means of confirmation, you should see the transaction in the transaction history with the block number of which it is included.

## Smart Contract Files 

It is easy to start with a template. I you have [imported](#python-knowledge) `teos.py` module already,and if the contract name can be `tokenika`, use the creator of the `teos.ContractTemplate` class:

```python
template_tokenika = teos.ContractTemplate("tokenika")
#  template contract: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika
```
Now, you have a new folder in the workspace. You can know the path to it...
```
template_tokenika.contract_dir
# '/mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika'
```
If you use the `Visual Studio Code`, you can open it in this contract folder. You will find there a configured, for EOSIO smart contract development, *InteliSense* space enabling code browsing. There you can (Ctrl+Shift+B) build the contract, producing WAST and ABI. We will add more of automatized functionality there: setting contract to the local node, running test, perhaps more.

The contract directory contains the source files of the contract:
```
template_tokenika.hpp
# '/mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika/tokenika.hpp'

template_tokenika.cpp
# '/mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika/tokenika.cpp'
```

The `template_tokenika.cpp` file is the source file that contains the functions of the contract.

Nota bene:

The original example in the EOSIO wiki [tutorial](#https://github.com/EOSIO/eos/wiki/Smart%20Contract) does not compile. We guess that it is outdated. We use an example from [another tutorial](#https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract)

```c++
#include <eosiolib/print.hpp>
#include <tokenika.hpp>

using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract; 

      /// @abi action 
      void hi( account_name user ) {
         print( "Hello, ", name{user} );
      }
};

EOSIO_ABI( hello, (hi) )
```

### wast

Any program to be deployed to the EOSIO blockchain must be compiled into WASM format. This is the only format the blockchain accepts.

Once you have the CPP file ready, you can compile it into a text version of WASM:
```python
wast = teos.WAST(template_tokenika.contract_dir)
#             WAST: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika/build/tokenika.wast
```
You can inspect the WAST, however, it is not interesting to us:
```python
print(wast.wast)
```
```
..............
     (set_local $4
      (i32.sub
       (i32.const 2147483644)
       (get_local $2)
      )
     )
     (set_local $11
      (i32.add
       (get_local $0)
       (i32.const 8392)
      )
     )
     (set_local $12
      (i32.add
       (get_local $0)
       (i32.const 8384)
      )
     )
     (set_local $13
      (tee_local $3
       (i32.load offset=8392
        (get_local $0)
       )
      )
     )
     (loop $label$8
      (call $eosio_assert
       (i32.eq
        (i32.load
         (i32.add
          (tee_local $1
           (i32.add
            (get_local $0)
            (i32.mul
             (get_local $13)
             (i32.const 12)
            )
           )
          )
          (i32.const 8200)
         )
        )
        (i32.load
         (tee_local $5
          (i32.add
           (get_local $1)
           (i32.const 8192)
          )
         )
        )
       )
       (i32.const 8448)
      )
..............
```

### abi

The Application Binary Interface (ABI) is a JSON-based description on how to convert user actions between their JSON and Binary representations. The ABI also describes how to convert the database state to/from JSON. Once you have described your contract via an ABI then developers and users will be able to interact with your contract seamlessly via JSON.

The ABI file can be generated from the `.hpp` files:

```python
abi = teos.ABI(template_tokenika.contract_dir)
#             WAST: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika/build/tokenika.wast
```
You can inspect the ABI:
```python
import pprint
pprint.pprint(abi.abi)
```
```json
{'____comment': 'This file was generated by eosio-abigen. DO NOT EDIT - 2018-04-29T09:37:28', 'ricardian_clauses': '', 'types': '', 'actions': [{'name': 'hi', 'type': 'hi', 'ricardian_contract': ''}], 'structs': [{'name': 'hi', 'base': '', 'fields': [{'name': 'user', 'type': 'account_name'}]}], 'tables': ''}
>>> pprint.pprint(abi.abi)
{'____comment': 'This file was generated by eosio-abigen. DO NOT EDIT - '
                '2018-04-29T09:37:28',
 'actions': [{'name': 'hi', 'ricardian_contract': '', 'type': 'hi'}],
 'ricardian_clauses': '',
 'structs': [{'base': '',
              'fields': [{'name': 'user', 'type': 'account_name'}],
              'name': 'hi'}],
 'tables': '',
 'types': ''}
```

You will notice that this ABI defines an action `hi` of type `hi`. This tells EOSIO that when `${account}->hi` action is seen that the payload is of type `hi`. The type `hi` is defined in the `structs` array in the object with `name` set to `hi`.

```json
 'structs': [{'base': '',
              'fields': [{'name': 'user', 'type': 'account_name'}],
              'name': 'hi'}],
```

The ABI has one field, namely `name`. This fields has the type `account_name`. `account_name` is a built-in type used to represent base32 string as `uint64`. To see more about what built-in types are available, check [here](https://github.com/EOSIO/eos/blob/master/libraries/chain/contracts/abi_serializer.cpp).

The entry `types` is empty here. In general it is used to define a list of aliases for existing types. Here, we define `name` as an alias of `account_name`.

## Debugging Smart Contract

In order to be able to debug your smart contract, you will need to setup local nodeos node. This local nodeos node can be run as separate private testnet or as an extension of public testnet (or the official testnet).

When you are creating your smart contract for the first time, it is recommended to test and debug your smart contract on a private testnet first, since you have full control of the whole blockchain. This enables you to have unlimited amount of eos needed and you can just reset the state of the blockchain whenever you want. When it is ready for production, debugging  on the public testnet (or official testnet) can be done by connecting your local nodeos to the public testnet (or official testnet) so you can see the log of the testnet in your local nodeos.

The concept is the same, so for the following guide, debugging on the private testnet will be covered.


If you haven't set up your own local nodeos, please follow the [setup guide](https://github.com/EOSIO/eos/wiki/Local-Environment). By default, your local nodeos will just run in a private testnet unless you modify the config.ini file to connect with public testnet (or official testnet) nodes as described in the following [guide](Testnet%3A%20Public).

### Method
The main method used to debug smart contract is **Caveman Debugging**, where we utilize the printing functionality to inspect the value of a variable and check the flow of the contract. Printing in smart contract can be done through the Print API ([C](https://github.com/EOSIO/eos/blob/master/contracts/eoslib/print.h) and [C++](https://github.com/EOSIO/eos/blob/master/contracts/eoslib/print.hpp)). The C++ API is the wrapper for C API, so most often we will just use the C++ API.

### Print
Print C API supports the following data type that you can print:
- prints - a null terminated char array (string)
- prints_l - any char array (string) with given size
- printi - 64-bit unsigned integer
- printi128 - 128-bit unsigned integer
- printd - double encoded as 64-bit unsigned integer
- printn - base32 string encoded as 64-bit unsigned integer
- printhex - hex given binary of data and its size 

While Print C++ API wraps some of the above C API by overriding the print() function so user doesn't need to determine which specific print function he needs to use. Print C++ API supports
- a null terminated char array (string)
- integer (128-bit unsigned, 64-bit unsigned, 32-bit unsigned, signed, unsigned)
- base32 string encoded as 64-bit unsigned integer
- struct that has print() method

### Example
Let's write a new contract as example for debugging, named `debug`:
```
template_debug = teos.ContractTemplate("debug")
#  template contract: /mnt/c/Workspaces/EOS/eosfactory/contracts/debug
```

- debug.hpp
```cpp
#include <eoslib/eos.hpp>
#include <eoslib/db.hpp>

namespace debug {
    struct foo {
        account_name from;
        account_name to;
        uint64_t amount;
        void print() const {
            eosio::print("Foo from ", eosio::name(from), " to ",eosio::name(to), " with amount ", amount, "\n");
        }
    };
}
```
- debug.cpp
```cpp
#include <debug.hpp>

extern "C" {

    void init()  {
    }

    void apply( uint64_t code, uint64_t action ) {
        if (code == N(debug)) {
            eosio::print("Code is debug\n");
            if (action == N(foo)) {
                 eosio::print("Action is foo\n");
                debug::foo f = eosio::current_message<debug::foo>();
                if (f.amount >= 100) {
                    eosio::print("Amount is larger or equal than 100\n");
                } else {
                    eosio::print("Amount is smaller than 100\n");
                    eosio::print("Increase amount by 10\n");
                    f.amount += 10;
                    eosio::print(f);
                }
            }
        }
    }
} // extern "C"
```
- debug.abi
```cpp
{
  "structs": [{
      "name": "foo",
      "base": "",
      "fields": {
        "from": "account_name",
        "to": "account_name",
        "amount": "uint64"
      }
    }
  ],
  "actions": [{
      "action_name": "foo",
      "type": "foo"
    }
  ]
}

```

Let's deploy it and send a message to it. Assume that you have `debug` account created and have its key in your wallet.
```bash
$ eosiocpp -o debug.wast debug.cpp
$ cleos set contract debug debug.wast debug.abi
$ cleos push message debug foo '{"from":"inita", "to":"initb", "amount":10}' --scope debug
```

When you check your local `nodeos` node log, you will see the following lines after the above message is sent.
```
Code is debug
Action is foo
Amount is smaller than 100
Increase amount by 10
Foo from inita to initb with amount 20
```
There, you can confirm that your message is going to the right control flow and the amount is updated correctly. You might see the above message at least 2 times and that's normal because each transaction is being applied during verification, block generation, and block application.

