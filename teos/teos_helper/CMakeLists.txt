set( LIB_NAME "teos_helper")

add_library( ${LIB_NAME} STATIC
  include/teos_helper.hpp
  teos_helper.cpp
)

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ../libraries/fc/include
    ../libraries/types/include
    ../libraries/utilities/include
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