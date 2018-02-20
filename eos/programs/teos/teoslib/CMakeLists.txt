
set( LIB_NAME "teoslib" )

set( TEST_ADDRESS "\"tokenika\"")
set( TEST_HOST "\"eos-testapi.tokenika.io\"" )
set( TEST_PORT "\"8888\"" )
set( CONFIG_JSON_FILE "config.json" )
set( CONFIG_JSON_PATH "${CONFIG_JSON_FILE}" )
set( CONFIG_JSON "\"${CONFIG_JSON_PATH}\"" )
set( LOGGING_DIR "\"log\"" )

configure_file (
  "config.h.in"
  "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.h"
)

file( GLOB HEADERS "include/teos/*.hpp" 
  "include/teos/command/*.hpp" "include/teos/control/*hpp" )
file( GLOB SRC "*cpp" "command/*.cpp" "control/*.cpp" )

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
    include
)

install ( TARGETS ${LIB_NAME} DESTINATION lib )
install( DIRECTORY include DESTINATION include )
install( FILES ${CONFIG_JSON_PATH} DESTINATION bin )
