# EOSFactory Release Notes - v1.1

## Compatibility

EOSFactory [v1.1](https://github.com/tokenika/eosfactory/releases/tag/v1.1) is compatible with EOS [v1.0.8](https://github.com/EOSIO/eos/releases/tag/v1.0.8) (or higher).

## Features available in previous releases

* Launch a single-node private testnet and fully control it: stop it and then continue running it or completely reset it.
* Initialize a testnet with the `bios` contract and several test accounts (available as `sess.alice`, `sess.bob ` and `sess.carol`).
* Create additional test accounts (their keys are automatically imported into the wallet).
* Manage the wallet (locking, unlocking etc).
* Have an easy access to demo contracts stored in the `contracts` folder of the *EOSIO* source code (you can instantiate them in EOSFactory by passing their folder name in the `Contract` class constructor).
* Compile a contract, both `ABI` & `WAST` (but please note that the ABI compiler has an experimental status in *EOSIO* repository).
* Create a new contract from a pre-defined template (this includes the creation of its [CMake](https://cmake.org/) files).
* Deploy a contract (the account holding the contract is created behind the scenes).
* Interact with a contract by pushing actions to it.
* Extract data from a contract's table.
* Integration with Python [UnitTest](https://docs.python.org/2/library/unittest.html) standard library.
* User-defined workspace for smart-contract storage.
* Support for debugging via logger output containing file name & line number.
* Preliminary code verification with `CLANG`.
* [Visual Studio Code](https://code.visualstudio.com/) integration, including [CMake](https://cmake.org/) builds and automated tasks.

## New features available in v1.1
* Full compatibility with production version of EOS ([v1.0.8](https://github.com/EOSIO/eos/releases/tag/v1.0.8) or higher).
* Ability to interact with a public testnet (e.g. [Jungle Testnet](http://dev.remote_testnet.io/)).
* Support for `keosd`, the official wallet management tool.
* Built-in mechanism for mapping random account names to fixed names needed for smart-contract testing.
* Color differentiation in console output.
* Improved error reporting.

## Current limitations

* There are some edge cases where account mappings get erased and the user needs to start from scratch in terms of setting up an account on a public testnet.
* Whereas the `nodeos` process runs in the background on MacOS, on other platforms (Windows & Ubuntu) it requires launching a separate terminal window (it's done automatically though). This might be a limitation for GUI-less systems like Ubuntu Server edition.
* The `Contract` class `abi()` and `build()` methods are relying on the *EOSIO* ABI generator which has an experimental status in the *EOSIO* repository. Thus the ABI output might be different than expected.
* The `Contract` class `push_action()` and `show_action` methods accept only verbose input, i.e. all action's parameters must be named in the JSON syntax.
