# EOSFactory Release Notes - v2.2

## Compatibility

EOSFactory [v2.2](https://github.com/tokenika/eosfactory/releases/tag/v2.1) is compatible with EOS [v1.3.x](https://github.com/EOSIO/eos/releases/tag/v1.3.0) and [v1.4.x](https://github.com/EOSIO/eos/releases/tag/v1.4.0)

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
* Color differentiation in console output.
* Support for `keosd`, the official wallet management tool.
* Full compatibility with production version of EOS ([v1.2.0](https://github.com/EOSIO/eos/releases/tag/v1.2.0) or higher).
* Seamless integration with public testnets (e.g. [Jungle Testnet](http://dev.remote_testnet.io/) or [Kylin Testnet](https://tools.cryptokylin.io)).
* The entire wallet management migrated to `keosd`, as for security reasons this feature is no longer supported by `nodeos`.
* Radically improved mechanism for mapping random account names to human-friendly aliases, including symbolic translation of *EOS* logger messages.
* New mechanism for caching public testnet settings.
* [Developer API](https://github.com/tokenika/eosfactory/blob/master/eosfactory/eosf.py) reduced to less than 20 basic commands and classes.
* Radially improved logger messaging, including highly customizable verbosity.
* Local testnet running in a headless mode (this allows you to run EOSFactory in a GUI-less environment, e.g. Ubuntu Server, or via SSH).
* All functionality ported to Python, no need to compile any C++ code.
* Precise error catching in unit tests, utilizing Python's `assertRaises(Error)` feature.

## New features available in v2.2
* Completely removed dependence on system variables: entries in the `~/.profile` or `~/.bash_profile` files are no longer needed.
* Radically improved (and simplified) installation process: the Python modules are now installed with `setuptools`.
* While using EOSFactory with *Visual Studio Code* is highly recommended, EOSFactory has become independent from any particular IDE and does not impose any particular folder structure inside your smart-contract project. The only requirement is having a folder called `build` on the same level or one level up from your C++ source files.
