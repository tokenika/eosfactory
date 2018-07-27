# EOSFactory Release Notes - v0.8

## Compatibility

EOSFactory [v0.8](https://github.com/tokenika/eosfactory/releases/tag/v0.8) is compatible with EOS [dawn-v4.0.0](https://github.com/EOSIO/eos/releases/tag/dawn-v4.0.0).

## What works in this release

* Launch a single-node private testnet and fully control it: stop it and then continue running it or completely reset it.
* Initialize a testnet with the `bios` contract and several test accounts (available as `sess.alice`, `sess.bob ` and `sess.carol`).
* Create additional test accounts (their keys are automatically imported into the wallet).
* Manage the wallet (locking, unlocking etc).
* Have an easy access to demo contracts stored in the `contracts` folder of the *EOSIO* source code (you can instantiate them in EOSFactory by passing their folder name in the `Contract` class constructor).
* Compile a contract, both ABI & WAST (but please note that the ABI compiler has an experimental status in *EOSIO* repository).
* Create a new contract from a pre-defined template (this includes the creation of its *CMake* files).
* Deploy a contract (the account holding the contract is created behind the scenes).
* Interact with a contract by pushing actions to it.
* Extract text messages logged by a contract (i.e. a contract's output stream produced by its `print()` method).
* Extract data from a contract's table.
* Run a simple unit-test utilizing all the above features.

## Current limitations

* Currently unit-tests in EOSFactory are just naïve demo examples. They don't have proper assertions, don't handle errors properly and they don't have proper tear-down methods.
* You cannot connect EOSFactory to a testnet of your choice, only to a private one running a single node.
* Whereas the `nodeos` process runs in the background on MacOS, on other platforms (Windows & Ubuntu) it requires launching a separate terminal window (it's done automatically though). This might be a limitation for GUI-less systems like Ubuntu Server edition.
* There are no utilities for debugging contracts, except for the "caveman" style, i.e. accessing the output stream produced by its `print()` method.
* There is no easy way to instantiate smart-contracts stored outside of EOSFactory `contracts` folder or EOSIO `contracts` folder. If you want to do that, you need to refer to the contract's folder by supplying its full path.
* The `TemplateCreate` class constructor only accepts a folder name, not a path (this is different from the `Contract` constructor which accepts both).
* The `Contract` class `abi()` and `build()` methods are relying on the *EOSIO* ABI compiler which has an experimental status in the *EOSIO* repository. Thus the ABI output might be different than expected.
* The `Contract` class `push_action()` and `show_action` methods accept only verbose input, i.e. all action's parameters must be named in the JSON syntax.