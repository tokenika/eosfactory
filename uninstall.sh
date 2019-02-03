#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script uninstalls EOSFactory. Specifically, it uninstalls 'eosfactory'
#   Python package.
#   This script needs to be executed from within the 'eosfactory' folder.
#   This file was downloaded from https://github.com/tokenika/eosfactory
###############################################################################
"

printf "%s" "
Uninstalling Python 'eosfactory' package...
"

sudo python3 setup.py develop --uninstall