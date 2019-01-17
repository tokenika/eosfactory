cmake_minimum_required( VERSION 3.5 )
project ( "Test-App" VERSION 1.0 LANGUAGES NONE
) 

include( CTest )

add_custom_target( wast ALL COMMAND python3 -c 'from eosfactory.shell.contract import ContractBuilder\; ContractBuilder(\"${CMAKE_SOURCE_DIR}\" ) .build() ' )

add_test( NAME tests COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/test1.py )
add_test( NAME unittest COMMAND python3 ${CMAKE_SOURCE_DIR}/tests/unittest1.py )

# ctest -V -R ^unittest$
# ctest -V -R ^tests$