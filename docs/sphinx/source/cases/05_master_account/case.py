from  eosfactory import *

reset()

create_wallet()
create_master_account("master")
master.info()

stop()

restart()

testnet = Testnet("http://88.99.97.30:38888", "dgxo1uyhoytn", "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY", "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA")

testnet.configure()
testnet.verify_production()
testnet.clear_cache()

create_wallet()
create_master_account("master", testnet)
master.info()
