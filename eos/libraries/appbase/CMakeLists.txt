
file(GLOB HEADERS "include/appbase/*.hpp")

add_library( appbase
  application.cpp
  ${HEADERS}
)

target_include_directories( appbase
  PUBLIC 
    ${Boost_INCLUDE_DIR}  
    include
)

INSTALL( TARGETS
   appbase

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
INSTALL( FILES ${HEADERS} DESTINATION "include/eos/appbase" )

