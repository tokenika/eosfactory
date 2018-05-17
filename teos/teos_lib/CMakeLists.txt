cmake_minimum_required(VERSION 3.5)

set( LIB_NAME "teoslib" )

set( VERSION_MAJOR 1 )
set( VERSION_MINOR 0 )
set( CMAKE_BUILD_TYPE "Debug" )
set( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed")


set( EOSIO_CONTEXT_DIR "NOT DEFINED !!" )
set( EOSIO_SOURCE_DIR "NOT DEFINED !!" )
set( EOSIO_BINARY_DIR "NOT DEFINED !!" )

set( CMAKE_INSTALL_PREFIX "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB_PREFIX "NOT DEFINED !!" )

message(STATUS "APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules")

# 'common.cmake' sets Lgos common values:
# EOSIO_CONTEXT_DIR, EOSIO_SOURCE_DIR. EOSIO_BINARY_DIR, 
# CMAKE_INSTALL_PREFIX, 
# CMAKE_CXX_STANDARD, CMAKE_BUILD_TYPE, 
include( ../common.cmake ) 
if( NOT DEFINED EOSIO_SOURCE_DIR )
	message( FATAL_ERROR "Something is wrong with the 'commom.cmake' definition file"	)
endif()

list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules" )

message(STATUS "CMAKE_SYSTEM_NAME: ${CMAKE_SYSTEM_NAME}")

set( CONFIG_JSON_FILE "config.json" )
set( CONFIG_JSON "${CONFIG_JSON_FILE}" )

set( Boost_USE_STATIC_LIBS ON )
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
set( BOOST_ROOT "$ENV{HOME}/opt/boost_1_66_0" )

find_package(Boost 1.66 REQUIRED COMPONENTS 
  thread  
  date_time   
  filesystem  
  system
  program_options
  chrono
  regex
  iostreams
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  EOSIO_BOOST_INCLUDE_DIRS: ${EOSIO_BOOST_INCLUDE_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

set( OPENSSL_ROOT_DIR "/usr/local/Cellar/openssl/1.0.2o_1")
set( OPENSSL_USE_STATIC_LIBS TRUE)
find_package( OpenSSL REQUIRED )
if( OpenSSL_FOUND )
  message( STATUS "OpenSSL found.
  OPENSSL_INCLUDE_DIR: ${OPENSSL_INCLUDE_DIR}
  OPENSSL_LIBRARIES: ${OPENSSL_LIBRARIES}" )
else( OpenSSL_FOUND)
  message( STATUS "OpenSSL not found. set environment variables:
  OPENSSL_ROOT_DIR (for example, %C_INCLUDE%/OpenSSL/Win64OpenSSL-1_0_2L)" )
endif( OpenSSL_FOUND )

find_package(LLVM 4.0 REQUIRED CONFIG)
if( LLVM_FOUND )
  message( STATUS "LLVM found.
  LLVM_INCLUDE_DIR: ${LLVM_INCLUDE_DIR}
  LLVM_LIBRARY_DIR: ${LLVM_LIBRARY_DIR}")
else( LLVM_FOUND )
  message ( STATUS "LLVM not found. set environment variable:
  LLVM_ROOT_DIR (for example, %C_INCLUDE%/LLVM_4_0_1")
endif( LLVM_FOUND )
llvm_map_components_to_libnames(LLVM_LIBS support core passes mcjit native DebugInfoDWARF)

set(teoslib_src ${CMAKE_SOURCE_DIR}/../teos_lib)

if( NOT ECC_IMPL STREQUAL openssl )
  find_package(Secp256k1 REQUIRED)
  find_package(GMP REQUIRED)
endif()


file( GLOB HEADERS "include/teoslib/*.hpp" 
  "include/teoslib/command/*.hpp" "include/teoslib/control/*hpp" )
file( GLOB SRC "*cpp" "command/*.cpp" "control/*.cpp" )

add_library(${LIB_NAME} STATIC
  ${HEADERS}
  ${SRC}
  )

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${EOSIO_BOOST_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}

    ${EOSIO_SOURCE_DIR}/libraries/wasm-jit/Include
    ${EOSIO_SOURCE_DIR}/libraries/fc/include
    ${EOSIO_SOURCE_DIR}/libraries/appbase/include
    ${EOSIO_SOURCE_DIR}/libraries/utilities/include
    ${EOSIO_SOURCE_DIR}/libraries/softfloat/source/include
    ${EOSIO_SOURCE_DIR}/libraries/chain/include
    ${EOSIO_SOURCE_DIR}/libraries/types/include
    ${EOSIO_SOURCE_DIR}/libraries/chainbase/include
    ${EOSIO_SOURCE_DIR}/plugins/database_plugin/include
    ${EOSIO_SOURCE_DIR}/plugins/chain_plugin/include

  PUBLIC
    include
)

install ( TARGETS ${LIB_NAME} DESTINATION lib )
install( DIRECTORY include DESTINATION include )
install( FILES ${CONFIG_JSON_PATH} DESTINATION bin )
