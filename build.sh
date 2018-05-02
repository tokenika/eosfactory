#!/bin/bash
##########################################################################
#   This script instals tokenika 'eosfactory' both Linux and Windows
#   (with WSL) computers. It has to be executed in the directory of an
#   'eosfactory' repository.
#   This file was downloaded from https://github.com/tokenika/eosfactory
##########################################################################

EOSIO_SOURCE_DIR__=""
CXX_COMPILER=clang++-4.0
C_COMPILER=clang-4.0
BUILD_TYPE="Debug"
ROOT_DIR_WINDOWS="%LocalAppData%\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState\\rootfs"
teos_python="teos_python"
library_dir="teos_lib"
executable_dir="teos"
build_dir="build"
contracts="contracts"

while getopts ":e:c:h" opt; do
  case $opt in
    e)
        EOSIO_SOURCE_DIR__=$OPTARG
        ;;
    c)
        if [ "$OPTARG" == "gnu" ]; then
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
shift $((OPTIND-1))

printf "%s\n" "
Arguments:
    EOSIO_SOURCE_DIR=${EOSIO_SOURCE_DIR__}
    CXX_COMPILER=${CXX_COMPILER}
    C_COMPILER=${C_COMPILER}
"

EOSIO_CONTEXT_DIR__="$PWD"
BUILD_DIR="${EOSIO_CONTEXT_DIR__}/build"

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

printf "%s" "
##########################################################################
"
printf "\n%s" "
Beginning build.
    $( date -u )
    git head id: $( cat .git/refs/heads/master )
    Current branch: $( git branch | grep \* )
    ARCHITECTURE: ${ARCH}
"

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

if [[ "$PROC_VERSION" == *"Microsoft"* ]]; then 
    IS_WSL="IS_WSL"
    printf "\t%s\n" "Detected Windows Subsystem Linux"
fi

if [ -z "$EOSIO_SOURCE_DIR__" -a -z "$EOSIO_SOURCE_DIR" ]; then
    printf "\n%s\n" "
EOSIO repository not found.
    Please, set environment variable 'EOSIO_SOURCE_DIR' pointing
    the path to the EOSIO repository
"    
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
# Set Linux environment variables
##########################################################################
printf "%s" "
##########################################################################
"
printf "\n%s\n" "Sets environment variables, if not set already:"

#./build.sh -cgnu -e/mnt/c/Workspaces/EOS/eos


if [ -z "$EOSIO_SHARED_MEMORY_SIZE_MB" ]; then
    value=100
    echo "export EOSIO_SHARED_MEMORY_SIZE_MB=$value" >> ~/.bashrc
    printf "\t%s\n" "setting EOSIO_SHARED_MEMORY_SIZE_MB: $value"
fi

if [ "$EOSIO_SOURCE_DIR" != "$EOSIO_SOURCE_DIR__" ]; then
    echo "export EOSIO_SOURCE_DIR=$EOSIO_SOURCE_DIR__" >> ~/.bashrc
    printf "\t%s\n" "setting EOSIO_SOURCE_DIR: $EOSIO_SOURCE_DIR__"
fi

if [ "$EOSIO_CONTEXT_DIR" != "$EOSIO_CONTEXT_DIR__" ]; then
    echo "export EOSIO_CONTEXT_DIR=$EOSIO_CONTEXT_DIR__" >> ~/.bashrc
    printf "\t%s\n" "setting EOSIO_CONTEXT_DIR: $EOSIO_CONTEXT_DIR__"
fi

PYTHONPATH__="$EOSIO_CONTEXT_DIR__/$teos_python"
if [[ -z "$PYTHONPATH" || "$PYTHONPATH" != *"$PYTHONPATH__"* ]]
then
    echo "export PYTHONPATH=${PYTHONPATH__}:${PYTHONPATH}" >> ~/.bashrc
    printf "\t%s\n" "setting PYTHONPATH: ${PYTHONPATH__}:"
fi

EOSIO_CONTRACT_WORKSPACE__="$EOSIO_CONTEXT_DIR__/$contracts"
if [ "$EOSIO_CONTRACT_WORKSPACE" != "$EOSIO_CONTRACT_WORKSPACE__" ]; then
    echo "export EOSIO_CONTRACT_WORKSPACE=$EOSIO_CONTRACT_WORKSPACE__" >> ~/.bashrc
    printf "\t%s\n" "setting EOSIO_CONTRACT_WORKSPACE: $EOSIO_CONTRACT_WORKSPACE__"
fi
 
##########################################################################
# Sert Windows environment variables
##########################################################################

if [ ! -z "$IS_WSL" ]; then
    printf "%s" "
