# EOSFactory Release Notes - Version 0.8

## What works in this release

Using Python commands you currently can:

* launch a single-node private testnet and fully control it: stop it and then continue running it or completely reset it,
* initialize the testnet with the `bios` contract and several test accounts available as `sess.alice`, `sess.bob ` and `sess.carol`,
* create additional test accounts (their keys are automatically imported into the wallet),
* manage the wallet,
* easy access to demo contracts stored in the `contracts` folder of the *EOSIO* source code (you can instantiate them in EOSFactory by passing their folder name in the `Contract` class constructor),
* compile a contract, both ABI & WAST (but please note that the ABI compiler has an experimental status in *EOSIO* repository),
* create a new contract from a pre-defined template (this includes the creation of its *CMake* files),
* deploy a contract (the account holding the contract is created behind the scenes),
* interact with a contract by pushing actions to it,
* extract text messages logged by the contract (i.e. a contract's output stream produced by its `print()` method),
* extract data from a contract's table,
* run a simple unit-test utilizing all the above features.

## Current limitations

* Currently unit-tests in EOSFactory are just naïve demo examples. They don't have proper assertions, don't handle errors properly and they don't have proper tear-down methods.
* You cannot connect EOSFactory to a testnet of your choice, only to the private one.
* There are no utilities for debugging contracts, except for the "caveman" style, i.e. accessing the output stream produced by its `print()` method.
* There is no easy way to work with smart-contracts stored outside of EOSFactory `contracts` folder or EOSIO `contracts` folder. If you want to do that you need to refer to the contract folder by its full path.
* The `Template` class constructor only accepts a folder name, not a path (this is different from the `Contract` constructor which accepts both).
* The `Contract` class `abi()` and `build()` methods are relying on the *EOSIO* ABI compiler which has an experimental status in the *EOSIO* repository. Thus the ABI output might be different than expected.
* The `Contract` class `push_action()` and `show_action` methods accept only verbose input, i.e. all action's parameters must be named in the JSON syntax.

## Plans for the next release

#### 1. Introduce proper unit-testing Python framework

We want to avoid reinventing the wheel and plan to utilize the power of existing Python unit-test frameworks, e.g. [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/en/latest/).

#### 2. Support a user-defined workspace

We'll introduce a clear separation between EOSFactory source code (including with its demo examples) and a user's workspace, where his/her contracts and unit-tests are stored.

#### 3. Enable debugging

Smart-contracts can never be properly debugged (as you cannot pause the blockchain easily), but we think we can come up with a quite useful way of tracking a contract's execution.

#### 4. Connect to non-private testnet

You'll be able to connect to any testnet you want, not just the single-node private one, as it is now.

#### 5. Extract the C++ layer as a separate project

We plan to move the C++ layer's source code (called `teos`) into a separate repository, so that it can also serve as a foundation for other projects. What's nice about `teos` is that it's a static library, not an executable like `cleos`, and therefore it's easy to integrate.

## Further plans

* Right now we are aiming for integration with [Visual Studio Code](https://code.visualstudio.com), but we also consider supporting other IDEs, e.g. [Eclipse](https://www.eclipse.org/ide/).
* We are thinking about integrating *Ricardian Contracts* into our unit-testing. This is a very interesting (and probably not widely known at this  stage) aspect of EOS smart-contracts. For more information please refer  to [EOSIO documentation](https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract#hello-world-ricardian-contract). 
* We are considering the pros and cons of connecting our Python layer directly to `cleos`, the official EOS CLI. Even if we do that, nothing will change on in the Python API. The biggest advantage of this approach is simplification of the installation process for EOSFactory.