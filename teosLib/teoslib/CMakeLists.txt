
set( TARGET_NAME "teoslib" )

file( GLOB HEADERS "include/teos/*.hpp" 
  "include/teos/command/*.hpp" "include/teos/control/*hpp" )
file( GLOB SRC "*cpp" "command/*.cpp" "control/*.cpp" )

add_library(${TARGET_NAME} SHARED
  ${HEADERS}
  ${SRC}
  )

#set_target_properties( ${TARGET_NAME} PROPERTIES VERSION ${PROJECT_VERSION} )
#set_target_properties( ${TARGET_NAME} PROPERTIES PUBLIC_HEADER ${HEADERS})

target_include_directories( ${TARGET_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}

    ${EOSIO_SOURCE_DIR}/libraries/wasm-jit/include
    ${EOSIO_SOURCE_DIR}/libraries/fc/include
    ${EOSIO_SOURCE_DIR}/libraries/appbase/include
    ${EOSIO_SOURCE_DIR}/libraries/utilities/include
    ${EOSIO_SOURCE_DIR}/libraries/chain/include
    ${EOSIO_SOURCE_DIR}/libraries/types/include
    ${EOSIO_SOURCE_DIR}/libraries/chainbase/include
    ${EOSIO_SOURCE_DIR}/plugins/database_plugin/include
    ${EOSIO_SOURCE_DIR}/plugins/chain_plugin/include

  PUBLIC
    include
)

include(GNUInstallDirs)

target_link_libraries( ${TARGET_NAME}
PRIVATE
  ${EOSIO_BINARY_DIR}/plugins/chain_plugin/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chain_plugin${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/plugins/database_plugin/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}database_plugin${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/chainbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chainbase${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/types/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eos_types${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/chain/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eos_chain${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/utilities/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eos_utilities${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/appbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}appbase${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}fc${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/wasm-jit/lib/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}WAST${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/wasm-jit/lib/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}WASM${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/wasm-jit/lib/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Runtime${CMAKE_STATIC_LIBRARY_SUFFIX}
  ${EOSIO_BINARY_DIR}/libraries/wasm-jit/lib/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}IR${CMAKE_STATIC_LIBRARY_SUFFIX}  
  ${EOSIO_BINARY_DIR}/libraries/wasm-jit/lib/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Logging${CMAKE_STATIC_LIBRARY_SUFFIX} 
  ${EOSIO_BINARY_DIR}/libraries/wasm-jit/lib/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Platform${CMAKE_STATIC_LIBRARY_SUFFIX} 
)

if( UNIX )
target_link_libraries( ${TARGET_NAME} 
  PRIVATE 
    asan        # static-libasan ?
)
endif()

if( NOT EOS_ECC_IMPL STREQUAL openssl )
target_link_libraries( ${TARGET_NAME}
  PRIVATE
    ${SECP256K1_LIBRARIES}
    ${GMP_LIBRARIES}
)

target_link_libraries( ${TARGET_NAME}
PRIVATE
  ${OPENSSL_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CMAKE_DL_LIBS}
  ${CMAKE_THREAD_LIBS_INIT}
)
endif()

if( WIN32 )
if( NOT EOS_ECC_IMPL STREQUAL openssl )
  target_link_libraries( ${TARGET_NAME}
    PRIVATE
      ${SECP256K1_LIBRARIES_DIR}/gcc.lib
  )
endif()

target_link_libraries( ${TARGET_NAME}
  PRIVATE
    "$(WindowsSDK_LibraryPath)/x64/crypt32.lib"
    "$(VC_ReferencesPath_VC_x64)/legacy_stdio_definitions.lib"
    "Userenv.lib"
    __iob_func
)
endif( WIN32 )

if( UNIX )
target_link_libraries( ${TARGET_NAME} 
PRIVATE 
  rt 
  pthread
)
endif()

install(TARGETS ${TARGET_NAME}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

