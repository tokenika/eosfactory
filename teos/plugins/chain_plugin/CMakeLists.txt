file(GLOB HEADERS "include/eos/chain_plugin/*.hpp")
set( LIB_NAME chain_plugin )

add_library( ${LIB_NAME}
  chain_plugin.cpp
  ${HEADERS} 
)

target_include_directories(${LIB_NAME} 
  PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
  PRIVATE 
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/appbase/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/chain/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/fc/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/types/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/chainbase/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/utilities/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../database_plugin/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/wasm-jit/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../db_plugin/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../../libraries/native_contract/include"    
)

#target_link_libraries( ${LIB_NAME} database_plugin db_plugin eos_native_contract eos_chain appbase )

install( TARGETS
   ${LIB_NAME}

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
install( FILES ${HEADERS} DESTINATION "include/eos/${LIB_NAME}" )
