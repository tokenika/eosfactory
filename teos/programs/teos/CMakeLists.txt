cmake_minimum_required (VERSION 3.8)
project ("teos")

set( VERSION_MAJOR 0 )
set( VERSION_MINOR 5 )
set( cmake_build_type debug )
set ( CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake" )
#include(cotire)
include( "${PROJECT_SOURCE_DIR}/CMake/config.cmake" )

set( TEST_ADDRESS "\"tokenika\"")
set( TEST_HOST "\"eos-testapi.tokenika.io\"" )
set( TEST_PORT "\"8888\"" )
set( CONFIG_JSON_FILE "teos_config.json" )
set( CONFIG_JSON_PATH "${CONFIG_JSON_FILE}" )
set( teos_HELPER_INSTALL_PATH "${CMAKE_SOURCE_DIR}/../eos/install" )

set( CONFIG_JSON "\"${CONFIG_JSON_PATH}\"" )
file( COPY ${CONFIG_JSON_PATH} DESTINATION "${CMAKE_BINARY_DIR}" )

set( LOGGING_DIR "\"log\"" )
configure_file (
   "${PROJECT_SOURCE_DIR}/teos_config.h.in"
   "${PROJECT_SOURCE_DIR}/teos_config.h"
   )
include_directories(${CMAKE_BINARY_DIR})

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

####################################### executables

macro( applLinkLibraries applName )

  target_sources( ${applName} 
    PRIVATE
      ${CMAKE_CURRENT_LIST_DIR}/teoslib/subcommands.hpp
      ${CMAKE_CURRENT_LIST_DIR}/teoslib/teos_command.hpp
      ${CMAKE_CURRENT_LIST_DIR}/teoslib/teos_get_commands.hpp
      ${CMAKE_CURRENT_LIST_DIR}/teoslib/teos_create_commands.hpp
      ${CMAKE_CURRENT_LIST_DIR}/teoslib/teos_wallet_commands.hpp
      ${CMAKE_CURRENT_LIST_DIR}/teoslib/teos_other_commands.hpp
  )

  target_include_directories( ${applName} 
    PRIVATE
     ${Boost_INCLUDE_DIR}
     ${OPENSSL_INCLUDE_DIR}
  )

  target_link_libraries( ${applName}
    PRIVATE
      teoslib
      teos_helper
      eos_types
      fc
      eos_utilities
  )

  if( NOT EOS_ECC_IMPL STREQUAL openssl )
    target_link_libraries( ${applName}
      PRIVATE
        ${SECP256K1_LIBRARIES}
        ${GMP_LIBRARIES}
    )
  endif()

  if( UNIX )
    set( pthread_library pthread )
    target_link_libraries( ${applName} PUBLIC rt )
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

endmacro( applLinkLibraries )

add_executable( teos teos.cpp )
applLinkLibraries( teos )
install( TARGETS teos RUNTIME DESTINATION bin)

add_executable( teos_lib_test teos_lib_test.cpp )
applLinkLibraries( teos_lib_test )
install( TARGETS teos_lib_test RUNTIME DESTINATION bin)

add_executable( teos_create_account 
  teos_create_account.cpp 
)
applLinkLibraries( teos_create_account )
install( TARGETS teos_create_account RUNTIME DESTINATION bin)

####################################### /executables

#cotire(${APPL_NAME})

