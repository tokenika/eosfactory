cmake_minimum_required(VERSION 3.5)
project(arbitration_example VERSION 1.0.0)
include(CTest)

find_package(eosio.cdt)

### Generate the wasm and abi
add_contract( arbitration arbitration src/arbitration.cpp )

### add the path to where the ricardian contracts/clauses are found
target_compile_options( arbitration.wasm PUBLIC -R${CMAKE_CURRENT_SOURCE_DIR}/resources )

add_test( NAME tests COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/test1.py )

# ctest -V -R ^tests$