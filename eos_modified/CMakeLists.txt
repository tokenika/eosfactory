cmake_minimum_required( VERSION 3.8 )
project( eos )

set(VERSION_MAJOR 0)
set(VERSION_MINOR 5)

set( LOGOS_DIR "NOT DEFINED !!" )
set( EOSIO_SOURCE_DIR "NOT DEFINED !!" )
set( EOSIO_BINARY_DIR "NOT DEFINED !!" )

set( CMAKE_INSTALL_PREFIX "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB_PREFIX "NOT DEFINED !!" )

option( ENABLE_ASAN "enable ASAN" OFF )
# LOGOS_DIR, EOSIO_SOURCE_DIR. EOSIO_BINARY_DIR, 
# CMAKE_INSTALL_PREFIX,
# CMAKE_CXX_STANDARD, CMAKE_BUILD_TYPE, 
include( ../common.cmake ) 
if( NOT DEFINED EOSIO_SOURCE_DIR )
	message( FATAL_ERROR "Something is wrong with the 'commom.cmake' definition file"	)
endif()

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
  
	if( ENABLE_ASAN )
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
	endif()
endif( MSVC )

add_subdirectory( libraries )
add_subdirectory( plugins )
