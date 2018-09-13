'''
# Arguments

This file can be executed as a python script: `python3 arguments.md`.

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
from eosf import *

reset() 
create_wallet()
create_master_account("master")
'''
```
## Case

### Account arguments

Accounts are represented either as blockchain names or as account objects. In
the following test, the 'account_master' object enters, at first, as itself ...

```md
'''
create_account("alice", master)
'''
```

... next, the 'account_master' is represented as a string, 'eosio` in this case:

```md
'''
create_account("bob", str(master))
'''
```

If an account argument is neither an account object nor a string, an error 
message is printed, or an error exception is thrown. For example, let the 
account argument be of the 'CreateKey' type:

```md
'''
set_throw_error(False)
create_account("charlie", CreateKey("xxx", is_verbose=0))
set_throw_error(True)
'''
```

![accounts](./img/accounts.png)

### Permission arguments

In the simpest form, permissions are like accounts: account objects or account 
names.

If an account name is used, it can be decorated with a permission level: 
'eosio@permission', for example.

Using the object oriented style, a permission may be a tuple enclosing an 
account object and 

```md
'''
create_account(
    "carol", master, 
    permission=[
        (master, Permission.OWNER), 
        (master, Permission.ACTIVE)])
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
create_account(
    "eve", master, 
    permission=CreateKey("xxx", is_verbose=0))
set_throw_error(True)
'''
```
![permissions](./img/permissions.png)

### Data arguments

Data arguments control the contract actions. Let us deploy an instance of the 
'eosio.token' contract in order to show varies forms of the data argument of 
the action 'transfer'. 

```md
'''
create_account("host", master)
contract = Contract(host, "02_eosio_token")
contract.deploy()


host.push_action(
    "create",
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS",
        "can_freeze": "0", 
        "can_recall": "0", 
        "can_whitelist": "0"
    }, 
    [master, host]) 

host.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    }, 
    permission=master)
'''
```

The data argument can be of the Python `dict` type, for example:

```md
'''
host.push_action(
    "transfer",
    {
        "from": alice, "to": carol,
        "quantity": "5.0000 EOS", "memo":""
    },
    permission=alice)
'''
```
The second example presents a `heredoc` form:
```md
'''
host.push_action(
    "transfer",
    '''{
        "from": alice, "to": carol,
        "quantity": "5.1000 EOS", "memo":""
    }''',
    permission=alice)
'''
```
The third example is the `cleos` origininal format:
```md
'''
host.push_action(
    "transfer",
    '{' 
        + '"from":' + str(alice) 
        + ', "to": ' + str(carol)
        + ', "quantity": "5.2000 EOS", "memo":""'
        + '}',
    permission=alice)  
'''
```

Note that the last version only maches the data arguments used in of the 
'cleos' and 'cleos_system' modules.

![data](./img/data.png)

'''