
set(LIB_NAME "eosclib")
add_library(${LIB_NAME} STATIC 
  eosc_command.cpp 
  eosc_get_commands
  eosc_wallet_commands
  subcommands.cpp
  ../eosc_test.cpp
  ../eosc
  )

find_path( HELPER_INCLUDE "eosc_helper.hpp" 
  HINTS "${EOSC_HELPER_INSTALL_PATH}/include")
if( HELPER_INCLUDE )
  target_include_directories( ${LIB_NAME}
    PUBLIC
    ${HELPER_INCLUDE}
  )
else()
  message( STATUS "
Cannot find the eosc helper includs path (where is eosc_helper.hpp header), 
namely \${EOSC_HELPER_INSTALL_PATH}/include
Please, set the path to this library in the top-level CMakeLists.txt as the
argument to the variable EOSC_HELPER_INSTALL_PATH.
The current value of EOSC_HELPER_INSTALL_PATH is ${EOSC_HELPER_INSTALL_PATH}  
  ")
  return()
endif()

target_include_directories( ${LIB_NAME} 
  PUBLIC
  ${Boost_INCLUDE_DIR}
  ${HELPER_INCLUDE}
  include
)

target_link_libraries( ${LIB_NAME}
  PUBLIC
  ${Boost_LIBRARIES}
  ${CMAKE_THREAD_LIBS_INIT}
)

if( WIN32 )
  set( HELPER_LIB_NAME eosc_helper.lib )
else()
  set( HELPER_LIB_NAME libeosc_helper.a )
endif()

find_file( HELPER_LIB ${HELPER_LIB_NAME} "${EOSC_HELPER_INSTALL_PATH}/lib")
if( HELPER_LIB )
  target_link_libraries( ${LIB_NAME}
    PRIVATE
    ${HELPER_LIB}
  )
else()
  message( STATUS "
Cannot find the eosc helper library, 
namely \${EOSC_HELPER_INSTALL_PATH}/lib/${HELPER_LIB_NAME}
Please, set the path to this library in the top-level CMakeLists.txt as the
argument to the variable EOSC_HELPER_INSTALL_PATH.
The current value of EOSC_HELPER_INSTALL_PATH is ${EOSC_HELPER_INSTALL_PATH}  
  ")
  return()
endif()


#install (TARGETS ${LIB_NAME} DESTINATION lib)
#install (FILES 
#  eosc_command.hpp 
#  eosc_get_commands.hpp 
#  eosc_wallet_commands.hpp 
#  subcommands.hpp
# DESTINATION include)