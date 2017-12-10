project (Simplest)
include(../config.cmake) 

set(CMAKE_BUILD_TYPE Debug)

set(Boost_USE_STATIC_LIBS ON)
find_package(Boost 1.64.0 REQUIRED COMPONENTS log)
set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
set(THREADS_PREFER_PTHREAD_FLAG TRUE)
find_package(Threads REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})

install (TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)
install (FILES "${PROJECT_BINARY_DIR}/config.h" DESTINATION include)
