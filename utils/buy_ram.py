from pyteos.eosf import *

testnet = get_testnet("KYLIN")
testnet.configure()
testnet.verify_production()

create_wallet(file=True)
create_master_account("master", testnet)
master.info()

master.buy_ram(10, master)
master.info()