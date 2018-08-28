from  eosfactory import *
import testnet_data

testnode = testnet_data.kylin
configure_testnet(testnode.url)
configure_testnet(testnode.url, prefix="registering_to_testnode")
remove_testnet_files()

verify_testnet()

create_wallet(file=True)
create_master_account("master")

testnode.create_master_account("master")

