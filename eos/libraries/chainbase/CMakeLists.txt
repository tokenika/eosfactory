file(GLOB HEADERS "include/chainbase/*.hpp")

add_library( chainbase src/chainbase.cpp ${HEADERS} )

target_include_directories( chainbase 
  PUBLIC 
    include
  PRIVATE
    ${Boost_INCLUDE_DIR}
)

install( TARGETS
   chainbase

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
install( FILES ${HEADERS} DESTINATION "include/" )
