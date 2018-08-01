"""
# EOSFactory configuration

<pre><normal>
This file can be executed as a python script: 'python3 configuration.md'.

The set-up statements are explained at <a href="setup.html">cases/setup</a>.
</pre></normal>

## Inspect the configuration

<pre><normal>
"""
import teos

ok = teos.GetConfig()

"""
</pre></normal>
<pre><normal>
Note that the same result is available with this bash command:
</pre></normal>
<pre><normal>
$eosf get config
</pre></normal>


## Override the installed configuration

<pre><normal>
There is the 'config.json' file in the 'teos' folder of the repository. 
The entries there prevail the default setup.
</pre></normal>

## Test run

<pre><normal>
In an linux bash, change directory to where this file exists, it is the 
directory 'docs/source/cases' in the repository, and enter the following 
command:
</pre></normal>
<pre><normal>
$ python3 configuration.md
</pre></normal>
<pre><normal>
or
</pre></normal>
<pre><normal>
$ $eosf get config
</pre></normal>
<pre><normal>
We hope that you get something similar to this shown in the image below.
You can change or add something in the configuration file 'teos/config.json' 
and see the result.
</pre></normal>
<img src="configuration.png" 
    onerror="this.src='../../../source/cases/configuration.png'"   
    alt="configuration" width="640px"/>
    
"""