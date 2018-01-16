
set(LIB_NAME "teoslib")
add_library(${LIB_NAME} STATIC 
  teos_command.cpp 
  teos_get_commands.cpp
  teos_wallet_commands.cpp
  teos_create_commands.cpp
  subcommands.cpp
  ../teos_test.cpp
  )

target_include_directories( ${LIB_NAME} 
  PUBLIC
  ${Boost_INCLUDE_DIR}
  ${HELPER_INCLUDE}
  include
  ${CMAKE_SOURCE_DIR}/teos_helper/include
)

target_link_libraries( ${LIB_NAME}
  PUBLIC
  teos_helper
  ${Boost_LIBRARIES}
  ${CMAKE_THREAD_LIBS_INIT}
)

install ( TARGETS ${LIB_NAME} DESTINATION lib )
install ( FILES 
  teos_command.hpp 
  teos_get_commands.hpp 
  teos_wallet_commands.hpp
  teos_create_commands.hpp
  subcommands.hpp
  DESTINATION include
)