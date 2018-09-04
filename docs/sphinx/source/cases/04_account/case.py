from eosf import *

reset()
create_wallet()   
create_master_account("master")

create_account("host", master)
host.info()

contract = Contract(host, "01_hello_world")
contract.build()
contract.deploy()

create_account("alice", master)
create_account("carol", master)

host.push_action("hi", {"user":alice}, alice)
host.push_action("hi", {"user":carol}, carol)

host.show_action("hi", {"user":carol}, carol)

stop()