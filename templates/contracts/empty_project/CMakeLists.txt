cmake_minimum_required( VERSION 3.5 )
project ( "foo" VERSION 1.0 LANGUAGES NONE ) 

SET( MODE "" CACHE STRING "Compilation mode: 'test_options' for native compilation, or nothing to apply the code mode" )

include( CTest )

add_custom_target( eosfactory.build ALL COMMAND python3 -m eosfactory.build \"${CMAKE_SOURCE_DIR}\" --c_cpp_prop \"${CMAKE_SOURCE_DIR}/.vscode/c_cpp_properties.json\" "${MODE}" )

add_test( NAME tests COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/test.py )

# for test mode: cmake -DMODE:STRING=test_options ..

# ctest -V -R ^unittest$
# ctest -V -R ^tests$