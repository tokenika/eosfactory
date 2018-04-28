# EOSIO Smart Contract

We rephrase an [article](#https://github.com/EOSIO/eos/wiki/Smart%20Contract) from EOSIO wiki.

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

We use Python scripts. Python is renowned for its intuitive simplicity. Let you start Python in the `eosfactory/teos_python` directory (issue `python3` UBUNTU bash command). Then launch the `teos`:
```python
import teos
teos.set_verbose(true)
```
The response is the path to the `teos` executable, which drives python functions.
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

It is easy to start with a template. I you have imported `teos.py` module already, if the contract name can be `tokenika_hello_world`, use the creator of the `teos.ContractTemplate` class:

```python
teos.ContractTemplate("tokenika_hello_world")
#      context dir: /mnt/c/Workspaces/EOS/eosfactory
#    contracts dir: /mnt/c/Workspaces/EOS/eosfactory/contracts
#     contract dir: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika_hello_world
#        build_dir: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika_hello_world/build
#     template.cpp: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika_hello_world/tokenika_hello_world.cpp
#     template.hpp: /mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika_hello_world/tokenika_hello_world.hpp
```
Now, you have a new folder in the workspace which is `/mnt/c/Workspaces/EOS/eosfactory/contracts/tokenika_hello_world'. If you use the `Visual Studio Code`, you can open it in this folder. You will find there a configured, for EOSIO smart contract development, *InteliSense* space enabling code browsing. There,you can also (Ctrl+Shift+B) build the contract, producing WAST and ABI. We will add more of automatized functionality there: setting contract to the local node, running test, perhaps more.



The above will create a new empty project in the `./${project}` folder with three files:
```base
${contract}.abi ${contract}.hpp ${contract}.cpp
```

### hpp

`${contract}.hpp` is the header file that contain the variables, constants, and functions referenced by the `.cpp` file.

### cpp

The `${contract}.cpp` file is the source file that contains the functions of the contract. 

If you generate the `.cpp` file using the `eosiocpp` tool, the generated .cpp file would look similar to the following:

```base
#include <${contract}.hpp>

/**
 *  The init() and apply() methods must have C calling convention so that the blockchain can lookup and
 *  call these methods.
 */
extern "C" {

    /**
     *  This method is called once when the contract is published or updated.
     */
    void init()  {
       eosio::print( "Init World!\n" ); // Replace with actual code
    }

    /// The apply method implements the dispatch of actions to this contract
    void apply( uint64_t code, uint64_t action ) {
       eosio::print( "Hello World: ", eosio::name(code), "->", eosio::name(action), "\n" ); 
    }

} // extern "C"
```

In this example you can see there are two functions, `init` and `apply`. All they do are log the actions delivered and makes no other checks. Anyone can deliver any action at any time provided the block producers allow it. Absent any required signatures, the contract will be billed for the bandwidth consumed.

**init**

The `init` function will only be executed once at initial deployment. It is used for initializing contract variables, e.g. the token supply for a currency contract.

**apply**

`apply` is the action handler, it listens to all incoming actions and reacts according to the specifications within the function. The `apply` function requires two input parameters, `code` and `action`.

**code filter**

In order to respond to a particular action, structure the `apply` function as follows. You may also construct a response to general actions by omitting the code filter.

```base
if (code == N(${contract_name}) {
    // your handler to respond to particular action
}
```

You can also define responses to respective actions in the code block.

**action filter**

To respond to a particular action, structure your `apply` function as follows. This is normally used in conjuction with the code filter.

```base
if (action == N(${action_name}) {
    //your handler to respond to a particular action
}
```

### wast

Any program to be deployed to the EOSIO blockchain must be compiled into WASM format. This is the only format the blockchain accepts.

Once you have the CPP file ready, you can compile it into a text version of WASM (.wast) using the `eosiocpp` tool.

```base
$ eosiocpp -o ${contract}.wast ${contract}.cpp
```
### abi

The Application Binary Interface (ABI) is a JSON-based description on how to convert user actions between their JSON and Binary representations. The ABI also describes how to convert the database state to/from JSON. Once you have described your contract via an ABI then developers and users will be able to interact with your contract seamlessly via JSON.

The ABI file can be generated from the `.hpp` files using the `eosiocpp` tool:

```base
$ eosiocpp -g ${contract}.abi ${contract}.hpp
```

The following is an example of what the skeleton contract ABI looks like:
```base
{
  "types": [{
      "new_type_name": "account_name",
      "type": "name"
    }
  ],
  "structs": [{
      "name": "transfer",
      "base": "",
      "fields": {
        "from": "account_name",
        "to": "account_name",
        "quantity": "uint64"
      }
    },{
      "name": "account",
      "base": "",
      "fields": {
        "account": "name",
        "balance": "uint64"
      }
    }
  ],
  "actions": [{
      "action": "transfer",
      "type": "transfer"
    }
  ],
  "tables": [{
      "table": "account",
      "type": "account",
      "index_type": "i64",
      "key_names" : ["account"],
      "key_types" : ["name"]
    }
  ]
}
```

You will notice that this ABI defines an action `transfer` of type `transfer`. This tells EOSIO that when `${account}->transfer` action is seen that the payload is of type `transfer`. The type `transfer` is defined in the `structs` array in the object with `name` set to `transfer`.

```base
...
  "structs": [{
      "name": "transfer",
      "base": "",
      "fields": {
        "from": "account_name",
        "to": "account_name",
        "quantity": "uint64"
      }
    },{
...
```

The ABI has several fields, including `from`, `to` and `quantity`. These fields have the corresponding types `account_name`, and `uint64`. `account_name` is a built-in type used to represent base32 string as `uint64`. To see more about what built-in types are available, check [here](https://github.com/EOSIO/eos/blob/master/libraries/chain/contracts/abi_serializer.cpp).

```base
{
  "types": [{
      "new_type_name": "account_name",
      "type": "name"
    }
  ],
...
```

Inside the above `types` array we define a list of aliases for existing types. Here, we define `name` as an alias of `account_name`.

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
Let's write a new contract as example for debugging
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

