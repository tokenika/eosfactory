
file(GLOB HEADERS "include/eos/utilities/*.hpp")

add_library( eos_utilities
  key_conversion.cpp
  string_escape.cpp
  tempdir.cpp
  words.cpp
  ${HEADERS} 
)

target_include_directories( eos_utilities
  PUBLIC 
    include
  PRIVATE
    ${CMAKE_SOURCE_DIR}/libraries/fc/include
    ${CMAKE_SOURCE_DIR}/libraries/wasm-jit/Include
)

install( TARGETS
   eos_utilities

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
install( FILES ${HEADERS} DESTINATION "include/eos/utilities" )
