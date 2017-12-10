cmake_minimum_required (VERSION 3.8)
project (eosc)
set (CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake")
include(cotire)
include("${PROJECT_SOURCE_DIR}/CMake/config.cmake")

set(VERSION_MAJOR 1)
set(VERSION_MINOR 0)
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
find_package(Boost 1.64.0 REQUIRED COMPONENTS 
system 
date_time 
program_options 
filesystem
)

set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_package(Threads REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(eosc_commands)

add_executable(${PROJECT_NAME} eosc_commands/eosc_command.cpp eosc.cpp )
target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
target_link_libraries(${PROJECT_NAME} eosc_commands)

cotire(${PROJECT_NAME})

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)