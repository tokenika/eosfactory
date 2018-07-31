# Visual Studio Code IDE for EOSIO smart contracts

```md
The ``Visual Studio Code`` is the base upon which we develop the ``EOSFactory``.
Although you can use the Factory with a plain bash terminal, we strongly 
recommend using the VScode instead: it can add new dimensions to your 
experience with the Factory.

For us, the ``EOSFactory`` is about an Integrated Development Environment for
the EOSIO smart contract. Ultimately, in the way that the ``Visual Studio`` is
for almost everything but EOSIO smart contract.
```
## Smart contract templates

```md
The Factory provides smart contract templates that may be a start point for
development of your own task.

For example, you can launch a smart contract named ``eosio_token_better`` 
    * starting with the original EOSIO code of the ``eosio.token``, 
    * with its root at your workspace directory, for example, 
        ``/mnt/c/Workspaces/EOS/contracts`` (if you omit the workspace directory 
        argument, this one set with the installation of the Factory will 
        be used)

If you have the VScode installed, use a bash terminal, it can be one belonging 
to an instance of the VScode: 
```
```md
$ $eosf template create eosio_token_better eosio.token\
    --workspace /mnt/c/Workspaces/EOS/contracts --vsc
```
```md
We hope that now you see an instance ot the VScode window.
```
## IDE workspace

```md
If cannot find in the workspace anything that you need for your work, we will 
try to add it in the next editions. Now, you can see the following items.

    * ``src`` directory, the cpp and hpp files are there.
    * ``test`` directory, test scripts are there.
    * ``resources`` directory, everything that does not fit to the previous two
        goes there. Now, it contains the Recardian contract files.
    * ``.vscode`` directory that contains intelisense definitions, task 
        definitions, etc.
    * ``CMakeLists.txt`` file, CMake definitions.

Also, you can see the ``Tasks`` dialog window:

    * ``Build`` results in building the contract, resulting ``ABI`` and ``WAST``
        files go to the ``build`` directory.
    * ``Compile`` results in compilation of the contract, without building
        (neither ``ABI`` nor ``WAST`` are produced), but code errors, if any,
        are listed.
    * ``EOSIO API`` results in opening (in the default browser) of the EOSIO
        manual.
    * ``Test`` - executes the ``test1`.py`` script.
    * ``Unittest`` - executes the ``unittest1`.py`` script.

Note that you can edit the literals. For example, if you change the test
name ``test1``, you have to update both ``CMakeLists.txt`` and 
``.vscode/tasks.json`` files.
```

<img src="ide/workspace.png" 
    onerror="this.src='../../../source/cases/ide/workspace.png'"   
    alt="smart contract IDE workspace" width="720px"/>

## Working on the code

```md
The VScode provides the intelisense and easy access to the context. Especially,
you can inspect any context code. The list of services is:
    * Go to Definition.
    * Pick Definition.
    * Go to Declaration.
    * Pick Declaration.

In the image below, you cen see a result of the ``Pick Definition`` service. 
```

<img src="ide/pick_definition.png" 
    onerror="this.src='../../../source/cases/ide/pick_definition.png'"   
    alt="eosio token contract" width="720px"/>

<img src="ide/cmake_build.png" 
    onerror="this.src='../../../source/cases/ide/cmake_build.png'"   
    alt="eosio token contract" width="720px"/>

<img src="ide/cmake_unittest.png" 
    onerror="this.src='../../../source/cases/ide/cmake_unittest.png'"   
    alt="eosio token contract" width="720px"/>

<img src="ide/logger.png" 
    onerror="this.src='../../../source/cases/ide/logger.png'"   
    alt="eosio token contract" width="720px"/>