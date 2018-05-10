project( "Raw" )

set( CMAKE_CXX_STANDARD 14 )
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
set( CXX_STANDARD_REQUIRED ON)
set( CMAKE_CXX_EXTENSIONS ON )
message( STATUS "CMAKE_CXX_STANDARD: ${CMAKE_CXX_STANDARD}" )

add_executable( "Raw" main.cpp )