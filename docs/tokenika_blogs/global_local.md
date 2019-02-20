## It is an artificial test case

Monty Python says:
>If you write Python stupidity, the result is unpredictable. Use Java or TypeScript to be protected against yourself.

Do you suggest that we should switch to TypeScript?

I could improve the *artificial test*, making it even more careless, still working with globals:

```python
if __name__ == '__main__':
    eosf = Master() # this is a singleton instance
    master_ = eosf # just for test purposes
    unittest.main()
```
The result is following:
```bash
======================================================================
ERROR: setUpClass (__main__.AccountsTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests/rkintzi.py", line 9, in setUpClass
    eosf.reset()
AttributeError: 'Master' object has no attribute 'reset'
```

Let us save our time keeping *artificial tests* away.

## The truth is that Python developers do not generally use global variables.

First of all let us decide whether the account variables could, or even should be represented as non-global objects.

### There are global variables in any Python program

There is plenty globals in any Python program. For example:

```bash
{
 'COMMENT': <function COMMENT at 0x7fcb1822e488>,
#..............................................
#..............................................
 '__annotations__': {},
 '__builtins__': <module 'builtins' (built-in)>,
 '__cached__': None,
 '__doc__': None,
 '__file__': 'tests/hello_world.py',
 '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7fcb198915f8>,
 '__name__': '__main__',
 '__package__': None,
 '__spec__': None,
 'account': <module 'eosfactory.shell.account' from '/mnt/c/Workspaces/EOS/eosfactory/eosfactory/shell/account.py'>,
 'cleos': <module 'eosfactory.core.cleos' from '/mnt/c/Workspaces/EOS/eosfactory/eosfactory/core/cleos.py'>,
 'contract': <module 'eosfactory.shell.contract' from '/mnt/c/Workspaces/EOS/eosfactory/eosfactory/shell/contract.py'>,
 'create_account': <function create_account at 0x7fcb15fd1268>,
 'create_master_account': <function create_master_account at 0x7fcb15fd10d0>,
 'create_wallet': <function create_wallet at 0x7fcb15fa3400>,
 'errors': <module 'eosfactory.core.errors' from '/mnt/c/Workspaces/EOS/eosfactory/eosfactory/core/errors.py'>,
 'get_testnet': <function get_testnet at 0x7fcb174f8f28>,
 'get_wallet': <function get_wallet at 0x7fcb15fa3488>,
 'info': <function info at 0x7fcb174f89d8>,
#.................................................
#.................................................
}
```
All of them represent permanent objects. Please, think about one, and tell me why it is global, and not local, or namespace (other than global) variable.

I bet that the same story can be applied to the account globals.

## Could EOSFactory be better if the account objects were local

Please, show an example of a test script that could be better -- by any reason you can image, if accounts were not represented with global objects
 

## Users


