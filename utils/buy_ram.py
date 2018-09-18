from eosf import *

#testnet = get_testnet("KYLIN")
testnet = Testnet("https://api.kylin.alohaeos.com", "xlg3pao3idlq", "5JBbCwe3t6j63yerYmguRVWg7ZVDY3nKXzGYMwkR9y5w4appKhk", "5JYZU9xPS54NhnJrmgQWzVXxZCWpzsVUPS3SBZVZnsPUBFtV5YK")

testnet.configure()
testnet.verify_production()
testnet.clear_cache()

create_wallet(file=True)
create_master_account("master", testnet)
master.info()

master.buy_ram(3, master)
master.info()