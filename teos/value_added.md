# What's the value added of EOSFactory?

## Dealing with the `Hello World` smart-contract

The `Hello World` smart-contract is very simple. It's explained in [*Tutorial Hello World Contract*](https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract).

Let us go through the tutorial:

* Create a new folder called `hello`, switch to this folder, then create a file `hello.cpp` with the following content:

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

* Compile the code to the Web Assembly `wast` format:

   ```
   $ eosiocpp -o hello.wast hello.cpp
   Build hello.wast
   ```

* Now, generate an `ABI` file:

   ```
   $ eosiocpp -g hello.abi hello.cpp
   Generated hello.abi
   ```

* Create an account and upload the contract:

   ```
   $ cleos push action hello.code hi '["user"]' -p user
   executed transaction: 4c10c1426c16b1656e802f3302677594731b380b18a44851d38e8b5275072857  244 bytes  1000 cycles
   #    hello.code <= hello.code::hi               {"user":"user"}
   >> Hello, user
   ```

* Open the `hello.cpp` file in your favorite editor and modify the `hi()` function in `hello.cpp` as follows:

   ```
   void hi( account_name user ) {
      require_auth( user );
      print( "Hello, ", name{user} );
   }
   ```

* Recompile your code to the Web Assembly `wast` format:

   ```
   $ eosiocpp -o hello.wast hello.cpp
   Build hello.wast
   ```

* Regenerate the `ABI` file:

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

And so on. It is simple stuff, but you need to be very careful to issue the right commands, and not to confuse any of the cryptographic keys.

## Integrated Development Environment (IDE)

What we are delaing with right now are simple demos. However, development of real-life smart-contracts is likely to be complex: most probably it's going to be a long sequence of trial-and-error events involving the source code being tested against a local *EOSIO* node.

That's why using a robust IDE seems to be crucial here. The main purpose of on an IDE is to automate everything that does not require creative thinking. Ideally, all what should be left to the coder is the buisness logic of the smart-contract.

## EOSFactory aims be a comprehensive IDE for EOS smart-contracts

EOSFactory is under development itself, but already we can see its potential in action, provided you have both EOSFactory and *Visual Studio Code* (VSC) installed on your machine.

* Create a new smart-contract project named `hello.tokenika`:

   ```
   $ $eosf bootstrap contract hello.tokenika skeleton --vsc
   #     template contract: /mnt/c/Workspaces/EOS/contracts/hello.tokenika
   ```

   As a result, a new *Visual Studio Code* project is created and launched. You'll notice its standardized structure and clear division betweem source files, builds and unit tests.

* To play with it, open the `hello.tokenika.cpp` file and try the *InteliSense* feature to see the definition of the `print` function:

![intelisense](VScode/intelisense1.png)

* Obviousely you'll be dealing with lots of errors in any code. Some can be spotted automatically with a compiler. Try `Tasks -> Run Task -> Compile` to invoke the `CLANG` compiler. This is the output you should get:

![compile](VScode/compile1.png)

* Now, Let's build the contract with the `WASM` compliler. For that use `Tasks -> Run Task -> Build`. The result of the build process should look like this:

![build](VScode/build1.png)

* Any contract has to be tested. Use `Tasks -> Run Task -> Unittest`. 
    A lot happened during the test process:
    * A local *EOSIO* testnet has been started.
    * Local wallet has been created.
    * *EOSIO* `eosio.bios` contract has been deployed.
    * Cryptographic keys have been created.
    * An account owning the contract has been created.
    * The contract has been deployed and then executed as part 
      of the unit test.
    * The local testnet has been stopped and torn down.

  This is the output you should get:

![unittest](VScode/unittest1.png)

* EOSFactory can more now, and it is going to be able more and more in the near future. Now:

   All the shown task functionality can be achieved with CMake procedures:
   * build:<br>
     $ cd build; cmake ..; make

   * compile:<br>
     $ cd build; cmake -DC ..; make

   * unittest:<br>
     $ cd build; ctest -V -R ^unittest$

   * test:<br>
     $ cd build; ctest -V -R ^test$

* EOSFactory has two flavours:

   *  `C/C++/Python` (using unit tests written in Python)
   * pure `C/C++` (no Python used, everything is in C/C++)

* As EOSFactory grows, it will include further libraries that could facilitate the process of smart-contract development.<br>
  Here we present one of such features in action: the logging tool. It's quite important, as the only way to debug a smart contract is actually by using loggers.<br>
  You'll notice the `logger.hpp` header file in the `src` directory. And in the `hello.tokenika.cpp` file you'll notice this line:<br>
  <code>&nbsp;&nbsp;&nbsp;&nbsp;logger_info("user: ", name{user});</code><br>
  The effect of the above code entry is the following output in test results:<br>
  <code>&nbsp;&nbsp;&nbsp;&nbsp;INFO user: carol @ 8:53:50 hello.tokenika.cpp\[16](hi)</code><br>
  What that means is that the logger offers you not only the value of a variable, but also the exact line number and the file name where this logger event occured.