cmake_minimum_required( VERSION 3.5 )
include(CTest)

set(teos $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos/teos)
add_custom_command(OUTPUT @CONTRACT_NAME@.abi COMMAND ${teos} generate abi ${CMAKE_SOURCE_DIR}/src)
add_custom_command(OUTPUT @CONTRACT_NAME@.wast COMMAND ${teos} build contract ${CMAKE_SOURCE_DIR}/src)
add_custom_target(abi ALL DEPENDS @CONTRACT_NAME@.abi)
add_custom_target(wast ALL DEPENDS @CONTRACT_NAME@.wast)

file(WRITE ${CMAKE_BINARY_DIR}/pythonpath "export PYTHONPATH=$ENV{PYTHONPATH}")
add_test(NAME unittest COMMAND python3 ${CMAKE_SOURCE_DIR}/test/test.py)
