
from eosfactory.eosf import *

reset()

create_master_account("MASTER")
MASTER.info()

create_account("ALICE", MASTER)
ALICE.info()

reboot()

testnet = manager.reset(
    "yvngxrjzbf3w",
    "5KCmAh23R9wZxm5m1BqRFePvAvw8fzYaDduACUg6DUAj9nmcZfQ",
    "5JkC4oFPaPjWzj866x2rMygsnVZaZzDkqynzX6dBw92LqR63tcD",
    "http://145.239.133.201:8888")

# resume("http://145.239.133.201:8888")

create_master_account("MASTER", testnet)
MASTER.info()

create_account("CAROL", MASTER, buy_ram_kbytes=8, stake_net=3, stake_cpu=3)
CAROL.info()
