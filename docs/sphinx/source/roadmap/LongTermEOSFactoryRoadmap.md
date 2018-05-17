# Long-term EOSFactory Roadmap

#### 1. Support for other IDEs

Our current priority is integration with [Visual Studio Code](https://code.visualstudio.com), but we also intend to support other IDEs, e.g. [Eclipse](https://www.eclipse.org/ide/).

#### 2. GUI support

We plan to provide a graphical interface for the existing Python CLI functionality by creating a *Visual Studio Code* extension for EOSFactory.

#### 3. Direct connection to EOSIO

We are considering pros & cons of connecting our Python layer directly to `cleos`, the official *EOSIO* CLI. The obvious advantage of this approach would be simplification of the installation process for EOSFactory.

#### 4. Two implementations

We are also considering splitting the EOSFactory project into two implementations: pure Python (based on [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/en/latest/)) and pure C++ (based on [Boost Unit Test Framework](https://www.boost.org/doc/libs/1_53_0/libs/test/doc/html/utf.html)).

#### 5. Ricardian Contracts

And finally, we are thinking about integrating *Ricardian Contracts* into our framework. For more information please refer to [EOSIO documentation](https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract#hello-world-ricardian-contract).

