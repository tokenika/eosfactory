if [ $( uname ) == "Linux" ]; then
    source scripts/ubuntu.sh
else
    source scripts/darwin.sh
fi

set_CXX_COMPILER__
set_C_COMPILER__

cd build
rm -r *



cmake -DCMAKE_BUILD_TYPE="Debug" \
    -DCMAKE_CXX_COMPILER="${CXX_COMPILER__}" \
    -DCMAKE_C_COMPILER="${C_COMPILER__}" ..

make VERBOSE=1