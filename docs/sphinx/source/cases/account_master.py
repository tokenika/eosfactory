from  eosfactory import *
import testnet_data

reset()
create_wallet()
create_master_account("master_local")
master_local.info()
stop()

restart()

testnet = testnet_data.kylin

set_nodeos_address(testnet.url, prefix="temp")
remove_files()
#set_testnet_configuration(testnet.url, prefix="temp")
#remove_testnet_files()

create_wallet()
create_master_account(
    "master_remote",
    testnet.account_name,
    testnet.owner_key,
    testnet.active_key
    )
master_remote.info()