# Tokenika TEOS library

## Rationale

Tokenika TEOS library was designed for the Tokenika EOSFactory. The EOSFactory is to be an IDE (Integrated Development Environment) for EOSIO smart-contracts.

*An integrated development environment (IDE) is a software application that provides comprehensive facilities to computer programmers for software development. An IDE normally consists of a source code editor, build automation tools, and a debugger.* [ (from Wikipedia)](#https://en.wikipedia.org/wiki/Integrated_development_environment)

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

Let you have installed *EOSFactory* according to our instructions.
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
$ $teos_cli bootstrap contract hello.teos
#  template contract: /mnt/c/Workspaces/EOS/contracts/hello.teos
```
Now, let you open *Visual Studio Code* in the `hello.teos` contract directory. Do `CTR+SHIFT+P`, chose `Open Folder...` (or `#+SHIFT+P` chose `Open...` with Mac), browse to the directory. Please, be sure that you have installed the `C/C++` extension to the *VS code*.

### InteliSense and code browsing

Now, you can open `hello.teos.cpp`. With the `C/C++`, you can go to definition/declaration, for example (see the description of te extension for many more): place right mouse over the `print` function name and chose `Pick Declaration`.

### Contract compilation

$teos_cli bootstrap contract hello.teos
```
VS code main menu Tasks -> Run Task... -> compile
```
You can see an error report, if they are compile errors. Linking is not executed.

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

Not implemented yet. 

However, please, see the following code snippet showing how contract testing can be done. We support two flavors *C++* and *Python*.

#### C++ example 

The example comes from from `eosfactory/teos/teos/unittest1.cpp`:
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
$ $EOSIO_EOSFACTORY_DIR/teos/build/teos/unittest1
```

#### Python example

Python example comes from `eosfactory/tests/unittest1.cpp`:

```Python
class Test1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
    def setUp(self):
        pass

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
    
    def test_00_node_reset(self):
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")
        self.assertTrue(node.reset(), "node reset")
        self.assertTrue(sess.setup(), "session setup")

    def test_01_contract(self):
        c = eosf.Contract("eosio.token")
        self.assertFalse(c.error, "Contract")

        self.assertTrue(c.get_code(), "get_code")
        self.assertTrue(c.deploy(), "deploy")
        self.assertTrue(c.get_code(), "get_code")

        self.assertTrue(
            c.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}'), 
            "push_action create")

        self.assertTrue(
            c.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"issue 100.0000 EOS"}', 
            sess.eosio), 
            "push_action issue")

        self.assertTrue(
            c.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
                "memo":"transfer 25.0000 EOS"}', 
            sess.alice), 
            "push_action transfer")

        x = c.push_action(
            "transfer", 
            '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", \
                "memo":"transfer 13.0000 EOS"}', 
            sess.carol)
        self.assertTrue(x, "push_action transfer")
        
        self.assertTrue(
            c.push_action(
            "transfer", 
            '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", \
                "memo":"transfer 2.0000 EOS"}', 
            sess.bob), 
            "push_action transfer")

        t1 =  c.get_table("accounts", sess.alice)
        self.assertFalse(t1.error, "get_table alice")
        t2 = c.get_table("accounts", sess.bob)
        self.assertFalse(t2.error, "get_table bob")
        t3 = c.get_table("accounts", sess.carol)
        self.assertFalse(t2.error, "get_table carol")

        self.assertEqual(
            t1.json["rows"][0]["balance"], "77.0000 EOS")
        self.assertEqual(
            t2.json["rows"][0]["balance"], "11.0000 EOS")
        self.assertEqual(
            t3.json["rows"][0]["balance"], "12.0000 EOS")


    def test_99_node_stop(self):
        x = node.stop()
        self.assertTrue(x)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        s = node.stop()
