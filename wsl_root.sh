#!/bin/bash

if [[ "$( uname -v )" != *"Microsoft"* ]]; then
    printf "%s" ""
    exit 0
fi

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
        return 0
    fi
    return 1
}

if [ ! -z "$1" ]; then
    WSL_ROOT="$1"
    verifyWslRoot "$1"
    if [ "$?" == 0 ]; then
        printf "%s" "$1"
        exit 0
    fi
    printf "%s" "$1"
    exit 1
fi

Lxss="hkcu\\Software\\Microsoft\\Windows\\CurrentVersion\\Lxss"
ddKey=$(reg.exe query $Lxss /v Defaultdistribution)
dd=$(echo $ddKey | grep -o -P '(?<={).*(?=})')
bpKey=$(reg.exe query "${Lxss}\\{$dd}" /v BasePath)
WSL_ROOT="$(echo $bpKey | \
                    grep -o -P '(?<=REG_SZ\s)[ A-Za-z0-9:\\\._]*')\\rootfs"

verifyWslRoot "${WSL_ROOT}"
if [ "$?" == 0 ]; then
    printf "%s" "${WSL_ROOT}"
    exit 0
fi
printf "%s" "${WSL_ROOT}"
exit 1


