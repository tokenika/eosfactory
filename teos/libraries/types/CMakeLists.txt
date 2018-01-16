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
  PUBLIC
  ${Boost_INCLUDE_DIR}
  ${OPENSSL_INCLUDE_DIR}
  ../fc/include
  ../utilities/include

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
  eos_utilities 
  fc 
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