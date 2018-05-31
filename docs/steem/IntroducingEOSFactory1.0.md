# Introducing EOSFactory 1.0 release with standard Python-based unit testing

We are proud to announce the second release of [EOSFactory](https://github.com/tokenika/eosfactory).

The initial release (v0.8 published three weeks ago) was a solid foundation but contained only simple examples of home-made unit tests, whose only point was to prove the concept. Therefore those unit tests could not be treated as a robust verification tool: they did not handle errors in an orderly manner and they did not offer proper assertions.

This release takes EOSFactory to the next level. We've integrated it with [Unittest](https://docs.python.org/2/library/unittest.html), the standard unit testing framework for Python. What it means is that from now on, when using EOSFactory for working with EOS smart-contracts, you have the power of standardized Python-based unit testing at your disposal.

Also, we've made the much needed separation between EOSFactory infrastructure and user-defined workspace for smart-contract development.

We believe that those two features make EOSFactory quite reliable and production-ready - hence we label it v1.0. 

Generally, EOSFactory when combined with [Visual Studio Code IDE](https://code.visualstudio.com/) is evolving into a robust EOS smart-contract development environment. All the essential programming tools become available to you, as EOSFactory smart-contract template generator is able to produce a complete Visual Studio Code project, which includes not only unit testing support but also `cmake` support, automated tasks and all the features that come with [IntelliSense](https://msdn.microsoft.com/en-us/library/hcw1s69b.aspx): code completion, content assist, and code hinting.

![img](https://cdn.steemitimages.com/DQmcYyhEcoz4Az2vEf7vA1AJYgTNzhvKewsKPqd7hqbphyo/peek.png)

And here is a complete list of EOSFactory features available in the 1.0 release:

#### 1. Standard unit-testing framework

We are utilizing the power of [Unittest](https://docs.python.org/3/library/unittest.html), the standard Python unit test framework. According to its documentation it's a fully fledged and highly standardized toolset:

> The `unittest` unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages. It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework. 

#### 2. Support for user-defined workspaces

We are introducing a clear separation between EOSFactory infrastructure (including its demo examples and smart-contract templates) and a dedicated user-defined workspace, where user-created smart-contracts and unit tests can be safely stored.

#### 3. Support for debugging

Smart-contracts can never be properly debugged (as you cannot pause the blockchain easily), but we've come up with a good work-around for tracking a smart-contract’s execution. What you can do with EOSFactory is put in your C++ code logger clauses (e.g. `logger_info("user: ", name{user});`) which will produce output to the console giving you the exact location of its origin, including the C++ file name and line number.

#### 4. Contract verification with CLANG

When using the standard EOS toolset, in order to check for errors in a smart-contract code you need to go through the entire process of building & linking performed by the WASM compiler. What we offer is the option of reducing this process to a simple CLANG compilation (i.e. without linking). And only when your code is error-free and you are ready for testnet deployment and unit testing, you can switch to the more heavy-weight WASM compiler.

------

As we mentioned in our previous post, all feedback is very welcome, especially critical, as it motivates us towards improvement.









