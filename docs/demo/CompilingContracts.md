# Compiling Contracts

The purpose of this tutorial is to demonstrate how *EOSFactory* and its Python syntax can be used to make compiling EOS contracts easy & intuitive.

## Prerequisites

This tutorial assumes that you have successfully installed *EOSIO* and *EOSFactory*.

## Initialize

In *Visual Studio Code* start a Bash console and type `python3` to run the Python CLI. 
Next, import the predefined *EOSFactory* Python classes:

```
$ import pyteos
```

Then start the testnet:

```
$ pyteos.run()
```

And initialize the workspace:

```
$ pyteos.init()
```

## Create a Contract Template

To create a contract template:

```
$ template = pyteos.Template("hello")
```

To check the path where the contract's files are located:

```
$ template.path()
```

## Edit code

```
#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>
using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract;

      /// @abi action 
      void hi( account_name user ) {
         print( "Hello, ", name{user} );
      }
};

EOSIO_ABI( hello, (hi) )
```

## Compile the Contract

```
$ pyteos.compile(template)
```

## Deploy the Contract

```
$ contract = pyteos.Contract("hello")
```

## Test the Contract

```
$ contract.push_action("hi", '{"user":"alice"}', alice)
```

```
$ contract.push_action("hi", '{"user":"carol"}', alice)
```

## Modify the code

```
#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>
using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract;

      /// @abi action 
        void hi( account_name user ) {
           require_auth( user );
           print( "Hello, ", name{user} );
        }
};

EOSIO_ABI( hello, (hi) )
```

## Re-compile the Contract

```
$ pyteos.compile(template)
```

## Re-deploy the Contract

```
$ contract = pyteos.Contract("hello")
```

## Re-test the Contract

```
$ contract.push_action("hi", '{"user":"alice"}', alice)
```

```
$ contract.push_action("hi", '{"user":"carol"}', alice)
```

## 

