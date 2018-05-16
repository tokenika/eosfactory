# Plan for Subsequent EOSFactory Releases

**Apply proper unit-testing Python framework**

We want to avoid reinventing the wheel and plan to utilize the power of existing Python unit-test frameworks, e.g. [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/en/latest/).

**Support a user-defined workspace**

We'll introduce a clear separation between EOSFactory source code (including its demo examples) and a dedicated workspace, where a user's contracts and unit-tests are stored.

**Verify contracts with a C++ compiler**

Currently the only way to verify the correctness of a contract's C++ code is to go through the entire process of building and linking done by the *EOSIO* WASM compiler. What we want to achieve is reduce this process to a simple C++ build (i.e. without the linking stage) and let you apply the WASM compiler only when there are no formal errors and you want to actually deploy the contract on a testnet.

**Enable debugging**

Smart-contracts can never be properly debugged (as you cannot pause the blockchain easily), but we think we can come up with a useful way of tracking a contract's execution.

**Connect to non-private testnet**

You'll be able to connect to any testnet you want, not just the single-node private one, as it is the case now.

**Extract the C++ layer as a separate project**

We plan to move the C++ layer's source code (called `teos`) into a separate repository, so that it can also serve as a foundation for other projects. What's nice about `teos` is that it's a static library, not an executable like `cleos`, and therefore it's much more suitable for integrations.