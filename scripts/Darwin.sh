printf "%s\n" "
         source scripts/${OS_NAME}.sh
"

function setLinuxVariable() {
    name=$1
    value=$2
    config=$(grep -Po '"$name":.*?[^\\]",' $EOSIO_EOSFACTORY_DIR__/$config_json)
    if [ -z "$config"  -a ! -z "$value" -a "${!name}" != "$value" ]; then
        export $name=$value
        echo export $name=$value >> ~/.bash_profile
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

