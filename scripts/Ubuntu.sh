printf "%s\n" "
         source scripts/${OS_NAME}.sh
"

function setLinuxVariable() {
    name=$1
    value=$2
    if [  ! -z "$value" -a "${!name}" != "$value" ]; then
        export $name=$value
        echo export $name=$value >> ~/.bashrc
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
    export BOOST_ROOT=${HOME}/opt/boost_1_66_0
    export OPENSSL_ROOT_DIR=/usr/include/openssl
    export WASM_ROOT=${HOME}/opt/wasm   

    C_COMPILER__=clang-4.0
    CXX_COMPILER__=clang++-4.0
}