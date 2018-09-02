from eosfactory import *

reset()
create_wallet()
get_wallet().keys()

create_master_account("master")
create_account("alice", master)
create_account("carol", master)

get_wallet().keys()
get_wallet().lock_all()

stop()
restart()
resume()

create_wallet()
get_wallet().keys()

stop()
