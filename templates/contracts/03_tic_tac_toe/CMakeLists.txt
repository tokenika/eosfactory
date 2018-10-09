cmake_minimum_required( VERSION 3.5 )

include( CTest )

add_custom_target( abi ALL COMMAND python3 -c 'import eosfactory.core.teos as teos\; teos.ABI(\"${CMAKE_SOURCE_DIR}/src\")' )
add_custom_target( wast ALL COMMAND python3 -c 'import eosfactory.core.teos as teos\; teos.WAST(\"${CMAKE_SOURCE_DIR}/src\")' )

add_test( NAME tests COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/test1.py )
add_test( NAME unittest COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/unittest1.py )

# ctest -V -R ^unittest$
# ctest -V -R ^tests$
