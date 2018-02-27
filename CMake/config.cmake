message(STATUS 
"//////////////////////////////////////////////////////////////////////////////" )
message(STATUS "includes ${CMAKE_CURRENT_LIST_FILE}")

set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/../install")
message(STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}")
set(EOSIO_GIT_DIR "/mnt/hgfs/Workspaces/EOS/eos")
message(STATUS "EOSIO_GIT_DIR: ${EOSIO_GIT_DIR}")

if( WIN32 )
  set(EOSIO_INSTALL_DIR "E:/Workspaces/EOS/Logos/eos/buildWindows/install" )
else( WIN32 )
  set( EOSIO_INSTALL_DIR "/mnt/hgfs/Workspaces/EOS/Logos/eos/build/install" )
endif( WIN32 )
message( STATUS "EOSIO_INSTALL_DIR: ${EOSIO_INSTALL_DIR}" )

set( CMAKE_CXX_STANDARD 14 ) 
set( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_BUILD_TYPE Debug ) 

include_directories( "${CMAKE_INSTALL_PREFIX}/include" )
message( STATUS 
"//////////////////////////////////////////////////////////////////////////////" )

