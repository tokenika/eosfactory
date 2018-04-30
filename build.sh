#!/bin/bash
##########################################################################
#   This script instals tokenika 'eosfactory' both Linux and Windows
#   (with WSL) computers. It has to be executed in the directory of an
#   'eosfactory' repository.
#   This file was downloaded from https://github.com/tokenika/eosfactory
##########################################################################

EOSIO_SOURCE_DIR_ARG=${EOSIO_SOURCE_DIR}
CXX_COMPILER=clang++-4.0
C_COMPILER=clang-4.0
BUILD_TYPE="Debug"
ROOT_DIR_WINDOWS="%LocalAppData%\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState\\rootfs"
teos_python="teos_python"
library_dir="teos_lib"
executable_dir="teos"
build_dir="build"

while getopts ":e:c:h" opt; do
  case $opt in
    e)
        EOSIO_SOURCE_DIR_ARG=$OPTARG
        ;;
    c)
        if [ $OPTARG == "gnu" ]; then
            CXX_COMPILER=g++
            C_COMPILER=gcc
        fi           
        ;;
    h)
        printf "%s\n" "
Usage: ./build.sh [OPTIONS]
    -e  EOSIO repository dir. Default is \${EOSIO_SOURCE_DIR}.
    -c  compiler, 'gnu' or 'clang'. Default is 'gnu'.
    -h  this message.
    "
        exit 0
        ;;
    \?)
        printf "Invalid option: -$OPTARG"
        exit 1
        ;;
    :)
        printf "Option -$OPTARG requires an argument."
        exit 1
        ;;
  esac
done

printf "%s\n" "
Arguments:
    EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR_ARG}
    CXX_COMPILER=${CXX_COMPILER}
    C_COMPILER=${C_COMPILER}
"

CONTEXT_DIR_ARG=$PWD
BUILD_DIR=${CONTEXT_DIR_ARG}/build

ARCH=$( uname )
TIME_BEGIN=$( date -u +%s )

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)
eosfactory="eosfactory"
repository="https://github.com/tokenika/${eosfactory}"
wiki="https://github.com/tokenika/${eosfactory}/wiki"

if [ ! -d .git ]; then
    printf "\n%s\n" "
This build script only works with sources cloned from git.
    Please clone a new eos directory with 'git clone ${repository} --recursive'
    See the wiki for instructions: ${wiki}
    Exiting now.    
"
    exit 1
fi

STALE_SUBMODS=$(( `git submodule status | grep -c "^[+\-]"` ))
if [ $STALE_SUBMODS -gt 0 ]; then
    printf "\n%s\n" "
git submodules are not up to date.
    Please run the command 'git submodule update --init --recursive'
    Exiting now.    
"
    exit 1
fi

printf "%s\n" "
##########################################################################
"
printf "\n%s\n" "
Beginning build.
    $( date -u )
    git head id: $( cat .git/refs/heads/master )
    Current branch: $( git branch | grep \* )
    ARCHITECTURE: ${ARCH}
"

if [ $ARCH == "Linux" ]; then
    
    if [ ! -e /etc/os-release ]; then
        printf "\n%s\n" "
    ${eosfactory} currently is tested with the Windows Subsystem Linux and Ubuntu.
    Please install on the latest version of one of these Linux distributions:
        https://www.microsoft.com/en-us/store/p/ubuntu/9nblggh4msv6
    or
        https://www.ubuntu.com/
    Exiting now.
"
        exit 1
    fi

    OS_NAME=$( cat /etc/os-release | grep ^NAME | cut -d'=' -f2 | sed 's/\"//gI' )
    PROC_VERSION=$(cat /proc/version)
    if [[ $PROC_VERSION == *"Microsoft"* ]]; then 
        IS_WSL="IS_WSL"
        printf "\t%s\n" "Detected Windows Subsystem Linux"
    fi
fi	

if [ x${EOSIO_SOURCE_DIR_ARG} == "x" ]; then
    printf "\n%s\n" "
EOSIO repository not found.
    Please, set environment variable 'EOSIO_SOURCE_DIR' pointing
    the path to the EOSIO repository
"
    exit 1
fi

