#!/usr/bin/env bash
export PROJECT_DIR=$( dirname "${BASH_SOURCE[0]}" )
export ROOT_DIR=${PROJECT_DIR}/..

set -eo pipefail

CDT_DIR_PROMPT=/usr/local/amax.cdt

function usage() {
   printf "Usage: $0 OPTION...
  -c DIR      Directory where AMAX.CDT is installed. (Default: /usr/local/amax.cdt)
  -t          Build unit tests.
  -h          Print this help menu.
   \\n" "$0" 1>&2
   exit 1
}

  # -e DIR      Directory where AMAX is installed. (Default: $HOME/amax/X.Y)

if [ $# -ne 0 ]; then
  while getopts "e:c:tyh" opt; do
    case "${opt}" in
      c )
        CDT_DIR_PROMPT=$OPTARG
      ;;
      h )
        usage
      ;;
      ? )
        echo "Invalid Option!" 1>&2
        usage
      ;;
      : )
        echo "Invalid Option: -${OPTARG} requires an argument." 1>&2
        usage
      ;;
      * )
        usage
      ;;
    esac
  done
fi


# if [[ -z $CDT_DIR_PROMPT ]]; then
#   echo 'ERROR: No AMAX.CDT location was specified.'
#   exit 1
# fi

# Include CDT_INSTALL_DIR in CMAKE_FRAMEWORK_PATH
echo "Using AMAX.CDT installation at: $CDT_INSTALL_DIR"
export CMAKE_FRAMEWORK_PATH="${CDT_INSTALL_DIR}:${CMAKE_FRAMEWORK_PATH}"



printf "\t=========== Building amax.contracts ===========\n\n"
RED='\033[0;31m'
NC='\033[0m'
CPU_CORES=$(getconf _NPROCESSORS_ONLN)
mkdir -p build
pushd build &> /dev/null
cmake  ../
make -j $CPU_CORES
popd &> /dev/null
