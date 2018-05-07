#!/bin/bash
##########################################################################
#   This script instals tokenika 'eosfactory' both Linux and Windows
#   (with WSL) computers. It has to be executed in the directory of an
#   'eosfactory' repository.
#   This file was downloaded from https://github.com/tokenika/eosfactory
##########################################################################

EOSIO_SOURCE_DIR__="$EOSIO_SOURCE_DIR"
CXX_COMPILER__=clang++-4.0
C_COMPILER__=clang-4.0
BUILD_TYPE__="Release"
ECC_IMPL__="secp256k1" # secp256k1 or openssl or mixed
ROOT_DIR_WINDOWS__="%LocalAppData%\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState\\rootfs"
EOSIO_SHARED_MEMORY_SIZE_MB__=100

pyteos="pyteos"
tests="tests"
library_dir="teos_lib"
executable_dir="teos"
build_dir="build"
contracts="contracts"
teos_exe="teos/build/teos"

function usage() {
    printf "%s\n" "
Usage: ./build.sh [OPTIONS]
    -e  EOSIO repository dir. Default is env. variable EOSIO_SOURCE_DIR.
    -c  compiler, 'gnu' or 'clang'. Default is 'clang'.
    -i  ECC implementation: 'secp256k1' or 'openssl' or 'mixed'. Default is 'secp256k1'.
    -t  Build type: 'Debug' or 'Release'. Default is 'Release'.
    -r  Reset the build.
    -s  EOSIO node shared memory size (in MB). Default is 100 
    -o  Path to the Windows WSL root, if applicable. Default is $ROOT_DIR_WINDOWS__
    -h  this message.
"    
}

while getopts ":e:c:i:t:s:rh" opt; do
  case $opt in
    e)
        EOSIO_SOURCE_DIR__=$OPTARG
        ;;

    c)
        compiler="$OPTARG"
        if [[ ! "$compiler" =~ (gnu|clang)$ ]]; then
            usage
            exit -1
        fi    
        if [ "$compiler" == "gnu" ]; then
            CXX_COMPILER__=g++
            C_COMPILER__=gcc
        fi          
        ;;

    i)  
        ECC_IMPL__="$OPTARG"
        if [[ ! "$ECC_IMPL__" =~ (secp256k1|openssl|mixed)$ ]]; then
            usage
            exit -1
        fi
        ;;

    t) 
        BUILD_TYPE__="$OPTARG"
        if [[ ! "$BUILD_TYPE__" =~(Debug|Release)$ ]]; then
            usage
            exit -1        
        fi
        ;;

    s)
        EOSIO_SHARED_MEMORY_SIZE_MB__="$OPTARG"
        ;;

    r)
        RESET__=RESET
        ;;

    o) 
        ROOT_DIR_WINDOWS__="$OPTARG"
        ;;

    h)
        usage
        exit 0
        ;;
        
    \?)
        printf "Invalid option: -$OPTARG"
        exit -1
        ;;

    :)
        printf "Option -$OPTARG requires an argument."
        exit -1
        ;;
  esac
done
shift $((OPTIND-1))

printf "%s\n" "
Arguments:
    EOSIO_SOURCE_DIR=$EOSIO_SOURCE_DIR__
    CXX_COMPILER__=$CXX_COMPILER__
    C_COMPILER__=$C_COMPILER__
    BUILD_TYPE__=$BUILD_TYPE__
    ECC_IMPL__=$ECC_IMPL__
    RESET__=$RESET__
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

if [ -z "$EOSIO_SOURCE_DIR__" ]; then
    printf "\n%s\n" "
EOSIO repository not found.
    Please, set the option `-e`, or environment variable 'EOSIO_SOURCE_DIR' 
    pointing the path to the EOSIO repository.
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
function setLinuxVariable() {
    name=$1
    value=$2

    if [ "${!name}" != "$value" ]; then
        echo "export $name=$value" >> ~/.bashrc
        printf "\t%s\n" "setting $name: $value"
    fi
}

printf "%s" "
##########################################################################
"
printf "\n%s\n" "Sets environment variables, if not set already:"
#./build.sh -cgnu -e/mnt/c/Workspaces/EOS/eos

setLinuxVariable "EOSIO_SOURCE_DIR" "$EOSIO_SOURCE_DIR__"
setLinuxVariable "EOSIO_CONTEXT_DIR" "$EOSIO_CONTEXT_DIR__"
setLinuxVariable "EOSIO_CONTRACT_WORKSPACE" "$EOSIO_CONTEXT_DIR__/$contracts"
setLinuxVariable "EOSIO_SHARED_MEMORY_SIZE_MB" "$EOSIO_SHARED_MEMORY_SIZE_MB__"
setLinuxVariable "EOSIO_TEOS" "$EOSIO_CONTEXT_DIR__/$teos_exe"

PYTHONPATH__="$EOSIO_CONTEXT_DIR__/${pyteos}:$EOSIO_CONTEXT_DIR__/${tests}"
if [[ -z "$PYTHONPATH" || "$PYTHONPATH" != *"$PYTHONPATH__"* ]]
then
    echo "export PYTHONPATH=${PYTHONPATH__}:${PYTHONPATH}" >> ~/.bashrc
    printf "\t%s\n" "setting PYTHONPATH: ${PYTHONPATH__}:"
fi
 
##########################################################################
# Set Windows environment variables
##########################################################################

function setWindowsVariable() {
    setOnWindows=$(cmd.exe /c echo %$1%)
    setOnWindows=${setOnWindows::-1}
    if [ "$setOnWindows" != "$2" ]; then
        setx.exe "$1" "$2"
        printf "\t%s\n" "setting windows $1: $2"
    fi    
}

