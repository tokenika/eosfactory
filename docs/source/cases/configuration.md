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
### Test run

```md
In an linux bash, change directory to where this file exists, it is the 
directory ``docs/source/cases`` in the repository, and enter the following 
command:
```
```md
$ python3 configuration.md
```
```md
or
```
```md
$ $eosf get config
```
```md
We hope that you get anything similar to this shown in the image below.
You can change something in the configuration file ``teos/config.json``, and
see the result.
```
<img src="configuration.png" 
    onerror="this.src='../../../source/cases/configuration.png'"   
    alt="configuration" width="680px"/>
    
"""