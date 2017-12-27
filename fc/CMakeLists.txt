cmake_minimum_required( VERSION 3.8 )
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_CXX_STANDARD 11)

if(${CMAKE_SYSTEM_NAME} EQUAL "Windows")
	message(STATUS "CMAKE_SYSTEM_NAME: ${CMAKE_SYSTEM_NAME")
	add_definitions(-DWIN32)
	add_definitions(-DMINGW_HAS_SECURE_API)
endif(${CMAKE_SYSTEM_NAME} EQUAL "Windows")



#MINGW_HAS_SECURE_API

set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.64.0 REQUIRED COMPONENTS 
#system 
#date_time 
#program_options 
#filesystem
)

SET( DEFAULT_HEADER_INSTALL_DIR include/${target} )
SET( DEFAULT_LIBRARY_INSTALL_DIR lib/ )
SET( DEFAULT_EXECUTABLE_INSTALL_DIR bin/ )
SET( CMAKE_DEBUG_POSTFIX _debug )
SET( BUILD_SHARED_LIBS NO )
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules" )
SET( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed" )

set(platformBitness 32)
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
  set(platformBitness 64)
endif()

SET (ORIGINAL_LIB_SUFFIXES ${CMAKE_FIND_LIBRARY_SUFFIXES})

find_package(Secp256k1 REQUIRED)
find_package(GMP REQUIRED)

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

MESSAGE(STATUS "Configuring fc to build on Unix/Apple")

SET(CMAKE_FIND_LIBRARY_SUFFIXES ".a;.so")

IF(NOT APPLE)
 # Linux or other unix
 SET(rt_library rt )
 SET(pthread_library pthread)
ENDIF(NOT APPLE)


IF(NOT "$ENV{OPENSSL_ROOT_DIR}" STREQUAL "")
  set(OPENSSL_ROOT_DIR $ENV{OPENSSL_ROOT_DIR} )
  set(OPENSSL_INCLUDE_DIR ${OPENSSL_ROOT_DIR}/include)
  message(STATUS "Setting up OpenSSL root and include vars to ${OPENSSL_ROOT_DIR}, ${OPENSSL_INCLUDE_DIR}")
ENDIF()

find_package(OpenSSL REQUIRED)

set( CMAKE_FIND_LIBRARY_SUFFIXES ${ORIGINAL_LIB_SUFFIXES} )

#setup_library( fc SOURCES ${sources} LIBRARY_TYPE STATIC )
add_library(fc STATIC 
  src/uint128.cpp
  src/real128.cpp
  src/variant.cpp
  src/exception.cpp
  src/variant_object.cpp
  src/string.cpp
  src/shared_ptr.cpp
  src/time.cpp
  src/filesystem.cpp 
  #src/utf8.cpp

  src/io/datastream.cpp
  src/io/json.cpp
  src/io/varint.cpp
  src/io/fstream.cpp
  src/io/console.cpp

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
  src/crypto/rand.cpp
 #src/crypto/base32.cpp

  src/network/ip.cpp
  src/network/resolve.cpp
  src/network/udp_socket.cpp
  src/network/url.cpp

  src/compress/smaz.cpp
  src/compress/zlib.cpp
)

INSTALL( TARGETS fc
   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
INSTALL( DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include DESTINATION . )
  
IF(APPLE)
  # As of 10.10 yosemite, the OpenSSL static libraries shipped with os x have a dependency
  # on zlib, so any time you link in openssl you also need to link zlib.  .  We really want to detect whether openssl was configured with the --no-zlib
  # option or not when it was built, but that's difficult to do in practice, so we
  # just always try to link it in on mac.
  find_package( ZLIB REQUIRED )
ELSE(APPLE)
  find_package( ZLIB )
ENDIF(APPLE)

if( ZLIB_FOUND )
  MESSAGE( STATUS "zlib found" )
  add_definitions( -DHAS_ZLIB )
else()
  MESSAGE( STATUS "zlib not found" )
  set( ZLIB_LIBRARIES "" )
endif( ZLIB_FOUND )

find_package( BZip2 )
if( BZIP2_FOUND )
   MESSAGE( STATUS "bzip2 found" )
   add_definitions( -DHAS_BZIP2 )
else()
   MESSAGE( STATUS "bzip2 not found" )
   set( BZIP2_LIBRARIES "" )
endif( BZIP2_FOUND )

# This will become unnecessary once we update to websocketpp which fixes upstream issue #395
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DWEBSOCKETPP_STRICT_MASKING")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBOOST_ASIO_HAS_STD_CHRONO")

target_include_directories(fc
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    ${Secp256k1_INCLUDE_DIR}
  )

IF(NOT WIN32)
  set(LINK_USR_LOCAL_LIB -L/usr/local/lib)
ENDIF()
target_link_libraries( fc PUBLIC ${LINK_USR_LOCAL_LIB} ${Boost_LIBRARIES} ${OPENSSL_LIBRARIES} ${ZLIB_LIBRARIES} ${BZIP2_LIBRARIES} ${PLATFORM_SPECIFIC_LIBS} ${RPCRT4} ${CMAKE_DL_LIBS} ${rt_library} ${readline_libraries} ${ECC_LIB} )


SET(OPENSSL_CONF_TARGET )
IF(DEFINED CMAKE_RUNTIME_OUTPUT_DIRECTORY)
  SET (OPENSSL_CONF_TARGET ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
ELSE()
  SET (OPENSSL_CONF_TARGET ${CMAKE_CURRENT_BINARY_DIR})
ENDIF()
