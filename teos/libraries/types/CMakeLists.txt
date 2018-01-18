set( LIB_NAME eos_types)

add_library( ${LIB_NAME} STATIC
  public_key.cpp
)

if( EOS_BUILD_RANGE STREQUAL all )
  target_sources( ${LIB_NAME} 
    PUBLIC
      ${CMAKE_CURRENT_LIST_DIR}/asset.cpp
      ${CMAKE_CURRENT_LIST_DIR}/type_parser.cpp
      ${CMAKE_CURRENT_LIST_DIR}/abi_serializer.cpp
      ${CMAKE_CURRENT_LIST_DIR}/native.cpp  
    )
endif( EOS_BUILD_RANGE STREQUAL all )    

target_include_directories( ${LIB_NAME}
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ../fc/include
    ../utilities/include

  PUBLIC 
    include
)

if( NOT EOS_ECC_IMPL STREQUAL openssl )
  target_include_directories( ${LIB_NAME}
    PRIVATE
      ${SECP256K1_INCLUDE_DIR}
      ${GMP_INCLUDE_DIR}
  )
endif()

install( DIRECTORY include DESTINATION . )
install(
  TARGETS ${LIB_NAME} 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)