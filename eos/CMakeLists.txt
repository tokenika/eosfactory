cmake_minimum_required( VERSION 3.8 )
project( eos )

set(VERSION_MAJOR 0)
set(VERSION_MINOR 5)
set( EOS_ECC_IMPL secp256k1 ) ## secp256k1 or openssl or mixed
set( EOS_BUILD_RANGE all ) ## teos or all
set( CMAKE_BUILD_TYPE "Debug" )
set( CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/install)

set( CMAKE_CXX_STANDARD 14 )
set( BUILD_SHARED_LIBS NO )
set( BUILD_DOXYGEN TRUE )
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules" )

message(STATUS "CMAKE_SYSTEM_NAME: ${CMAKE_SYSTEM_NAME}")

if( WIN32 )
  add_definitions( -D_WIN32_WINNT=0x0501 -D_CRT_SECURE_NO_WARNINGS)
  add_compile_options( /std:c++14 )
  add_compile_options( /bigobj )
endif( WIN32 )

####################################### DEPENDENCIES

set( Boost_USE_STATIC_LIBS ON )
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
set( BOOST_ROOT $ENV{HOME}/opt/boost_1_64_0 )
if( WIN32 )
  set( Boost_NO_SYSTEM_PATHS ON )
  set( BOOST_INCLUDEDIR $ENV{BOOST_INCLUDEDIR})
  message( STATUS "BOOST_INCLUDEDIR: $ENV{BOOST_INCLUDEDIR}")
  set( BOOST_LIBRARYDIR $ENV{BOOST_LIBRARYDIR} )
  message( STATUS "BOOST_LIBRARYDIR: $ENV{BOOST_LIBRARYDIR}")
endif( WIN32 )
find_package(Boost 1.62 REQUIRED COMPONENTS 
  system
  chrono
  date_time 
  program_options
  filesystem
  regex
  thread
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}
  Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-msvc-14.1)
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

if( NOT EOS_ECC_IMPL STREQUAL openssl )
  find_package(GMP REQUIRED)
  if( GMP_FOUND )
    message( STATUS "gmp found.
    GMP_INCLUDE_DIR: ${GMP_INCLUDE_DIR}
    GMP_LIBRARIES: ${GMP_LIBRARIES}    
    " )
  else( GMP_FOUND )
    message( STATUS "gmp not found. set environment variables:
    GMP_DIR (for example, E:/C_INCLUDE/gmp)" )
  endif( GMP_FOUND )

  find_package(Secp256k1 REQUIRED)
  if( SECP256K1_FOUND )
    message( STATUS "Secp256k1 found.
    SECP256K1_INCLUDE_DIR: ${SECP256K1_INCLUDE_DIR}
    SECP256K1_LIBRARIES: ${SECP256K1_LIBRARIES}" )
  else( SECP256K1_FOUND )
    message( STATUS "Secp256k1 not found. set environment variables:
    SECP256K1_DIR (for example, E:/C_INCLUDE/secp256k1)" )
  endif( SECP256K1_FOUND )
endif( NOT EOS_ECC_IMPL STREQUAL openssl )

####################################### /DEPENDENCIES

add_subdirectory( libraries )
add_subdirectory( plugins )
#add_subdirectory( programs/teos )
