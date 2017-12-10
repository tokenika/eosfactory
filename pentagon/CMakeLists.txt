cmake_minimum_required (VERSION 3.8)
project (pentagon)
set (CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/../CMake")
include(cotire)
include("${PROJECT_SOURCE_DIR}/../config.cmake")

set(VERSION_MAJOR 1)
set(VERSION_MINOR 0)
set(CONFIG_JSON "\"${PROJECT_SOURCE_DIR}/../config.json\"")
set(LOGGING_DIR "\"${CMAKE_INSTALL_PREFIX}\"")
configure_file (
   "${PROJECT_SOURCE_DIR}/config.h.in"
   "${CMAKE_INSTALL_PREFIX}/include/config.h"
   )
message(STATUS "config.h: ${CMAKE_INSTALL_PREFIX}/include/config.h")

set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.64.0 REQUIRED COMPONENTS system date_time)

set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_package(Threads REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(pent_core)
add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
target_link_libraries(${PROJECT_NAME} pent_core)
target_link_libraries(${PROJECT_NAME} "${PROJECT_SOURCE_DIR}/build/eosc_commands/libeosc_commands.a")

cotire(${PROJECT_NAME})

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)
