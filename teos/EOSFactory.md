# Tokenika TEOS library


## Rationale

The EOSFactory grows to be an mature IDE (Integrated Development Environment) for EOSIO smart-contracts.

*An integrated development environment (IDE) is a software application that provides comprehensive facilities to computer programmers for software development. An IDE normally consists of a source code editor, build automation tools, and a debugger.* [ (from Wikipedia)](#https://en.wikipedia.org/wiki/Integrated_development_environment)


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

Let you have installed *EOSFactory* according to our instructions. Now, you can start development of a *token* contract from a template, for example:
```
$ $teos_cli bootstrap contract token eosio.token.cpp
#     template contract: /mnt/c/Workspaces/EOS/contracts/token
```
The second positional parameter name the template used. 

Let you open *Visual Studio Code* in the `token` contract directory.


### InteliSense and code browsing

You can open `token.cpp`. With the `C/C++`, you can go to definition/declaration, for example (see the description of te extension for many more): place right mouse over the `print` function name and chose `Pick Declaration`.


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
\- results in placing WAST and ABI files in the contract build directory, and building the tests.

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
...............................
...............................

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


