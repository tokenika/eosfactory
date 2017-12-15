cmake_minimum_required (VERSION 3.8)
project (tunnel)
set (CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMake")

set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/../target")
set(EOSIO_INSTALL_DIR "/mnt/hgfs/Workspaces/EOS/eos")
message(STATUS "EOSIO_INSTALL_DIR: ${EOSIO_INSTALL_DIR}")
message(STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE Debug) 

include_directories("${CMAKE_INSTALL_PREFIX}/include")

set(VERSION_MAJOR 1)
set(VERSION_MINOR 0)
set(CONFIG_JSON_FILE "eosc_config.json")
set(CONFIG_JSON_PATH "${CONFIG_JSON_FILE}")

set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.64.0 REQUIRED COMPONENTS 
system 
program_options 
)

set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_package(Threads REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} tunnel.cpp )
target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)