# EOSFactory Release Notes - v1.0

## Compatibility

EOSFactory [v1.0](https://github.com/tokenika/eosfactory/releases/tag/v1.0) is compatible with EOS [dawn-v4.0.0](https://github.com/EOSIO/eos/releases/tag/dawn-v4.0.0).

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

## New features available in v1.0

* Integration with Python [UnitTest](https://docs.python.org/2/library/unittest.html) standard library.
* User-defined workspace for smart-contract storage.
* Support for debugging via logger output containing file name & line number.
* Preliminary code verification with `CLANG`.
* [Visual Studio Code](https://code.visualstudio.com/) integration, including [CMake](https://cmake.org/) builds and automated tasks.

## Current limitations

* You cannot connect EOSFactory to a testnet of your choice, only to a private one running a single node.
* Whereas the `nodeos` process runs in the background on MacOS, on other platforms (Windows & Ubuntu) it requires launching a separate terminal window (it's done automatically though). This might be a limitation for GUI-less systems like Ubuntu Server edition.
* The `Contract` class `abi()` and `build()` methods are relying on the *EOSIO* ABI generator which has an experimental status in the *EOSIO* repository. Thus the ABI output might be different than expected.
* The `Contract` class `push_action()` and `show_action` methods accept only verbose input, i.e. all action's parameters must be named in the JSON syntax.
