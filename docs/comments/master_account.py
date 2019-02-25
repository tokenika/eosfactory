
from eosfactory.eosf import *

reset()

create_master_account("MASTER")
MASTER.info()

create_account("ALICE", MASTER)
ALICE.info()

from eosfactory.eosf import *

testnet = Testnet(
    "nukjygmgkn3x",
    "5KXxczFPdcsLrCYpRRREfd4e2xVDTZZqBpZWmvxLZYxUbPzqrWL",
    "5KJLMupynNYFiM9gZWtDnDX55hbaF18EsWpFr8UvyJeADqbwN7A",
    "http://145.239.133.201:8888"
    )

testnet.configure()
testnet.verify_production()
testnet.clear_cache()

create_master_account("MASTER", testnet)
MASTER.info()

create_account("CAROL", MASTER, buy_ram_kbytes=8, stake_net=3, stake_cpu=3)
CAROL.info()
