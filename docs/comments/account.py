
from eosfactory.eosf import *

reset()
create_master_account("MASTER")

create_account("HOST", MASTER)

HOST.info()

create_account("HOST", MASTER)

create_account("HOST", MASTER, str(HOST))

contract = Contract(HOST, "hello_world")

contract.build()
contract.deploy()

create_account("alice", MASTER)
create_account("carol", MASTER)

HOST.push_action("hi", {"user":alice}, alice)
HOST.push_action("hi", {"user":carol}, carol)

HOST.show_action("hi", {"user":alice}, alice)

stop()
