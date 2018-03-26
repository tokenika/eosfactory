file(GLOB HEADERS "include/eosio/chain/*.hpp" "include/eosio/chain/contracts/*.hpp")

add_library( eosio_chain
  chain_config.cpp
  merkle.cpp
  name.cpp
  transaction.cpp
  block.cpp
  wast_to_wasm.cpp
  wasm_interface.cpp
  apply_context.cpp
  # rate_limiting.cpp #
  fork_database.cpp
  # get_config.cpp #
  block_log.cpp
  asset.cpp
  global_property_object.cpp
  chain_controller.cpp
  contracts/eosio_contract.cpp
  # contracts/producer_objects.cpp #
  contracts/staked_balance_objects.cpp
  contracts/chain_initializer.cpp
  # contracts/genesis_state.cpp #
  contracts/abi_serializer.cpp
  ${HEADERS}
)  

target_include_directories( eosio_chain
  PUBLIC 
    include 
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    "${CMAKE_CURRENT_BINARY_DIR}/include"
    "${CMAKE_SOURCE_DIR}/libraries/utilities/include"
    "${CMAKE_SOURCE_DIR}/libraries/fc/include"
    "${CMAKE_SOURCE_DIR}/libraries/chainbase/include"    
    "${CMAKE_SOURCE_DIR}/libraries/wasm-jit/Include"    
)

if( WIN32 )
  target_include_directories( eosio_chain
    PRIVATE
       ${CMAKE_SOURCE_DIR}/libraries/int128/include
  )
endif()

INSTALL( TARGETS
   eosio_chain

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
INSTALL( FILES ${HEADERS} DESTINATION "include/eosio/chain" )


