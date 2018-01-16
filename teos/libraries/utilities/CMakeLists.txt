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
  PUBLIC
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ../fc/include
  
  PUBLIC  
    include
)

target_link_libraries( ${LIB_NAME}
  PUBLIC
    ${Boost_LIBRARIES} 
    ${OPENSSL_LIBRARIES}
  
  PUBLIC
    eos_types 
    fc 
)

if( NOT EOS_ECC_IMPL STREQUAL openssl )
  target_link_libraries( ${LIB_NAME}
    PUBLIC
      ${SECP256K1_LIBRARIES}
      ${GMP_LIBRARIES}
  )
endif()

install( DIRECTORY include DESTINATION . )
install(
  TARGETS ${LIB_NAME} 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)