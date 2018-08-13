## /usr/local/bin vs /usr/local/eosio/bin #35

### Q

I had to move the nodeos and cleos binaries over to /usr/local/bin
Can eosfactory be updated to look in /usr/local/eosio/bin for the appropriate 
binaries?

### A

You can see the current configuration. Use a bash terminal:
```
$ $eosf get config
```
Or use a python3 terminal:
```
>>> import teos
>>> ok = teos.GetConfig()
```

You get something like this:
```
#  {
#      "EOSIO_SOURCE_DIR": "/mnt/c/Workspaces/EOS/eos",
#      "EOSIO_EOSFACTORY_DIR": "/mnt/c/Workspaces/EOS/eosfactory",
#      "EOSIO_DATA_DIR": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/",
#      "EOSIO_CONFIG_DIR": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/",
#      "EOSIO_WALLET_DIR": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet/",
#      "KEOSD_WALLET_DIR": "${HOME}/eosio-wallet/",
#      "nodeExe": "/mnt/c/Workspaces/EOS/eos/build/programs/nodeos/nodeos",
#      "cleosExe": "/mnt/c/Workspaces/EOS/eos/build/programs/cleos/cleos",
#      "genesisJson": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json",
#      "EOSIO_DAEMON_ADDRESS": "127.0.0.1:8888",
#      "EOSIO_KEY_PRIVATE": "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
#      "EOSIO_KEY_PUBLIC": "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
#      "EOSIO_WALLET_ADDRESS": "127.0.0.1:8888",
#      "EOSIO_DAEMON_NAME": "nodeos",
#      "EOSIO_WASM_CLANG": "/home/cartman/opt/wasm/bin/clang",
#      "EOSIO_BOOST_INCLUDE_DIR": "/home/cartman/opt/boost/include",
#      "EOSIO_WASM_LLVM_LINK": "/home/cartman/opt/wasm/bin/llvm-link",
#      "EOSIO_WASM_LLC": "/home/cartman/opt/wasm/bin/llc",
#      "sharedMemory": "200",
#      "contractWorkspace": "/mnt/c/Workspaces/EOS/contracts",
#      "workspaceEosio": "/mnt/c/Workspaces/EOS/eos/build/contracts/"
#  }
```
Now, you can change any setting: there is the 'config.json' file in the 'teos' 
folder of the repository. The entries there prevail the default settings.

For example put there the following text:
{
    "EOSIO_DAEMON_ADDRESS": "127.0.0.1:8999"
}

## unittest1-3 fails #36

### Q

### A

EOSIO evolves. 

