"""
# Debugging smart contracts

```md
This file can be executed as a python script: 
'python3 debugging.md'.
```
<pre>
The EOSIO documentation <a href="https://eosio-cpp.readme.io/docs/debugging">advertises</a> the proposed debugging method as 'Caveman 
Debugging':

''The main method used to debug smart contract is Caveman Debugging, where we 
utilize the printing functionality to inspect the value of a variable and check 
the flow of the contract.''

We attempt to make it more refined, introducing a logging utility implemented 
in the 'logger.hpp` header file.
</pre>

## Set-up

<pre>
The set-up statements are explained at <a href="setup.html">cases/setup</a>.

The debugging test uses the 'hello' contract that comes with every EOS 
distribution. The EOSFactory has a copy of the code in its 'contracts' 
directory. Contract directories there can be accessed simply by their names.

The set-up for the debugging test involves the wallet, 'account master' account, 
an account for holding the tested contract, and to working accounts (here, 
'account_alice' and 'account_carol').
</pre>

```md
"""
import sys
import unittest
import setup
import eosf
import time

from eosf import Verbosity
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

eosf.Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
eosf.use_keosd(False)

eosf.restart()
eosf.set_is_testing_errors(False)
eosf.set_throw_error(True)
eosf.reset([eosf.Verbosity.TRACE]) 

wallet = Wallet()
account_master_create("account_master")
account_create("account_hello", account_master)
account_create("account_alice", account_master)
account_create("account_carol", account_master)
"""
```
### Include logger.hpp

```md
Let us have the header #include, and a 'logger_info' line in the source 
code of the contract that is the 'contracts/hello/src.hello.cpp' file:
```
```md
#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

#define DEBUG
#include "logger.hpp"
#include "hello.hpp" 

using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract; 

      // @abi action 
      void hi( account_name user ) {

        logger_info( "user: ", name{user} );

        require_auth( user );
        print( "Hello, ", name{user} );
      }
};

EOSIO_ABI( hello, (hi) )
```

## Case
```md
Build and deploy the contract. Push contract actions:
```

```md
"""
contract_hello = Contract(account_hello, "hello")
contract_hello.build()
contract_hello.deploy()

account_hello.push_action(
    "hi", {"user":account_alice}, account_alice)

account_hello.push_action(
    "hi", {"user":account_carol}, account_carol)
"""
```

### Test run
```md
In an linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:
```
```md
$ python3 debugging.md
```
```md
We hope that you have something similar to what is shown in the image below.
```
<img src="debugging.png" 
    onerror="this.src='../../../source/cases/debugging.png'"   
    alt="account name conflict" width="720px"/>

"""
