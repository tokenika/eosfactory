from  eosfactory import *
from eosf_wallet import Wallet

reset()
create_wallet()
Wallet.wallet.keys()

create_master_account("master")
create_account("alice", master)
create_account("carol", master)
Wallet.wallet.keys()
Wallet.wallet.lock_all()

stop()
restart()
run()

create_wallet()
Wallet.wallet.keys()

stop()
