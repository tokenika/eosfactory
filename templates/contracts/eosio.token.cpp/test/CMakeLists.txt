
set( BUILD_SHARED_LIBS NO )
set( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed")
option( ENABLE_ASAN "enable ASAN" OFF )

list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules" )

## BEGIN DEPENDENCIES ########################################################

set( Boost_USE_STATIC_LIBS ON )
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
set( BOOST_ROOT "$ENV{U_HOME}/opt/boost_1_66_0" )
message(STATUS "BOOST_ROOT: ${BOOST_ROOT}")

find_package(Boost 1.66 REQUIRED COMPONENTS 
  thread  
  date_time   
  filesystem  
  system
  program_options
  unit_test_framework
  chrono
  regex
  iostreams
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  EOSIO_BOOST_INCLUDE_DIRS: ${EOSIO_BOOST_INCLUDE_DIRS}
  Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-WIN32-14.1)
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

set( OPENSSL_USE_STATIC_LIBS TRUE)
find_package( OpenSSL REQUIRED )
if( OpenSSL_FOUND )
  message( STATUS "OpenSSL found.
  OPENSSL_INCLUDE_DIR: ${OPENSSL_INCLUDE_DIR}
  OPENSSL_LIBRARIES: ${OPENSSL_LIBRARIES}" )
else( OpenSSL_FOUND)
  message( STATUS "OpenSSL not found. set environment variables:
  OPENSSL_ROOT_DIR (for example, %C_INCLUDE%/OpenSSL/Win64OpenSSL-1_0_2L)" )
endif( OpenSSL_FOUND )

find_package(LLVM 4.0 REQUIRED CONFIG)
if( LLVM_FOUND )
  message( STATUS "LLVM found.
  LLVM_INCLUDE_DIR: ${LLVM_INCLUDE_DIR}
  LLVM_LIBRARY_DIR: ${LLVM_LIBRARY_DIR}")
else( LLVM_FOUND )
  message ( STATUS "LLVM not found. set environment variable:
  LLVM_ROOT_DIR (for example, %C_INCLUDE%/LLVM_4_0_1")
endif( LLVM_FOUND )
llvm_map_components_to_libnames(LLVM_LIBS support core passes mcjit native DebugInfoDWARF)

set(teoslib_src ${CMAKE_SOURCE_DIR}/teos_lib)

if( NOT ECC_IMPL STREQUAL openssl )
  set(Secp256k1_INCLUDE_DIR /usr/local/include)
  set(Secp256k1_LIBRARY /usr/local/lib/libsecp256k1.a)
  find_package(Secp256k1 REQUIRED)
  find_package(GMP REQUIRED)
endif()
## END DEPENDENCIES ##########################################################

install( FILES "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.json" 
  DESTINATION "bin" )

install( FILES "${CMAKE_CURRENT_SOURCE_DIR}/include/teos/config.json" 
  DESTINATION "bin" )


## BEGIN macro( applLinkLibraries applName ) #################################
macro( applLinkLibraries applName )

  file(GLOB HEADERS "${teoslib_src}/include/teoslib/*.hpp")
  target_sources( ${applName} 
    PRIVATE
      ${HEADERS}
  )

  target_include_directories( ${applName} 
    PRIVATE
      ${EOSIO_BOOST_INCLUDE_DIR}
      ${OPENSSL_INCLUDE_DIR}
      include "$ENV{EOSIO_EOSFACTORY_DIR}/teos/teos"
      include "$ENV{EOSIO_EOSFACTORY_DIR}/teos/teos_lib/include"
      include "$ENV{EOSIO_EOSFACTORY_DIR}/teos/teos_lib/include"
  )

  if( ENABLE_ASAN )
    if( UNIX )
    target_link_libraries( ${applName} 
      PRIVATE 
        asan        # static-libasan ?
    )
    endif()
  endif()

  set( TARGET_DIR "" )

  set( EOSIO_BINARY_DIR "$ENV{EOSIO_SOURCE_DIR}/build" )
  if(EXISTS "${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}fc_debug${CMAKE_STATIC_LIBRARY_SUFFIX}")
    set(fc "fc_debug")
  endif()
  if(EXISTS "${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}fc${CMAKE_STATIC_LIBRARY_SUFFIX}")
    set(fc "fc")
  endif()  

  target_link_libraries( ${applName} 
    PRIVATE
      $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos_lib/libteoslib.a
      ${EOSIO_BINARY_DIR}/plugins/chain_plugin/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chain_plugin${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/chain/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eosio_chain${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/chainbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}chainbase${CMAKE_STATIC_LIBRARY_SUFFIX}        
      ${EOSIO_BINARY_DIR}/libraries/utilities/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}eos_utilities${CMAKE_STATIC_LIBRARY_SUFFIX}      
      ${EOSIO_BINARY_DIR}/libraries/appbase/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}appbase${CMAKE_STATIC_LIBRARY_SUFFIX} 
      ${EOSIO_BINARY_DIR}/libraries/fc/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}${fc}${CMAKE_STATIC_LIBRARY_SUFFIX}       

      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Emscripten/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Emscripten${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Runtime/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Runtime${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/WAST/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}WAST${CMAKE_STATIC_LIBRARY_SUFFIX}
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/WASM/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}WASM${CMAKE_STATIC_LIBRARY_SUFFIX}      
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/IR/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}IR${CMAKE_STATIC_LIBRARY_SUFFIX}       
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Logging/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Logging${CMAKE_STATIC_LIBRARY_SUFFIX} 
      ${EOSIO_BINARY_DIR}/libraries/wasm-jit/Source/Platform/${TARGET_DIR}/${CMAKE_STATIC_LIBRARY_PREFIX}Platform${CMAKE_STATIC_LIBRARY_SUFFIX}
  )

  target_link_libraries( ${applName}
    PRIVATE
      ${OPENSSL_LIBRARIES}
      ${Boost_LIBRARIES}
      ${LLVM_LIBS}
      ${CMAKE_DL_LIBS}
      ${CMAKE_THREAD_LIBS_INIT}
  )

  set(THREADS_PREFER_PTHREAD_FLAG ON)
  find_package(Threads REQUIRED)
  target_link_libraries(${applName} 
    PRIVATE
      Threads::Threads
  )

  if( NOT ECC_IMPL STREQUAL openssl )
    target_link_libraries( ${applName}
      PRIVATE
        ${Secp256k1_LIBRARY}
        ${GMP_LIBRARIES}
    )
  endif()

endmacro( applLinkLibraries )
## END macro( applLinkLibraries applName ) ###################################


## add executables ###########################################################
##############################################################################

add_executable( test1 test1.cpp )
applLinkLibraries( test1 )

add_executable( unittest1 unittest1.cpp )
applLinkLibraries( unittest1 )

add_test( NAME test COMMAND test1 )
add_test( NAME unittest COMMAND unittest1 )
