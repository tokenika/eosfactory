from  eosfactory import *
import testnode_data

reset()
create_wallet()
create_master_account("master_local")
master_local.info()
stop()

restart()

testnet = testnode_data.kylin

configure_testnet(testnet.url, prefix="temp")
remove_testnet_files()
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