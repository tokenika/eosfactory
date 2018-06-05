cmake_minimum_required( VERSION 3.5 )

set(CMAKE_C_COMPILER "clang-4.0")
set(CMAKE_CXX_COMPILER "clang++-4.0")
# set(CMAKE_C_COMPILER "gcc-7")
# set(CMAKE_CXX_COMPILER "g++-7")

project ("@CONTRACT_NAME@")

set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14" )
set( C false CACHE BOOL "compile only")

include( CTest )

set( teos $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos/teos )
if( ${C})
    add_custom_target( wast ALL COMMAND ${teos} build contract ${CMAKE_SOURCE_DIR}/src -c )
else()
    add_custom_target( abi ALL COMMAND ${teos} generate abi ${CMAKE_SOURCE_DIR}/src )
    add_custom_target( wast ALL COMMAND ${teos} build contract ${CMAKE_SOURCE_DIR}/src )
endif()


add_subdirectory( test )

# ctest -V -R ^unittest$
# ctest -V -R ^test$
