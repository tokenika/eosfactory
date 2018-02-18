set( Boost_USE_STATIC_LIBS ON )
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
set( BOOST_ROOT $ENV{HOME}/opt/boost_1_64_0 )
if( WIN32 )
  set( Boost_NO_SYSTEM_PATHS ON )
  set( BOOST_INCLUDEDIR $ENV{BOOST_INCLUDEDIR})
  message( STATUS "BOOST_INCLUDEDIR: $ENV{BOOST_INCLUDEDIR}")
  set( BOOST_LIBRARYDIR $ENV{BOOST_LIBRARYDIR} )
  message( STATUS "BOOST_LIBRARYDIR: $ENV{BOOST_LIBRARYDIR}")
endif( WIN32 )
find_package( Boost 1.62 REQUIRED COMPONENTS 
  system
  #chrono
  date_time 
  #program_options
  filesystem
  regex
  thread
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}
  Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_LIBRARYDIR (for example, %BOOST_ROOT%/lib64-msvc-14.1)
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

macro( appDependencies applName )
  file(GLOB HEADERS "include/control/*.hpp")
  target_sources( ${applName} 
    PRIVATE
      ${HEADERS}
      ${CMAKE_SOURCE_DIR}/config.cpp
  )
  target_include_directories( ${applName}
    PRIVATE
      ${Boost_INCLUDE_DIR}
      include
  )
  target_link_libraries( ${applName}
    PRIVATE
      ${Boost_LIBRARIES}  
  )
  if( UNIX )
    target_link_libraries( ${applName} 
      PRIVATE 
        rt 
        pthread
    )
  endif()
endmacro()

add_executable( echo_server
  async_tcp_echo_server.cpp
)
appDependencies( echo_server )

add_executable( echo_client
  blocking_tcp_echo_client.cpp
)
appDependencies( echo_client )

add_executable( boost_process
  boostProcess.cpp;
)
appDependencies( boost_process )

add_executable( eosiodServer
  eosiodServer.cpp
)
appDependencies( eosiodServer )
