cmake_minimum_required( VERSION 3.5 )

set(teos $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos/teos)
add_custom_command(OUTPUT @skeleton@.abi COMMAND ${teos} generate abi ${CMAKE_SOURCE_DIR})
add_custom_command(OUTPUT @skeleton@.wast COMMAND ${teos} build contract ${CMAKE_SOURCE_DIR}/src)
add_custom_target(abi ALL DEPENDS @skeleton@.abi)
add_custom_target(wast ALL DEPENDS @skeleton@.wast)
