from  eosfactory import *

reset() 
create_wallet()
create_master_account("master")

create_account("alice", master)
create_account("carrol", master)
create_account("alice", master)