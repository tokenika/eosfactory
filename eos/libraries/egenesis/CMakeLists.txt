
add_library( eos_egenesis_none
   egenesis_none.cpp
   include/eos/egenesis/egenesis.hpp
   )

target_link_libraries( eos_egenesis_none eos_chain eos_native_contract fc )
target_include_directories( eos_egenesis_none
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
  PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include" 
  )

add_executable( embed_genesis
   embed_genesis.cpp
   )
target_include_directories( embed_genesis
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
)
target_link_libraries( embed_genesis 
  PRIVATE
    eos_chain 
    eos_egenesis_none 
    fc
  PRIVATE
    ${OPENSSL_LIBRARIES}
    ${Boost_LIBRARIES}    
)
if( NOT EOS_ECC_IMPL STREQUAL openssl )
target_link_libraries( embed_genesis
  PRIVATE
    ${SECP256K1_LIBRARIES}
    ${GMP_LIBRARIES}
)
endif()

if( UNIX )
  target_link_libraries( embed_genesis PUBLIC rt )
endif()
if( WIN32 )
if( NOT EOS_ECC_IMPL STREQUAL openssl )
  target_link_libraries( embed_genesis
    PRIVATE
      ${SECP256K1_LIBRARIES_DIR}/gcc.lib
  )
endif()

target_link_libraries( embed_genesis
  PRIVATE
    "$(WindowsSDK_LibraryPath)/x64/crypt32.lib"
    "$(VC_ReferencesPath_VC_x64)/legacy_stdio_definitions.lib"
    "Userenv.lib"
    __iob_func
)
endif( WIN32 )


set( embed_genesis_args
   -t "${CMAKE_CURRENT_SOURCE_DIR}/egenesis_brief.cpp.tmpl---${CMAKE_CURRENT_BINARY_DIR}/egenesis_brief.cpp"
   -t "${CMAKE_CURRENT_SOURCE_DIR}/egenesis_full.cpp.tmpl---${CMAKE_CURRENT_BINARY_DIR}/egenesis_full.cpp"
   )

MESSAGE( STATUS "egenesis: " ${EOS_EGENESIS_JSON} )

if( EOS_EGENESIS_JSON )
   list( APPEND embed_genesis_args --genesis-json "${EOS_EGENESIS_JSON}" )
endif( EOS_EGENESIS_JSON )

MESSAGE( STATUS "embed_genesis_args: " ${embed_genesis_args} )

add_custom_command(
   OUTPUT
      "${CMAKE_CURRENT_BINARY_DIR}/egenesis_brief.cpp"
      "${CMAKE_CURRENT_BINARY_DIR}/egenesis_full.cpp"
   WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
   COMMAND embed_genesis ${embed_genesis_args}
   DEPENDS
      "${EOS_EGENESIS_JSON}"
      "${CMAKE_CURRENT_SOURCE_DIR}/egenesis_brief.cpp.tmpl"
      "${CMAKE_CURRENT_SOURCE_DIR}/egenesis_full.cpp.tmpl"
      embed_genesis )

add_library( eos_egenesis_brief "${CMAKE_CURRENT_BINARY_DIR}/egenesis_brief.cpp" include/eos/egenesis/egenesis.hpp )
add_library( eos_egenesis_full  "${CMAKE_CURRENT_BINARY_DIR}/egenesis_full.cpp" include/eos/egenesis/egenesis.hpp )

target_link_libraries( eos_egenesis_brief eos_chain eos_native_contract fc )
target_link_libraries( eos_egenesis_full eos_chain eos_native_contract fc )

target_include_directories( eos_egenesis_brief
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
  PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include" 
)
target_include_directories( eos_egenesis_full
  PRIVATE
     ${Boost_INCLUDE_DIR}
  PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include" 
)

INSTALL( TARGETS
   embed_genesis eos_egenesis_none eos_egenesis_brief eos_egenesis_full

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
