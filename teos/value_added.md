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

And so on. It is easy, but be sure that you issue the right commands, and do not confuse the cryptographic keys.

### Integrated Development Environment (IDE)

What we do now is a play. However, development of a real smart-contract is a pain: it is an (seemingly) too long chain of corrections in code and tests with a local EOSIO node.

An IDE is of help here. It automatize - as mach as its construction is clever of - logistics. Ideally, all what is left to the codder is care about the logics of the contract. 

## EOSFactory grows to be a good IDE for EOSIO smart-contracts

*EOSFactory* is under development itself, but already now we can see it in action, if you have installed both *EOSFactory* and *Visual Studio Code*.

* Issue command that starts a new smart-contract project that is named *hello.tokenika*, and you want to develope it basing on the same template as the one used above:
```
$ $teos_cli bootstrap contract hello.tokenika skeleton
#     template contract: /mnt/c/Workspaces/EOS/contracts/hello.tokenika
Code.exe c:\\Workspaces\\EOS\\contracts\\token Will be integrated
```

As the result, you have a new *Visual Studio Code* open in the contracts folder.
You can see a standardized structure of this folder. Open the source file: `hello.tokenika.cpp`. Try the *InteliSense* feature to see the definition of the `print` function:

<img src="VScode/intelisense.png" width="620" />

* There happen errors in any code. Some can be spotted automatically with a compiler. Tasks->Run Task...->compile. The result of the compilation is in the following figure:

<img src="VScode/compile.png" width="620" />

* Let us build the contract. Use Tasks->Run Task...->build. The result of the build process is in the following figure:

<img src="VScode/build.png" width="620" />

* Any contract has to be tested. Use Tasks->Run Task...->unittest. The result of the build process is in the following figure. A lot happened during the test process:
    * Local node started clean;
    * Local wallet was created;
    * EOSIO `eosio.bios` contract was deployed;
    * Cryptographic keys were created
    * An account owning the contract was craeated;
    * Tested contract was deployed;
    * Tested contract was executed;
    * Local node was stopped.

<img src="VScode/unittest.png" width="620" />

* The EOSFactory can more now, and it is going to be able more and more in the near future. Now:
    * All the shown task functionality can be achieved with CMake procedures:
        * build:<br>
        $ cd build; cmake ..; make
        * compile:<br>
        $ cd build; cmake -DC ..; make
        * unittest:<br>
        $ cd build; ctest -V -R ^unittest$
        * test:<br>
        $ cd build; ctest -V -R ^test$
    * EOSFactory has two flavours: `C/C++/Python` and pure `C/C++`. The former one uses tests written in *Python*
    * EOSFactory is going to develop and collect libraries that could facile the process of the development of the EOSIO smart-contracts. Now, we can show one example in action. This is the `logger.hpp` header in the directory `src`. (Of course, it is placed there temporarily.)<br><br>
    The only way to debug a smart contract is by loggers. An example is in the line `logger_info("user: ", name{user});` in the file `src/hello.tokenika.cpp`. The effect fronm this code entry is line `INFO user: carol  @ 8:53:50 hello.tokenika.cpp[16](hi)` of the test results.

    Enjoy.       


