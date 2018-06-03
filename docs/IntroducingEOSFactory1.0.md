# Introducing EOSFactory 1.0 release with standard Python-based unit testing

**We are proud to announce the second release of EOSFactory. With this release unit tests for EOS smart-contracts become standardized and thus much more reliable. Also, you can now tap into all the utilities offered by Visual Studio Code IDE. Our long-term goal is to turn EOSFactory into a comprehensive IDE (Integrated Development Environment) for EOS smart-contracts.**

![img](https://cdn.steemitimages.com/DQmR21xQNJ4CbS1DoJEAutvYFWU9mD11PAYkCQZpLnHXLdY/EOSFactory%20logo.png)

## Standardized unit testing

The initial release (v0.8 [published](https://steemit.com/eos/@tokenika/introducing-eosfactory-an-eos-smart-contract-development-and-testing-framework) three weeks ago) was a solid foundation but contained only simple examples of home-made unit tests, whose only point was to prove the concept. Therefore those unit tests could not be treated as a robust verification tool: they did not handle errors in an orderly manner and they did not offer proper assertions.

This release takes [EOSFactory](https://github.com/tokenika/eosfactory) to the next level. We've integrated it with [Unittest](https://docs.python.org/2/library/unittest.html), the standard unit testing framework for Python. What it means is that from now on, when using EOSFactory for working with EOS smart-contracts, you have the power of standardized Python-based unit testing at your disposal.

Below is an example of an EOSFactory unit test output:

```
Test project /mnt/d/Workspaces/EOS/contracts/hello.tokenika/build
    Start 1: unittest
1/2 Test #1: unittest .........................   Passed    6.58 sec
    Start 2: test
2/2 Test #2: test .............................   Passed    5.12 sec

100% tests passed, 0 tests failed out of 2

Total Test time (real) =  11.71 sec
```

### Main features in v1.0

We believe the features available in this release make EOSFactory quite reliable and production-ready - hence we label it v1.0.  Below is a complete list of those new features.

#### 1. Standard unit-testing framework

We are utilizing the power of [Unittest](https://docs.python.org/3/library/unittest.html), the standard Python unit test framework. As emphasized in the documentation, Unittest is a fully fledged and highly standardized toolset:

> The `unittest` unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages. It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework. 

#### 2. Support for user-defined workspaces

We are introducing a clear separation between EOSFactory infrastructure (including its demo examples and smart-contract templates) and a dedicated user-defined workspace, where user-created smart-contracts and unit tests can be safely stored.

#### 3. Support for debugging

Smart-contracts can never be properly debugged (as you cannot pause the blockchain easily), but we've come up with a good work-around for tracking a smart-contract’s execution. What you can do with EOSFactory is put in your C++ code special logger clauses (e.g. `logger_info("user: ", name{user});`) which will produce output to the console giving you the exact location of its origin, including the C++ file name and line number.

#### 4. Contract verification with `CLANG`

When using the standard EOS toolset, in order to check for errors in a smart-contract code you need to go through the entire process of building & linking performed by the `WASM` compiler. What we offer is the option of reducing this process to a simple `CLANG` compilation (i.e. without linking). And only when your code is error-free and you are ready for testnet deployment and unit testing, you can switch to the more heavy-weight `WASM` compiler.

#### 5. *Visual Studio Code* integration

EOSFactory is becoming more tightly integrated with [Visual Studio Code](https://code.visualstudio.com/). When you create a new smart-contract in EOSFactory, what you get is an entire VSC project, with support for [CMake](https://cmake.org/) builds, automated tasks and [IntelliSense](https://msdn.microsoft.com/en-us/library/hcw1s69b.aspx) features.

## Why is EOSFactory needed?

Undoubtedly, everything that EOSFactory offers can be done with the official EOSIO toolset, i.e. `cleos` and `eosiocpp`. Does it make EOSFactory just a simple alternative to those tools? Not really.

Try to go through [EOS tutorials](https://github.com/EOSIO/eos/wiki/Tutorial-eosio-token-Contract) based on `cleos` and you'll see how much concentration is required to follow those simple examples without making a single mistake. And now imagine doing it 10 or 100 times. Surely, it's a daunting task!

Code development and unit-testing involve tasks that need to be executed hundreds of times, and each time in exactly the same way and exactly the same context. Therefore those tasks need to be fully automated, as otherwise a lot of time is being wasted and, what's even worse, a lot of additional uncertainty is introduced. Manually performed actions are prone to errors.

And this is what EOSFactory actually brings to the table: an easy & intuitive way to automate the process of dealing with smart-contracts. Write down, in the form of a Python script, what needs to be done multiple times in exactly the same way and exactly the same context, and then just run the script. EOSFactory will take care of everything else: it will compile your smart-contract, create a new testnet, deploy the contract, invoke its methods and verify the response, then tear down the testnet, and finally report the results. And all of this done in a couple of seconds.

## Aiming to become a comprehensive EOS IDE

Generally, EOSFactory when combined with [Visual Studio Code](https://code.visualstudio.com/) is evolving into a robust EOS smart-contract IDE (Integrated Development Environment), as defined by [Wikipedia](https://mail.google.com/mail/u/0/#https://en.wikipedia.org/wiki/Integrated_development_environment):

> An integrated development environment (IDE) is a software application that provides comprehensive facilities to computer programmers for software development. An IDE normally consists of a source code editor, build automation tools, and a debugger.

With *Visual Studio Code* integration all the essential programming tools become easily available, as EOSFactory smart-contract template generator is able to produce a complete *Visual Studio Code* project, which includes not only unit testing support but also:

- Linux, MacOS and Windows compatibility,
- [CMake](https://cmake.org/) support allowing you to compile, build and unit test your smart-contract by running those three commands: `cmake`, `make`, `ctest`.
- automated tasks accessible from the VSC menu,
- all the features that come with [IntelliSense](https://msdn.microsoft.com/en-us/library/hcw1s69b.aspx): e.g. code completion, content assist, code hinting,
- multiple community-driven extensions, including the possibility to create a specialized EOS smart-contract extension.

![img](https://cdn.steemitimages.com/DQmcYyhEcoz4Az2vEf7vA1AJYgTNzhvKewsKPqd7hqbphyo/peek.png)

## Documentation

EOSFactory source code can be found in [this repository](https://github.com/tokenika/eosfactory) on GitHub. As for more detailed documentation, tutorials and installation guides, please refer to [this website](http://eosfactory.io/sphinx/build/html/).

## Feedback is welcome

As we mentioned in our previous post, all feedback is very welcome, especially critical, as it motivates us towards improvement.

---

**NOTE:** For the time being EOSFactory `v1.0` is compatible EOSIO `dawn-v4.0.0`. Once EOSIO stops changing rapidly and becomes stable, the subsequent EOSFactory release will be compatible with the latest EOSIO release.