EOSFactory [v1.1](https://github.com/tokenika/eosfactory/releases/tag/v1.1) is compatible with EOS [v1.0.8](https://github.com/EOSIO/eos/releases/tag/v1.0.8).

Our message in the release notes: 'is compatible with EOS [v1.0.8](https://github.com/EOSIO/eos/releases/tag/v1.0.8) (or higher)' was 
over-optimistic.



## http-server-address cannot be changed #37

### Q jonericcook

When I change http-server-address in the config.ini file, node.reset() still 
starts a node on 127.0.0.1:8888

### Q andresberrios

I think that for the node that eosfactory spins up, you need to edit the eosfactory-specific config.ini file in 
eosfactory/build/daemon/data-dir/config.ini

### A

In fact, there is a configuration system in the EOSFactory, already.

First, you can see the current configuration. Use a bash terminal:
```
$ $eosf get config
```

Or use a python3 terminal:
```
>>> import teos
>>> ok = teos.GetConfig()
```

You get something like this:
```
#  {
#      "EOSIO_SOURCE_DIR": "/mnt/c/Workspaces/EOS/eos",
#      "EOSIO_EOSFACTORY_DIR": "/mnt/c/Workspaces/EOS/eosfactory",
#      "EOSIO_DATA_DIR": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/",
#      "EOSIO_CONFIG_DIR": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/",
#      "EOSIO_WALLET_DIR": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet/",
#      "KEOSD_WALLET_DIR": "${HOME}/eosio-wallet/",
#      "nodeExe": "/mnt/c/Workspaces/EOS/eos/build/programs/nodeos/nodeos",
#      "cleosExe": "/mnt/c/Workspaces/EOS/eos/build/programs/cleos/cleos",
#      "genesisJson": "/mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json",
#      "EOSIO_DAEMON_ADDRESS": "127.0.0.1:8888",
#      "EOSIO_KEY_PRIVATE": "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
#      "EOSIO_KEY_PUBLIC": "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
#      "EOSIO_WALLET_ADDRESS": "127.0.0.1:8888",
#      "EOSIO_DAEMON_NAME": "nodeos",
#      "EOSIO_WASM_CLANG": "/home/cartman/opt/wasm/bin/clang",
#      "EOSIO_BOOST_INCLUDE_DIR": "/home/cartman/opt/boost/include",
#      "EOSIO_WASM_LLVM_LINK": "/home/cartman/opt/wasm/bin/llvm-link",
#      "EOSIO_WASM_LLC": "/home/cartman/opt/wasm/bin/llc",
#      "sharedMemory": "200",
#      "contractWorkspace": "/mnt/c/Workspaces/EOS/contracts",
#      "workspaceEosio": "/mnt/c/Workspaces/EOS/eos/build/contracts/"
#  }
```
Now, you can change any setting: there is the 'config.json' file in the 'teos' 
folder of the repository. The entries there prevail the default settings.

For example put there the following text:
{
    "EOSIO_DAEMON_ADDRESS": "127.0.0.1:8999"
}

Again:
$eosf get config

...


## Support for dictionaries to supply action data #38

### Q
I don't see why the action data should be specified as a JSON string. It would 
be much nicer to write if the data parameters for pushing actions would be 
python dicts that simply get converted to JSON internally before sending to 
cleos. Of course directly writing JSON strings would still be supported.

What do you think?

### A
Thank you for your message. It prompted us to improve the EOSFactory.

The problem is that EOS has their own concept of the JSON: the order of 
items is meaningful for them. (Perhaps, it is still more ridiculous that they
use their original, 4000 lines long, implementation of the std::string.)
Hence, we cannot use the python dict without 'improving' the Python.

But, I agree with the message from you: current implementation is ugly. We 
change it (in the next edition, soon). As it was something like this ...

account_tic_tac_toe.push_action(
    "create", 
    '{"challenger":"' + str(account_alice) 
        +'", "host":"' + str(account_carol) + '"}',
    account_carol)


... now it is like this

account_tic_tac_toe.push_action(
    "create", 
    '''{
        "challenger": "account_alice",
        "host":"account_carol"
    }''',
    account_carol)

Of course, directly writing JSON strings is still supported.

# Documentation Update #40

## Q

I have two questions:

* I was looking to try and list the accounts in the sess.wallet object, but 
couldn't find any documentation on this.
* I tried finding this in the documentation, but maybe I missed it. What is the 
procedure for running unit tests against a smart contract?

## A

In the context of the EOSFactory, the task 'list the accounts' can be specified 
in two ways.

* If you mean the 'get accounts' command of the CLEOS tool, the EOSFactory 
representation is 'cleos.GetAccounts(...)'
```
>>> import cleos
>>> cleos.GetAccounts(account_alice.owner_key)
```
Where 'account_alice` is an account object. The response is like this:
```
{
  "account_names": [
    "cznzipxsl35s"
  ]
}
```
* If you mean the list of the account objects that are referenced in the 
wallet, the wallet object has the method 'restore_accounts(), typically used 
when the wallet starts. Please, forgive us that I quote notation of newest 
edition:
```
>>> import eosf_account
....
>>> eosf_account.wallet_singleton.restore_accounts()
```
The responce is:
```
######### Restored accounts as global variables:
account_carol (cznzipxsl35s)
account_tic_tac_toe (1ja5ifnilhsg)
account_alice (xdmmfyfcatqy)
```

## EOSFactory Testnet Error 
https://eosio.stackexchange.com/questions/1852/eosfactory-testnet-error

Problem results from a change of the nodeos command line arguments.

EOSFactory v1.1 is compatible with EOS v1.0.8.

Our message in the release notes: 'is compatible with EOS v1.0.8 (or higher)' was over-optimistic.

## Can you pls publish a step by step guide on how to set up VS Code to be able 
to debug nodeos?

We were able to debug cleos then, very probably, it is possible to debug nodeos,
as well. However, it has to be difficult and annoying. And even it you start the 
debugger, you will probably be disappointed with what you find out: EOS code 
is over-complicated, spaghetti-like. Additionally, I expect that it crashes if 
it is stopped.

To start, you have to compile EOS in 'debug' mode. You have to change  
'eosio_build.sh' accordingly. 

Also, you have to change the compiler there in 'eosio_build.sh' because there 
is no 'clang' debugger for VS Code for Windows. You have to use the highest 
'gnu' compiler, version 7.

If you have it compiled, please, let me know it, and I will pass you further 
instructions, promptly.