if [ ! -z "$IS_WSL" ]; then
    printf "%s" "
##########################################################################
    "
    printf "\n%s\n" "Sets Windows environment variables, if not set already:"

    EOSIO_SOURCE_DIR_SET=""
    if [ ! -z "$EOSIO_SOURCE_DIR__" -a "$EOSIO_SOURCE_DIR" != "$EOSIO_SOURCE_DIR__" ]; then
        EOSIO_SOURCE_DIR_SET=$EOSIO_SOURCE_DIR__
    else
        EOSIO_SOURCE_DIR_SET=$EOSIO_SOURCE_DIR
    fi

    setWindowsVariable "EOSIO_CONTRACT_WORKSPACE" "$EOSIO_CONTEXT_DIR__/$contracts"
    setWindowsVariable "EOSIO_TEOS" "$EOSIO_CONTEXT_DIR__/$teos_exe"
    retval=""
    wslMapLinux2Windows retval $EOSIO_SOURCE_DIR_SET
    setWindowsVariable "EOSIO_SOURCE_DIR" "$retval" 

    ### env variable HOME

    bashrc=".bashrc"
    homePathSet=$(cmd.exe /c echo %HOME%)
    bashrcPathSet="${homePathSet::-1}\\$bashrc"
    bashrcDirSet=$(cmd.exe /c dir /B  $bashrcPathSet)
    if [ ! -z ${bashrcDirSet} ]; then
        bashrcDirSet=${bashrcDirSet::-1}
    fi
    # printf "//// left: %s\n" "${#bashrcDirSet} $bashrcDirSet"
    # printf "/// right: %s\n" "${#bashrc} $bashrc"    
    if [ "$bashrcDirSet" != "$bashrc" ]; then
        homeWindows=${ROOT_DIR_WINDOWS__}\\"home"\\$USER

        bashrcPath=${homeWindows}\\$bashrc
        bashrcDir=$(cmd.exe /c dir /B  $bashrcPath)

        if [ ! -z ${bashrcDir} ]; then
            #a=${a// /}
            bashrcDir=${bashrcDir::-1}
        fi 

        # printf "//// left: %s\n" "${#bashrcDir} $bashrcDir"
        # printf "/// right: %s\n" "${#bashrc} $bashrc"    
        if [ "$bashrcDir" == "$bashrc" ]; then 
            setx.exe "HOME" "$homeWindows"
            printf "HOME: %s\n" "$homeWindows"
        else
            printf "\n%s" "
    ######################################################################
    #   Cannot find the root of the WSL file system which was tried to be
    #
    #   ${ROOT_DIR_WINDOWS__}
    #
    #   Please, find the path in your computer, and restart the ./build.sh
    #   with option 
    #   -o <path to the root of the WSL file system>
    #   added to the command line.
    ######################################################################
    " 
        exit 1
        fi
    fi
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
        ${BUILD_DIR}  # binary dir
            daemon  # local EOSIO node documents
                data-dir  # the EOSIO node data-dir
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
# Is EOSIO_SOURCE_DIR set?
##########################################################################

if [ -z "$EOSIO_SOURCE_DIR" ]; then
    printf "/n%s\n" "
##########################################################################
#   THE BUILD IS NOT FINISHED!
#
#   THE BASH HAS TO BE RESET in order to load newly set environment 
#   variables.
#
#   Afterwards, this script can be restarted to continue this build.
##########################################################################
"
    exit -1
fi


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
if [ ! -z "$RESET__" ]; then
    printf "%s\n" "Deleting the contents of $PWD"
    rm -r *
fi

printf "\n%s\n" "Compiling ${library_dir}. Current directory is ${PWD}"

$CMAKE -DCMAKE_BUILD_TYPE=${BUILD_TYPE__} \
    -DCMAKE_CXX_COMPILER=${CXX_COMPILER__} \
    -DCMAKE_C_COMPILER=${C_COMPILER__} -DECC_IMPL=$ECC_IMPL__ ..

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
if [ ! -z "$RESET__" ]; then
    printf "%s\n" "Deleting the contents of $PWD"
    rm -r *
fi

printf "\n%s\n" "Compiling ${executable_dir}. Current directory is ${PWD}"

$CMAKE -DCMAKE_BUILD_TYPE=${BUILD_TYPE__} \
    -DCMAKE_CXX_COMPILER=${CXX_COMPILER__} \
    -DCMAKE_C_COMPILER=${C_COMPILER__} -DECC_IMPL=$ECC_IMPL__ ..

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
printf "\n%s\n%dmin %dsec\n\n" "EOSFactory has been successfully built." \
    $(($TIME_END/60)) $(($TIME_END%60))

printf "${bldred}%s${txtrst}" '
         _______  _______  _______     _______ 
        (  ____ \(  ___  )(  ____ \   (  _____|
        | (    \/| (   ) || (    \/   | (
        | (__    | |   | || (_____    | (___ 
        |  __)   | |   | |(_____  )   |  ___|
        | (      | |   | |      ) |   | (
        | (____/\| (___) |/\____) |   | (
        (_______/(_______)\_______)   (_)

'

if [ ! -z "$IS_WSL" ]; then
    printf "%s\n" "
RESTART the WSL bash terminal before using EOSFactory."
else
    printf "%s\n" "
RESTART the bash terminal before using EOSFactory or at least reload bashrc:
$ source ~/.bashrc
"
fi

printf "\n%s\n" "
VERIFY the EOSFactory installation by running the following command:
$ python3 ./tests/test1.py
"