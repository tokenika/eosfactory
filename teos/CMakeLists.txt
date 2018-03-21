cmake_minimum_required (VERSION 3.8)
project ("teos")

set( VERSION_MAJOR 1 )
set( VERSION_MINOR 0 )
set( CMAKE_BUILD_TYPE "Debug" )


set( LOGOS_DIR "NOT DEFINED !!" )
set( EOSIO_SOURCE_DIR "NOT DEFINED !!" )
set( EOSIO_BINARY_DIR "NOT DEFINED !!" )

set( CMAKE_INSTALL_PREFIX "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB "NOT DEFINED !!" )
set( CMAKE_INSTALL_LIB_PREFIX "NOT DEFINED !!" )

option( ENABLE_ASAN "enable ASAN" OFF )
# 'common.cmake' sets Lgos common values:
# LOGOS_DIR, EOSIO_SOURCE_DIR. EOSIO_BINARY_DIR, 
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

if( WIN32 )
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
else( WIN32 )
	# Ensure that even static libraries are relocatable so they can be linked into a .so
  set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC" )

  if( ENABLE_ASAN )
    # TODO: hard codding, make it better! //////////////////////  
		#set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
	endif()

endif( WIN32 )

## BEGIN DEPENDENCIES ########################################################

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

if( WIN32 )
  add_library(__iob_func __iob_func.cpp )
endif()

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

## END DEPENDENCIES ##########################################################

if( WIN32 )
  set( WASM_CLANG "" )
  set( WASM_LLVM_LINK "" )
  set( WASM_LLC "" )
  set( BINARYEN_BIN "" )
else()
  set( WASM_CLANG "${HOME}/opt/wasm/bin/clang" )
  set( WASM_LLVM_LINK "${HOME}/opt/wasm/bin/llvm-link" )
  set( WASM_LLC "${HOME}/opt/wasm/bin/llc" )
  set( BINARYEN_BIN "/usr/local/binaryen/bin/" )
endif()

## BEGIN CONFIG FILES ########################################################

configure_file (
  "config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/teoslib/include/teoslib/config.h"
)

install( FILES "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.json" 
  DESTINATION "bin" )

install( FILES "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.json" 
  DESTINATION "bin" )

configure_file (
  "config.json.in"
  "${CMAKE_BINARY_DIR}/config.json"
)

## END CONFIG FILES ##########################################################

add_subdirectory(teoslib)

## BEGIN executables #########################################################

macro( applLinkLibraries applName )

  file(GLOB HEADERS "teoslib/include/*.hpp")
  target_sources( ${applName} 
    PRIVATE
      ${HEADERS}
  )

  target_include_directories( ${applName} 
    PRIVATE
     ${Boost_INCLUDE_DIR}
     ${OPENSSL_INCLUDE_DIR}
     include
     teoslib/include
  )

  if( ENABLE_ASAN )
    if( UNIX )
    target_link_libraries( ${applName} 
      PRIVATE 
        asan        # static-libasan ?
    )
    endif()
  endif()

  if( WIN32 )
    set( TARGET_DIR ${CMAKE_BUILD_TYPE} )
  else()
    set( TARGET_DIR "" )
  endif()

  target_link_libraries( ${applName} 
    PRIVATE
      teoslib
      ${EOSIO_BINARY_DIR}/plugins/chain_plugin/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chain_plugin${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/chain/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eosio_chain${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/chainbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chainbase${CMAKE_STATIC_LIBRARY_SUFFIX}  
      ${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}fc_debug${CMAKE_STATIC_LIBRARY_SUFFIX}        
      ${EOSIO_BINARY_DIR}/libraries/utilities/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eos_utilities${CMAKE_STATIC_LIBRARY_SUFFIX}      
      ${EOSIO_BINARY_DIR}/libraries/appbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}appbase${CMAKE_STATIC_LIBRARY_SUFFIX} 
      

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


  if( WIN32 )
    target_link_libraries( ${applName}
      PRIVATE
        "$(WindowsSDK_LibraryPath)/x64/crypt32.lib"
        "$(VC_ReferencesPath_VC_x64)/legacy_stdio_definitions.lib"
        "Userenv.lib"
        __iob_func
    )
  endif( WIN32 )

  if( UNIX )
  target_link_libraries( ${applName} 
    PRIVATE 
      rt 
      pthread
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


