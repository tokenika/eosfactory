# Why EOS accounts are represented with Python globals?

Once upon a time, all program variables were global.

Now, the locals are of the first choice. Especially with Python that even discourages using globals by forcing the special notation.

## Local variables, global variables

Local variables added a lot of strength to programming languages: they greatly increased scalability. 

However, there are computable problems that can benefit from global variables. If a program represents fixed objects, they can be properly represented with globals variables or singletons.

For example, if a computer program is about the Earth, it is a trouble if the Earth is represented as independent local objects in different threads of the program.

EOSFactory is about EOS accounts. Once created, they last forever. (Well, it is not so with a local testnet, but none serious work is limited to local testnets.) As the accounts are unique and eternal, they are best represented with globals.

If you write a test, treating a problem of many account-roles, it is natural to name the accounts adequately to their roles.

For example, if in the first test of a series an account is locally named `buyer`, and one meter farther in the program the same -- physically -- account is represented as the local variable `purchaser`, then a reader -- possibly a law professionalist (see the next section), yet not trained in computer programing, who supervises a business-oriented smart-contract project and wants to get an insight into test results, is, certainly, confused.

Well, the programmer can be careful not to alter the names. But computer-writing is difficult enough bother about name-bookkeeping.

## The truth is that Python developers do not generally use global variables.

However, there is plenty globals in any Python program. Please, think about one, and tell me why it is global, and not local, or namespace (other than global) variable.

I bet that the same story can be applied to globals.

## Readability of the scripts

People also ask why *Python*, and not *javascript*. We have chosen Python because its inherent drive to readability by a layman: it is possible to write Python code closely resembling natural english. 

Our idea is that well-readable machine tests could be included into Ricardian Contracts that are obligatory for serious EOS smart-contract works. Then the human-readable Ricardian contracts, addressed to law professionals, could gain precision, still remaining readable by inteligent, yet without IT training, professionals. Please, see `docs.cases.account.md` in the EOSFactory repository, and execute the bash command `eosfactory/pythonmd.sh docs/cases/account.md`, still in the EOSFactory repository directory. You can get the idea.

Globals in EOSFactory gain readability. Compare:

```python
create_account("postman", post_office_manager)
```
and

```python
self.postman = create_account(post_office_manager)
```

With the local `self.postman` you would have to explain the meaning of the `self` prependix in the Ricardian Contract.

## Compactness of the scripts, and functionality

* You might note that the wallet that is an essential element of EOS account functionality, is invisibly transparent to the test script developer, and to a script reader. Hence, the script is shorter by numerous lines of code, necessary for explicit wallet operations. 

* Also note that all the responses from the testnet, including internal names of the accounts, and their public keys, are automatically translated into the corresponding names of the variables involved.

* You can see that account variables are restored between test sessions.


Valuable functionalities of EOSFactory result from mapping between global account variables and their names. This mapping could not be possible (well, noting is impossible with a computer) if account variables were local.

Consider:

```python
self.postman = create_account(post_office_manager)
function(create_account(post_office_manager))
```

You cannot know the name of the account variable `self.postman` without unreliable hacking. And you can never know the name of the (temporal) account variable used as the argument in the `function`.

If you do not care, you can do it in this way, in your scripts:

```python
self.postman = create_account("postman", post_office_manager)
function(create_account("postman1", post_office_manager))
```
But then you have to live with the sin of redundant information. And still you have globals undercover.

This mean codding is possible now, as the account factory functions, `create_account` and `create_master_account`, return the globals that they create. We do not document this feature, used internally, since we consider it anaesthetic and misleading.

## But, finally, what is really wrong with the global accounts?

* A global account variable, can overwrite another, unrelated global variable, for example, imported module name. With EOSFactory, this is impossible.
* In computer programing, wrong is possibility of misunderstanding the code. Can you point such a case? We show the opposite.
* Wrong is if EOSFactory is unable to express any practical test scenario. Can show such a scenario?
* Wrong is if you can write a better expressed test script if account variables are local. Can you show such an example?
* Wrong is automatic disgust at globals. This can be cured by reasoning.
* What else is wrong? We will try to correct it.
* Python linter (`plinter`, for example) complains about undefined variables. You can disable linter argues. If you do care, with `plinter` you can chose a special pattern for account variables.<br>
If you use VSCode, in `Settings` click `{}` in the upper right corner and add this entry:
`"python.linting.pylintArgs": [
    "--dummy-variables-rgx='(_+[a-zA-Z0-9]*?$)|dummy|qdict'"
]`


