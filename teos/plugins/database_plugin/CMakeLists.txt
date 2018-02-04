file(GLOB HEADERS "include/eos/database_plugin/*.hpp")
set( LIB_NAME database_plugin )

add_library( ${LIB_NAME}
             database_plugin.cpp
             ${HEADERS} )

#target_link_libraries( ${LIB_NAME} appbase chainbase fc )
target_include_directories( ${LIB_NAME} 
  PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include" 
  PRIVATE 
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    "${CMAKE_SOURCE_DIR}/libraries/appbase/include"
    "${CMAKE_SOURCE_DIR}/libraries/chainbase/include"
    "${CMAKE_SOURCE_DIR}/libraries/fc/include"
		"${CMAKE_SOURCE_DIR}/plugins/database_plugin/include"
)

install( TARGETS ${LIB_NAME}
   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
install( FILES ${HEADERS} DESTINATION "include/eos/${LIB_NAME}" )
