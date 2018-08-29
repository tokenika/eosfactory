from  eosfactory import *
import testnode_data

testnet = testnode_data.kylin
configure_testnet(testnet.url)
configure_testnet(testnet.url, prefix="registering_to_testnode")
remove_testnet_files()

verify_testnet()

create_wallet(file=True)
create_master_account("master")

testnet.create_master_account("master")

