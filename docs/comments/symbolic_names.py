
from eosfactory.eosf import *

reset()
create_master_account("master")
create_account("host", master)
create_account("alice", master)
create_account("carol", master)

contract = Contract(host, "eosio_token")
contract.build(force=False)
contract.deploy()

host.push_action(
    "create", 
    {
        "issuer": master,
        "maximum_supply": "1000000000.0000 EOS"
    }, [master, host])

setup.is_translating = False

host.push_action(
    "issue",
    {
        "to": alice, "quantity": "100.0000 EOS", "memo": ""
    },
    master)

setup.is_translating = True

host.push_action(
    "issue",
    {
        "to": carol, "quantity": "100.0000 EOS", "memo": ""
    },
    master)

stop()
