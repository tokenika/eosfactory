"""
# EOSFactory configuration
```md
The structure of the ``Cases`` files is explained in the file ``setup.md`` in
this file's directory.

Note, that all case files are both ``Markdown`` and ``Python` scripts. 
Therefore, you can execute them with `python3 <file name>` bash command, or 
you can view them, (RIGHT MOUSE -> Open Preview if you use the ``Visual Studio 
Code``).
```
```md
Primarily, ``EOSFactory`` is configured when it is installed with the 
``build.sh`` script in the root of the repository
```

## Inspect the configuration

```md
"""
import teos

ok = teos.GetConfig()

"""
```
```md
Note that the same result is available with a bash command:
```
```md
$eosf get config
```


## Override the installed configuration

```md
There is the ``config.json`` file in the ``teos`` folder. The entries there 
prevail the default setup.
```
"""