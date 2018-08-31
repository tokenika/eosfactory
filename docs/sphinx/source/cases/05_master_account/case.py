from  eosfactory import *
import testnode_data

reset()
create_wallet()
create_master_account("master_local")
master_local.info()
stop()

restart()

testnet = testnode_data.kylin

set_nodeos_address(testnet.url, prefix="temp")
remove_testnet_cache()
#set_testnet_configuration(testnet.url, prefix="temp")
#remove_testnet_cache()

create_wallet()
create_master_account(
    "master_remote",
    testnet.account_name,
    testnet.owner_key,
    testnet.active_key
    )
master_remote.info()