# Exchanging EOSIO Contract Projects

If you want to pass to a colleague your EOSIO contract project which is a VSCode folder, the fist guess, is to zip the folder and e-mail it. However, this plan is not quite straightforward:

* There are volume binaries there.
* There are local configuring files in the `.vscode` folder.
* There are your private notes and scratchpads there.
* The paths in the `.vscode/c_cpp_properties.json` are localized according to your operating system.

Hence, you should copy the folder, and edit it.

EOSFactory has a tool that makes the compression, automatically solving the issues. It produces a zip file, in the project folder. The file is named after the folder name. Another tool developes a compressed project folder.

## `.eosideignore` file

There is the `.eosideignore` file in any project started with EOSFactory, containing the default excludes:

* .vscode/ipch/*
* .vscode/settings.json
* .vscode/tasks.json
* build/*
* command_lines.txt

This list can be edited. Files that match the patterns in the list are excluded from the zip file.

## `.vscode/c_cpp_properties.json` file

The configuration file contains entries that refer to local file system paths. For example:

* `/usr/local/Cellar/eosio.cdt/1.6.1/opt/eosio.cdt/include` for Mac,
* `C:/Users/cartman/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/usr/opt/eosio.cdt/1.6.1/include` for Windows,
* `/usr/opt/eosio.cdt/1.6.1/include` for Ubuntu.

EOSFactory converts the paths prior to zipping the file to the form `${eosio_cdt_home}include`, and attempts to restore existing paths upon decompression.

## EOSFactory tools

The tool is `amaxfactory.pack_contract.py`. By default, it zips the contract folder that is the current working directory. The zip file is then placed in the contract folder, named after the name of the folder. If the contract folder does not contain its `.eosideignore` file, a default one is created.

```
$ python3 -m amaxfactory.pack_contract
ERROR:
There is not the '.eosideignore' file in the project directory
    /mnt/c/Workspaces/EOS/contracts/helloi
Creating a default one.
adding .vscode/c_cpp_properties.json
adding CMakeLists.txt
adding ricardian/helloi.clauses.md
adding ricardian/helloi.contracts.md
adding src/helloi.cpp
adding tests/test1.py
adding tests/unittest1.py
```

Now, expand the zip file into a new project in the folder `../halloo`

```
$ python3 -m amaxfactory.pack_contract --unpack --dir ../helloo --zip ./helloi.zip
```
