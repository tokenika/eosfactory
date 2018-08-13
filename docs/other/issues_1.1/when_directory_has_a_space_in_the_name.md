# Build fails in WSL when directory has a space in the name #33

https://github.com/tokenika/eosfactory/issues/33

## Q

Using WSL, attempting to build in a directory with a space in the name:
./build.sh -e "/mnt/c/Users/Some\ Username/Documents/eos" -w ...

Produces the following error:

```
##############################################################################
#   The EOSIO_SOURCE_DIR system variable seems to be incorrect.
#   It must be so that /mnt/c/Users/Some\ Username/Documents/eos/build/programs/nodeos/nodeos
#   points to the nodeos executable.
##############################################################################
Removing the escape character in the path results in directories not being found 
and a failure to locate the rootfs path

./build.sh -e "/mnt/c/Users/Some Username/Documents/eos" -w ...

...
The system cannot find the file specified.
The system cannot find the path specified.
The system cannot find the file specified.
The system cannot find the path specified.
The system cannot find the file specified.
The system cannot find the path specified.

        ######################################################################
        #   Cannot find the root of the WSL file system which was tried to be
        #
        #   %LocalAppData%\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\rootfs
        #   and
        #   %LocalAppData%\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs
        #
        #   Please, find the path in your computer, and restart the ./build.sh
        #   with the option
        #   -o <path to the root of the WSL file system>
        #   added to the command line.
        ######################################################################
```

## A

I guess that you cannot have both escape character in quotation marks, in the 
same time:
```
./build.sh -e "/mnt/c/Users/Some\ Username/Documents/eos" -w ...
```
Try quotation marks alone:
```
./build.sh -e "/mnt/c/Users/Some Username/Documents/eos" -w ...
```

