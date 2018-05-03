# Introducing *EOSFactory* - an EOS smart-contract development framework

![Huta-Szkla-Julia-111.jpg](https://steemitimages.com/DQma9A6x8WFLDDtQrGgJ2o9Mma1apHGfjFH1mY9PdKYvGLn/Huta-Szkla-Julia-111.jpg)

[EOS Factory](http://eosfactory.io/) is a smart-contract development framework, created by [Tokenika](https://tokenika.io). We want to offer a similar functionality to Ethereum's [Truffle Framework](http://truffleframework.com/).

**Our ultimate goal is this: using a simple command-line interface within a single IDE you'll be able to launch a private testnet and then compile, unit-test and deploy EOS smart-contracts.**

*EOSFactory* works nicely with [Visual Studio Code](https://code.visualstudio.com). This will allow you to write EOS smart-contracts, play with them and then perform proper unit-testing, all within one robust IDE.

### Cross-platform compatibility

We make sure everything we do is fully compatible with any major operating system, including Windows. Thus our toolset will enable you to run an EOS node and interact with it on Windows 10. As far as we know, no other EOS development solution is able to offer that.

### Architecture

In *EOSFactory* you use Python to interact with your smart-contracts. However, under the hood our toolset is powered by C++.

Thus *EOSFactory* is composed of two layers:

- C++ bridge called `teos` connected to an EOS node running a private testnet,
- Python wrapper called `pyteos` acting as a convenient human-oriented interface.

In other words, we have Python outside, while C++ inside.

### Development cycle

This is what the smart-contract development cycle might look like:

1. Write a smart-contract (in C++).
2. Write unit-tests (in Python).
3. Compile your smart-contract.
4. Start a fresh single-node testnet.
5. The testnet is initialized with the *Bios* contract and a couple of test accounts to play with.
6. Deploy your smart-contract.
7. Run your unit-tests.
8. Tear down the testnet.
9. Modify your smart-contract and/or unit-tests and jump to stage 3.

In *EOSFactory* every step of the above process is fully automated by Python classes and methods - you, as a developer, only supply the creative part, i.e. the content of the smart-contracts and unit-tests. Unit-tests are designed to be written in Python, while of course smart-contracts are written in C++. Visual Studio Code perfectly supports both those languages.

### Object-oriented vs. procedural

Thanks to Python, what you are dealing with in *EOSFactory* are classes and objects. For example, a smart-contract is an object, and you handle it by using its methods, e.g. `contract.compile()`, `constract.deploy()`, `contract.push()` to push actions, and `contract.get()` to extract data from its tables. This is the opposite of procedural commands used in `cleos`, the official CLI for EOS.

### Python-based unit-testing

This is what a simple unit test might look like in *EOSFactory*:

```
c = Contract("eosio.token")
c.deploy()

c.push("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}')

c.push("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', eosio)

c.push("transfer", '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"}', alice)

c.push("transfer", '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", "memo":"memo"}', carol)

c.push("transfer", '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", "memo":"memo"}', bob)

t1=c.get("accounts", alice)
t2=c.get("accounts", bob)
t3=c.get("accounts", carol)

assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
assert t3.json["rows"][0]["balance"] == '12.0000 EOS'

print("Test OK")
```

And this is the output you receive after running it:

```
#  nodeos exe file: /mnt/d/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#  genesis state file: /mnt/d/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json
#   server address: 127.0.0.1:8888
#  config directory: /mnt/d/Workspaces/EOS/eosfactory/build/daemon/data-dir
#  wallet directory: /mnt/d/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet
#  head block number: 0
#  head block time: 2017-12-04T01:00:00

#         password: PW5Jpe2U2D8HwXgZ89NrNYmZEzXiQY7KZa4hQ2FaKeqB7UyKzTggg

#   transaction id: c9dd03ad7329b989d808b0022a87a1281215406778599e82c7b80da978d9d2e3

#         key name: key_owner
#      private key: 5HzFMEvvxqDzFdTtDWLSk4h4wfLX242oefLWQiKtB4yCoibzrVN
#       public key: EOS6C4RpBVmXQV1jDU32chZSYdCCX7mShKLrWeU8yerSMWBYTDbGu

#         key name: key_active
#      private key: 5KiB6GeF68WfFwoSYcJSxsceRz6rkjUujJ9o8fSjxvNL7e6Mqpt
#       public key: EOS5fkdAoYvacFotu4pK2tQ4wHK3Fx2sAuPyzZfFS4yDNrY6iT7aD

#   transaction id: b9129c757cc7967f2c630df1de1b669fae6d63cd5174f09068880c39245d4ba9

#   transaction id: 5c818883604be2971fc44f89c30106818ab00957e38c21f16fb0a0d2ac0ad600

#   transaction id: eb15db310b3821a3f84ce39ef5f8d9dd046623b17d93e16b3d7d1d747879158f

#         key name: key_owner
#      private key: 5KAjZovyFjaPzSVLSpUAcHjJPtrCYgEG4c9L29rAv5pQnmkjGEA
#       public key: EOS64rdurm2WkRMeSZuTEVf1LAqcQ71azzkT24E29gfFjAPpUcjkQ

#         key name: key_active
#      private key: 5JBWhJbTS7YH7ESfDM3uQ6yKgm9WzP8L6utSFAnAWdVURECqmYA
#       public key: EOS8i9wu4SYhvA1SLAXMGchqXvPENnKLVPXM5BwWKHuZ7KARbAHTq

#   transaction id: 726e158f9688d0695644a1d48a0501209f6251a54bad12389cc4e473901fcb51

#   transaction id: 06147a1ab90ffde760ed76b9428ad85b14c7b7fd2b12525eb6f9dc23f79f82ec

#   transaction id: 18fc0413baf67b6209959de710030e81fd14e433fc5b505e685dabae154b66dc

#   transaction id: 314bd2df50fd46585797b4d7521a78a746cf5cb19388bbd7f6d535594e12d77b

#   transaction id: e2942f1bea72c2a69335dc96e54a9f7fb31ab146ab853b1369c41ecde8d2b7f3

#   transaction id: b1c8f14a2f1c897597f51f129d64804aeb301565dd89d1cf3655b678bbe9c0d3

#   transaction id: 3ede831bf1b7c05c8828f96f024862f13fdf943d9fb3ef28d76eb86eeacfaf77

#  {
#      "rows": [
#          {
#              "balance": "77.0000 EOS",
#              "frozen": "0",
#              "whitelist": "1"
#          }
#      ],
#      "more": "false"
#  }
#

#  {
#      "rows": [
#          {
#              "balance": "11.0000 EOS",
#              "frozen": "0",
#              "whitelist": "1"
#          }
#      ],
#      "more": "false"
#  }
#

#  {
#      "rows": [
#          {
#              "balance": "12.0000 EOS",
#              "frozen": "0",
#              "whitelist": "1"
#          }
#      ],
#      "more": "false"
#  }
#

Test OK
#  Daemon is stopped.
```

### Documentation

You'll find the source code of *EOSFactory* in [this repository](https://github.com/tokenika/eosfactory).

And here is a list of available documentation:

* Installing EOSFactory
* Interacting with EOS Contracts in EOSFactory
* Compiling EOS Contracts in EOSFactory
* Unit-testing EOS Contracts in EOSFactory

### The roadmap

*EOSFactory* is still under development. What we present today is just a quick preview. 

Right now we are working on the following features:

* Firstly, we want to build a robust mechanism for creating and managing unit-tests. They will be stored as a hierarchy of Python files, in a similar way the process is organized in Ethereum's [Truffle Framework](http://truffleframework.com/) - we just use Python instead of JavaScript. Also, we plan to add support for other IDEs, e.g. [Eclipse](https://www.eclipse.org/ide/).
* Secondly, we are considering the pros and cons of connecting our Python layer directly to `cleos`, the official EOS CLI. When we started working on *EOSFactory*, `cleos` (at that time named `eosc`) was in a bad shape and thus not suitable for our needs, so we had to build our own C++ interface to an EOS node. Currently, it might be the case that we could simplify our approach by relying on `cleos`.
* And finally, we are thinking about integrating *Ricardian Contracts* into our unit-testing. This is a very interesting (and probably not widely known at this stage) aspect of EOS smart-contracts. For more information please refer to [EOSIO documentation](https://github.com/EOSIO/eos/wiki/Tutorial-Hello-World-Contract#hello-world-ricardian-contract).

We plan to have a next release of *EOSFactory* in a couple of weeks, ideally before EOS is launched.

Any feedback, especially critical, is very welcome.

---

`Image source: hutajulia.com`