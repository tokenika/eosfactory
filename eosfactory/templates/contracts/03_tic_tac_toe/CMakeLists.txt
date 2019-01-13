cmake_minimum_required(VERSION 3.5)
project(${CONTRACT_NAME}_example VERSION 1.0.0)
include(CTest)

find_package(eosio.cdt)

### Generate the wasm and abi
add_contract( ${CONTRACT_NAME} ${CONTRACT_NAME} src/${CONTRACT_NAME}.cpp )

### add the path to where the ricardian contracts/clauses are found
target_compile_options( ${CONTRACT_NAME}.wasm PUBLIC -R${CMAKE_CURRENT_SOURCE_DIR}/resources )

add_test( NAME tests COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/test1.py )
add_test( NAME unittest COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/unittest1.py )

# ctest -V -R ^unittest$
# ctest -V -R ^tests$