'''
# EOSFactory configuration

This file can be executed as a python script: 'python3 configuration.md'.

## Inspect the configuration

```md
'''
import teos
ok = teos.get_config()
'''
```
Note that the same result is available with this bash command:

```md
$eosf get config
```


## Override the installed configuration

There is the 'config.json' file in the 'teos' folder of the repository. 
The entries there prevail the default settings.

## Test run

With a linux bash, change directory to where this file exists, that is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:

```md
$ python3 configuration.md
```

or

```md
$ $eosf get config -j
```

The flag `-j` makes json output. We expect that you get something similar to 
this one shown in the image below.
You can change or add something in the configuration file 'teos/config.json' 
and see the result.

<img src="configuration.png" 
    onerror="this.src='../../../source/cases/configuration.png'" width="720px"/>
'''