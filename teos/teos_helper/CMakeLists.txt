set( LIB_NAME "teos_helper")

add_library( ${LIB_NAME} STATIC
  teos_helper.cpp
)

target_include_directories( ${LIB_NAME} 
  PUBLIC
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
    PUBLIC
    ${SECP256K1_INCLUDE_DIR}
    ${GMP_INCLUDE_DIR}
  )
endif()

target_link_libraries( ${LIB_NAME}
  PUBLIC
  ${Boost_LIBRARIES} 
  ${OPENSSL_LIBRARIES}

  PUBLIC
  fc
  eos_types
  eos_utilities
)

if( NOT EOS_ECC_IMPL STREQUAL openssl )
  target_link_libraries( ${LIB_NAME}
    PUBLIC
    ${SECP256K1_LIBRARIES}
    ${GMP_LIBRARIES}
  )
endif()

if( WIN32 )
  target_include_directories( ${LIB_NAME}
    PUBLIC
    ${OPENSSL_INCLUDE_DIR}
  )

  if( NOT EOS_ECC_IMPL STREQUAL openssl )
    target_link_libraries( ${LIB_NAME}
      PUBLIC
      ${SECP256K1_LIBRARIES_DIR}/gcc.lib
    )
  endif()

  target_link_libraries( ${LIB_NAME}
    PUBLIC
    "$(WindowsSDK_LibraryPath)/x64/crypt32.lib"
    "$(VC_ReferencesPath_VC_x64)/legacy_stdio_definitions.lib"
    "Userenv.lib"
  )
endif( WIN32 )

install( DIRECTORY include DESTINATION . )
install(
  TARGETS ${LIB_NAME} 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)