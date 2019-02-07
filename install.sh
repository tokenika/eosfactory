#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script installs EOSFactory. It needs to be executed from within
#   the 'eosfactory' folder.
#   This file was downloaded from https://github.com/tokenika/eosfactory
###############################################################################
"

printf "%s" "
Installing 'eosfactory' package locally with the Python pip system...
"

###############################################################################
# It is essential that the package is installed as a symlink, with
# the flag '-e'
###############################################################################
sudo  -H python3 -m pip install -e .
# sudo python3 setup_develop.py develop

printf "%s\n" "
Configuring the eosfactory installation...
"

python3 eosfactory/install.py "${WSL_ROOT}"
python3 -m eosfactory.config --dependencies

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)
printf "${bldred}%s${txtrst}" "
         ______ ____   _____  ______      _____ _______ ____  _______     __
        |  ____/ __ \ / ____||  ____/\   / ____|__   __/ __ \|  __ \ \   / /
        | |__ | |  | | (___  | |__ /  \ | |       | | | |  | | |__) \ \_/ /
        |  __|| |  | |\___ \ |  __/ /\ \| |       | | | |  | |  _  / \   /
        | |___| |__| |____) || | / ____ \ |____   | | | |__| | | \ \  | |
        |______\____/|_____/ |_|/_/    \_\_____|  |_|  \____/|_|  \_\ |_|

"
printf "%s\n" "
To verify EOSFactory installation navigate to the 'eosfactory' folder and run
these tests:
"
printf "%s\n" "
    $ python3 tests/01_hello_world.py
    $ python3 tests/02_eosio_token.py
    $ python3 tests/03_tic_tac_toe.py
"
