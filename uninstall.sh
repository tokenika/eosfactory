#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script uninstalls EOSFactory.
#   This file was downloaded from https://github.com/tokenika/eosfactory
###############################################################################
"

printf "%s" "
Uninstalling Python 'eosfactory' package...
"

# sudo -H pip3 uninstall eosfactory-tokenika
pip3 uninstall eosfactory-tokenika # must be without sudo -H 