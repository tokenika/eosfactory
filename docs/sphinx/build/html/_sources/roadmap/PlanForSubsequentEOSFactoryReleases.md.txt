# Plan for Subsequent EOSFactory Releases

#### Compatibility with EOSIO v1.0

For the time being EOSFactory v1.0 is compatible EOSIO dawn-v4.0.0. Once EOSIO stops changing rapidly and becomes stable, the subsequent EOSFactory release will be compatible with the latest EOSIO release.

#### Connect to non-private testnet

You'll be able to connect to any testnet you want, not just the single-node private one, as it is now.

#### Extract the C++ layer as a separate project

We plan to move the C++ layer's source code (called `teos`) into a separate repository, so that it can also serve as a foundation for other projects. What's nice about `teos` is that it's a static library, not an executable like `cleos`, and therefore it's much more suitable for integrations.