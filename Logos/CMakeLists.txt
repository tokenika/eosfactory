cmake_minimum_required (VERSION 3.8)
set( projectName pentagon )
project( ${projectName} )

set( VERSION_MAJOR 0 )
set( VERSION_MINOR 5 )
set( CONFIG_JSON "\"config.json\"" )
set( LOGGING_DIR "\"\"" )
configure_file(
  "${PROJECT_SOURCE_DIR}/config.h.in"
  "${CMAKE_SOURCE_DIR}/include/config.h"
)
set( CMAKE_BUILD_TYPE "Debug" )

add_subdirectory(control)
