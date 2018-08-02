"""
# EOSFactory configuration

<pre>
This file can be executed as a python script: 'python3 configuration.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre>

## Inspect the configuration

<pre>
"""
import teos

ok = teos.GetConfig()

"""
</pre>
<pre>
Note that the same result is available with this bash command:
</pre>
<pre>
$eosf get config
</pre>


## Override the installed configuration

<pre>
There is the 'config.json' file in the 'teos' folder of the repository. 
The entries there prevail the default settings.
</pre>

## Test run

<pre>
In an linux bash, change directory to where this file exists, it is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:
</pre>
<pre>
$ python3 configuration.md
</pre>
<pre>
or
</pre>
<pre>
$ $eosf get config
</pre>
<pre>
We hope that you get something similar to this one shown in the image below.
You can change or add something in the configuration file 'teos/config.json' 
and see the result.
</pre>
<img src="configuration.png" 
    onerror="this.src='../../../source/cases/configuration.png'"   
    alt="configuration" width="640px"/>
    
"""