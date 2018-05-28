cmake_minimum_required (VERSION 3.5)
# set(CMAKE_C_COMPILER "clang-4.0")
# set(CMAKE_CXX_COMPILER "clang++-4.0")

project ("teos")

set( VERSION_MAJOR 1 )
set( VERSION_MINOR 0 )
set( CMAKE_BUILD_TYPE "Debug" )
set( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed")
option( ENABLE_ASAN "enable ASAN" OFF )
set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14" )
set( CMAKE_INSTALL_PREFIX "./install" )
set( BUILD_DOXYGEN TRUE )

if( NOT DEFINED ENV{EOSIO_SOURCE_DIR} )
  message( FATAL_ERROR "
EOSIO_SOURCE_DIR environment variable has to be set, e.g. \
'EOSIO_SOURCE_DIR /mnt/c/Workspaces/EOS/eos'" )
endif()
set( EOSIO_SOURCE_DIR "$ENV{EOSIO_SOURCE_DIR}" )
set( EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}/build" )

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeModules")

add_subdirectory( teos_lib )
add_subdirectory( teos )
