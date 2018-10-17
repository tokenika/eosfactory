#!/bin/bash

printf "%s\n" "
###############################################################################
#   This script installs EOSFactory. It needs to be executed from within 
#   the 'eosfactory' folder.
#   This file was downloaded from https://github.com/tokenika/eosfactory
###############################################################################
"

IS_WSL="" # Windows Subsystem Linux
function is_wsl {
    uname_a=$( uname -a )
    if [[ "$uname_a" == *"Microsoft"* ]]; then 
        IS_WSL="IS_WSL"
    fi
}
is_wsl

WSL_ROOT=""
if [ ! -z "$IS_WSL" ]; then
    printf "%s\n" "Windows Subsystem Linux detected"

    WSL_ROOT_IS_SET=""
    function verifyWslRoot() {
        path=$1
        bashrc=".bashrc"
        home=${path}\\home\\${USER}
        bashrcPath=${home}\\$bashrc
        bashrcDir=$(cmd.exe /c dir /B  $bashrcPath)

        if [ ! -z ${bashrcDir} ]; then
            bashrcDir=${bashrcDir::-1}
        fi
        if [ "$bashrcDir" == "$bashrc" ]; then 
            WSL_ROOT=${path}        
            printf "WSL ROOT is %s\n" "$WSL_ROOT"
            WSL_ROOT_IS_SET=true
        fi
    }

    Lxss="hkcu\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss"
    ddKey=$(reg.exe query $Lxss /v Defaultdistribution)
    dd=$(echo $ddKey | grep -o -P '(?<={).*(?=})')
    bpKey=$(reg.exe query "${Lxss}\\{$dd}" /v BasePath)

    if [ -z "$WSL_ROOT_IS_SET" ]; then
        verifyWslRoot "$(echo $bpKey | \
            grep -o -P '(?<=REG_SZ)[ A-Za-z0-9:\\\._]*')\\rootfs"
    fi
    
    while [ -z "$WSL_ROOT_IS_SET" ]; do
            printf "\n%s" "
Cannot find the root of the WSL file system which was tried to be
${WSL_ROOT}.
Please, find the path in your computer and enter it. Enter nothing, if you do
not care about having the Visual Studio Code intelisense efficient.
"
    echo "Enter the path:"
    read wslRootDir
    if [ -z "${wslRootDir}"]; then
        break
    fi

    verifyWslRoot "${wslRootDir}"
    done
fi

printf "%s" "
Installing the 'eosfactory' package locally with the Python pip system...
"

###############################################################################
# It is essentioal that the package is installed as a symlink, with 
# the flag '-e'
###############################################################################
sudo  -H python3 -m pip install -e .

printf "%s\n" "
Configuring the eosfactory installation...
"

if [ ! -z "$IS_WSL" ]; then
    python3 eosfactory/install.py ${WSL_ROOT}
else
    python3 eosfactory/install.py ""
fi

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)
printf "${bldred}%s${txtrst}" '
         ______ ____   _____  ______      _____ _______ ____  _______     __
        |  ____/ __ \ / ____||  ____/\   / ____|__   __/ __ \|  __ \ \   / /
        | |__ | |  | | (___  | |__ /  \ | |       | | | |  | | |__) \ \_/ / 
        |  __|| |  | |\___ \ |  __/ /\ \| |       | | | |  | |  _  / \   /  
        | |___| |__| |____) || | / ____ \ |____   | | | |__| | | \ \  | |   
        |______\____/|_____/ |_|/_/    \_\_____|  |_|  \____/|_|  \_\ |_|   
                                                      
'
printf "%s\n" "
To verify EOSFactory installation navigate to the 'eosfactory' folder and run 
these tests:
"
printf "%s\n" "    
    $ python3 tests/01_hello_world.py
    $ python3 tests/02_eosio_token.py
    $ python3 tests/03_tic_tac_toe.py
"