```
In order to see it in action, do
```
$ python3 $EOSIO_EOSFACTORY_DIR/tests/unittest1.py
```

## Library structure

The library has three layers:
  * raw basic operation classes, for example GetInfo, DaemonStart, BuildContract;
  * command-line drivers for the basic operations, for example GetInfoOptions, DaemonStartOptions;
  * EOSIO notion abstraction classes like Account, Contract, Wallet.

### Command-line drivers

The command-line drivers, operated by the main `teos` application, mimic and/or extend *EOSIO cleos*, but they are limited in their functionality to the needs of our smart contract IDE. They are not going to replace  *EOSIO cleos* as a client to a remote EOSIO node. 

However, *Tokeniks teos* can play with a local node. For example, the following sequence of bash commands make sense:

```
$ $teos_cli bootstrap contract hello.teos     ## new contract template
#  template contract: /mnt/c/Workspaces/EOS/contracts/hello.teos

$ $teos_cli build contract hello.teos ## relative to the workspace
#  WAST: /mnt/c/Workspaces/EOS/contracts/hello.teos/build/hello.teos.wast

$ $teos_cli generate abi hello.teos ## relative to the workspace
#  ABI: /mnt/c/Workspaces/EOS/contracts/hello.teos/build/hello.teos.abi

$ $teos_cli daemon start -c                   ## reset local node
#  nodeos exe file: /mnt/c/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#  genesis state file: 
  /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json
#   server address: 127.0.0.1:8888
#  config directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir
#  wallet directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet
#  head block number: 3
#  head block time: 2018-05-23T16:02:40

$ $teos_cli wallet create
#         password: PW5K5jzJZaCXEtrwThSgPjgSjiZj8d9i1fCGZSUM7ZC9XEUySarnD
#  You need to save this password to be able to lock/unlock the wallet!

$ $teos_cli set contract eosio hello.teos --permission eosio
#   transaction id: 
  ef2744011c17b219f346c2841ebc316c0ebd21da9804ec804c860f71558481ba

$ $teos_cli create key owner
#         key name: owner
#      private key: 5J5Th3pDjjhkvwiPSETfqoSPp95APj8y7RaaghHtfq7UMUjy3Xa
#       public key: EOS6GKYMgKHeuMAaHb3v4nGBg9NiYRcJoU3YegUYeUwSjUfSJWLdP

$ $teos_cli create key active
#         key name: active
#      private key: 5Jq3guBccY52bw7h3qTTLUHMvg99vx6qDTtyGN7LQrL68nQzszQ
#       public key: EOS7gnfsg5ZiS9wfGUJah18Dmkq4aXz7gQDTcmcFKtV9tMuhB5AeA

$ $teos_cli wallet import default \
  5J5Th3pDjjhkvwiPSETfqoSPp95APj8y7RaaghHtfq7UMUjy3Xa
#           wallet: default
#     key imported: 5J5Th3pDjjhkvwiPSETfqoSPp95APj8y7RaaghHtfq7UMUjy3Xa

$ $teos_cli wallet import default 
  5Jq3guBccY52bw7h3qTTLUHMvg99vx6qDTtyGN7LQrL68nQzszQ
#           wallet: default
#     key imported: 5Jq3guBccY52bw7h3qTTLUHMvg99vx6qDTtyGN7LQrL68nQzszQ

$ $teos_cli create account eosio hello.teos \
  EOS6GKYMgKHeuMAaHb3v4nGBg9NiYRcJoU3YegUYeUwSjUfSJWLdP \
    EOS7gnfsg5ZiS9wfGUJah18Dmkq4aXz7gQDTcmcFKtV9tMuhB5AeA \
#   transaction id: 
  0ff62a96bde5bd911da135557da56fabb3fc1282d8be8797be485aafa519bce4

$ $teos_cli set contract hello.teos hello.teos
#   transaction id: 
  2820976a76893685f4cfc2578c7c0f0ff3e8b9112732de202dab16afd7b56884

$ $teos_cli push action hello.teos hi '["hello.teos"]' -p hello.teos
#   transaction id: 
  bdbace3b4327f70ccc7d63d1b1287a7abbec4240be9b2d7695192bf80da45f92
#  INFO account name: 7684013990126944256  @ 17:56:15 hello.teos.cpp[16](hi)
#  Hello, hello.teos

$ $teos_cli daemon stop
#  Daemon is stopped.
```

This command-line drivers to the basic operation classes power the Python implementation of the  EOSIO abstraction classes.

### C++ EOSIO abstraction classes

The abstraction classes are intent for writing of C++ tests for smart contracts. They make an alternative to the use of the *Tokenika pyteos classes*.

