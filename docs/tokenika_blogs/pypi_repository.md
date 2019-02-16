tokenika
qQWZZwPMAn3Z8pGCNPJJk

### Uninstalling eosfactory Python package

Un-installation command...
```bash
pip3 uninstall eosfactory-tokenika
```
...results:
```bash
Uninstalling eosfactory-tokenika-2.1.1:
  Would remove:
    /usr/local/eosfactory/config.ini
    /usr/local/eosfactory/config.json
    /usr/local/eosfactory/genesis.json
    /usr/local/eosfactory/templates/contracts/hello_world/.vscode/c_cpp_properties.json
    /usr/local/eosfactory/templates/contracts/hello_world/.vscode/settings.json
    /usr/local/eosfactory/templates/contracts/hello_world/.vscode/tasks.json
    /usr/local/eosfactory/templates/contracts/hello_world/CMakeLists.txt
    /usr/local/eosfactory/templates/contracts/hello_world/resources/CONTRACT_NAME.clauses.md
    /usr/local/eosfactory/templates/contracts/hello_world/resources/CONTRACT_NAME.contracts.md
    /usr/local/eosfactory/templates/contracts/hello_world/src/CONTRACT_NAME.cpp
    /usr/local/eosfactory/templates/contracts/hello_world/src/logger.hpp
    /usr/local/eosfactory/templates/contracts/hello_world/tests/test1.py
    /usr/local/eosfactory/templates/contracts/hello_world/tests/unittest1.py
    ....................................
    ....................................
    /usr/local/lib/python3.5/dist-packages/eosfactory/*
    /usr/local/lib/python3.5/dist-packages/eosfactory_tokenika-2.1.1-py3.5.egg-info
Proceed (y/n) y
Successfully uninstalled eosfactory-tokenika-2.1.1
```

### EOSFactory Python package link

>The `easy-install.pth` list is automatically pre-pended to the `system.path` python list, and, therefore, EOSFactory there obscures one installed as a regular package. See `sudo nano /usr/local/lib/python3.7/site-packages/easy-install.pth`

#### Install

```bash
python3 setup.py sdist bdist_wheel
sudo  -H python3 -m pip install -e .
```
The result is:
```bash
Obtaining file:///mnt/c/Workspaces/EOS/eosfactory
Requirement already satisfied: termcolor in /usr/local/lib/python3.7/site-packages (from eosfactory-tokenika==2.0.0) (1.1.0)
Installing collected packages: eosfactory-tokenika
  Found existing installation: eosfactory-tokenika 2.0.0
    Can't uninstall 'eosfactory-tokenika'. No files were found to uninstall.
  Running setup.py develop for eosfactory-tokenika
Successfully installed eosfactory-tokenika
```
The relevant entry is in the file `easy-install.pth`

#### Uninstall

```bash
sudo -H pip3 uninstall eosfactory-tokenika
```
The result is:
```bash
Uninstalling eosfactory-tokenika-2.0.0:
  Would remove:
    /usr/local/lib/python3.7/site-packages/eosfactory-tokenika.egg-link
Proceed (y/n)? y
  Successfully uninstalled eosfactory-tokenika-2.0.0
```
The entry in the file `easy-install.pth` removed.

### Alternative install

```bash
sudo python3 setup_develop.py develop
```
The result is:
```bash
running develop
running egg_info
creating eosfactory_tokenika.egg-info
writing eosfactory_tokenika.egg-info/PKG-INFO
writing dependency_links to eosfactory_tokenika.egg-info/dependency_links.txt
writing requirements to eosfactory_tokenika.egg-info/requires.txt
writing top-level names to eosfactory_tokenika.egg-info/top_level.txt
writing manifest file 'eosfactory_tokenika.egg-info/SOURCES.txt'
reading manifest file 'eosfactory_tokenika.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
writing manifest file 'eosfactory_tokenika.egg-info/SOURCES.txt'
running build_ext
Creating /usr/local/lib/python3.7/site-packages/eosfactory-tokenika.egg-link (link to .)
Adding eosfactory-tokenika 2.1.0 to easy-install.pth file

Installed /mnt/c/Workspaces/EOS/eosfactory
Processing dependencies for eosfactory-tokenika==2.1.0
Searching for termcolor==1.1.0
Best match: termcolor 1.1.0
Adding termcolor 1.1.0 to easy-install.pth file

Using /usr/local/lib/python3.7/site-packages
Finished processing dependencies for eosfactory-tokenika==2.1.0
```
The relevant entry is in the file `easy-install.pth`