function wslMapWindows2Linux() {
    path=$2
    drive_letter=${path:0:1}
    drive_letter=${drive_letter,,}
    path=${path//\\//}
    eval "$1=mnt/${drive_letter}${path:2}"
}

function wslMapLinux2Windows() {
    path=$2
    drive_letter=${path:5:1}
    eval "$1=${drive_letter}:${path:6}"
}

##########################################################################
# Make the file structure
##########################################################################
printf "%s\n" "
##########################################################################
"
printf "%s" "
Makes the file structure:

    ${CONTEXT_DIR_ARG}          #(eosfactory repository)
        ${BUILD_DIR}        #(binary dir: where compilation results go)
            daemon          #(the imputs and outputs of the local EOSIO node)
                data-dir    #(the data-dir from the EOSIO node help)
                    wallet  #(where local wallets are kept)
                    genesis.json
                    config.in
"

cd ${CONTEXT_DIR_ARG}
mkdir -p ${BUILD_DIR}
mkdir -p ${BUILD_DIR}/daemon/data-dir/wallet

cp -u ${EOSIO_SOURCE_DIR}/programs/snapshot/genesis.json \
    ${BUILD_DIR}/daemon/data-dir/genesis.json
cp -u ${CONTEXT_DIR_ARG}/resources/config.ini \
    ${BUILD_DIR}/daemon/data-dir/config.ini

##########################################################################
# Make Linux environment variables
##########################################################################
printf "%s\n" "
##########################################################################
"
printf "\n%s\n" "Makes environment variables, if not set already:"

if [ ${CONTEXT_DIR_ARG} != ${CONTEXT_DIR} ]; then
    echo "export CONTEXT_DIR=${CONTEXT_DIR_ARG}" >> ~/.bashrc
    printf "\t%s\n" "CONTEXT_DIR: ${CONTEXT_DIR_ARG}"
fi

if [ ${EOSIO_SOURCE_DIR_ARG} != ${EOSIO_SOURCE_DIR} ]; then
    echo "export EOSIO_SOURCE_DIR=${EOSIO_SOURCE_DIR_ARG}" >> ~/.bashrc
    printf "\t%s\n" "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR_ARG}"
fi

if [ x${PYTHONPATH} != "x" ]; then
    if [[ ${PYTHONPATH} != *"${CONTEXT_DIR_ARG}/${teos_python}"* ]]; then
        echo "export PYTHONPATH=\
        /mnt/c/Workspaces/EOS/eosfactory/teos_python:${PYTHONPATH}" >> ~/.bashrc
        printf "\t%s\n" "PYTHONPATH: ${PYTHONPATH}"
    fi
fi

##########################################################################
# Make Windows environment variables
##########################################################################

if [ x${IS_WSL} != "x" ]; then
    printf "%s\n" "
    ##########################################################################
    "
    printf "\nMakes Windows environment variables:\n"

    setx.exe EOSIO_SOURCE_DIR ${EOSIO_SOURCE_DIR_ARG}
    printf "\t%s\n" "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR_ARG}"

    EOSIO_SOURCE_DIR_ARG_WINDOWS=""
    wslMapLinux2Windows EOSIO_SOURCE_DIR_ARG_WINDOWS ${EOSIO_SOURCE_DIR_ARG}
    setx.exe EOSIO_SOURCE_DIR_WINDOWS ${EOSIO_SOURCE_DIR_ARG_WINDOWS}
    printf "\t%s\n" "EOSIO_SOURCE_DIR_WINDOWS: ${EOSIO_SOURCE_DIR_ARG_WINDOWS}"

    HOME_WINDOWS=${ROOT_DIR_WINDOWS}\\home\\${USER}
    setx.exe HOME_WINDOWS ${HOME_WINDOWS}
    echo -E "    HOME_WINDOWS: ${HOME_WINDOWS}"
fi

if [ -z $CMAKE ]; then
    CMAKE=$( which cmake )
fi

##########################################################################
# compiling library
##########################################################################
printf "%s\n" "
##########################################################################
"
cd ${CONTEXT_DIR_ARG}
cd ${library_dir}
mkdir build
cd build

printf "\n%s\n" "Compiling ${library_dir}. Current directory is ${PWD}"

$CMAKE -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
    -DCMAKE_CXX_COMPILER=${CXX_COMPILER} \
    -DCMAKE_C_COMPILER=${C_COMPILER} ..

if [ $? -ne 0 ]; then
    printf "\n\t%s\n\n" "
>>>>>> CMAKE building ${library_dir} has exited with the above error."
    exit -1
fi

make

if [ $? -ne 0 ]; then
    printf "\n\t%s\n" "
>>>>>> MAKE building ${library_dir} has exited with the above error."
    exit -1
fi

##########################################################################
# compiling executable
##########################################################################
printf "%s\n" "
##########################################################################
"
cd ${CONTEXT_DIR_ARG}
cd ${executable_dir}
mkdir build
cd build

printf "\n%s\n" "Compiling ${executable_dir}. Current directory is ${PWD}"

$CMAKE -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
    -DCMAKE_CXX_COMPILER=${CXX_COMPILER} \
    -DCMAKE_C_COMPILER=${C_COMPILER} ..

if [ $? -ne 0 ]; then
    printf "\n\t%s\n\n" "
>>>>>> CMAKE building ${executable_dir} has exited with the above error."
    exit -1
fi

make

if [ $? -ne 0 ]; then
    printf "\n\t%s\n" "
>>>>>> MAKE building ${executable_dir} has exited with the above error."
    exit -1
fi

##########################################################################
# finishing
##########################################################################
printf "%s\n" "
##########################################################################
"
TIME_END=$(( `date -u +%s` - $TIME_BEGIN ))

printf "\n%s\n%d:%d:%d\n\n" "eosfactory has been successfully built." $(($TIME_END/3600)) $(($TIME_END%3600/60)) $(($TIME_END%60))

if [ x${IS_WSL} != "x" ]; then
    printf "%s\n" "
    If you use the 'Visual Studio Code', restart it in order to access new 
    environment variables.

    Also check whether ${ROOT_DIR_WINDOWS}
    is a valid and existing Windows path. If it is not, set a local Windows
    environment variable 'ROOT_DIR_WINDOWS' to the value of the root of the
    WSL file system. Note that this value may be similar to the displayed one."

else
    source ~/.bashrc
fi

printf "\n%s\n" "
To verify your installation run the following commands:
    python3
    Python 3.5.2 (default, Nov 23 2017, 16:37:01)
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import teos
    teos exe: /mnt/c/Workspaces/EOS/eosfactory/teos/build/teos
    >>> teos.DaemonClear()
    #  nodeos exe file: /mnt/c/Workspaces/EOS/eos/build/programs/nodeos/nodeos
    #  genesis state file: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json
    #   server address: 127.0.0.1:8888
    #  config directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir
    #  wallet directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet
    #  head block number: 1
    #  head block time: 2018-04-30T13:57:08

    >>> teos.GetInfo()
    #       head block: 52
    #  head block time: 2018-04-30T14:33:05
    #  last irreversible block: 51

We hope, you will see a minimized window running a local EOSIO node.
"
