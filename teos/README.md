# Tokenika TEOS library

## Rationale

Tokenika TEOS library was designed for the Tokenika EOSFactory. The EOSFactory is to be an IDE (Integrated Development Environment) for EOSIO smart-contracts.

From [Wikipedia](#https://en.wikipedia.org/wiki/Integrated_development_environment):

*An integrated development environment (IDE) is a software application that provides comprehensive facilities to computer programmers for software development. An IDE normally consists of a source code editor, build automation tools, and a debugger.*

The TEOS library is the engine that powers these *comprehensive facilities*.

## Walkthrough

Our plan is to build around the [*Visual Studio Code*](#https://code.visualstudio.com/). With VS code, we can have all what we want in one:

    * Linux Mac and Windows compatibility,
    * multi-language (C/C++, Python) support as InteliSense, code browsing,
    * VS code task system,
    * plentifulness of extensions,
    * a room for specialized EOSIO smart-contract IDE extension.

Please, walkthrough the following outline of our IDE.

### Starting with a template

Let you have installed *EOSFactory* according to uor instructions.
Let you have your smart-contract workspace defined, either with the `-w` option of the `eosfactory` installer, or with a corresponding entry in the `config.json` file, for example:
```
{
........................................
    "EOSIO_CONTRACT_WORKSPACE": "/mnt/c/Workspaces/EOS/contracts", 
........................................
}
```
You can start development from a template, for example:
```
$ $EOSIO_TEOS bootstrap contract hello.teos
#  template contract: /mnt/c/Workspaces/EOS/contracts/hello.teos
```
Now, let you open *Visual Studio Code* in the `hello.teos` contract directory. Do `CTR+SHIFT+P`, chose `Open Folder...` browse to the directory. Please, be sure that you have installed the `C/C++` extension to the *VS code*.

### InteliSense and code browsing

Now, you can open `hello.teos.cpp`. With the `C/C++`, you can go to definition/declaration, for example (see the description of te extension for many more): place right mouse over the `print` function name and chose `Pick Declaration`.

### Contract compilation

Not implemented yet.

### EOSIO smart contract API
```
VS code main menu Tasks -> Run Task... -> API
```
opens [Smart Contract API Reference](#https://eosio.github.io/eos/group__contractdev.html).


### Contract build

You can build the contract in two ways: with the *VS code* build task, or with the cmake procedures.

#### *VS code* build task
```
VS code main menu Tasks -> Run Task Build... -> API
```
results in placing WAST and ABI files in the contract build directory:
```
Executing task: /mnt/c/Workspaces/EOS/eosfactory/teos/build/teos/teos generate abi /mnt/c/Workspaces/EOS/contracts/hello.teos;/mnt/c/Workspaces/EOS/eosfactory/teos/build/teos/teos build contract /mnt/c/Workspaces/EOS/contracts/hello.teos <

#              ABI: /mnt/c/Workspaces/EOS/contracts/hello.teos/build/hello.teos.abi
#             WAST: /mnt/c/Workspaces/EOS/contracts/hello.teos/build/hello.teos.wast
```
#### CMake procedures
```
$ cd build
$ cmake ..
.......................
-- Configuring done
-- Generating done
-- Build files have been written to: /mnt/c/Workspaces/EOS/contracts/hello.teos/build
$ make
Scanning dependencies of target abi
[ 50%] Built target abi
Scanning dependencies of target wast
[100%] Built target wast
```

### Contract testing

Not implemented yet. However, please, see the following code snippet showing how contract testing cen be done. It comes from `eosfactory/teos/teos/unittest1.cpp:
```c++
BOOST_AUTO_TEST_CASE(test1)
{
  AccountEosio* eosio;
  Wallet* wallet;
  Key* key_owner; 
  Key* key_active;
  Account* alice;
  Account* bob;
  Account* carol;

  BOOST_REQUIRE(setup(
    eosio, wallet, key_owner, key_active, alice, bob, carol));

  string name = "eosio.token";
  Account account_contract(*eosio, name, *key_owner, *key_active);

  Contract contract(account_contract, name);
  
  BOOST_REQUIRE(contract.deploy());
  BOOST_REQUIRE(contract.push_action(
    "create", 
    R"({"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0})")
  );
  
  BOOST_REQUIRE(contract.push_action(
    "issue", 
    R"({"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"})", eosio));

  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"})", 
    alice));

  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"carol", "to":"bob", "quantity":"13.0000 EOS", "memo":"memo"})", 
    carol));
    
  BOOST_REQUIRE(contract.push_action(
    "transfer", 
    R"({"from":"bob", "to":"alice", "quantity":"2.0000 EOS", "memo":"memo"})", bob));

  BOOST_REQUIRE(
    contract.get_table("accounts", alice).get("rows..balance", "ERROR!") 
      == "77.0000 EOS"
  );
  BOOST_REQUIRE(
    contract.get_table("accounts", bob).get("rows..balance", "ERROR!") 
      == "11.0000 EOS"
  );
  BOOST_REQUIRE(
    contract.get_table("accounts", carol).get("rows..balance", "ERROR!") 
      == "12.0000 EOS"
  );

  teardown(eosio, wallet, key_owner, key_active, alice, bob, carol);
```
In order to see it in action, do
```
$ $EOSIO_CONTEXT_DIR/teos/build/teos/unittest1
```
