
set( LIB_NAME "teoslib" )

file( GLOB HEADERS "include/teoslib/*.hpp" 
  "include/teoslib/command/*.hpp" "include/teoslib/control/*hpp" )
file( GLOB SRC "*cpp" "command/*.cpp" "control/*.cpp" )

add_library(${LIB_NAME} STATIC
  ${HEADERS}
  ${SRC}
  )

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}

    ${EOSIO_SOURCE_DIR}/libraries/wasm-jit/Include
    ${EOSIO_SOURCE_DIR}/libraries/fc/include
    ${EOSIO_SOURCE_DIR}/libraries/appbase/include
    ${EOSIO_SOURCE_DIR}/libraries/utilities/include
    ${EOSIO_SOURCE_DIR}/libraries/softfloat/source/include
    ${EOSIO_SOURCE_DIR}/libraries/chain/include
    ${EOSIO_SOURCE_DIR}/libraries/types/include
    ${EOSIO_SOURCE_DIR}/libraries/chainbase/include
    ${EOSIO_SOURCE_DIR}/plugins/database_plugin/include
    ${EOSIO_SOURCE_DIR}/plugins/chain_plugin/include

  PUBLIC
    include
)

install ( TARGETS ${LIB_NAME} DESTINATION lib )
install( DIRECTORY include DESTINATION include )
install( FILES ${CONFIG_JSON_PATH} DESTINATION bin )
