'''
# Debugging smart contracts

This file can be executed as a python script: 
`python3 debugging.md`.

The EOSIO documentation <a href="https://eosio-cpp.readme.io/docs/debugging">advertises</a> the proposed debugging method as 'Caveman Debugging':

''The main method used to debug smart contract is Caveman Debugging, where we 
utilize the printing functionality to inspect the value of a variable and check 
the flow of the contract.''

We attempt to make it more refined, introducing a logging utility implemented 
in the 'hpp` header file.
</pre>

## Set-up

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

The debugging test uses the 'hello' contract that comes with every EOS 
distribution. The EOSFactory has a copy of the code in its 'contracts' 
directory. Contract directories there can be accessed simply by their names.

The set-up for the debugging test involves the wallet, 'account master' account, 
an account for holding the tested contract, and to working accounts (here, 
'alice' and 'carol').

```md
'''
from  eosfactory import *
Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
CONTRACT_DIR = "01_hello_world"

restart()
set_is_testing_errors(False)
set_throw_error(True)
reset() 

create_wallet()
create_master_account("account_master")
create_account("greeter", account_master)
create_account("alice", account_master)
create_account("carol", account_master)
'''
```
### Include hpp

Let us have the header #include, and a 'logger_info' line in the source 
code of the contract that is the 'contracts/hello/src.hello.cpp' file:

```md
#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

#define DEBUG
#include "hpp"
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

Build and deploy the contract. Push contract actions:

```md
'''
contract = Contract(greeter, CONTRACT_DIR)
contract.build()
contract.deploy()

greeter.push_action(
    "hi", {"user":alice}, alice)

greeter.push_action(
    "hi", {"user":carol}, carol)
'''
```

### Test run

In an linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:

```md
$ python3 debugging.md
```

We hope that you have something similar to what is shown in the image below.

![debugging](./img/debugging.png)

'''
