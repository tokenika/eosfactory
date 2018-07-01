printf "%s\n" "
         source scripts/${OS_NAME}.sh
"

function setLinuxVariable() {
    name=$1
    value=$2
    config=$(grep -Po '"$name":.*?[^\\]",' $EOSIO_EOSFACTORY_DIR__/$config_json)
    if [ -z "$config"  -a ! -z "$value" -a "${!name}" != "$value" ]; then
        export $name=$value
        echo export $name=$value >> ~/.profile
        printf "\t%s\n" "setting $name: $value"
    fi
}

function set_CXX_COMPILER__(){
    CXX_COMPILER__=clang++-4.0
}

function set_C_COMPILER__(){
    C_COMPILER__=clang-4.0
}

function setCompilersAndDependencies(){
    export BOOST_ROOT=${U_HOME}/opt/boost
    export OPENSSL_ROOT_DIR=/usr/include/openssl
    export WASM_ROOT=${U_HOME}/opt/wasm   

    C_COMPILER__=clang-4.0
    CXX_COMPILER__=clang++-4.0
}