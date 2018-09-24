### Permissions

In the simplest form, permissions are like accounts: account objects or account names.

If an account name is used, it can be decorated with a permission level, e.g. `eosio@owner` or `eosio@active`.

Using the object oriented style, a permission may be a tuple enclosing an account object, for example:

```md
create_account(
    "carol", master,
    permission=[(master, Permission.OWNER), (master, Permission.ACTIVE)])
```

An equivalent form:

```
create_account(
    "carol", master,
    permission=[("eosio", "owner"), ("eosio", "active")])
```

And another one:

```
create_account(
    "carol", master,
    permission=["eosio@owner", "eosio@active"])
```

