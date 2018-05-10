message(STATUS 
"common eosfactory settings: ///////////////////////////////////////////////////////" )

set( EOS_FACTORY_EOS eos )

message( STATUS "CMAKE_SYSTEM_NAME: ${CMAKE_SYSTEM_NAME}" )
if( NOT DEFINED ENV{EOSIO_SOURCE_DIR} )
  message( FATAL_ERROR "
EOSIO_SOURCE_DIR environment variable has to be set, e.g. \
'EOSIO_SOURCE_DIR E:/Workspaces/EOS/eos/', for Windows file system." )
endif()
set( EOSIO_SOURCE_DIR "$ENV{EOSIO_SOURCE_DIR}" )
message( STATUS "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR}" )

set ( EOSIO_CONTEXT_DIR "${CMAKE_CURRENT_LIST_DIR}" )
message( STATUS "EOSIO_CONTEXT_DIR: ${EOSIO_CONTEXT_DIR}" )

if( WIN32 )
  set( CMAKE_INSTALL_PREFIX "${EOSIO_CONTEXT_DIR}/install/windows" )
  set( EOSIO_BINARY_DIR "${EOSIO_CONTEXT_DIR}/${EOS_FACTORY_EOS}/buildWindows" )
else( WIN32 )
  set( CMAKE_INSTALL_PREFIX "${EOSIO_CONTEXT_DIR}/install/ubuntu" )
  #set( EOSIO_BINARY_DIR "${EOSIO_CONTEXT_DIR}/${EOS_FACTORY_EOS}/build" )
  set( EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}/build" )
endif( WIN32 )
message( STATUS "EOSIO_BINARY_DIR: ${EOSIO_BINARY_DIR}" )
message( STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}" )

set( CMAKE_CXX_STANDARD 14 )
set( CXX_STANDARD_REQUIRED ON)
message( STATUS "CMAKE_CXX_STANDARD: ${CMAKE_CXX_STANDARD}" )

set( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_BUILD_TYPE Debug ) 

message( STATUS 
"//////////////////////////////////////////////////////////////////////////////" )

