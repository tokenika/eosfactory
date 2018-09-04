# Plan for Subsequent EOSFactory Releases

#### Integration with `eosjs` instead of `cleos`

Right now *EOSFactory* is using C++-based `cleos` to communicate with a local or remote testnet. In the future we plan to switch this dependence to JavaScript-based `eosjs`.

#### Better integration with *Visual Studio Code*

There is still a lot of things we can do to make *EOSFactory* more tightly integrated with VSC. What's important, we still want to offer the option to perform all the tasks in a standard bash terminal & your favorite code editor or IDE, thus work entirely outside of VSC.

#### Extracting the C++ layer as a separate project

We plan to move the C++ layer's source code (i.e.`teos`) into a separate repository, so that it can also serve as a foundation for other projects. What's nice about `teos` is that it's a static library, not an executable like `cleos`, and therefore it's much more suitable for integrations.