cmake_minimum_required (VERSION 3.5)
# set(CMAKE_C_COMPILER "clang-4.0")
# set(CMAKE_CXX_COMPILER "clang++-4.0")

project ("teos")

set( VERSION_MAJOR 1 )
set( VERSION_MINOR 0 )
set( CMAKE_BUILD_TYPE "Debug" )
set( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed")

add_subdirectory( teos_lib )
add_subdirectory( teos )