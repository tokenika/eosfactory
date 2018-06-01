# What value ads the EOSFactory?

## Smart-contract Hello World for smart ones.

Hello World smart contract is easy. It is explain in an EOSIO tutorial, namely [*Tutorial Hello World Contract*](https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract).

Let us go through the tutorial.

* Create a new folder called "hello", cd into the folder, then create a file "hello.cpp" with the following contents:
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

* Compile your code to web assembly (.wast) as follows:
```
$ eosiocpp -o hello.wast hello.cpp
Build hello.wast
```
* Now, generate the abi:
```
$ eosiocpp -g hello.abi hello.cpp
Generated hello.abi
```

* Create an account and upload the contract:
```
cleos push action hello.code hi '["user"]' -p user
executed transaction: 4c10c1426c16b1656e802f3302677594731b380b18a44851d38e8b5275072857  244 bytes  1000 cycles
#    hello.code <= hello.code::hi               {"user":"user"}
>> Hello, user
```

* Open the file "hello.cpp" in your favorite editor and modify the hi() function in hello.cpp as follows:
```
void hi( account_name user ) {
   require_auth( user );
   print( "Hello, ", name{user} );
}
```

* Recompile your code to web assembly (.wast) as follows:
```
$ eosiocpp -o hello.wast hello.cpp
Build hello.wast
```

* Again, regenerate the abi:
```
$ eosiocpp -g hello.abi hello.cpp
Generated hello.abi
```

* Create an account and upload the contract:
```
$ cleos create account eosio hello.code EOS7ijWCBmoXBi3CgtK7DJxentZZeTkeUnaSDvyro9dq7Sd1C3dC4 
EOS7ijWCBmoXBi3CgtK7DJxentZZeTkeUnaSDvyro9dq7Sd1C3dC4
...
$ cleos set contract hello.code ../hello -p hello.code
...
```

* Finally, you can run the contract:
```
$ cleos push action hello.code hi '["user"]' -p user
executed transaction: 4c10c1426c16b1656e802f3302677594731b380b18a44851d38e8b5275072857  244 bytes  1000 cycles
#    hello.code <= hello.code::hi               {"user":"user"}
>> Hello, user
```

And so on. It is very easy, but by sure that you do not confuse the cryptographic keys. Therefore, you must be a smart (enough) one, rather, as well.

## Smart-contract Hello World for dummies.

![EOSFactory](code.png)


