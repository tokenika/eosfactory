## Release 0.8 on 17 May 2018

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

## Release 1.0 on 6 Jun 2018

* Integration with Python UnitTest standard library.
* User-defined workspace for smart-contract storage.
* Support for debugging via logger output containing file name & line number.
* Preliminary code verification with CLANG.
* Visual Studio Code integration, including CMake builds and automated tasks.

## Release 1.1 on 11 Jul 2018

* Full compatibility with production version of EOS (v1.0.8 or higher).
* Ability to interact with a public testnet (e.g. Jungle Testnet).
* Support for keosd, the official wallet management tool.
* Built-in mechanism for mapping random account names to fixed names needed for smart-contract testing.
* Color differentiation in console output.
* Improved error reporting.

## Release 2.0 on 13 Sep 2018

* Full compatibility with production version of EOS (v1.2.0 or higher).
* Seamless integration with public testnets (e.g. Jungle Testnet or Kylin Testnet).
* The entire wallet management migrated to keosd.
* Radically improved mechanism for mapping random account names to human-friendly aliases, including symbolic translation of EOS logger messages.
* New mechanism for caching public testnet settings.
* Developer API reduced to less than 20 basic commands and classes.
* Radially improved logger messaging, including highly customizable verbosity.

## Release 2.1 on 25 Sep 2018

* Local testnet running in a headless mode (this allows you to run EOSFactory in a GUI-less environment, e.g. Ubuntu Server, or via SSH).
* All functionality ported to Python, no need to compile any C++ code.
* Precise error catching in unit tests, utilizing Python's assertRaises(Error) feature.
* Improved folder structure within Python modules.
* Simplified syntax for logger management.

## Release 2.2 on 30 Oct 2018

* Completely removed dependence on system variables: entries in the ~/.profile or ~/.bash_profile files are no longer needed.
* Radically improved (and simplified) installation process: the Python modules are now installed with setuptools.
* While using EOSFactory with Visual Studio Code is highly recommended, EOSFactory has become independent from any particular IDE and does not impose any particular folder structure inside your smart-contract project. The only requirement is having a folder called build on the same level or one level up from your C++ source files.

## Release 2.3 on 10 Dec 2018

* Compatibility with EOSIO v1.5.0
* Support for binary version of EOSIO (while support for a source code build is maintained)
* Smart-contract are built using EOSIO Contract Development Toolkit (CDT)
* Support for setting account and action permissions
* Optional nodeos output to file
* Several bug fixes

## Release 2.4 on 4 Jan 2019

* General code overhaul & clean-up.
* Documentation improved & revised.
* Introduction of code patterns.
* Several bug fixes.


## Release 3.0.2 on 5 Mar 2019

* New alternative syntax introduced for creating references to EOS accounts: `foo = new_account(...)`.
* EOSFactory package can be installed from PyPi repository.
* Compatibility with python linter: now linter doesn't raise warnings about dynamically created account objects.
* Cleaner code, better documented.