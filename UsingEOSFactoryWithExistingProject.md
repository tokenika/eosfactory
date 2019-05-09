# Using EOSFactory With an Existing EOS Smart-Contract Project

The purpose of this tutorial is to demonstrate how to apply EOSFactory to an existing EOS smart-contract project with arbitrary folder structure.

## Assumptions

* You have successfully installed EOSFactory on your machine, including all its dependencies, such as Python, PIP and EOSIO. For further details please refer to [this guide](https://eosfactory.io/build/html/tutorials/01.InstallingEOSFactory.html).
* Your smart-contract project is located inside a folder named `foo_project`.
* Your smart-contract's C++ source code is contained in a file named `foo_source.cpp`, located anywhere inside the `foo_project` folder (it can also be located in a subfolder inside the `foo_project` folder).
* If your project requires a C++ header file, it's contained in a file named `foo_header.hpp`, located anywhere inside the `foo_project` folder (it can also be located in a subfolder inside the `foo_project` folder).
* A test scenario for your contract is contained in a file named `foo_test.py`. This file can be located anywhere you want - it doesn't need to be inside the `foo_project` folder.

**NOTE:** Obviously, `foo_project`, `foo_source`, `foo_header` and `foo_test` are placeholders - they can be replaced by any names you prefer.

**NOTE:** We assume there is only one C++ source code file (i.e. an  `*.cpp` file) within the `foo_project` folder. If your project for some reasons requires more than one `*.cpp` file, EOSFactory can handle this situation but it requires a more complex setup, which is beyond the scope of this guide.

## Usage

Firstly, make sure the `foo_test.py` file contains the EOSFactory import clause:

```
from eosfactory.eosf import *
```

Secondly, make sure the `foo_test.py` file defines the  `PROJECT_DIR` constant as a string equal to the absolute path to the `foo_project` folder, i.e. it contains an expression like this:

```
PROJECT_DIR = "/path/to/the/foo_project/folder/"
```

And here is an example of a valid `foo_test.py` file:

```
import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

PROJECT_DIR = "/mnt/c/Workspaces/EOS/foo_project/"

# Actors of the test:
MASTER = MasterAccount()
HOST = Account()
ALICE = Account()
CAROL = Account()

def test():
    SCENARIO('''
    Execute simple actions.
    ''')
    reset()
    create_master_account("MASTER")

    COMMENT('''
    Build and deploy the contract:
    ''')
    create_account("HOST", MASTER)
    smart = Contract(HOST, PROJECT_DIR)
    smart.build(force=False)
    smart.deploy()

    COMMENT('''
    Create test accounts:
    ''')
    create_account("ALICE", MASTER)
    create_account("CAROL", MASTER)

    stop()

if __name__ == "__main__":
    test()
```

