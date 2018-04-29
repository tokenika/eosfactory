#!/bin/bash
##########################################################################
# This script instals tokenika 'eosfactory' both both Linux and Windows
# (with WSL) computers.
# This file was downloaded from https://github.com/tokenika/eosfactory
##########################################################################

EOSIO_SOURCE_DIR_ARG=${EOSIO_SOURCE_DIR}
CXX_COMPILER=clang++
C_COMPILER=clang
BUILD_TYPE="Debug"

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
        printf "Usage:\n"
        printf "./build [-e <eosio repository dir>] [-c {gnu|clang}] [-h]\n"
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

printf "Arguments:\n"
printf "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR_ARG}\n"
printf "CXX_COMPILER=${CXX_COMPILER}\n"
printf "C_COMPILER=${C_COMPILER}\n"

WORK_DIR=$PWD
BUILD_DIR=${WORK_DIR}/build
TEMP_DIR=/tmp

ARCH=$( uname )
TIME_BEGIN=$( date -u +%s )

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)
eosfactory="eosfactory"
repository="https://github.com/tokenika/${eosfactory}"
wiki="https://github.com/tokenika/${eosfactory}/wiki"

if [ ! -d .git ]; then
    printf "\n\tThis build script only works with sources cloned from git\n"
    printf "\tPlease clone a new eos directory with 'git clone ${repository} --recursive'\n"
    printf "\tSee the wiki for instructions: ${wiki}\n"
    exit 1
fi

STALE_SUBMODS=$(( `git submodule status | grep -c "^[+\-]"` ))
if [ $STALE_SUBMODS -gt 0 ]; then
    printf "\ngit submodules are not up to date\n"
    printf "\tPlease run the command 'git submodule update --init --recursive'\n"
    exit 1
fi

printf "\n\tBeginning build"
printf "\t$( date -u )\n"
printf "\tgit head id: $( cat .git/refs/heads/master )\n"
printf "\tCurrent branch: $( git branch | grep \* )\n"
printf "\n\tARCHITECTURE: ${ARCH}\n"

if [ $ARCH == "Linux" ]; then
    
    if [ ! -e /etc/os-release ]; then
        printf "\n\t${eosfactory} currently is tested with the Windows Subsystem Linux and Ubuntu.\n"
        printf "\tPlease install on the latest version of one of these Linux distributions.\n"
        printf "\thttps://www.microsoft.com/en-us/store/p/ubuntu/9nblggh4msv6\n"
        printf "\thttps://www.ubuntu.com/\n"
        printf "\tExiting now.\n"
        exit 1
    fi

    OS_NAME=$( cat /etc/os-release | grep ^NAME | cut -d'=' -f2 | sed 's/\"//gI' )
    PROC_VERSION=$(cat /proc/version)
    if [[ $PROC_VERSION == *"Microsoft"* ]]; then 
        IS_WSL="IS_WSL"
        printf "\n\tDetected Windows Subsystem Linux\n"
    fi
fi	


if [ -z ${EOSIO_SOURCE_DIR_ARG+x} ]; then
    printf "\n\tEOSIO repository not found.\n"
    printf "Please, set environment variable 'EOSIO_SOURCE_DIR' pointing\n"
    pri
else
    printf "\n\tEOSIO repository: ${EOSIO_SOURCE_DIR}"
fi

cd ${WORK_DIR}
mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

if [ -z $CMAKE ]; then
    CMAKE=$( which cmake )
fi

# $CMAKE -DCMAKE_BUILD_TYPE=${BUILD_TYPE} 
#     -DCMAKE_CXX_COMPILER=${CXX_COMPILER} \
#     -DCMAKE_C_COMPILER=${C_COMPILER} \
# ..

if [ $? -ne 0 ]; then
    printf "\n\t>>>>>>>>>>>>>>>>>>>> CMAKE building EOSIO has exited with the above error.\n\n"
    exit -1
fi

#make -j${CPU_CORE}

if [ $? -ne 0 ]; then
    printf "\n\t>>>>>>>>>>>>>>>>>>>> MAKE building EOSIO has exited with the above error.\n\n"
    exit -1
fi

TIME_END=$(( `date -u +%s` - $TIME_BEGIN ))

printf "\n\tEOS FACTORY has been successfully built. %d:%d:%d\n\n" $(($TIME_END/3600)) $(($TIME_END%3600/60)) $(($TIME_END%60))
printf "\tTo verify your installation run the following commands:\n"
