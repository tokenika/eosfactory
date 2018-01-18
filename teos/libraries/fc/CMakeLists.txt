# Read https://crascit.com/2016/01/31/enhanced-source-file-handling-with-target_sources/
set( LIB_NAME fc)

if( NOT EOS_ECC_IMPL )
  set( EOS_ECC_IMPL openssl)
endif( NOT EOS_ECC_IMPL )

if( EOS_ECC_IMPL STREQUAL openssl )
  message( STATUS "EOS_ECC_IMPL is openssl" )
  set( ECC_REST src/crypto/elliptic_impl_pub.cpp )
else( EOS_ECC_IMPL STREQUAL openssl )
  if( EOS_ECC_IMPL STREQUAL mixed )
    message( STATUS "EOS_ECC_IMPL is mixed" )
    set( ECC_REST src/crypto/elliptic_impl_priv.cpp src/crypto/elliptic_impl_pub.cpp )
  else( EOS_ECC_IMPL STREQUAL mixed )
    set( ECC_REST src/crypto/elliptic_impl_priv.cpp )
  endif( EOS_ECC_IMPL STREQUAL mixed )
endif( EOS_ECC_IMPL STREQUAL openssl )

add_library( ${LIB_NAME} STATIC 
  src/uint128.cpp
  src/real128.cpp
  src/variant.cpp
  src/exception.cpp
  src/variant_object.cpp
  src/string.cpp
  src/shared_ptr.cpp
  src/time.cpp
  src/filesystem.cpp 
  src/utf8.cpp
  
  src/io/datastream.cpp
  src/io/json.cpp
  
  src/log/log_message.cpp

  src/crypto/_digest_common.cpp
  src/crypto/aes.cpp
  src/crypto/crc.cpp
  src/crypto/city.cpp
  src/crypto/base36.cpp
  src/crypto/base58.cpp
  src/crypto/base64.cpp
  src/crypto/bigint.cpp
  src/crypto/hex.cpp
  src/crypto/sha1.cpp
  src/crypto/openssl.cpp
  src/crypto/ripemd160.cpp
  src/crypto/sha256.cpp
  src/crypto/sha224.cpp
  src/crypto/sha512.cpp
  src/crypto/elliptic_common.cpp
  ${ECC_REST}
  src/crypto/elliptic_${EOS_ECC_IMPL}.cpp
  src/crypto/rand.cpp
)

if( EOS_BUILD_RANGE STREQUAL all )
  target_sources( ${LIB_NAME} 
    PUBLIC
      ${CMAKE_CURRENT_LIST_DIR}/src/io/varint.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/io/fstream.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/io/console.cpp

      ${CMAKE_CURRENT_LIST_DIR}/src/log/logger.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/log/appender.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/log/console_appender.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/log/gelf_appender.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/log/logger_config.cpp

      ${CMAKE_CURRENT_LIST_DIR}/src/crypto/dh.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/crypto/blowfish.cpp

      ${CMAKE_CURRENT_LIST_DIR}/src/interprocess/file_mapping.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/interprocess/mmap_struct.cpp

      ${CMAKE_CURRENT_LIST_DIR}/src/compress/smaz.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/compress/zlib.cpp

      ${CMAKE_CURRENT_LIST_DIR}/src/network/ip.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/network/resolve.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/network/udp_socket.cpp
      ${CMAKE_CURRENT_LIST_DIR}/src/network/url.cpp      
  )
endif( EOS_BUILD_RANGE STREQUAL all )

target_include_directories(${LIB_NAME} 
  PRIVATE 
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ${SECP256K1_INCLUDE_DIR}
  PUBLIC
    include
    vendor/websocketpp
)

install( DIRECTORY include DESTINATION . )
install(
  TARGETS ${LIB_NAME} 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)
