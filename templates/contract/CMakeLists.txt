cmake_minimum_required( VERSION 3.5 )

set(teos $ENV{EOSIO_CONTEXT_DIR}/teos/build/teos)
add_custom_command(OUTPUT @contract_name@.abi COMMAND ${teos} generate abi ../)
add_custom_command(OUTPUT @contract_name@.wast COMMAND ${teos} build contract ../)
add_custom_target(abi ALL DEPENDS @contract_name@.abi)
add_custom_target(wast ALL DEPENDS @contract_name@.wast)
