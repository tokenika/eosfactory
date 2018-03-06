cmake_minimum_required( VERSION 3.8 )
project( eos )

set(VERSION_MAJOR 0)
set(VERSION_MINOR 5)
set( CMAKE_BUILD_TYPE "Debug" )

message(STATUS 
"//////////////////////////////////////////////////////////////////////////////" )

if( NOT DEFINED ENV{EOSIO_SOURCE_DIR} )
  message( FATAL_ERROR "
EOSIO_SOURCE_DIR environment variable has to be set, for example: EOSIO_SOURCE_DIR=E:/Workspaces/EOS/eos/" )
endif()
#set( EOSIO_SOURCE_DIR "$ENV{EOSIO_SOURCE_DIR}" )
set( EOSIO_SOURCE_DIR "E:/Workspaces/EOS/eos" )

set ( LOGOS_DIR "${CMAKE_SOURCE_DIR}/.." )
if( WIN32 )
  set( EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}/buildWindows")
  set( CMAKE_INSTALL_PREFIX "${LOGOS_DIR}/install/windows" )
else( WIN32 )
  set( EOSIO_BINARY_DIR "${EOSIO_SOURCE_DIR}/build" )
  set( CMAKE_INSTALL_PREFIX "${LOGOS_DIR}/install/ubuntu" )
endif( WIN32 )

message(STATUS "EOSIO_SOURCE_DIR: ${EOSIO_SOURCE_DIR}")
message( STATUS "EOSIO_INSTALL_DIR: ${EOSIO_INSTALL_DIR}" )
message(STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}")

set( CMAKE_CXX_STANDARD 14 ) 
set( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_BUILD_TYPE Debug ) 

include_directories( "${CMAKE_INSTALL_PREFIX}/include" )
message( STATUS 
"//////////////////////////////////////////////////////////////////////////////" )

# if openssl, Secp256k1 and gmp not needed:
set( EOS_ECC_IMPL openssl ) ## secp256k1 or openssl or mixed

set( EOS_BUILD_RANGE all ) ## teos or all
set( CMAKE_BUILD_TYPE "Debug" )
set( CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/../install/eos )

set( CMAKE_CXX_STANDARD 17 )
set( BUILD_SHARED_LIBS NO )
set( BUILD_DOXYGEN TRUE )
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules" )

message(STATUS "CMAKE_SYSTEM_NAME: ${CMAKE_SYSTEM_NAME}")

if( WIN32 )
  add_definitions( -D_WIN32_WINNT=0x0501 -D_CRT_SECURE_NO_WARNINGS)
  add_compile_options( /std:c++14 )
  add_compile_options( /bigobj )
endif( WIN32 )

if( MSVC )
	# Taken out of the VC projects to avoid the compiler complaining about POSIX code
	add_definitions( -D_SCL_SECURE_NO_WARNINGS )
	add_definitions( -D_SCL_SECURE_NO_DEPRECATE )
	add_definitions( -D_CRT_SECURE_NO_WARNINGS )
	add_definitions( -D_CRT_SECURE_N_DEPRECATE )
	add_definitions( -D_CRT_NONSTDC_NO_DEPRECATE )
	add_definitions( -D_CRT_NONSTDC_NO_WARNINGS )
	add_definitions( -D__STDC_CONSTANT_MACROS )
	add_definitions( -D__STDC_FORMAT_MACROS )
	add_definitions( -D__STDC_LIMIT_MACROS )
	add_definitions( -D_WIN32_WINNT=0x0501 )
	#treats warning as error - No
  add_compile_options( /WX- )
  
  add_compile_options( /bigobj )

  	# Compile with all warnings and fatal warnings
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /WX" )
	if( CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
		string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}" )
	else()
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4" )
	endif()

	# disable warning: conditional expression is constant
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4127" )
	# disable warning: unreferenced formal parameter
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4100" )
	# disable warning: assignment operator could not be generated
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4512" )
	# disable warning: 'typedef ': ignored on left of '' when no variable is declared
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4091" )
	# disable warning: 'inline': used more than once
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4141" )
	# disable warning: cast truncates constant value
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4310" )
	# disable warning: unreachable code
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4702" )
	# disable warning: The result of the unary '&' operator may be unaligned
	set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4366" )
else( MSVC )
	# Ensure that even static libraries are relocatable so they can be linked into a .so
  set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC" )
  
	# Enable asan in debug builds.
	if( CMAKE_BUILD_TYPE MATCHES "Debug" )
		option( ENABLE_ASAN "enable ASAN" ON )
		add_definitions( "-D_DEBUG" )
	else()
		option( ENABLE_ASAN "enable ASAN" OFF )
	endif()
	if( ENABLE_ASAN )
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
	endif()
endif( MSVC )


####################################### DEPENDENCIES

# set( Boost_USE_STATIC_LIBS ON )
# set( Boost_USE_MULTITHREADED ON )
# set( Boost_USE_STATIC_RUNTIME OFF )
# set( BOOST_ROOT $ENV{HOME}/opt/boost_1_64_0 )
# if( WIN32 )
#   set( Boost_NO_SYSTEM_PATHS ON )
#   set( BOOST_INCLUDEDIR $ENV{BOOST_INCLUDEDIR})
#   message( STATUS "BOOST_INCLUDEDIR: $ENV{BOOST_INCLUDEDIR}")
#   set( BOOST_LIBRARYDIR $ENV{BOOST_LIBRARYDIR} )
#   message( STATUS "BOOST_LIBRARYDIR: $ENV{BOOST_LIBRARYDIR}")
# endif( WIN32 )
# find_package(Boost 1.62 REQUIRED COMPONENTS 
#   system
#   chrono
#   date_time 
#   program_options
#   filesystem
#   regex
#   thread
# )
# if( Boost_FOUND )
#   message( STATUS "Boost found.
#   Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}
#   Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}" )
# else( Boost_FOUND )
#   message ( STATUS "Boost not found. set environment variables:
#   BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-msvc-14.1)
#   BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
# endif( Boost_FOUND )

# set( OPENSSL_USE_STATIC_LIBS TRUE)
# find_package( OpenSSL REQUIRED )
# if( OpenSSL_FOUND )
#   message( STATUS "OpenSSL found.
#   OPENSSL_INCLUDE_DIR: ${OPENSSL_INCLUDE_DIR}
#   OPENSSL_LIBRARIES: ${OPENSSL_LIBRARIES}" )
# else( OpenSSL_FOUND)
#   message( STATUS "OpenSSL not found. set environment variables:
#   OPENSSL_ROOT_DIR (for example, %C_INCLUDE%/OpenSSL/Win64OpenSSL-1_0_2L)" )
# endif( OpenSSL_FOUND )

# if openssl, Secp256k1 and gmp not needed:
# if( NOT EOS_ECC_IMPL STREQUAL openssl )
#   find_package(GMP REQUIRED)
#   if( GMP_FOUND )
#     message( STATUS "gmp found.
#     GMP_INCLUDE_DIR: ${GMP_INCLUDE_DIR}
#     GMP_LIBRARIES: ${GMP_LIBRARIES}    
#     " )
#   else( GMP_FOUND )
#     message( STATUS "gmp not found. set environment variables:
#     GMP_DIR (for example, E:/C_INCLUDE/gmp)" )
#   endif( GMP_FOUND )

#   find_package(Secp256k1 REQUIRED)
#   if( SECP256K1_FOUND )
#     message( STATUS "Secp256k1 found.
#     SECP256K1_INCLUDE_DIR: ${SECP256K1_INCLUDE_DIR}
#     SECP256K1_LIBRARIES: ${SECP256K1_LIBRARIES}" )
#   else( SECP256K1_FOUND )
#     message( STATUS "Secp256k1 not found. set environment variables:
#     SECP256K1_DIR (for example, E:/C_INCLUDE/secp256k1)" )
#   endif( SECP256K1_FOUND )
# endif( NOT EOS_ECC_IMPL STREQUAL openssl )

####################################### /DEPENDENCIES

add_subdirectory( libraries )
#add_subdirectory( plugins )
