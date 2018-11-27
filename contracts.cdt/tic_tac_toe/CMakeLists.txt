cmake_minimum_required(VERSION 3.5)
project(hello_example VERSION 1.0.0)

find_package(eosio.cdt)

### Generate the wasm and abi
add_contract( tic_tac_toe tic_tac_toe src/tic_tac_toe.cpp )

### add the path to where the ricardian contracts/clauses are found
target_compile_options( tic_tac_toe.wasm PUBLIC -R${CMAKE_CURRENT_SOURCE_DIR}/resources )