
set( BUILD_SHARED_LIBS NO )
list( APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../CMakeModules" )

set( TEST_ADDRESS "tokenika")
set( TEST_HTTP_ADDRESS "eos-testapi.tokenika.io:8888" )

## BEGIN DEPENDENCIES ########################################################

set( Boost_USE_STATIC_LIBS ON )
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
set( BOOST_ROOT "$ENV{U_HOME}/opt/boost" )

find_package(Boost 1.67 REQUIRED COMPONENTS 
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
  Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}
  Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-WIN32-14.1)
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

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
      ${Boost_INCLUDE_DIRS}
      include
      "${teoslib_src}/include"
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

  target_link_libraries( ${applName} 
    PRIVATE
      ${CMAKE_BINARY_DIR}/teos_lib/libteoslib.a
  )

  target_link_libraries( ${applName}
    PRIVATE
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
        # ${Secp256k1_LIBRARY}
        # ${GMP_LIBRARIES}
    )
  endif()

endmacro( applLinkLibraries )
## END macro( applLinkLibraries applName ) ###################################


## add executables ###########################################################
##############################################################################

add_executable( teos teos.cpp )
applLinkLibraries( teos )
install( TARGETS teos RUNTIME DESTINATION bin)

add_executable( test1 test1.cpp )
applLinkLibraries( test1 )
install( TARGETS test1 RUNTIME DESTINATION bin)

add_executable( unittest1 unittest1.cpp )
applLinkLibraries( unittest1 )
install( TARGETS unittest1 RUNTIME DESTINATION bin)

## install ###################################################################
install( TARGETS
   teos
   RUNTIME DESTINATION "/usr/local/bin"
)


