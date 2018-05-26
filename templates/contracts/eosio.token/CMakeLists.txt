cmake_minimum_required( VERSION 3.5 )

set(teos $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos/teos)
add_custom_command(OUTPUT @eosio.token@.abi COMMAND ${teos} generate abi ${CMAKE_SOURCE_DIR}/src)
add_custom_command(OUTPUT @eosio.token@.wast COMMAND ${teos} build contract ${CMAKE_SOURCE_DIR}/src)
add_custom_target(abi ALL DEPENDS @eosio.token@.abi)
add_custom_target(wast ALL DEPENDS @eosio.token@.wast)
