set( LIB_NAME eos_chain)

add_library( ${LIB_NAME} 
  wast_to_wasm.cpp
  chain_controller.cpp
  wasm_interface.cpp
  block_schedule.cpp
  fork_database.cpp
  transaction.cpp
  block.cpp
  get_config.cpp
  block_log.cpp
  blockchain_configuration.cpp
  types.cpp
  chain_administration_interface.cpp
  message_handling_contexts.cpp
  producer_objects.cpp
  staked_balance_objects.cpp  wast_to_wasm.cpp
  chain_controller.cpp
  wasm_interface.cpp
  block_schedule.cpp
  fork_database.cpp
  transaction.cpp
  block.cpp
  get_config.cpp
  block_log.cpp  
  blockchain_configuration.cpp
  types.cpp
  chain_administration_interface.cpp
  message_handling_contexts.cpp
  producer_objects.cpp
  staked_balance_objects.cpp
)

target_include_directories(${LIB_NAME} 
	PRIVATE
		${Boost_INCLUDE_DIR}
		${OPENSSL_INCLUDE_DIR}
    ${SECP256K1_INCLUDE_DIR}
	PUBLIC
		include
		../wasm-jit/Include
		../fc/include
		../types/include
		../chainbase/include
		../utilities/include
)

if( WIN32 )
  add_compile_options( /bigobj )
endif( WIN32 )

install( DIRECTORY include DESTINATION . )
install(
  TARGETS ${LIB_NAME} 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)
