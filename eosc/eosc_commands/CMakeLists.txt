
include_directories("${CMAKE_INSTALL_PREFIX}/include")
include_directories(${Boost_INCLUDE_DIRS})

add_library(eosc_commands STATIC eosc_command.cpp)

target_link_libraries(eosc_commands ${Boost_LIBRARIES})

install (TARGETS eosc_commands DESTINATION lib)
install (FILES eosc_command.hpp eosc_get_commands.hpp 
  DESTINATION include)