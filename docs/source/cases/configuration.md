"""
# EOSFactory configuration

```md
This file can be executed as a python script: ``python3 configuration.md``.
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