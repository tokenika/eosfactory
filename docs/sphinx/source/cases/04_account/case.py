from  eosfactory import *

reset()
create_wallet()   
create_master_account("master")
create_account("host", master)

contract = Contract(host, "01_hello_world")
if not contract.is_built():
    contract.build()
contract.deploy()

create_account("alice", master)
create_account("carol", master)

host.push_action(
    "hi", '{"user":"' + str(alice) + '"}', alice)

host.push_action(
    "hi", '{"user":"' + str(carol) + '"}', carol)