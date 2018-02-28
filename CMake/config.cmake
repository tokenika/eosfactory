message(STATUS 
"//////////////////////////////////////////////////////////////////////////////" )
message(STATUS "includes ${CMAKE_CURRENT_LIST_FILE}")

set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/../install")
message(STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}")

if( WIN32 )
  set(EOSIO_SOURCE_DIR "E:/Workspaces/EOS/Logos/eos")
  set(EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}/buildWindows")
  set(EOSIO_INSTALL_DIR "E:/Workspaces/EOS/Logos/eos/buildWindows/install" )
else( WIN32 )
  set(EOSIO_SOURCE_DIR "/mnt/hgfs/Workspaces/EOS/eos")
  set(EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}/build")
  set( EOSIO_INSTALL_DIR "/mnt/hgfs/Workspaces/EOS/Logos/eos/build/install" )
endif( WIN32 )

message(STATUS "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR}")
message( STATUS "EOSIO_INSTALL_DIR: ${EOSIO_INSTALL_DIR}" )

set( CMAKE_CXX_STANDARD 14 ) 
set( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_BUILD_TYPE Debug ) 

include_directories( "${CMAKE_INSTALL_PREFIX}/include" )
message( STATUS 
"//////////////////////////////////////////////////////////////////////////////" )

