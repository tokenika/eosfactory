
include_directories("${CMAKE_INSTALL_PREFIX}/include")
include_directories(${Boost_INCLUDE_DIRS})

set(LIB_NAME "eosclib")
add_library(${LIB_NAME} STATIC 
  eosc_command.cpp 
  eosc_get_commands
  eosc_wallet_commands
  subcommands.cpp
  ../eosc_test.cpp
  ../eosc
  )

target_link_libraries(${LIB_NAME} ${Boost_LIBRARIES})
target_link_libraries(${LIB_NAME} ${CMAKE_THREAD_LIBS_INIT} )

install (TARGETS ${LIB_NAME} DESTINATION lib)
install (FILES 
  eosc_command.hpp 
  eosc_get_commands.hpp 
  eosc_wallet_commands.hpp 
  subcommands.hpp
  DESTINATION include)