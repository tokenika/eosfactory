cmake_minimum_required (VERSION 3.8)
project ("Tokenika_Eosc")
set (CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake")
include(cotire)
include("${PROJECT_SOURCE_DIR}/CMake/config.cmake")

set(VERSION_MAJOR 0)
set(VERSION_MINOR 5)
set(CONFIG_JSON_FILE "eosc_config.json")
set(CONFIG_JSON_PATH "${CONFIG_JSON_FILE}")

set(CONFIG_JSON "\"${CONFIG_JSON_PATH}\"")
file(COPY ${CONFIG_JSON_PATH} DESTINATION "${CMAKE_BINARY_DIR}")

set(LOGGING_DIR "\"log\"")
configure_file (
   "${PROJECT_SOURCE_DIR}/eosc_config.h.in"
   "${PROJECT_SOURCE_DIR}/eosc_config.h"
   )
include_directories(${CMAKE_BINARY_DIR})

set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.62.0 REQUIRED COMPONENTS 
  system 
  date_time 
  program_options 
  filesystem
)

find_package(Threads REQUIRED)
add_subdirectory(eosclib)

set(APPL_NAME "eosc")
add_executable(${APPL_NAME} eosc.cpp )
target_link_libraries(${APPL_NAME} eosclib)

add_executable("eosc_lib_test" eoec_lib_test.cpp)
target_link_libraries("eosc_lib_test" eosclib)

cotire(${APPL_NAME})

install(TARGETS ${APPL_NAME} RUNTIME DESTINATION bin)