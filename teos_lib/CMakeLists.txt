cmake_minimum_required(VERSION 3.5)

set( LIB_NAME "teoslib" )

set( VERSION_MAJOR 1 )
set( VERSION_MINOR 0 )
set( CMAKE_BUILD_TYPE "Debug" )


set( LOGOS_DIR "NOT DEFINED !!" )
set( EOSIO_SOURCE_DIR "NOT DEFINED !!" )
set( EOSIO_BINARY_DIR "NOT DEFINED !!" )

set( CMAKE_INSTALL_PREFIX "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB_PREFIX "NOT DEFINED !!" )

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules")

# 'common.cmake' sets Lgos common values:
# LOGOS_DIR, EOSIO_SOURCE_DIR. EOSIO_BINARY_DIR, 
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

if( WIN32 )
  set( Boost_NO_SYSTEM_PATHS ON )
  set( BOOST_INCLUDEDIR $ENV{BOOST_INCLUDEDIR})
  message( STATUS "BOOST_INCLUDEDIR: $ENV{BOOST_INCLUDEDIR}")
  set( BOOST_LIBRARYDIR $ENV{BOOST_LIBRARYDIR} )
  message( STATUS "BOOST_LIBRARYDIR: $ENV{BOOST_LIBRARYDIR}")
endif( WIN32 )
find_package(Boost 1.66 REQUIRED COMPONENTS 
  system
  chrono
  date_time 
  program_options
  filesystem
  regex
  thread
  iostreams
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

file( GLOB HEADERS "include/teoslib/*.hpp" 
  "include/teoslib/command/*.hpp" "include/teoslib/control/*hpp" )
file( GLOB SRC "*cpp" "command/*.cpp" "control/*.cpp" )

add_library(${LIB_NAME} STATIC
  ${HEADERS}
  ${SRC}
  )

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIR}
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
