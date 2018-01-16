cmake_minimum_required (VERSION 3.8)
project ("Tokenika_Eosc")

set(VERSION_MAJOR 0)
set(VERSION_MINOR 5)
set(cmake_build_type debug)
set (CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake")
include(cotire)
include("${PROJECT_SOURCE_DIR}/CMake/config.cmake")

set(VERSION_MAJOR 0)
set(VERSION_MINOR 5)
set(CONFIG_JSON_FILE "eosc_config.json")
set(CONFIG_JSON_PATH "${CONFIG_JSON_FILE}")
set(EOSC_HELPER_INSTALL_PATH "${CMAKE_SOURCE_DIR}/../eos/install" )

set(CONFIG_JSON "\"${CONFIG_JSON_PATH}\"")
file(COPY ${CONFIG_JSON_PATH} DESTINATION "${CMAKE_BINARY_DIR}")

set(LOGGING_DIR "\"log\"")
configure_file (
   "${PROJECT_SOURCE_DIR}/eosc_config.h.in"
   "${PROJECT_SOURCE_DIR}/eosc_config.h"
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

add_subdirectory(eosclib)

set(APPL_NAME "eosc")
add_executable(${APPL_NAME} eosc.cpp )
target_include_directories( ${APPL_NAME} 
  PRIVATE
  ${BOOST_INCLUDEDIR}
)
target_link_libraries( ${APPL_NAME}
  PRIVATE
  eosclib 
)

add_executable( "eosc_lib_test" eoec_lib_test.cpp )
target_link_libraries( "eosc_lib_test" 
  PRIVATE
  eosclib
)

#######################################

set( APPL_NAME "testxx" )
add_executable( ${APPL_NAME} test.cpp )

find_path( HELPER_INCLUDE "eosc_helper.hpp" 
  HINTS "${EOSC_HELPER_INSTALL_PATH}/include")
if( HELPER_INCLUDE )
  message( STATUS "HELPER_INCLUDE: ${HELPER_INCLUDE}" )
  target_include_directories( ${APPL_NAME}
    PUBLIC
    ${HELPER_INCLUDE}
  )
else()
  message( STATUS "
Cannot find the eosc helper includs path (where is eosc_helper.hpp header), 
namely \${EOSC_HELPER_INSTALL_PATH}/include
Please, set the path to this library in the top-level CMakeLists.txt as the
argument to the variable EOSC_HELPER_INSTALL_PATH.
The current value of EOSC_HELPER_INSTALL_PATH is ${EOSC_HELPER_INSTALL_PATH}  
  ")
  return()
endif()

if( WIN32 )
  set( HELPER_LIB_NAME eosc_helper.lib )
else()
  set( HELPER_LIB_NAME libeosc_helper.a )
endif()

find_file( HELPER_LIB ${HELPER_LIB_NAME} "${EOSC_HELPER_INSTALL_PATH}/lib")
if( HELPER_LIB )
message( STATUS "HELPER_LIB: ${HELPER_LIB}")
  target_link_libraries( ${APPL_NAME}
    PRIVATE
    ${HELPER_LIB}
  )
else()
  message( STATUS "
Cannot find the eosc helper library, 
namely \${EOSC_HELPER_INSTALL_PATH}/lib/${HELPER_LIB_NAME}
Please, set the path to this library in the top-level CMakeLists.txt as the
argument to the variable EOSC_HELPER_INSTALL_PATH.
The current value of EOSC_HELPER_INSTALL_PATH is ${EOSC_HELPER_INSTALL_PATH}  
  ")set( APPL_NAME "testxx" )
  add_executable( ${APPL_NAME} test.cpp )
  
  find_path( HELPER_INCLUDE "eosc_helper.hpp" 
    HINTS "${EOSC_HELPER_INSTALL_PATH}/include")
  if( HELPER_INCLUDE )
    message( STATUS "HELPER_INCLUDE: ${HELPER_INCLUDE}" )
    target_include_directories( ${APPL_NAME}
      PUBLIC
      ${HELPER_INCLUDE}
    )
  else()
    message( STATUS "
  Cannot find the eosc helper includs path (where is eosc_helper.hpp header), 
  namely \${EOSC_HELPER_INSTALL_PATH}/include
  Please, set the path to this library in the top-level CMakeLists.txt as the
  argument to the variable EOSC_HELPER_INSTALL_PATH.
  The current value of EOSC_HELPER_INSTALL_PATH is ${EOSC_HELPER_INSTALL_PATH}  
    ")
    return()
  endif()
  
  if( WIN32 )
    set( HELPER_LIB_NAME eosc_helper.lib )
  else()
    set( HELPER_LIB_NAME libeosc_helper.a )
  endif()
  
  find_file( HELPER_LIB ${HELPER_LIB_NAME} "${EOSC_HELPER_INSTALL_PATH}/lib")
  if( HELPER_LIB )
  message( STATUS "HELPER_LIB: ${HELPER_LIB}")
    target_link_libraries( ${APPL_NAME}
      PRIVATE
      ${HELPER_LIB}
    )
  else()
    message( STATUS "
  Cannot find the eosc helper library, 
  namely \${EOSC_HELPER_INSTALL_PATH}/lib/${HELPER_LIB_NAME}
  Please, set the path to this library in the top-level CMakeLists.txt as the
  argument to the variable EOSC_HELPER_INSTALL_PATH.
  The current value of EOSC_HELPER_INSTALL_PATH is ${EOSC_HELPER_INSTALL_PATH}  
    ")
    return()
  endif()
  
  target_link_libraries( ${APPL_NAME}
    PRIVATE
    ${Boost_LIBRARIES}
  )
  
  return()
endif()

target_link_libraries( ${APPL_NAME}
  PRIVATE
  ${Boost_LIBRARIES}
)

#######################################

cotire(${APPL_NAME})

install(TARGETS ${APPL_NAME} RUNTIME DESTINATION bin)