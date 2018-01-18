
set(LIB_NAME "teoslib")
add_library(${LIB_NAME} STATIC 
  teos_command.hpp 
  teos_get_commands.hpp 
  teos_wallet_commands.hpp
  teos_create_commands.hpp
  teos_command.cpp 
  teos_get_commands.cpp
  teos_wallet_commands.cpp
  teos_create_commands.cpp
  subcommands.cpp
  ../teos_test.cpp
  )

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIR}

  PUBLIC
    ${HELPER_INCLUDE}
    include
    ${CMAKE_SOURCE_DIR}/teos_helper/include
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