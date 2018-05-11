function setLinuxVariable() {
    name=$1
    value=$2
    if [  ! -z "$value" -a "${!name}" != "$value" ]; then
        echo "export $name=$value" >> ~/.bash_profile
        printf "\t%s\n" "setting $name: $value"
    fi
}

function setCompilersAndDependencies(){
    export BOOST_ROOT=${HOME}/opt/boost_1_66_0
    export OPENSSL_ROOT_DIR=/usr/local/opt/openssl
    export WASM_ROOT=/usr/local/wasm

    C_COMPILER__=clang
    CXX_COMPILER__=clang++
}