##########################################################################
    "
    printf "\nSets Windows environment variables:\n"

    setx.exe EOSIO_SOURCE_DIR $EOSIO_SOURCE_DIR__
    printf "\t%s\n" "setting windows EOSIO_SOURCE_DIR: $EOSIO_SOURCE_DIR__"

    EOSIO_SOURCE_DIR_ARG_WINDOWS=""
    wslMapLinux2Windows EOSIO_SOURCE_DIR_ARG_WINDOWS $EOSIO_SOURCE_DIR__
    setx.exe EOSIO_SOURCE_DIR_WINDOWS ${EOSIO_SOURCE_DIR_ARG_WINDOWS}
    printf "\t%s\n" "setting windows EOSIO_SOURCE_DIR_WINDOWS: $EOSIO_SOURCE_DIR_ARG_WINDOWS"

    HOME_WINDOWS=${ROOT_DIR_WINDOWS}\\home\\$USER
    setx.exe HOME_WINDOWS $HOME_WINDOWS
    printf "HOME_WINDOWS: %s\n"  "$HOME_WINDOWS"
fi

if [ -z "$CMAKE" ]; then
    CMAKE=$( which cmake )
fi

##########################################################################
# Make the file structure
##########################################################################
printf "%s" "
##########################################################################
"
printf "%s" "
Makes the file structure:

    ${EOSIO_CONTEXT_DIR__}  # eosfactory repository
        ${BUILD_DIR}    # binary dir
            daemon          # local EOSIO node documents
                data-dir    # the EOSIO node data-dir
                    wallet  # local wallets
                    genesis.json
                    config.in
"

cd ${EOSIO_CONTEXT_DIR__}
mkdir -p ${BUILD_DIR}
mkdir -p ${BUILD_DIR}/daemon/data-dir/wallet

cp -u ${EOSIO_SOURCE_DIR}/programs/snapshot/genesis.json \
    ${BUILD_DIR}/daemon/data-dir/genesis.json
cp -u ${EOSIO_CONTEXT_DIR__}/resources/config.ini \
    ${BUILD_DIR}/daemon/data-dir/config.ini


##########################################################################
# compiling library
##########################################################################
printf "%s" "
##########################################################################
"
cd ${EOSIO_CONTEXT_DIR__}
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
printf "%s" "
##########################################################################
"
cd ${EOSIO_CONTEXT_DIR__}
cd ${executable_dir}
mkdir build
cd build

printf "\n%s\n" "Compiling ${executable_dir}. Current directory is ${PWD}"

$CMAKE -DCMAKE_BUILD_TYPE=${BUILD_TYPE} \
    -DCMAKE_CXX_COMPILER=${CXX_COMPILER} \
    -DCMAKE_C_COMPILER=${C_COMPILER} ..

if [ $? -ne 0 ]; then
    printf "\n\t%s\n\n" \
        ">> CMAKE building ${executable_dir} has exited with the above error."
    exit -1
fi

make

if [ $? -ne 0 ]; then
    printf "\n\t%s\n" \
    ">> MAKE building ${executable_dir} has exited with the above error."
    exit -1
fi

##########################################################################
# finishing
##########################################################################
printf "%s" "
##########################################################################
"
TIME_END=$(( `date -u +%s` - $TIME_BEGIN ))
printf "\n%s\n%dmin %dsec\n\n" "eosfactory has been successfully built." \
    $(($TIME_END/60)) $(($TIME_END%60))

if [ ! -z "$IS_WSL" ]; then
    printf "%s\n" "
    If you use the 'Visual Studio Code', restart it in order to access new 
    environment variables.

    Also check whether ${ROOT_DIR_WINDOWS}
    is an existing Windows path. If it is not, set a local Windows environment 
    variable 'ROOT_DIR_WINDOWS' to the value of the root of the WSL file system. 
    Note that this value may be similar to the displayed one."
else
    printf "%s\n" "PLEASE, RESET BASH!."
fi

printf "\n%s\n" "
To verify your installation run the following commands:
    python3
    Python 3.5.2 (default, Nov 23 2017, 16:37:01)
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import teos
    teos exe: /mnt/c/Workspaces/EOS/eosfactory/teos/build/teos
    >>> teos.node_reset()
    #  nodeos exe file: /mnt/c/Workspaces/EOS/eos/build/programs/nodeos/nodeos
    #  genesis state file: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/genesis.json
    #   server address: 127.0.0.1:8888
    #  config directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir
    #  wallet directory: /mnt/c/Workspaces/EOS/eosfactory/build/daemon/data-dir/wallet
    #  head block number: 1
    #  head block time: 2018-04-30T13:57:08

    >>> teos.node_info()
    #       head block: 52
    #  head block time: 2018-04-30T14:33:05
    #  last irreversible block: 51

    teos.node_stop()
    #  Daemon is stopped.

We hope, you will see a minimized window running a local EOSIO node.
"
