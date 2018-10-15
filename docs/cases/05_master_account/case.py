from eosfactory.eosf import *

reset()

create_master_account("master")
master.info()

create_account("alice", master)
alice.info()

reboot()

testnet = Testnet("http://88.99.97.30:38888", "dgxo1uyhoytn", "5JE9XSurh4Bmdw8Ynz72Eh6ZCKrxf63SmQWKrYJSXf1dEnoiKFY", "5JgLo7jZhmY4huDNXwExmaWQJqyS1hGZrnSjECcpWwGU25Ym8tA")

testnet.configure()
testnet.verify_production()
testnet.clear_cache()

create_master_account("master", testnet)
master.info()

create_account("alice", master, buy_ram_kbytes=8, stake_net=3, stake_cpu=3)
alice.info()
