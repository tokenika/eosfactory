'''
# Arguments

This file can be executed as a python script: 'python3 arguments.md'.

Arguments of the EOSFactory statements are polymorphic. For example, a 
'permission` argument can have the following forms:

    * <account object>
    * <the name of an account object>
    * (<account object>, <permission level>), that is a tuple of two items
    * <the name of an account object>@<permission level>
    * [(<account object>, <permission level>), ...] that is a list of tuples
    * combinations of the above

The polymorphism results from the origin of the EOSFactory, started as a wrapper 
for the 'CLEOS' commands. We have not decided yet, whether it is a value: a 
disadvantage is that type errors are not detected by the compiler. An advantage 
may be that users like it.

## Setup

The set-up statements are explained at <a href="setup.html">cases/setup</a>.

Local test node reset, wallet started, master account object created:

```md
'''
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT]

CONTRACT_DIR = "02_eosio_token"

reset([Verbosity.INFO]) 
create_wallet()
account_master_create("account_master")
'''
```
## Case

### Account arguments

Accounts are represented either as blockchain names or as account objects. In
the following test, the 'account_master' object enters, at first, as itself ...

```md
'''
account_create("alice", account_master)
'''
```

... next, the 'account_master' is represented as a string, 'eosio` in this case:

```md
'''
account_create("bob", str(account_master))
'''
```

If an account argument is neither an account object nor a string, an error 
message is printed, or an error exception is thrown. For example, let the 
account argument be of the 'CreateKey' type:

```md
'''
set_throw_error(False)

account_create("jimmy", CreateKey("xxx", is_verbose=0))

set_throw_error()
'''
```
<img src="arguments/accounts.png" 
    onerror="this.src='../../../source/cases/arguments/accounts.png'"   
    width="720px"/>

### Permission arguments

In the simpest form, permissions are like accounts: account objects or account 
names.

If an account name is used, it can be decorated with a permission level: 
'eosio@permission', for example.

Using the object oriented style, a permission may be a tuple enclosing an 
account object and 

```md
'''
account_create(
    "carol", account_master, 
    permission=[
        (account_master, Permission.OWNER), 
        (account_master, Permission.ACTIVE)])
'''
```

equivalent forms:
permission=[ ("eosio", "owner"), ("eosio", "active")])
    or
permission=[ "eosio@owner", "eosio@active"])

If a permission argument type is not supported, an error message is printed, or 
an error exception is thrown. For example, let the account argument be of the 
'CreateKey' type:

```md
'''
set_throw_error(False)

account_create(
    "account_carol_b", account_master, 
    permission=CreateKey("xxx", is_verbose=0))

set_throw_error()
'''
```
<img src="arguments/permissions.png" 
    onerror="this.src='../../../source/cases/arguments/permissions.png'"   
    width="720px"/>

### Data arguments

Data arguments control the contract actions. Let us deploy an instance of the 
'eosio.token' contract in order to show varies forms of the data argument of 
the action 'transfer'. 

```md
'''
account_create("eosio_token", account_master)
contract_eosio_token = Contract(eosio_token, CONTRACT_DIR)
deploy = contract_eosio_token.deploy()

eosio_token.push_action(
    "create", 
    {
        "issuer": account_master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0", 
        "can_recall": "0", 
        "can_whitelist": "0"
    }, 
    [account_master, eosio_token]) 

eosio_token.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    }, 
    permission=account_master) 
'''
```

The data argument can be of the puthon 'dict` type, as in the first example.
The second example presents a 'heredoc` form. The third version is the 'CLEOS' 
origin.

Note that the last version only maches the data arguments used in of the 
'cleos' and 'cleos_system' modules.

```md
'''
eosio_token.push_action(
    "transfer",
    {
        "from": alice, "to": carol,
        "quantity": "5.0000 EOS", "memo":""
    },
    permission=alice)

eosio_token.push_action(
    "transfer",
    '''{
        "from": alice, "to": carol,
        "quantity": "5.1000 EOS", "memo":""
    }''',
    permission=alice)

eosio_token.push_action(
    "transfer",
    '{' 
        + '"from":' + str(alice) 
        + ', "to": ' + str(carol)
        + ', "quantity": "5.2000 EOS", "memo":""'
        + '}',
    permission=alice)    
'''
```
<img src="arguments/data.png" 
    onerror="this.src='../../../source/cases/arguments/data.png'"   
    width="720px"/>
'''