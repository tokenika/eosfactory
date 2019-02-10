#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script uninstalls EOSFactory. 
#   This script needs to be executed from within the 'eosfactory' folder.
#   This file was downloaded from https://github.com/tokenika/eosfactory
###############################################################################
"

printf "%s" "
Uninstalling Python 'eosfactory' package...
"

sudo python3 setup_develop.py develop --uninstall # uninstall linked package
pip3 uninstall eosfactory-tokenika # uninstall regular package