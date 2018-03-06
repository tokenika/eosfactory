
SET( ECC_IMPL openssl CACHE STRING "secp256k1 or openssl or mixed" )

MESSAGE(STATUS "ECC_IMPL: ${ECC_IMPL}")
IF( ECC_IMPL STREQUAL openssl )
  SET( ECC_REST src/crypto/elliptic_impl_pub.cpp )
ELSE( ECC_IMPL STREQUAL openssl )
  SET( ECC_LIB ${Secp256k1_LIBRARY} ${GMP_LIBRARIES} )
  IF( ECC_IMPL STREQUAL mixed )
    SET( ECC_REST src/crypto/elliptic_impl_priv.cpp src/crypto/elliptic_impl_pub.cpp )
  ELSE( ECC_IMPL STREQUAL mixed )
    SET( ECC_REST src/crypto/elliptic_impl_priv.cpp )
  ENDIF( ECC_IMPL STREQUAL mixed )
ENDIF( ECC_IMPL STREQUAL openssl )

file( GLOB_RECURSE HEADERS ${CMAKE_CURRENT_SOURCE_DIR} *.hpp *.h )

add_library( fc STATIC
${HEADERS}
src/uint128.cpp
src/real128.cpp
src/variant.cpp
src/exception.cpp
src/variant_object.cpp
src/string.cpp
src/shared_ptr.cpp
src/time.cpp
src/utf8.cpp
src/io/datastream.cpp
src/io/json.cpp
src/io/varint.cpp
src/io/fstream.cpp
src/io/console.cpp
src/filesystem.cpp
src/interprocess/file_mapping.cpp
src/interprocess/mmap_struct.cpp
src/log/log_message.cpp
src/log/logger.cpp
src/log/appender.cpp
src/log/console_appender.cpp
src/log/gelf_appender.cpp
src/log/logger_config.cpp
src/crypto/_digest_common.cpp
src/crypto/openssl.cpp
src/crypto/aes.cpp
src/crypto/crc.cpp
src/crypto/city.cpp
#     src/crypto/base32.cpp
src/crypto/base36.cpp
src/crypto/base58.cpp
src/crypto/base64.cpp
src/crypto/bigint.cpp
src/crypto/hex.cpp
src/crypto/sha1.cpp
src/crypto/ripemd160.cpp
src/crypto/sha256.cpp
src/crypto/sha224.cpp
src/crypto/sha512.cpp
src/crypto/dh.cpp
src/crypto/blowfish.cpp
src/crypto/elliptic_common.cpp
${ECC_REST}
src/crypto/elliptic_${ECC_IMPL}.cpp
src/crypto/elliptic_r1.cpp
src/crypto/rand.cpp
src/crypto/public_key.cpp
src/crypto/private_key.cpp
src/crypto/signature.cpp
src/network/ip.cpp
src/network/resolve.cpp
src/network/udp_socket.cpp
src/network/url.cpp
src/compress/smaz.cpp
src/compress/zlib.cpp

)

target_include_directories(fc
  PUBLIC 
    include
  PRIVATE 
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/vendor/websocketpp
    ./
    ${CMAKE_CURRENT_SOURCE_DIR}/vendor/boost_1.51/include
    ${CMAKE_CURRENT_SOURCE_DIR}/vendor/cyoencode-1.0.2/src
    ${CMAKE_SOURCE_DIR}/libraries/utilities/include
  )

INSTALL( TARGETS fc
   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
INSTALL( DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include DESTINATION . )
