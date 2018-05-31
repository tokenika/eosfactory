# Tokenika TEOS library


## Rationale

Tokenika TEOS library is designed for the Tokenika EOSFactory. The EOSFactory grows to be an mature IDE (Integrated Development Environment) for EOSIO smart-contracts.

*An integrated development environment (IDE) is a software application that provides comprehensive facilities to computer programmers for software development. An IDE normally consists of a source code editor, build automation tools, and a debugger.* [ (from Wikipedia)](#https://en.wikipedia.org/wiki/Integrated_development_environment)

The TEOS library is the engine that powers these *comprehensive facilities*.


## Walkthrough

Our plan is to build around the [*Visual Studio Code*](#https://code.visualstudio.com/). With VS code, we can have all what we want in one:

    * Linux Mac and Windows compatibility,
    * multi-language (C/C++, Python) support as InteliSense, code browsing,
    * VS code task system,
    * plentifulness of extensions, 
    * a room for specialized EOSIO smart-contract IDE extension.

Please, walkthrough the following outline of our IDE.


### Starting with a template

The EOSFactory has two flavours: one purely C/C++ with EOSIO smart-contract tests written in C++, another with Python tests. Here we show the former version.

Let you have installed *EOSFactory* according to our instructions.
Let you have your smart-contract workspace defined, either with the `-w` option of the `eosfactory` installer, or with a corresponding entry in the `config.json` file, for example:
```
{
........................................
    "EOSIO_CONTRACT_WORKSPACE": "/mnt/c/Workspaces/EOS/contracts", 
........................................
}
```
You can start development from a template, for example:
```
$ $teos_cli bootstrap contract token eosio.token.cpp
#     template contract: /mnt/c/Workspaces/EOS/contracts/token
```
The second positional parameter name the template used. Templates are in directory `eosfactory/templates`. Currently, only one `cpp` template is available.

Now, let you open *Visual Studio Code* in the `token` contract directory. Do `CTR+SHIFT+P`, chose `Open Folder...` (or `#+SHIFT+P` chose `Open...` with Mac), browse to the directory. Please, be sure that you have installed the `C/C++` extension to the *VS code*.


### InteliSense and code browsing

Now, you can open `token.cpp`. With the `C/C++`, you can go to definition/declaration, for example (see the description of te extension for many more): place right mouse over the `print` function name and chose `Pick Declaration`.


### Tasks

The VS Code supports custom tasks, accessible from the main menu.


#### task EOSIO smart contract API

```
VS code main menu Tasks -> Run Task... -> API
```
opens [Smart Contract API Reference](#https://eosio.github.io/eos/group__contractdev.html).


#### task compile
```
VS code main menu Tasks -> Run Task... -> compile
```
You can see an error report, if they are compile errors. Linking is not executed.


####  task build
```
VS code main menu Tasks -> Run Task... -> build
```
results in placing WAST and ABI files in the contract build directory, and building the tests:
```
......................
Scanning dependencies of target wast
# WAST: /mnt/c/Workspaces/EOS/contracts/token/src/../build/token.wast
[  0%] Built target wast
Scanning dependencies of target abi
NOTE:
An ABI exists in the source directory. Cannot overwrite it:
/mnt/c/Workspaces/EOS/contracts/token/src/token.abi
        Just copying it to the target directory.
[  0%] Built target abi
Scanning dependencies of target unittest1
[ 25%] Building CXX object test/CMakeFiles/unittest1.dir/unittest1.cpp.o
[ 50%] Linking CXX executable unittest1
[ 50%] Built target unittest1
Scanning dependencies of target test1
[ 75%] Building CXX object test/CMakeFiles/test1.dir/test1.cpp.o
[100%] Linking CXX executable test1
[100%] Built target test1
.....................
```


#### task unittest

```
VS code main menu Tasks -> Run Task... -> unittest
```
The test is defined in file `test/unittest1.cpp`. Its result is similar to the following:
```
..............................

test 2
    Start 2: unittest

2: Test command: /mnt/c/Workspaces/EOS/contracts/token/build/test/unittest1
2: Test timeout computed to be: 1500
2: Running 1 test case...
2:
2:     First test of the TEOS library (C++).
2:     The library is to assist development of EOSIO smart contracts.
2:     Please, see the documentation.
2:
2:
2: issue
2: INFO quantity.amount: 1000000  @ 7:17:25 token.cpp[54](issue)
2: eosio balance: 100.0000 EOS
2:
2: transfer from alice to carol 25.0000 EOS
2: alice balance: 75.0000 EOS
2: carol balance: 25.0000 EOS
2:
2: transfer from carol to bob 13.0000 EOS
2: carol balance: 12.0000 EOS
2: bob balance: 13.0000 EOS
2:
2: transfer from bob to alice 2.0000 EOS
2: bob balance: 11.0000 EOS
2: alice balance: 77.0000 EOS
2:
2:
2: *** No errors detected
1/1 Test #2: unittest .........................   Passed    3.76 sec

The following tests passed:
        unittest

100% tests passed, 0 tests failed out of 1

Total Test time (real) =   3.77 sec
```


#### task test

The task executes a functional test, defined in file `test/test1.cpp`:
```
................................

test 1
    Start 1: test

1: Test command: /mnt/c/Workspaces/EOS/contracts/token/build/test/test1
1: Test timeout computed to be: 1500
1: code: 0000000000000000000000000000000000000000000000000000000000000000
1: code: 0d01c32281f130a464a435fe17cd2ec63c6243bcbb37eb79a2af39fe140ebf28
1:
1:
1: issue
1: INFO quantity.amount: 1000000  @ 8:12:46 token.cpp[54](issue)

..............................
```


### CMake procedures


#### cmake build

```
$ cd build
$ cmake ..
$ make
```

The result is the same as with the *build* task.


#### cmake compile

```
$ cd build
$ cmake -DC=true ..
$ make
```
The result is the same as with the *compile* task.


### ctest

```
ctest -V -R ^unittest$
ctest -V -R ^test$
```
The result is the same as with the *unittest* and *test* tasks.

## Helper library

We will develop and collect libraries that could facile the process of the development of the EOSIO smart-contracts. Now, we can show one example in action. This is the `logger.hpp` header in the directory `src`. (Of course, it is placed there temporarily.)

The only way to debug a smart contract is by loggers. An example is in the line `54` in the file `src/token.cpp`. The effect fronm this code entry is seen in the last line reproduces as a result of the functional test.


## Library structure

The library has three layers:
  * raw basic operation classes, for example GetInfo, DaemonStart, BuildContract;
  * command-line drivers for the basic operations, for example GetInfoOptions, DaemonStartOptions;
  * EOSIO notion abstraction classes like Account, Contract, Wallet.


### Command-line drivers

The command-line drivers, operated by the main `teos` application, mimic and/or extend *EOSIO cleos*, but they are limited in their functionality to the needs of our smart contract IDE. They are not going to replace  *EOSIO cleos* as a client to a remote EOSIO node. 

However, *Tokeniks teos* can play with a local node. For example, the following sequence of bash commands make sense:

```
$ $teos_cli bootstrap contract hello.teos     ## new contract template
#  template contract: /mnt/c/Workspaces/EOS/contracts/hello.teos

$ $teos_cli build contract hello.teos ## relative to the workspace
#  WAST: /mnt/c/Workspaces/EOS/contracts/hello.teos/build/hello.teos.wast

$ $teos_cli generate abi hello.teos ## relative to the workspace
#  ABI: /mnt/c/Workspaces/EOS/contracts/hello.teos/build/hello.teos.abi

$ $teos_cli daemon start -c                   ## reset local node
#  nodeos exe file: /mnt/c/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#  genesis state file: 
  /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json
#   server address: 127.0.0.1:8888
#  config directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir
#  wallet directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet
#  head block number: 3
#  head block time: 2018-05-23T16:02:40

$ $teos_cli wallet create
#         password: PW5K5jzJZaCXEtrwThSgPjgSjiZj8d9i1fCGZSUM7ZC9XEUySarnD
#  You need to save this password to be able to lock/unlock the wallet!

$ $teos_cli set contract eosio hello.teos --permission eosio
#   transaction id: 
  ef2744011c17b219f346c2841ebc316c0ebd21da9804ec804c860f71558481ba

$ $teos_cli create key owner
#         key name: owner
#      private key: 5J5Th3pDjjhkvwiPSETfqoSPp95APj8y7RaaghHtfq7UMUjy3Xa
#       public key: EOS6GKYMgKHeuMAaHb3v4nGBg9NiYRcJoU3YegUYeUwSjUfSJWLdP

$ $teos_cli create key active
#         key name: active
#      private key: 5Jq3guBccY52bw7h3qTTLUHMvg99vx6qDTtyGN7LQrL68nQzszQ
#       public key: EOS7gnfsg5ZiS9wfGUJah18Dmkq4aXz7gQDTcmcFKtV9tMuhB5AeA

$ $teos_cli wallet import default \
  5J5Th3pDjjhkvwiPSETfqoSPp95APj8y7RaaghHtfq7UMUjy3Xa
#           wallet: default
#     key imported: 5J5Th3pDjjhkvwiPSETfqoSPp95APj8y7RaaghHtfq7UMUjy3Xa

$ $teos_cli wallet import default 
  5Jq3guBccY52bw7h3qTTLUHMvg99vx6qDTtyGN7LQrL68nQzszQ
#           wallet: default
#     key imported: 5Jq3guBccY52bw7h3qTTLUHMvg99vx6qDTtyGN7LQrL68nQzszQ

$ $teos_cli create account eosio hello.teos \
  EOS6GKYMgKHeuMAaHb3v4nGBg9NiYRcJoU3YegUYeUwSjUfSJWLdP \
    EOS7gnfsg5ZiS9wfGUJah18Dmkq4aXz7gQDTcmcFKtV9tMuhB5AeA \
#   transaction id: 
  0ff62a96bde5bd911da135557da56fabb3fc1282d8be8797be485aafa519bce4

$ $teos_cli set contract hello.teos hello.teos
#   transaction id: 
  2820976a76893685f4cfc2578c7c0f0ff3e8b9112732de202dab16afd7b56884

$ $teos_cli push action hello.teos hi '["hello.teos"]' -p hello.teos
#   transaction id: 
  bdbace3b4327f70ccc7d63d1b1287a7abbec4240be9b2d7695192bf80da45f92
#  INFO account name: 7684013990126944256  @ 17:56:15 hello.teos.cpp[16](hi)
#  Hello, hello.teos

$ $teos_cli daemon stop
#  Daemon is stopped.
```

This command-line drivers to the basic operation classes power the Python implementation of the  EOSIO abstraction classes.


### C++ EOSIO abstraction classes

The abstraction classes are intent for writing of C++ tests for smart contracts. They make an alternative to the use of the *Tokenika pyteos classes*. They are used in the files `test/unittest1.cpp` and `test/test1.cpp`.

