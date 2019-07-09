============================
Welcome to EOSFactory v3.4.0
============================

`EOSFactory <http://eosfactory.io/>`_ is a Python-based `EOS <https://eos.io>`_ smart-contract development & testing framework, created by `Tokenika <https://tokenika.io>`_.

With a single command-line interface you can create a private testnet and then compile, test and deploy EOS smart-contracts.

All of this using intuitive yet powerful `Python <https://www.python.org/>`_ syntax.

Why it’s needed?
----------------

Code development and testing involve tasks that need to be executed hundreds of times, and each time in exactly the same way and exactly the same context. Therefore those tasks need to be fully automated, as otherwise a lot of time is being wasted and, what’s even worse, a lot of additional uncertainty is introduced. Manually performed actions are prone to errors.

And this is what *EOSFactory* actually brings to the table: an easy & intuitive way to automate the process of dealing with smart-contracts. Write down, in the form of a Python script, what needs to be done multiple times in exactly the same way and exactly the same context, and then just run the script. *EOSFactory* will take care of everything else: it will compile your smart-contract, create a new local testnet, deploy the contract, invoke its methods and verify the response, then tear down the testnet, and finally report the results. And all of this done in a couple of seconds.

Main features
-------------

Object-oriented
^^^^^^^^^^^^^^^

When you use tools like `cleos` all you have at your disposal is issuing separate, one-off commands, as `cleos` is not able to keep your state. Thus each time you interact with a contract, you need to tell `cleos` which contract and which account you mean. Contrary to that, in *EOSFactory* everything is an object. You create a contract (or an account), keep reference to it and then invoke its various methods.

Simple syntax
^^^^^^^^^^^^^

The front-end of *EOSFactory* is simply a Python3 *Command Line Interface*. This way you can interact with EOS smart-contract, and prove it works as expected, instead having to deal with the raw primitives of the EOSIO `cleos`. In most cases Python syntax is immediately clear for everyone.

Support for both local and remote testnet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running tests on a public testnet is much more complex than using a local one where you have full control. The whole infrastructure of *EOSFactory* is designed in such a way that the same test is able to work in both environments, and switching between them is just a matter of changing one parameter.

Aliases for account names
^^^^^^^^^^^^^^^^^^^^^^^^^

*EOSIO* accounts are indexed by their names, thus those names have to be unique within the blockchain namespace and have to follow specific restrictions. As a result, most of the human readable combinations are already taken, even in a testnet environment. *EOSFactory* hides the actual names of an *EOSIO* accounts behind a system of human-friendly aliases.

Truly cross-platform
^^^^^^^^^^^^^^^^^^^^

We make sure everything we do is fully compatible with Windows - our toolset enables you to run an EOS node and interact with it on any operating system, including Windows, MacOS and Linux. 

User documentation
------------------

* `Introduction to EOSFactory <http://eosfactory.io/build/html/tutorials/00.IntroductionToEOSFactory.html>`_
* `Installing EOSFactory <https://eosfactory.io/build/html/tutorials/01.InstallingEOSFactory.html>`_
* `Interacting with EOS Contracts in EOSFactory <https://eosfactory.io/build/html/tutorials/02.InteractingWithEOSContractsInEOSFactory.html>`_
* `Building and deploying EOS Contracts in EOSFactory <https://eosfactory.io/build/html/tutorials/03.BuildingAndDeployingEOSContractsInEOSFactory.html>`_
* `Working with EOS Contracts using EOSFactory in VSC <https://eosfactory.io/build/html/tutorials/04.WorkingWithEOSContractsUsingEOSFactoryInVSC.html>`_
* `Interacting with Public Testnet <https://eosfactory.io/build/html/tutorials/05.InteractingWithPublicTestnet.html>`_

Use cases
---------

* `Wallet Class <https://eosfactory.io/build/html/cases/wallet.html>`_
* `Symbolic Names <https://eosfactory.io/build/html/cases/symbolic_names.html>`_
* `Account Class <https://eosfactory.io/build/html/cases/account.html>`_
* `Master Account <https://eosfactory.io/build/html/cases/master_account.html>`_

Complete documentation
----------------------

Please refer to the `table of contents <https://eosfactory.io/build/html/index.html>`_.


Roadmap
-------

Our final goal is to turn *EOSFactory* into a comprehensive IDE (Integrated Development Environment) for EOS smart-contracts.

Support
-------

For issues not covered in the documentation there is a dedicated `EOS Factory Support <https://t.me/EOSFactorySupport>`_ channel on Telegram.

Licence
-------

This code is provided as is, under MIT Licence.
