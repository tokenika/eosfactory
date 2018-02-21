cmake_minimum_required (VERSION 3.8)
project ("teos")

set( VERSION_MAJOR 0 )
set( VERSION_MINOR 6 )
set( CMAKE_BUILD_TYPE "Debug" )
set ( CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake" )
#include(cotire)
include( "${PROJECT_SOURCE_DIR}/CMake/config.cmake" )

set( TEST_ADDRESS "\"tokenika\"")
set( TEST_HOST "\"eos-testapi.tokenika.io\"" )
set( TEST_PORT "\"8888\"" )
set( CONFIG_JSON_FILE "config.json" )
set( CONFIG_JSON_PATH "${CONFIG_JSON_FILE}" )
set( CONFIG_JSON "\"${CONFIG_JSON_PATH}\"" )
set( LOGGING_DIR "\"log\"" )

configure_file (
  "config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.h"
)

if( WIN32 )
  add_definitions( -D_WIN32_WINNT=0x0501 )
  add_compile_options( /std:c++14 )
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
  thread
  system 
  date_time 
  program_options 
  filesystem
  chrono
  regex
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}
  Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}
  ")
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-msvc-14.1)
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)
  " )
endif( Boost_FOUND )

if( NOT WIN32 AND NOT APPLE)
  find_package(Threads REQUIRED)
endif()

add_subdirectory(teoslib)
configure_file (
  "config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/teoslib/include/teoslib/config.h"
)

####################################### executables

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
     ${CMAKE_SOURCE_DIR}/libraries/wasm-jit/include
  )

  if( UNIX )
  target_link_libraries( ${applName} 
    PRIVATE 
      asan        # static-libasan ?
      rt 
      pthread
  )
  endif()

  target_link_libraries( ${applName}
    PRIVATE
      teoslib
			chain_plugin
			database_plugin
      chainbase
      eos_types
      eos_chain
      eos_utilities
      appbase
      fc
			IR
			WAST
			WASM
			Runtime
  )

  if( NOT EOS_ECC_IMPL STREQUAL openssl )
    target_link_libraries( ${applName}
      PRIVATE
        ${SECP256K1_LIBRARIES}
        ${GMP_LIBRARIES}
    )
  endif()

  if( WIN32 )
    if( NOT EOS_ECC_IMPL STREQUAL openssl )
      target_link_libraries( ${applName}
        PRIVATE
          ${SECP256K1_LIBRARIES_DIR}/gcc.lib
      )
    endif()

    target_link_libraries( ${applName}
      PRIVATE
        "$(WindowsSDK_LibraryPath)/x64/crypt32.lib"
        "$(VC_ReferencesPath_VC_x64)/legacy_stdio_definitions.lib"
        "Userenv.lib"
        __iob_func
    )
  endif( WIN32 )

  target_link_libraries( ${applName}
    PRIVATE
      ${OPENSSL_LIBRARIES}
      ${Boost_LIBRARIES}
      ${CMAKE_DL_LIBS}
      ${CMAKE_THREAD_LIBS_INIT}
  )

  install( FILES ${CONFIG_JSON_PATH} DESTINATION bin )

endmacro( applLinkLibraries )

add_executable( teos teos.cpp teos_test.cpp )
applLinkLibraries( teos )
install( TARGETS teos RUNTIME DESTINATION bin)

add_executable( teos_lib_test teos_lib_test.cpp )
applLinkLibraries( teos_lib_test )
install( TARGETS teos_lib_test RUNTIME DESTINATION bin)

####################################### /executables

#cotire(${APPL_NAME})

