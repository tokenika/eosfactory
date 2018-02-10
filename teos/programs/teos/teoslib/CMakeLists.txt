
set(LIB_NAME "teoslib")

file(GLOB HEADERS "include/*.hpp")
file(GLOB SRC LIST_DIRECTORIES false "src/*.cpp")
add_library(${LIB_NAME} STATIC
  ${HEADERS}
  ${SRC}
  )

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ${CMAKE_SOURCE_DIR}/libraries/fc/include
    ${CMAKE_SOURCE_DIR}/libraries/types/include
    ${CMAKE_SOURCE_DIR}/libraries/utilities/include
    ${CMAKE_SOURCE_DIR}/libraries/appbase/include
    ${CMAKE_SOURCE_DIR}/libraries/chainbase/include
    ${CMAKE_SOURCE_DIR}/libraries/chain/include
    ${CMAKE_SOURCE_DIR}/libraries/wasm-jit/include
		${CMAKE_SOURCE_DIR}/plugins/chain_plugin/include
		${CMAKE_SOURCE_DIR}/plugins/database_plugin/include
    include
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