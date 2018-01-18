set( LIB_NAME eos_utilities)

add_library(${LIB_NAME} STATIC 
  key_conversion.cpp
)

if( EOS_BUILD_RANGE STREQUAL all )
  target_sources( ${LIB_NAME} 
    PUBLIC
      ${CMAKE_CURRENT_LIST_DIR}/string_escape.cpp
      ${CMAKE_CURRENT_LIST_DIR}/tempdir.cpp
      ${CMAKE_CURRENT_LIST_DIR}/words.cpp
    )
    endif( EOS_BUILD_RANGE STREQUAL all )    

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ../fc/include
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ${SECP256K1_INCLUDE_DIR}
  PUBLIC  
    include
)

install( DIRECTORY include DESTINATION . )
install(
  TARGETS ${LIB_NAME} 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)