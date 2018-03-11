message(STATUS 
"common Logos settings: ///////////////////////////////////////////////////////" )

set( LOGOS_EOS eos )

if( NOT DEFINED ENV{EOSIO_SOURCE_DIR} )
  message( FATAL_ERROR "
EOSIO_SOURCE_DIR environment variable has to be set, e.g. \
'EOSIO_SOURCE_DIR E:/Workspaces/EOS/eos/', for Windows file system." )
endif()
set( EOSIO_SOURCE_DIR "$ENV{EOSIO_SOURCE_DIR}" )
message( STATUS "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR}" )

set ( LOGOS_DIR "${CMAKE_CURRENT_LIST_DIR}" )
message( STATUS "LOGOS_DIR: ${LOGOS_DIR}" )

if( WIN32 )
  set( CMAKE_INSTALL_PREFIX "${LOGOS_DIR}/install/windows" )
  set( EOSIO_BINARY_DIR "${LOGOS_DIR}/${LOGOS_EOS}/buildWindows" )
else( WIN32 )
  set( CMAKE_INSTALL_PREFIX "${LOGOS_DIR}/install/ubuntu" )
  #set( EOSIO_BINARY_DIR "${LOGOS_DIR}/${LOGOS_EOS}/build" )
  set( EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}build" )
endif( WIN32 )
message( STATUS "EOSIO_BINARY_DIR: ${EOSIO_BINARY_DIR}" )
message( STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}" )


set( CMAKE_CXX_STANDARD 14 ) 
set( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_BUILD_TYPE Debug ) 

message( STATUS 
"//////////////////////////////////////////////////////////////////////////////" )

