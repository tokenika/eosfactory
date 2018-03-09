file(GLOB HEADERS "include/eos/chain_plugin/*.hpp")
add_library( chain_plugin
             chain_plugin.cpp
             ${HEADERS} )

target_include_directories( chain_plugin 
  PUBLIC 
    include
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    "${CMAKE_SOURCE_DIR}/libraries/appbase/include"
    "${CMAKE_SOURCE_DIR}/libraries/utilities/include"
    "${CMAKE_SOURCE_DIR}/libraries/fc/include"
    "${CMAKE_SOURCE_DIR}/libraries/chainbase/include" 
    "${CMAKE_SOURCE_DIR}/libraries/chain/include" 
    # "${CMAKE_SOURCE_DIR}/libraries/wasm-jit/Include"   
)

install( TARGETS
   chain_plugin

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
install( FILES ${HEADERS} DESTINATION "include/eos/chain_plugin" )
