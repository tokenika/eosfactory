# Welcome to EOSFactory

[EOSFactory](http://eosfactory.io/) is a smart-contract development framework, created by [Tokenika](https://tokenika.io).

The goal is to achieve a similar functionality to Ethereum's [Truffle Framework](http://truffleframework.com/).

Using a single command-line interface you can create a private testnet and then compile, unit-test and deploy [EOS](https://eos.io/) smart-contracts.

All of this using simple yet powerful [Python3](https://www.python.org/) syntax.

## Why it’s needed?

Everything that EOSFactory offers can be done with the the official EOS toolset, i.e. `cleos` and `eosiocpp`. Is EOSFactory just another tool like that? Not really.

Code development and unit-testing involve tasks that need to be  executed hundreds of times, and each time in exactly the same way and in  the exactly the same context. Therefore those tasks need to be fully  automated, as otherwise a lot of time is being wasted and, what’s even  worse, a lot of additional uncertainty is introduced. Manually performed  actions are prone to errors.

And this is what EOSFactory actually brings to the table: an easy  & intuitive way to automate the process of dealing with  smart-contracts. Write down, in the form of a Python script, what needs  to be done multiple times in exactly the same way and in exactly the  same context, and then just run the script. EOSFactory will take care of  everything else: it will compile your smart-contract, create a new  testnet, deploy the contract, invoke its methods and verify the  response, then tear down the testnet, and finally report the results.  And all of this done in a couple of seconds.

## Main features

### Object-oriented

When you use tools like `cleos` all you have at your disposal is issuing separate, one-off commands, as `cleos` is not able to keep your state. Thus each time you interact with a contract, you need to tell `cleos`  which contract and which account you mean. Contrary to that, in  EOSFactory everything is an object. You create a contract (or an  account), keep reference to it and then invoke its various methods.

### Simple syntax

The front-end of EOSFactory is simply a Python3 Command Line  Interface. This way you can interact with EOS smart-contract, and prove  it works as expected, without having to deal with the complexity of a  low-level language like C++. In most cases Python’s syntax is clear for  everyone.

### Real testnet

As EOS full node is very quick we don’t need to rely on a testnet simulator similar to [TestRPC](https://github.com/trufflesuite/ganache-cli)  in Ethereum. Instead, we can work with a real testnet and this makes  unit-tests much more reliable. Thus EOSFactory has the ability to launch  and tear down an EOS testnet in a very efficient way, so that you can  fully test your smart-contract in a couple of seconds and do it multiple  times.

## Truly cross-platform

We make sure everything we do is fully compatible with Windows - our toolset enables you to run an EOS node and interact with it on any operating system, including Windows, MacOS and Linux.

## Architecture

EOSFactory is composed of two layers:
- C++ bridge connected to an EOS node running a private testnet
- Python wrapper acting as a convenient human-oriented interface

Using Python will allow us to build [interactive tutorials](http://eosfactory.io/sphinx/build/html/) for EOS smart-contracts.

## User documentation

* [Introduction to EOSFactory](http://eosfactory.io/sphinx/build/html/00.IntroductionToEOSFactory.html)
* [Installing EOSFactory](http://eosfactory.io/sphinx/build/html/01.InstallingEOSFactory.html)
* [Interacting with EOS Contracts in EOSFactory](http://eosfactory.io/sphinx/build/html/02.InteractingWithEOSContractsInEOSFactory.html)
* [Compiling EOS Contracts using EOSFactory in VSC](http://eosfactory.io/sphinx/build/html/03.CompilingEOSContractsUsingEOSFactoryInVSC.html)
* [Unit-testing EOS Contracts using EOSFactory in VSC](http://eosfactory.io/sphinx/build/html/04.UnitTestingEOSContractsUsingEOSFactoryInVSC.html)

## Developer documentation

Please refer to [this index of Python modules](http://eosfactory.io/sphinx/build/html/py-modindex.html) which constitute the front-end of EOSFactory.

## Roadmap

EOSFactory is currently at an MVP stage. It was initially released in May 2018 and there are subsequent releases to be expected in the near future.
