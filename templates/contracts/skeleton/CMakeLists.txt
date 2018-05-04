cmake_minimum_required( VERSION 3.5 )

set(teos $ENV{EOSIO_CONTEXT_DIR}/teos/build/teos)
add_custom_command(OUTPUT @skeleton@.abi COMMAND ${teos} generate abi ../)
add_custom_command(OUTPUT @skeleton@.wast COMMAND ${teos} build contract ../)
add_custom_target(abi ALL DEPENDS @skeleton@.abi)
add_custom_target(wast ALL DEPENDS @skeleton@.wast)
