# Long-term EOSFactory Roadmap

#### Support for other IDEs

Right now we are aiming for integration with [Visual Studio Code](https://code.visualstudio.com) (VSC), but we also consider supporting other IDEs, e.g. [Eclipse](https://www.eclipse.org/ide/).

#### GUI support

As far as VSC is concerned, we'd like to create a VSC extension providing GUI interface to EOSFactory CLI functionality.

#### Two implementations

We are also considering splitting the EOSFactory project into two implementations: pure Python (based on [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/en/latest/)) and pure C++ (based on [Boost Unit Test Framework](https://www.boost.org/doc/libs/1_53_0/libs/tests/doc/html/utf.html)).

#### Ricardian Contracts

We are thinking about integrating *Ricardian Contracts* into our unit-testing. This is a very interesting (and probably not widely known at this  stage) aspect of EOS smart-contracts. For more information please refer to [EOSIO documentation](https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract#hello-world-ricardian-contract).

