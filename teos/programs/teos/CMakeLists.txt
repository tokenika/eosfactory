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
  system 
  date_time 
  program_options 
  filesystem
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

set(APPL_NAME "teos")
add_executable(${APPL_NAME} teos.cpp )
target_include_directories( ${APPL_NAME} 
  PRIVATE
  ${BOOST_INCLUDEDIR}
)
target_link_libraries( ${APPL_NAME}
  PRIVATE
  teoslib
  teos_helper
)

#cotire(${APPL_NAME})

install( TARGETS ${APPL_NAME} RUNTIME DESTINATION bin)
