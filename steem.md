# Introducing *EOSFactory* smart-contract framework

[EOS Factory](http://eosfactory.io/) is a smart-contract development framework, created by [Tokenika](https://tokenika.io). Our aim is to offer a similar functionality to Ethereum's [Truffle Framework](http://truffleframework.com/).

This is our ultimate goal: using a single command-line interface within an IDE you'll be able to create a private testnet and then compile, unit-test and deploy EOS smart-contracts. 

*EOSFactory* is tightly integrated with the [Visual Studio Code](https://code.visualstudio.com) IDE. This will allow you to write EOS smart-contracts, play with them and then perform proper unit-testing, all within one robust IDE.

### Cross-platform compatibility

We make sure everything we do is fully compatible with any major operating system, including Windows. Thus our toolset will enable you to run an EOS node and interact with it on Windows 10 - as far as we know no other EOS development solution is able to offer that.

### Architecture

In *EOSFactory* you use Python to interact with your smart-contracts. However under the hood our toolset is powered by C++. 

Thus *EOSFactory* is composed of two layers:

- C++ bridge called `teos` connected to an EOS node running a private testnet
- Python wrapper called `pyteos` acting as a convenient human-oriented interface

### Smart-contract development cycle

This is what the development cycle might look like:

* You write a smart-contract.
* You compile your smart-contract.
* You start a fresh single-node testnet.
* You deploy your smart-contract.
* You run unit-tests.
* You tear down the testnet.

All the above is done using Python - of course apart from the task of writing smart-contracts  And everything works within Visual Studio Code IDE.

### Python-based unit-testing

This is what a simple unit test could look like in *EOSFactory*:

```
c = Contract("eosio.token")
c.deploy()

c.push("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}')

c.push("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', s.eosio)

c.push("transfer", '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"}', s.alice)

c.push("transfer", '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", "memo":"memo"}', s.carol)

c.push("transfer", '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", "memo":"memo"}', s.bob)

t1=c.get("accounts", s.alice)
t2=c.get("accounts", s.bob)
t3=c.get("accounts", s.carol)

assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
assert t3.json["rows"][0]["balance"] == '12.0000 EOS'

print("Test OK")
```

And this is the output you receive when running it:

```
#  nodeos exe file: /mnt/d/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#  genesis state file: /mnt/d/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json
#   server address: 127.0.0.1:8888
#  config directory: /mnt/d/Workspaces/EOS/eosfactory/build/daemon/data-dir
#  wallet directory: /mnt/d/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet
#  head block number: 0
#  head block time: 2017-12-04T01:00:00

#         password: PW5Jpe2U2D8HwXgZ89NrNYmZEzXiQY7KZa4hQ2FaKeqB7UyKzTggg
#  You need to save this password to be able to lock/unlock the wallet!

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

* EOSFactory repository
* Installing EOSFactory
* Interacting with EOS Contracts in EOSFactory
* Compiling EOS Contracts in EOSFactory
* Unit-testing EOS Contracts in EOSFactory

### The roadmap

*EOSFactory* is still under development. What we present today is just a quick preview. We plan to release it before June 2018.