Uninstall:
```bash
sudo -H pip3 uninstall eosfactory-tokenika
```
The entry in the file easy-install.pth removed.

### Making distribution

```bash
python3 setup.py sdist bdist_wheel
```

### Installing Python package

Pip version has to be precisely defined, otherwise uses the highest available one.
```bash
pip3 install --user dist/eosfactory_tokenika*.tar.gz
```
The result is:
```bash
Processing ./dist/eosfactory_tokenika-2.1.1.tar.gz
Requirement already satisfied: termcolor in /usr/local/lib/python3.7/site-packages (from eosfactory-tokenika==2.1.1) (1.1.0)
Building wheels for collected packages: eosfactory-tokenika
  Building wheel for eosfactory-tokenika (setup.py) ... done
  Stored in directory: /root/.cache/pip/wheels/ef/92/33/b7e1e9f6a6ab63affc942f451f8474f7f864ad2c16e632d28d
Successfully built eosfactory-tokenika
Installing collected packages: eosfactory-tokenika
  Found existing installation: eosfactory-tokenika 2.1.1
    Uninstalling eosfactory-tokenika-2.1.1:
      Successfully uninstalled eosfactory-tokenika-2.1.1
Successfully installed eosfactory-tokenika-2.1.1
```
## Uploading

Bash command:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
Command result:
```bash
Enter your username: tokenika
Enter your password:
Uploading distributions to https://test.pypi.org/legacy/
Uploading eosfactory_tokenika-2.1.1-py3-none-any.whl
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 106k/106k [00:02<00:00, 45.1kB/s]Uploading eosfactory_tokenika-2.1.1.tar.gz
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 75.4k/75.4k [00:01<00:00, 43.9kB/s]
```

## Viewing repository

Once uploaded your package should be viewable on TestPyPI, for example,
https://test.pypi.org/project/eosfactory-tokenika

## Importing package

```bash
pip3 install -i https://test.pypi.org/simple/ eosfactory-tokenika
```


## thrash
```bash
# python3 setup_develop.py develop
# pip freeze -- output installed packages in requirements format.
# 
pip freeze
```
```bash
# ..........................
docutils==0.14
-e git+https://github.com/tokenika/eosfactory.git@4b81198a3a9fb9c80f2b46fbfa91ec56dd4b360e#egg=eosfactory_tokenika
idna==2.6
# ..........................
```
This shall list names of all packages, you have installed (and which were detected by pip). The name can be sometime long, then use just the name of the package being shown at the and after #egg=. You can also in most cases ignore the version part (whatever follows == or -).
Then uninstall the package:
```
$ pip3 uninstall eosfactory-tokenika==2.0
```
If it asks for confirmation about removing the package, then you are lucky guy and it will be removed.
## 
You could install the package and make it available for any of your Python apps with:
```bash
python3 setup.py install --user
```
If you publish the above structure on a public repository, e.g. on Gibhub, anyone could easily install it with:
```bash
git clone https://www.github.com/yourname/yourpackage
cd yourpackage
python setup.py install --user
```
### Where eosfactory data
The /usr/local hierarchy is for use by the system administrator when installing software locally. It needs to be safe from being overwritten when the system software is updated. It may be used for programs and data that are shareable amongst a group of hosts, but not found in /usr 