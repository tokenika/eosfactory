cmake_minimum_required( VERSION 3.5 )

set(teos $ENV{EOSIO_EOSFACTORY_DIR}/teos/build/teos)
add_custom_command(OUTPUT tic.tac.toe.abi COMMAND ${teos} generate abi ../)
add_custom_command(OUTPUT tic.tac.toe.wast COMMAND ${teos} build contract ../)
add_custom_target(abi ALL DEPENDS tic.tac.toe.abi)
add_custom_target(wast ALL DEPENDS tic.tac.toe.wast)

