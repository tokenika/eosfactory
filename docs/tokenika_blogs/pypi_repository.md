tokenika
qQWZZwPMAn3Z8pGCNPJJk

### Uninstalling eosfactory Python package link

If the `easy-install` thing is in the system, local packages are included to the 'easy-install.pth` if the package is linked to the list of installed packages.

This happens as results of both installation methods:
* sudo  -H python3 -m pip install -e .
* sudo python3 setup_develop.py develop

The local EOSFactory entry is not removed on un-installation.
I follow an [article](http://matthew-brett.github.io/pydagogue/un_easy_install.html), advising killing the easy-install.

```bash
sudo python3 setup_develop.py develop --uninstall
```
nano /usr/local/lib/python3.7/site-packages/easy-install.pth

```bash
running develop
Removing /usr/local/lib/python3.5/dist-packages/eosfactory-tokenika.egg-link (link to .)
```

### Uninstalling eosfactory Python package

```bash
sudo -H pip3 uninstall eosfactory-tokenika==2.1.0
```
```bash
Uninstalling eosfactory-tokenika-2.1.0:
  Would remove:
    /usr/local/eosfactory/config.ini
    /usr/local/eosfactory/config.json
    /usr/local/eosfactory/genesis.json
    /usr/local/eosfactory/templates/contracts/01_hello_world/.vscode/c_cpp_properties.json
    /usr/local/eosfactory/templates/contracts/01_hello_world/.vscode/settings.json
    /usr/local/eosfactory/templates/contracts/01_hello_world/.vscode/tasks.json
    /usr/local/eosfactory/templates/contracts/01_hello_world/CMakeLists.txt
    /usr/local/eosfactory/templates/contracts/01_hello_world/resources/CONTRACT_NAME.clauses.md
    /usr/local/eosfactory/templates/contracts/01_hello_world/resources/CONTRACT_NAME.contracts.md
    /usr/local/eosfactory/templates/contracts/01_hello_world/src/CONTRACT_NAME.cpp
    /usr/local/eosfactory/templates/contracts/01_hello_world/src/logger.hpp
    /usr/local/eosfactory/templates/contracts/01_hello_world/tests/test1.py
    /usr/local/eosfactory/templates/contracts/01_hello_world/tests/unittest1.py
    ....................................
    ....................................
    /usr/local/lib/python3.5/dist-packages/eosfactory/*
    /usr/local/lib/python3.5/dist-packages/eosfactory_tokenika-2.1.0-py3.5.egg-info
Proceed (y/n) y
Successfully uninstalled eosfactory-tokenika-2.1.0
```

### Making distribution

```bash
python3 setup.py sdist bdist_wheel
```

```bash
python3 setup.py sdist --format zip
```

### Installing Python package with a whl file

Pip version has to be precisely defined, otherwise uses the highest available one.
```bash
sudo -H pip3 install /mnt/c/Workspaces/EOS/eosfactory/dist/eosfactory_tokenika-2.1.0-py3-none-any.whl
```
```bash
sudo -H pip3 install /mnt/c/Workspaces/EOS/eosfactory/dist/eosfactory_tokenika-2.1.0.zip
```
```bash
Processing /mnt/c/Workspaces/EOS/eosfactory/dist/eosfactory-tokenika-2.1.0.zip
Requirement already satisfied: termcolor in /usr/local/lib/python3.5/dist-packages (from eosfactory-tokenika==2.1.0) (1.1.0)
Installing collected packages: eosfactory-tokenika
  Found existing installation: eosfactory-tokenika 2.0
    Uninstalling eosfactory-tokenika-2.0:
      Successfully uninstalled eosfactory-tokenika-2.0
  Running setup.py install for eosfactory-tokenika ... done
Successfully installed eosfactory-tokenika-2.1.0
```

However when I run "python setup.py install" none of my data files are written - only the "whyteboard" source package, and the whyteboard.py is placed in /usr/local/lib/python2.6/dist-packages/.

python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl
Once uploaded your package should be viewable on TestPyPI, for example,
https://test.pypi.org/project/eosfactory-tokenika
You can use pip to install your package and verify that it works. Create a new virtualenv (see Installing Packages for detailed instructions) and install your package from TestPyPI:
sudo -H python3 -m pip install --index-url https://test.pypi.org/simple/ eosfactory-tokenika
to remove egg-link:
sudo python3.5 setup.py develop --uninstall
## uninstall
Check, how is your installed package named from pip point of view:
```bash
# sudo python3 setup_develop.py develop
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
$ sudo -H pip3 uninstall eosfactory-tokenika==2.0
```
If it asks for confirmation about removing the package, then you are lucky guy and it will be removed.
## 
You could install the package and make it available for any of your Python apps with:
```
python setup.py install
```
If you publish the above structure on a public repository, e.g. on Gibhub, anyone could easily install it with:
```
git clone https://www.github.com/yourname/yourpackage
cd yourpackage
python setup.py install
```
### Where eosfactory data
The /usr/local hierarchy is for use by the system administrator when installing software locally. It needs to be safe from being overwritten when the system software is updated. It may be used for programs and data that are shareable amongst a group of hosts, but not found in /usr 