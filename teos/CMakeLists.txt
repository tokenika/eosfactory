cmake_minimum_required (VERSION 3.5)
# set(CMAKE_C_COMPILER "clang-4.0")
# set(CMAKE_CXX_COMPILER "clang++-4.0")

project ("teos")

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

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules")

option( ENABLE_ASAN "enable ASAN" OFF )
# 'common.cmake' sets Lgos common values:
# EOSIO_CONTEXT_DIR, EOSIO_SOURCE_DIR. EOSIO_BINARY_DIR, 
# CMAKE_INSTALL_PREFIX, 
# CMAKE_CXX_STANDARD, CMAKE_BUILD_TYPE, 
include( ../common.cmake ) 
if( NOT DEFINED EOSIO_SOURCE_DIR )
	message( FATAL_ERROR "Something is wrong with the 'commom.cmake' definition file"	)
endif()


set( BUILD_SHARED_LIBS NO )
set( BUILD_DOXYGEN TRUE )
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules" )

message(STATUS "CMAKE_SYSTEM_NAME: ${CMAKE_SYSTEM_NAME}")

set( TEST_ADDRESS "tokenika")
set( TEST_HTTP_ADDRESS "eos-testapi.tokenika.io:8888" )
set( CONFIG_JSON_FILE "config.json" )
set( CONFIG_JSON "${CONFIG_JSON_FILE}" )

# Ensure that even static libraries are relocatable so they can be linked into a .so
set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC" )

if( ENABLE_ASAN )
  # TODO: hard codding, make it better! //////////////////////  
  #set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
endif()


## BEGIN DEPENDENCIES ########################################################

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
  EOSIO_BOOST_INCLUDE_DIRS: ${EOSIO_BOOST_INCLUDE_DIRS}
  Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-WIN32-14.1)
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

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

## END DEPENDENCIES ##########################################################

# set( EOSIO_WASM_CLANG "\${HOME}/opt/wasm/bin/clang" )
# set( EOSIO_WASM_LLVM_LINK "\${HOME}/opt/wasm/bin/llvm-link" )
# set( EOSIO_WASM_LLC "\${HOME}/opt/wasm/bin/llc" )
# set( EOSIO_BINARYEN_BIN "/usr/local/binaryen/bin/" )

## BEGIN CONFIG FILES ########################################################

configure_file (
  "config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.h"
)

configure_file (
  "config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/../teos_lib/include/teoslib/config.h"
)

install( FILES "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.json" 
  DESTINATION "bin" )

install( FILES "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.json" 
  DESTINATION "bin" )

configure_file (
  "config.json.in"
  "${CMAKE_BINARY_DIR}/config.json"
)

## END CONFIG FILES #########################################################

## BEGIN executables #########################################################

macro( applLinkLibraries applName )

  file(GLOB HEADERS "${teoslib_src}/include/teoslib/*.hpp")
  target_sources( ${applName} 
    PRIVATE
      ${HEADERS}
  )

  target_include_directories( ${applName} 
    PRIVATE
      ${EOSIO_BOOST_INCLUDE_DIR}
      ${OPENSSL_INCLUDE_DIR}
      include
      "${teoslib_src}/include"
  )

  if( ENABLE_ASAN )
    if( UNIX )
    target_link_libraries( ${applName} 
      PRIVATE 
        asan        # static-libasan ?
    )
    endif()
  endif()

  set( TARGET_DIR "" )
 
  if(EXISTS "${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}fc_debug${CMAKE_STATIC_LIBRARY_SUFFIX}")
    set(fc "fc_debug")
  endif()
  if(EXISTS "${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}fc${CMAKE_STATIC_LIBRARY_SUFFIX}")
    set(fc "fc")
  endif()  

  target_link_libraries( ${applName} 
    PRIVATE
      ${teoslib_src}/build/libteoslib.a
      ${EOSIO_BINARY_DIR}/plugins/chain_plugin/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chain_plugin${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/chain/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eosio_chain${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/chainbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chainbase${CMAKE_STATIC_LIBRARY_SUFFIX}        
      ${EOSIO_BINARY_DIR}/libraries/utilities/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eos_utilities${CMAKE_STATIC_LIBRARY_SUFFIX}      
      ${EOSIO_BINARY_DIR}/libraries/appbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}appbase${CMAKE_STATIC_LIBRARY_SUFFIX} 
      ${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}${fc}${CMAKE_STATIC_LIBRARY_SUFFIX}       

      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Emscripten/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Emscripten${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Runtime/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Runtime${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/WAST/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}WAST${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/WASM/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}WASM${CMAKE_STATIC_LIBRARY_SUFFIX}      
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/IR/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}IR${CMAKE_STATIC_LIBRARY_SUFFIX}       
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Logging/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Logging${CMAKE_STATIC_LIBRARY_SUFFIX} 
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Platform/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Platform${CMAKE_STATIC_LIBRARY_SUFFIX}
  )

  target_link_libraries( ${applName}
    PRIVATE
      ${OPENSSL_LIBRARIES}
      ${Boost_LIBRARIES}
      ${LLVM_LIBS}
      ${CMAKE_DL_LIBS}
      ${CMAKE_THREAD_LIBS_INIT}
  )

  set(THREADS_PREFER_PTHREAD_FLAG ON)
  find_package(Threads REQUIRED)
  target_link_libraries(${applName} 
    PRIVATE
      Threads::Threads
  )

  if( NOT ECC_IMPL STREQUAL openssl )
    target_link_libraries( ${applName}
      PRIVATE
        ${Secp256k1_LIBRARY}
        ${GMP_LIBRARIES}
    )
  endif()

endmacro( applLinkLibraries )

add_executable( teos teos.cpp )
applLinkLibraries( teos )
install( TARGETS teos RUNTIME DESTINATION bin)

add_executable( teos_lib_test teos_lib_test.cpp )
applLinkLibraries( teos_lib_test )
install( TARGETS teos_lib_test RUNTIME DESTINATION bin)

## END executables ###########################################################


