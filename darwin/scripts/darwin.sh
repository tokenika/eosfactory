function setLinuxVariable() {
    name=$1
    value=$2
    if [  ! -z "$value" -a "${!name}" != "$value" ]; then
        echo "export $name=$value" >> ~/.bashrc
        printf "\t%s\n" "setting $name: $value"
    fi
}

function set_CXX_COMPILER__(){
    CXX_COMPILER__=clang
}

function set_C_COMPILER__(){
    C_COMPILER__=clang
}