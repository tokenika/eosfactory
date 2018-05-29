cmake_minimum_required( VERSION 3.5 )

include(CTest)

set(teos $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos/teos)
add_custom_command(OUTPUT @CONTRACT_NAME@.abi COMMAND ${teos} generate abi ${CMAKE_SOURCE_DIR}/src)
add_custom_command(OUTPUT @CONTRACT_NAME@.wast COMMAND ${teos} build contract ${CMAKE_SOURCE_DIR}/src)
add_custom_target(abi ALL DEPENDS @CONTRACT_NAME@.abi)
add_custom_target(wast ALL DEPENDS @CONTRACT_NAME@.wast)

add_test(NAME unittest COMMAND python3 ${CMAKE_SOURCE_DIR}/test/unittest1.py)
add_test(NAME test COMMAND python3 ${CMAKE_SOURCE_DIR}/test/test1.py ${CMAKE_SOURCE_DIR})

# ctest -V -R ^unittest$
# ctest -V -R ^test$
